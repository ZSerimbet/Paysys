class TransactionSchema():
    def schema(self):
        return """
            CREATE TABLE IF NOT EXISTS transactions (
                id    INTEGER,
                type  varchar,
                currency  varchar,
                amount   decimal,
                uuid    varchar,
                PRIMARY KEY(id AUTOINCREMENT)
            );
        """