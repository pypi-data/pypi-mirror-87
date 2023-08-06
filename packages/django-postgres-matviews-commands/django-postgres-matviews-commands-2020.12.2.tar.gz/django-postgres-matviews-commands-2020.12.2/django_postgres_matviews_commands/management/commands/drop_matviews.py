from django.core.management.base import BaseCommand
from django.db import connection

SQL = """
SELECT schemaname, matviewname FROM pg_matviews
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute(SQL)
        for r in cursor.fetchall():
            schemaname, matviewname = r
            sql = """DROP MATERIALIZED VIEW IF EXISTS "%s"."%s" CASCADE;""" % (schemaname, matviewname)
            print(sql.strip())
            cursor.execute(sql)
