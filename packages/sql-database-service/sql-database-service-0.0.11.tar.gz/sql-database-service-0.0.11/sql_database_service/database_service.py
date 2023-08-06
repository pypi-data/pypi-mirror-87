class DatabaseService:
    """ A class of some useful functions to deal with the database """

    def __init__(self, database):
        self.database = database

    def create_all(self):
        self.database.create_all()

    def drop_all(self):
        self.database.drop_all()

    def set_fk_check(self):
        # Activate foreign key checking
        self.database.engine.execute('SET FOREIGN_KEY_CHECKS = 1;')

    def reset_fk_check(self):
        # De-activate foreign key checking
        self.database.engine.execute('SET FOREIGN_KEY_CHECKS = 0;')

    def drop_alembic_version(self):
        # Useful to delete migration table
        self.database.engine.execute('DROP TABLE alembic_version;')

    def delete_table_content(self, table_name):
        # Useful to delete all the table contents
        self.database.engine.execute(
            # 'DELETE FROM {};'.format(self.table.__name__)
            'DELETE FROM {};'.format(table_name)
        )


class MySQLDatabaseService(DatabaseService):
    """ A class of some useful functions to deal with MySQL database """
    def __init__(self, database):
        super().__init__(database)

    def reset(self):
        self.reset_fk_check()
        self.drop_all()
        self.create_all()
        self.set_fk_check()

    def set_charset(self, db_uri):
        """
        This is required to make the database accept arabic characters
        To make sure that the database has been updated, use the following query
        SELECT default_character_set_name FROM information_schema.SCHEMATA
            WHERE schema_name = "db_name"; [USE THE QUOTES]
        :param db_uri: uri to connect with the database
        :return:
        """
        db_name = db_uri.split('/')[-1]
        self.database.engine.execute(
            'ALTER DATABASE {} CHARACTER SET UTF8MB4 COLLATE UTF8MB4_unicode_520_ci;'.format(db_name))


class SQLiteDatabaseService(DatabaseService):
    """ A class of some useful functions to deal with SQLite database """
    def __init__(self, database):
        super().__init__(database)

    def reset(self):
        self.drop_all()
        self.create_all()
        self.enforce_sqlite_fk_integrity()

    def enforce_sqlite_fk_integrity(self):
        self.database.engine.execute('pragma foreign_keys = 1')