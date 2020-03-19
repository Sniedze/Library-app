from csv import DictReader

from django.core.management import BaseCommand

from library_app.models import Books

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the pet data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Books.objects.exists():
            print('Book data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Creating book data")

        for row in DictReader(open('./books_new.csv')):
            book = Books()
            book.title = row['Title']
            book.author = row['Author']

            book.save()
