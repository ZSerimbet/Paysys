import sqlite3

from django.conf import settings
from transactions.schema import TransactionSchema

class TransactionManager():
    def __init__(self):
        transaction_schema = TransactionSchema()

        self.conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
        cur = self.conn.cursor()
        cur.execute(transaction_schema.schema())
        self.conn.commit()

    def close():
        self.conn.close()

    def all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM transactions;")
        data = cur.fetchall()

        return data

    def get(self, uuid):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE uuid = ?;", (uuid,))
        data = cur.fetchall()

        return data

    def create(self, transaction):
        cur = self.conn.cursor()
        cur.execute("""
                    INSERT INTO transactions (type, currency, amount, uuid) VALUES (?, ?, ?, ?);
                    """, (str(transaction['type']), str(transaction['currency']), transaction['amount'], transaction['uuid']))
        self.conn.commit()

    def update(self, transaction):
        cur = self.conn.cursor()
        cur.execute(cur.execute("""
                    UPDATE transaction SET type = ?, currency = ?, amount = ? WHERE id = ?;
                    """, (transaction['type'], transaction['currency'], transaction['amount'], transaction['id'])))
        self.conn.commit()

    def erase(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM transactions;")
        self.conn.commit()