import sqlite3
import os
from flask import g, current_app

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None


def _using_postgres():
    return bool(current_app.config.get('DATABASE_URL'))


def get_db():
    if 'db' not in g:
        if _using_postgres():
            g.db = psycopg2.connect(
                current_app.config['DATABASE_URL'],
                cursor_factory=psycopg2.extras.DictCursor
            )
        else:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def _adapt_query(query):
    # SQLite uses ?, Postgres uses %s — translate automatically
    return query.replace('?', '%s') if _using_postgres() else query


def init_db(app):
    with app.app_context():
        db = get_db()
        schema_file = 'schema_postgres.sql' if _using_postgres() else 'schema.sql'
        schema_path = os.path.join(os.path.dirname(__file__), schema_file)
        with open(schema_path, 'r') as f:
            sql = f.read()
            if _using_postgres():
                cur = db.cursor()
                cur.execute(sql)
                cur.close()
            else:
                db.executescript(sql)
            db.commit()
    app.teardown_appcontext(close_db)


def query_db(query, args=(), one=False):
    cur = get_db().execute(_adapt_query(query), args) if not _using_postgres() else None
    if _using_postgres():
        cur = get_db().cursor()
        cur.execute(_adapt_query(query), args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=()):
    db = get_db()
    cur = db.cursor() if _using_postgres() else db.cursor()
    cur.execute(_adapt_query(query), args)
    db.commit()
    if _using_postgres():
        try:
            last_id = cur.fetchone()[0]  # requires RETURNING id in the query
        except (TypeError, Exception):
            last_id = None
    else:
        last_id = cur.lastrowid
    cur.close()
    return last_id