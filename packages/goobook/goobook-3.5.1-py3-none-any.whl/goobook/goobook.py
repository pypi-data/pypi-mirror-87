# vim: fileencoding=UTF-8 filetype=python ff=unix expandtab sw=4 sts=4 tw=120
# maintainer: Christer Sjöholm -- goobook AT furuvik DOT net
# authors: Marcus Nitzschke -- marcus.nitzschke AT gmx DOT com
#
# Copyright (C) 2009  Carlos José Barroso
# Copyright (C) 2010  Christer Sjöholm
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The idea is make an interface to google contacts that mimics the behaviour of abook for mutt."""
import collections
import datetime
import email.parser
import email.header
import logging
import os
import pickle
import re
import sys
import time

import httplib2
from googleapiclient.discovery import build

from goobook.storage import Storage, storageify, unstorageify

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

CACHE_FORMAT_VERSION = '5.1'

TypedValue = collections.namedtuple('TypedValue', ['value', 'type'])


class GooBook():
    """Application logic.

    This class can't be used as a library as it looks now, it uses sys.stdin
    print and sys.exit().
    """

    def __init__(self, config):
        self.__config = config
        self.cache = Cache(config)
        self.cache.load()

    def query(self, query, simple=False):
        """Do the query, and print it out in specified format.

        simple=False is the mutt format
        simple format is:
          "Name <email>"
        simple format for group matches is a , separated list of Name <email>
        the group name is not printed using simple format.
        """
        # query contacts
        matching_contacts = sorted(self.__query_contacts(query), key=lambda c: c.display_name)
        # query groups
        matching_groups = sorted(self.__query_groups(query), key=lambda g: g[0])
        if not simple:
            # mutt's query_command expects the first line to be a message,
            # which it discards.
            print('')
        for contact in matching_contacts:
            if contact.emails:
                emailaddrs = sorted(contact.emails)
                groups = set(contact.groups)
                groups = groups.difference(('My Contacts',))
                groups_str = ', '.join(('"' + g + '"' for g in groups))
                for (emailaddr, kind) in emailaddrs:
                    extra_str = kind
                    if groups_str:
                        extra_str = extra_str + ' groups: ' + groups_str
                    if simple:
                        print(f"{contact.display_name} <{emailaddr}>")
                    else:
                        print('\t'.join((emailaddr, contact.display_name, extra_str)))

        for title, contacts in matching_groups:
            emails = ['%s <%s>' % (c.display_name, c.emails[0][0]) for c in contacts if c.emails]
            emails = ', '.join(emails)
            if not emails:
                continue
            if simple:
                print(emails)
            else:
                print('%s\t%s (group)' % (emails, title))

    def query_details(self, query):
        """Method for querying the contacts and printing a detailed view."""
        out = sys.stdout

        # query contacts
        matching_contacts = list(self.__query_contacts(query))
        # query groups
        for group in self.__query_groups(query):
            for contact in group[1]:
                if contact not in matching_contacts:
                    matching_contacts.append(contact)

        matching_contacts = sorted(matching_contacts, key=lambda c: c.display_name)

        for contact in matching_contacts:
            print("-------------------------", file=out)
            print(contact.display_name, file=out)
            for org in contact.organizations:
                if org.name:
                    print("Organization: ", org.name, file=out)
                if org.department:
                    print("Department:   ", org.department, file=out)
                if org.title:
                    print("Title:        ", org.title, file=out)
            if contact.birthday:
                print("Birthday:     ", contact.birthday.strftime("%x"), file=out)
            if contact.phonenumbers:
                print("Phone:", file=out)
                for (number, kind) in contact.phonenumbers:
                    print("\t", number, " (" + kind + ")", file=out)
            if contact.emails:
                print("EMail:", file=out)
                emailaddrs = sorted(contact.emails)
                for (emailaddr, kind) in emailaddrs:
                    print("\t", emailaddr, " (" + kind + ")", file=out)
            if contact.im:
                print("IM:", file=out)
                for (nick, protocol) in contact.im:
                    print("\t", nick, " (", protocol, ")", file=out)
            if contact.addresses:
                print("Address:", file=out)
                for (address, kind) in contact.addresses:
                    lines = address.splitlines()
                    lines[0] = '%s ( %s )' % (lines[0], kind)
                    print("\t" + '\n\t'.join(lines), file=out)
            groups = set(contact.groups).difference(('My Contacts',))
            if groups:
                print("Groups:", file=out)
                groups_str = '\n\t'.join(groups)
                print("\t" + groups_str, file=out)

    def __query_contacts(self, query):
        match = re.compile(query.replace(' ', '.*'), re.I).search  # create a match function
        for contact in self.cache.contacts:
            if self.__config.filter_groupless_contacts and not contact.groups:
                continue  # Skip contacts without groups
            if any(map(match, list(contact.all_names) + [str(number) for (number, kind) in contact.phonenumbers])):
                yield contact
                continue
            matching_addrs = [(email, kind) for (email, kind) in contact.emails if match(email)]
            if matching_addrs:
                contact.emails = matching_addrs  # only show matching
                yield contact
                continue
            for org in contact.organizations:
                for field in ('name', 'title', 'department'):
                    if org[field] and match(org[field]):
                        yield contact
                        continue

    def __query_groups(self, query):
        match = re.compile(query.replace(' ', '.*'), re.I).search  # create a match function
        for group in self.cache.groups:
            # Collect all values to match against
            all_values = (group,)
            if any(map(match, all_values)):
                contacts = list(self.__get_group_contacts(group))
                yield group, contacts

    def __get_group_contacts(self, group):
        for contact in self.cache.contacts:
            if group in contact.groups:
                yield contact

    def add_mail_contact(self, name, mailaddr, phone=None):
        contact = {
            'names': [{'givenName': name}],
            'emailAddresses': [{'value': mailaddr}],
            'phoneNumbers': [{'value': phone}],
        }

        gcont = GoogleContacts(self.__config)
        log.debug('Going to create contact name: %s email: %s phone: %s', name, mailaddr, phone)
        gcont.create_contact(contact)
        log.info('Created contact name: %s email: %s %s', name, mailaddr, phone)

    def add_email_from(self, lines):
        """Add an address from From: field of a mail.

        This assumes a single mail file is supplied through.

        Args:
        ----
          lines: A generator of lines, usually a open file.

        """
        parser = email.parser.HeaderParser()
        headers = parser.parse(lines)
        if 'From' not in headers:
            print("Not a valid mail file!")
            sys.exit(2)

        (name, mailaddr) = email.utils.parseaddr(headers['From'])
        if not name:
            name = mailaddr
        else:
            # This decodes headers like "=?iso-8859-1?q?p=F6stal?="
            values = email.header.decode_header(name)
            if not values:
                # Can't this be possible?
                name = mailaddr
            else:
                # There should be only one element anyway
                (name, encoding) = values[0]

                if encoding is not None:
                    name = name.decode(encoding)

        self.add_mail_contact(name, mailaddr)


class Cache():
    def __init__(self, config):
        self.__config = config
        self.contacts = None  # list of Storage
        self.groups = None  # list of Storage

    def load(self, force_update=False):
        """Load the cached addressbook feed, or fetch it (again) if it is old or missing or invalid or anything.

        Args:
        ----
          force_update: force update of cache

        """
        cache = {}

        # if cache newer than cache_expiry_hours
        if not force_update and (os.path.exists(self.__config.cache_filename) and
                                 ((time.time() - os.path.getmtime(self.__config.cache_filename)) <
                                  (int(self.__config.cache_expiry_hours) * 60 * 60))):
            try:
                log.debug('Loading cache: %s', self.__config.cache_filename)
                cache = pickle.load(open(self.__config.cache_filename, 'rb'))
                if cache.get('goobook_cache') != CACHE_FORMAT_VERSION:
                    log.info('Detected old cache format')
                    cache = None  # Old cache format
            except Exception as err:
                log.info('Failed to read the cache file: %s', err)
                raise
        if cache:
            self.contacts = storageify(cache.get('contacts'))
            self.groups = storageify(cache.get('groups'))
        else:
            self.update()
        if not self.contacts:
            raise Exception('Failed to find any contacts')  # TODO

    def update(self):
        log.info('Retrieving contact data from Google.')
        gcs = GoogleContacts(self.__config)
        groupname_by_id = parse_groups(gcs.fetch_contact_groups())
        self.contacts = list(parse_contacts(gcs.fetch_contacts(), groupname_by_id))
        self.groups = list(groupname_by_id.values())
        self.save()

    def save(self):
        """Pickle the addressbook and a timestamp."""
        if self.contacts:  # never write a empty addressbook
            cache = {'contacts': unstorageify(self.contacts),
                     'groups': unstorageify(self.groups),
                     'goobook_cache': CACHE_FORMAT_VERSION}
            pickle.dump(cache, open(self.__config.cache_filename, 'wb'))


def parse_contact(person, groupname_by_id):
    """Extracts interesting contact info from cache.

    https://developers.google.com/people/api/rest/v1/people
    """
    contact = Storage()
    contact.emails = []
    contact.birthday = None  # datetime.date
    contact.im = []
    contact.addresses = []
    contact.display_name = None
    contact.all_names = []
    contact.groups = []
    contact.phonenumbers = []  # [TypedValue]
    contact.organizations = []  # [Storage()]

    for emaila in person.get('emailAddresses', []):
        contact.emails.append(TypedValue(emaila['value'], emaila.get('type', '')))

    if 'birthdays' in person.keys() and person['birthdays'] and 'date' in person['birthdays'][0]:
        birthday = person['birthdays'][0]['date']
        if len(birthday) == 3:  # we skip incomplete birthdates
            contact.birthday = datetime.date(birthday['year'], birthday['month'], birthday['day'])

    for name in person.get('names', []):
        if 'displayName' in name and contact.display_name is None:
            # use first displayName found
            contact.display_name = name['displayName']
        for field in ("displayName", "displayNameLastFirst", "familyName", "givenName", "middleName",
                      "honorificPrefix", "honorificSuffix", "phoneticFullName", "phoneticFamilyName",
                      "phoneticGivenName", "phoneticMiddleName", "phoneticHonorificPrefix",
                      "phoneticHonorificSuffix"):
            if field in name:
                contact.all_names.append(name[field])

    if contact.display_name is None and contact.emails:
        # if there is no displayName use a email address
        contact.display_name = contact.emails[0].value

    for membership in person.get('memberships', []):
        if "contactGroupMembership" in membership:
            contact.groups.append(groupname_by_id['contactGroups/' +
                                                  membership['contactGroupMembership']['contactGroupId']])

    for phone in person.get('phoneNumbers', []):
        contact.phonenumbers.append(TypedValue(phone['value'], phone.get('type', '')))

    for address in person.get('addresses', []):
        if 'formattedValue' in address:
            contact.addresses.append(TypedValue(address['formattedValue'], address.get('type', '')))

    for item in person.get('imClients', []):
        if 'username' in item:
            contact.im.append(TypedValue(item['username'], item.get('protocol', '')))

    if 'organizations' in person.keys() and person['organizations']:
        for org in person['organizations']:
            if not contact.display_name:
                contact.display_name = org.get('name')
            contact.organizations.append(Storage(name=org.get('name'),
                                                 title=org.get('title'),
                                                 department=org.get('department')))
    log.debug('Parsed contact %s', contact)
    if not contact.display_name:
        log.info('Skipping contact because of no name/e-mail/organization: %s', person)
        return None
    return contact


def parse_contacts(raw_contacts, groupname_by_id):
    for contact in raw_contacts:
        parsed = parse_contact(contact, groupname_by_id)
        if parsed:
            yield parsed


def parse_groups(raw_groups):
    groupname_by_id = {}
    for entry in raw_groups:
        groupname_by_id[entry['resourceName']] = entry['formattedName']
    return groupname_by_id


class GoogleContacts():

    def __init__(self, config):
        http_client = self.__get_client(config.creds)
        self.service = build('people', 'v1', http=http_client)
        # self.__additional_headers = {
        #     'GData-Version': GDATA_VERSION,
        #     'Content-Type': 'application/atom+xml'
        # }

    @staticmethod
    def __get_client(credentials):
        """Login to Google and return a ContactsClient object."""
        if not credentials or credentials.invalid:
            sys.exit('No or invalid credentials, run "goobook authenticate"')  # TODO raise exception instead
        http_auth = credentials.authorize(httplib2.Http())
        return http_auth

    def fetch_contacts(self):
        connections = []
        request = self.service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,  # Number of connections in response
            x__xgafv=None,
            pageToken=None,
            sortOrder=None,
            personFields=('names,nicknames,emailAddresses,memberships,'
                          'phoneNumbers,birthdays,imClients,organizations,addresses'),
            requestSyncToken=None,
            syncToken=None,
            requestMask_includeField=None)

        # Loop until all pages have been processed.
        while request is not None:
            # Get the next page.
            response = request.execute()
            # Accessing the response like a dict object with an 'items' key
            # returns a list of item objects (connections).
            connections.extend(response.get('connections', []))
            # Get the next request object by passing the previous request object to
            # the list_next method.
            request = self.service.people().connections().list_next(request, response)
        return connections

    def fetch_contact_groups(self):
        groups = []
        request = self.service.contactGroups().list(pageSize=500)

        # Loop until all pages have been processed.
        while request is not None:
            # Get the next page.
            response = request.execute()
            # Accessing the response like a dict object with an 'items' key
            # returns a list of item objects (groups).
            groups.extend(response.get('contactGroups', []))
            # Get the next request object by passing the previous request object to
            # the list_next method.
            request = self.service.contactGroups().list_next(request, response)
        return groups

    def create_contact(self, contact):
        self.service.people().createContact(body=contact).execute()
