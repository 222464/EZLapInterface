import psycopg as psy

class DBInterface:
    def __init__(self):
        self.conn = psy.connect('dbname=postgres2 user=miniz')

    def insert(self, uid, dt, ts):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT EXISTS (
                   SELECT FROM information_schema.tables 
                   WHERE  table_schema = 'public'
                   AND    table_name   = 'laptimes')
                """)

            table = cur.fetchone()

            if table == (False,):
                cur.execute("""
                    CREATE TABLE laptimes (
                        uid integer,
                        dt integer,
                        ts integer)
                    """)

            cur.execute(
                "INSERT INTO laptimes (uid, dt, ts) VALUES (%s, %s, %s)",
                (uid, dt, ts))

            self.conn.commit()

    def read_last_n(self, n):
        result = []

        with self.conn.cursor() as cur:
            cur.execute("""SELECT EXISTS (
                   SELECT FROM information_schema.tables 
                   WHERE  table_schema = 'public'
                   AND    table_name   = 'laptimes')
                """)

            table = cur.fetchone()

            if table == (False,):
                return result

            cur.execute(
                "SELECT * FROM laptimes ORDER BY ts DESC LIMIT (%s)",
                (n,))

            result = cur.fetchall()

        return result




