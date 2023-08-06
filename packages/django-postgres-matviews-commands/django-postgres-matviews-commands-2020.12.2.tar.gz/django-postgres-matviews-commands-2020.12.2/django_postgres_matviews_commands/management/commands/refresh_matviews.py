from django.core.management.base import BaseCommand
from django.db import connection

SQL = """
SELECT format('%s.%s',schemaname,matviewname)
FROM pg_matviews
ORDER BY format('%s.%s',schemaname,matviewname)
"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute(SQL)
        for row in cursor.fetchall():
            schemaname, matviewname = row[0].split('.')
            sql = """
set search_path to "%s", public;
REFRESH MATERIALIZED VIEW "%s"."%s";
""" % (schemaname,schemaname,matviewname)
            print(sql)
            try:
                cursor.execute(sql)
            except Exception as e:
                print('%s: %s' % (type(e),str(e)))
