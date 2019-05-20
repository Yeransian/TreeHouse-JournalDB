
from collections import OrderedDict
import datetime
import sys

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
    # content
    content = TextField()
    # timestamp
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """ Create the database and the table if they don't exist. """
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """ Show the menu """
    choice = None
    while choice != 'q':
        print('Enter q to quit.')
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower()
        if choice in menu:
            menu[choice]()


def add_entry():
    """Add an entry."""
    entry = ""
    print("Log you idea, print 'done' to finish.")
    while True:
        data = input('> ')
        if data.lower() != 'done':
            entry += data + "\n"
        else:
            break
    # data = sys.stdin.read().strip()

    if entry:
        if input('Save entry? [Y]/n ').lower() != 'n':
            Entry.create(content=entry)
            print("Saved!")
        else:
            print("Your entry wasn't save")


    # BELOW COMMENTED OUT CODE, CTRL+D, DOES NOT WORK
    # print("Enter your entry, press ctrl+d when finished.")
    # data = sys.stdin.read().strip()
    # if data:
    #     if input('Save entry? [Yn]').lower() != 'n':
    #         Entry.create(content=data)
    #         print("Saved successfully")


def view_entries(search_query=None):
    """ View previous entries. """
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))
    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('\n\n' + '=' * len(timestamp))
        print('n) for next entry')
        print('d) Delete entry')
        print('q) return to main menu')

        next_action = input('Action: [N\q\d] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search entries for a string."""
    view_entries(input('Search query'))


def delete_entry(entry):
    """ Delete an entry """
    if input("Are you sure y/N?").lower() == 'y':
        entry.delete_instance()
        print("Entry was deleted!")


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])

if __name__ == '__main__':
    initialize()
    menu_loop()
