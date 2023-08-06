from django.db import connection

from .classes import Matview

SQL = """
SELECT format('%s.%s',schemaname,matviewname)
FROM pg_matviews
ORDER BY format('%s.%s',schemaname,matviewname)
"""


def get_matviews():
    cursor = connection.cursor()
    cursor.execute(SQL)
    return list(map(lambda r: Matview(r[0]), cursor.fetchall()))


def drop_matviews():
    cursor = connection.cursor()
    for m in get_matviews():
        sql = """DROP MATERIALIZED VIEW IF EXISTS "%s"."%s" CASCADE;""" % (
            m.schemaname, m.matviewname)
        cursor.execute(sql)


def refresh_matviews():
    cursor = connection.cursor()
    for m in get_matviews():
        sql = 'REFRESH MATERIALIZED VIEW "%s.%s";' % (
            m.schemaname, m.matviewname)
        cursor.execute(sql)


def drop(matview):
    cursor = connection.cursor()
    sql = """DROP MATERIALIZED VIEW IF EXISTS "%s" CASCADE;""" % matview
    cursor.execute(sql)


def refresh(matview):
    cursor = connection.cursor()
    sql = """REFRESH MATERIALIZED VIEW "%s";""" % matview
    cursor.execute(sql)
