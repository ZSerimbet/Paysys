import sqlite3

from django.conf import settings
from accounts.schema import AccountSchema

class AccountManager():
    """
    Класс ответственный за работу с базой данных
    """

    def __init__(self):
        """
        Инициализация
        """

        # Инициализируем класс в котором находится схема текущей таблицы (account)
        account_schema = AccountSchema()

        # Устанавливаем соединение с базой
        self.conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
        cur = self.conn.cursor()

        # Выполняем запрос к базе
        # Создаем схему нашей таблицы в базе
        cur.execute(account_schema.schema())
        self.conn.commit()

    def close():
        """
        Метод который закрывает соединение с базой
        """
        self.conn.close()

    def all(self):
        """
        Метод получения всех счетов из базы
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts;")
        data = cur.fetchall()

        return data

    def get(self, uuid):
        """
        Метод получения определенного счёта из базы, по uuid
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE uuid = ?;", (uuid,))
        data = cur.fetchall()

        return data

    def create(self, account):
        """
        Метод создания нового счёта в базе
        """
        cur = self.conn.cursor()
        cur.execute("""
                    INSERT INTO accounts (currency, uuid, balance) VALUES (?, ?, ?);
                    """, (str(account['currency']), str(account['uuid']), account['balance']))
        self.conn.commit()

    def refill(self, account):
        """
        Метод пополнения счёта в базе
        """
        cur = self.conn.cursor()
        cur.execute("""
                    UPDATE accounts SET balance = balance + ? WHERE uuid = ?;
                    """, (account['balance'], account['uuid']))
        self.conn.commit()

    def writeoff(self, account):
        """
        Метод списания со счёта в базе
        """
        cur = self.conn.cursor()
        cur.execute("""
                    UPDATE accounts SET balance = balance - ? WHERE uuid = ?;
                    """, (account['balance'], account['uuid']))
        self.conn.commit()

    def erase(self):
        """
        Метод очистки таблицы
        """
        cur = self.conn.cursor()
        cur.execute("DELETE FROM accounts;")
        self.conn.commit()