class AccountSchema():
    """
    Класс преставляющий схему таблицы accounts
    """
    def schema(self):
        """
        Метод возвращающий строку с SQL-запросом, который инициализирует таблицу accounts
        """
        return """
            CREATE TABLE IF NOT EXISTS accounts (
                id    INTEGER,
                currency  varchar,
                uuid  varchar,
                balance   decimal,
                PRIMARY KEY(id AUTOINCREMENT)
            );
        """