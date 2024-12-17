import psycopg as psy

class DBInterface:
    def __init__(self):
        self.conn = psy.connect('dbname=miniz user=postgres')

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
            cur.execute(
                "SELECT * FROM laptimes ORDER BY ts DESC LIMIT (%s)",
                (n,))

            cur.fetchall()

            for record in cur:
                result.append(record)

        return result




