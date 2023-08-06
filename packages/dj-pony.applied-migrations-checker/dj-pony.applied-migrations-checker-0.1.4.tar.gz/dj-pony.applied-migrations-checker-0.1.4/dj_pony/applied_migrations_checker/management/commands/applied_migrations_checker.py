import time
from django.core.management.base import BaseCommand
from django.db.migrations.executor import MigrationExecutor
from django.db import connections


def check_databases():
    """Confirm that all the specified databases are available to communicate with."""
    database_connection_check_results = []
    for database_connection_name in connections:
        connection = connections[database_connection_name]
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT (1)')
            database_connection_check_results.append(True)
        except:  # noqa
            database_connection_check_results.append(False)
        finally:
            cursor.close()
    return all(database_connection_check_results)


def count_outstanding_migrations():
    """Count the number of migrations not yet applied to database(s)"""
    # South is external.
    number_of_migrations = 0
    for database_connection_name in connections:
        connection = connections[database_connection_name]
        try:
            connection.prepare_database()
        except AttributeError:
            pass
        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        number_of_migrations += len(executor.migration_plan(targets))
    return number_of_migrations


class Command(BaseCommand):
    """Check if we have any outstanding database migrations, and wait for them to complete."""
    help = 'Waits for database and migrations to be available and complete'

    def add_arguments(self, parser):
        parser.add_argument('--wait', action='store_true')

    def handle(self, *args, **options):
        while True:
            if check_databases():
                number_of_migrations = count_outstanding_migrations()

                if number_of_migrations == 0:
                    print('Migrations complete!')
                    exit(0)
                print(f'{number_of_migrations} migrations have not yet been applied...')
            else:
                print('Unable to connect to database...')

            if not options['wait']:
                exit(1)

            time.sleep(5.0)
