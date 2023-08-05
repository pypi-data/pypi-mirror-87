# -*- coding: utf8 -*-

"""
Eines per a la connexió a bases de dades relacionals (Oracle i MariaDB)
i la manipulació de les seves dades i estructures.
"""

import datetime
import os
import random
import time

from .constants import (IS_PYTHON_3, TMP_FOLDER,
                        MARIA_CHARSET, MARIA_COLLATE, MARIA_STORAGE)
from .aes import AESCipher
from .services import DB_INSTANCES, DB_CREDENTIALS
from .textfile import TextFile


class StreamArray(list):
    def __init__(self, gen, *args):
        self.gen = gen
        self.args = args

    def __iter__(self):
        return self.gen(*self.args)

    def __len__(self):
        return 1


def get_selects(sql):
    sqlSelect = sql[sql.find("select") + 6:sql.find("from")]
    i = 0
    stack = []
    rm = []
    while i < len(sqlSelect):
        if "(" == sqlSelect[i]:
            stack.append(i)
        elif ")" == sqlSelect[i]:
            if len(stack) == 1:
                rm.append((stack.pop(), i))
            else:
                stack.pop()
        i += 1
    rm.reverse()
    for r1, r2 in rm:
        sqlSelect = sqlSelect[0:r1] + sqlSelect[r2 + 1:]
    sqlSelect = (sqlSelect.replace(" ", "").replace("distinct", "")
                 .replace("\n", "").lower().split(","))
    return sqlSelect


class Database(object):
    """
    Classe principal. S'instancia per cada connexió a una base de dades.
    Tots els mètodes es poden utilitzar per Oracle i MariaDB
    si no s'especifica el contrari.
    """

    def set_debug(self, deb=True):
        self.DEBUG = deb

    DEBUG = False
    NUM2L = (["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
              "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
              "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"])
    TEMPLATE = {
        # cod + val() <- has to be called
        'cod': (('TT101', lambda: random.random() * 250.0 + 1.0),
                ('TT102', lambda: random.random() * 200.0 + 20.0),
                ('TT103', lambda: random.random() * 50.0 + 10.0)),
        'dat': (lambda: str(random.randint(2000, 2020)) + random.choice(Database.NUM2L[0:12]) + random.choice(Database.NUM2L)),
        'naix': (lambda: str(random.randint(1930, 2005)) + random.choice(Database.NUM2L[0:12]) + random.choice(Database.NUM2L)),
        'id': (lambda: random.randint(1, 6)),
        'id_cip': (lambda: random.randint(1, 6)),
        'codi': (lambda: random.choice(["TT101", "TT102", "TT103", "Q78544", "Q03566", "Q03585", "N19627", "N19640", "N19685", "N18427", "N18440", "N18485", "G76211", "G40291", "013731", "G40111", "Q85544", "Q75958", "W29485", "Q85585", "N18542", "N18527", "N18540", "N18585", "009780", "013110"])),
        'descripcio': (lambda: "lorem ipsum algo no se que cosas latin"),
        'des': (lambda: "lorem ipsum otro algo no se latin"),
        'cataleg': (lambda: random.randint(1, 32)),
        'scs_codi': (lambda: "00089"),
        'ics_desc': (lambda: "ABS AMPOSTA"),
        'data_type': (lambda: random.choice(["date", "int", "bigint", "double", "varchar", "DATE", "DATE_J", "DATETIME", "TIMESTAMP(6)", "NUMBER", "VARCHAR2", "CHAR"])),
        'sector': lambda: random.choice(['6416', '6844', '6838', '6731', '6735', '6625', '6521', '6102', '6519', '6626', '6522', '6839', '6523', '6211', '6520', '6209', '6728', '6310', '6627', '6837', '6734'])
    }

    def __init__(self, instance, schema, retry=None):
        """
        Inicialització de paràmetres i connexió a la base de dades.
        En cas d'error, intenta cada (retry) segons.
        """
        hacked_instance = instance + 'p' if schema == 'prod' else instance
        attributes = DB_INSTANCES[hacked_instance]

        self.database = schema
        self.engine = attributes['engine']
        self.host = attributes['host']
        self.port = attributes['port']
        self.data = {}

        self.local_infile = None
        if self.engine == "my":
            self.local_infile = attributes['local_infile']

    def generate_one(self, sql):
        sqlSelect = get_selects(sql)
        data = {}
        if self.DEBUG:
            print(sqlSelect)
        if len(sqlSelect) > 0:
            for select in sqlSelect:
                while select in data:
                    select = select + "_aux"
                if select in Database.TEMPLATE:
                    if select == 'cod':
                        info = random.choice(Database.TEMPLATE[select])
                        data['cod'] = info[0]
                        data['val'] = info[1]()
                    else:
                        data[select] = Database.TEMPLATE[select]()
                elif select != 'val':
                    data[select] = str(random.randint(-50, -10))
                if "convert" in select:
                    data[select] = data[select].encode()
        sorted_data = sorted(data.items(), key=lambda x: sqlSelect.index(x[0])
                             if x[0] in sqlSelect else
                             len(sqlSelect) + 1)
        result = tuple(map(lambda d: d[1], sorted_data))
        if self.DEBUG:
            print(data)
            print(sorted_data)
        return result[0:len(sqlSelect)]

    def connect(self, existent=True):
        """Desencripta password i connecta a la base de dades."""
        pass

    def execute(self, sql):
        """Executa una sentència SQL."""
        print(sql)

    def recreate_database(self):
        """Elimina i torna a crear una base de dades (MariaDB)."""
        self.execute('drop database if exists {}'.format(self.database))
        sql = 'create database {} character set {} collate {}'
        self.execute(sql.format(self.database, MARIA_CHARSET, MARIA_COLLATE))
        self.execute('use {}'.format(self.database))

    def create_table(self, table, columns,
                     pk=None,
                     partition_type='hash', partition_id='id', partitions=None,
                     storage=MARIA_STORAGE, remove=False):
        """Crea una taula a la base de dades."""
        if remove:
            self.drop_table(table)
        if pk:
            if self.engine == 'my':
                spec = '({}, PRIMARY KEY ({}))'.format(', '.join(columns),
                                                       ', '.join(pk))
            elif self.engine == 'ora':
                spec = '({}, CONSTRAINT {}_pk PRIMARY KEY ({}))'.format(
                    ', '.join(columns),
                    table,
                    ', '.join(pk))
        else:
            spec = '({})'.format(', '.join(columns))
        if self.engine == 'my':
            this = ' engine {} character set {} collate {}'
            spec += this.format(storage, MARIA_CHARSET, MARIA_COLLATE)
        if partitions:
            this = ' partition by {} ({}) {}'
            spec += this.format(partition_type, partition_id,
                                'partitions {}'.format(partitions)
                                if partition_type == 'hash'
                                else '({})'.format(', '.join(partitions)))
        try:
            self.execute('create table {} {}'.format(table, spec))
        except Exception as e:
            s = str(e)
            if not any([word in s for word in ('1050', 'ORA-00955')]):
                raise e

    def drop_table(self, table):
        """Elimina una taula."""
        if self.engine == 'my':
            self.execute('drop table if exists {}'.format(table))
        elif self.engine == 'ora':
            try:
                self.execute('drop table {} PURGE'.format(table))
            except Exception:
                pass

    def rename_table(self, old_name, new_name, ts=False):
        """Reanomena una taula."""
        if ts:
            ara = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            new_name += '_{}'.format(ara)
        self.drop_table(new_name)
        try:
            if self.engine == 'my':
                self.execute('rename table {} to {}'.format(old_name,
                                                            new_name))
            elif self.engine == 'ora':
                self.execute('rename {} to {}'.format(old_name, new_name))
        except Exception:
            done = False
        else:
            done = True
        return done

    def get_all(self, sql, limit=None):
        """
        Crea un generator que retorna d'un en un tots els registres
        obtinguts per una sentència SQL.
        """
        self.execute(sql)

        def _gen(sql, limit=None):
            if not (limit is None):
                sql = self.get_limit_clause(sql, limit)
            r = random.randint(0, 100)
            while r >= 5:
                r = random.randint(0, 100)
                row = self.generate_one(sql)
                yield row

        return StreamArray(_gen, sql, limit)

    def get_many(self, sql, n, limit=None):
        """
        Crea un generator que retorna de n en n tots els registres
        obtinguts per una sentència SQL.
        """
        self.execute(sql)

        def _gen(sql, limit=None):
            if limit:
                sql = self.get_limit_clause(sql, limit)

            r = random.randint(0, 1000)
            while r >= 2:
                r = random.randint(0, 1000)
                row = self.generate_one(sql)
                yield row

        return StreamArray(_gen, sql, limit)

    def get_limit_clause(self, sql, rows):
        """
        Modifica la sentència SQL de get_all o get_many
        per limitar el número de registres.
        """
        if self.engine == 'my':
            spec = ' limit {}'.format(rows)
        elif self.engine == 'ora':
            particula = 'and' if 'where' in sql else 'where'
            spec = ' {} rownum <= {}'.format(particula, rows)
        sql += spec
        return sql

    def get_one(self, sql):
        """Retorna un registre d'una sentència SQL."""
        self.execute(sql)
        return self.generate_one(sql)

    def list_to_table(self, iterable, table, partition=None, chunk=None):
        """
        Insereix un iterable a una taula:
          -a MariaDB utilitza txt_to_table
          -a Oracle utilitza _list_to_table_oracle
        """
        print(str(table) + ": " + str(iterable))
        if table in self.data:
            self.data[table].append(iterable)
        else:
            self.data[table] = iterable

    def _list_to_table_oracle(self, sql, iterable):
        """Auxiliar per càrrega a oracle."""
        self.execute(sql)

    def file_to_table(self, filename, table, partition, delimiter, endline):
        """Carrega un fitxer a una taula (MariaDB)."""
        sql = "LOAD DATA {local} INFILE '{filename}' \
               ignore INTO TABLE {table} {partition} \
               CHARACTER SET {charset} \
               FIELDS TERMINATED BY '{delimiter}' \
               LINES TERMINATED BY '{endline}'"
        sql = sql.format(
            local='LOCAL' if self.local_infile else '',
            filename=filename,
            table=table,
            partition='PARTITION ({})'.format(
                partition) if partition else '',
            charset=MARIA_CHARSET,
            delimiter=delimiter,
            endline=endline
        )
        self.execute(sql)
        os.remove(filename)

        def get_tables(self):
            """Retorna les taules de la base de dades."""
            if self.engine == 'my':
                sql = "select table_name, table_rows \
                       from information_schema.tables \
                       where table_schema = '{}'".format(self.database)
            elif self.engine == 'ora':
                sql = "select table_name, num_rows from all_tables"
            tables = {table: rows for table, rows in self.get_one(sql)}
            return tables

    def get_table_owner(self, table, dblink=None):
        """Retorna el propietari i el nom original d'una taula (Oracle)."""
        table = table.upper()
        dblink_txt = "@{}".format(dblink.upper()) if dblink else ""
        try:
            sql = "select table_name from user_tables{} \
                   where table_name = '{}'"
            table, = self.get_one(sql.format(dblink_txt, table))
            owner, = self.get_one('select user from dual')
        except TypeError:
            try:
                sql = "select table_owner, table_name from user_synonyms{} \
                       where synonym_name = '{}'"
                owner, table = self.get_one(sql.format(dblink_txt, table))
                try:
                    sql = "select table_owner, table_name from all_synonyms{} \
                           where owner = '{}' and synonym_name = '{}'"
                    owner, table = self.get_one(sql.format(dblink_txt, owner,
                                                           table))
                except TypeError:
                    pass
            except TypeError:
                try:
                    sql = "select table_owner, table_name from all_synonyms{} \
                           where owner = 'PUBLIC' and \
                                 synonym_name = '{}' and \
                                 db_link is null"
                    owner, table = self.get_one(sql.format(dblink_txt, table))
                except TypeError:
                    sql = "select owner, table_name from all_tables{} \
                           where table_name = '{}'"
                    owner, table = self.get_one(sql.format(dblink_txt, table))
        return owner, table

    def get_table_count(self, table, owner=None, dblink=None):
        """Retorna el número de registres d'una taula."""
        return int(random.random() * 250.0)

    def get_table_partitions(self, table, owner=None, dblink=None):
        """
        Retorna un diccionari amb les particions d'una taula
        i el seu número de registres.
        """
        if self.engine == 'my':
            sql = "select engine from information_schema.tables \
                   where table_schema = '{}' and table_name = '{}'"
            sql = sql.format(self.database, table)
            is_merge = 'MRG' in self.get_one(sql)[0]
            if is_merge:
                sql = 'show create table {}'.format(table)
                create = self.get_one(sql)[1]
                raw_tables = create.split('UNION=(')[1][:-1].split(',')
                tables = [tab.replace('`', '') for tab in raw_tables]
                sql = "select table_name, table_rows \
                       from information_schema.tables \
                       where table_schema = '{}' and table_name in {}"
                sql = sql.format(self.database, tuple(tables))
            else:
                sql = "select partition_name, table_rows \
                       from information_schema.partitions \
                       where table_schema = '{}' and table_name = '{}' \
                       and partition_name is not null"
                sql = sql.format(self.database, table)
        elif self.engine == 'ora':
            if not owner:
                owner, table = self.get_table_owner(table, dblink=dblink)
            dblink_txt = "@{}".format(dblink.upper()) if dblink else ""
            sql = "select partition_name, nvl(num_rows, 0) \
                   from all_tab_partitions{} \
                   where table_owner = '{}' and table_name = '{}'"
            sql = sql.format(dblink_txt, owner.upper(), table.upper())
        partitions = {}
        for partition, rows in self.get_all(sql):
            partitions[partition] = rows
        return partitions

    def get_table_columns(self, table, owner=None, dblink=None):
        """Retorna una llista amb les columnes de la taula."""
        if self.engine == 'my':
            sql = "select column_name from information_schema.columns \
                   where table_schema = '{}' and table_name = '{}' \
                   order by ordinal_position".format(self.database, table)
        elif self.engine == 'ora':
            if not owner:
                owner, table = self.get_table_owner(table, dblink=dblink)
            dblink_txt = "@{}".format(dblink.upper()) if dblink else ""
            sql = "select column_name from all_tab_columns{} \
                   where owner = '{}' and table_name='{}' \
                   order by column_id".format(dblink_txt, owner.upper(),
                                              table.upper())
        columns = [column for column, in self.get_all(sql)]
        return columns

    def get_column_information(self, column, table, owner=None,
                               desti='my', dblink=None):
        """
        Retorna un diccionari amb les instrucciones necessàries
        tant per crear com per consultar la columna especificada.
        """
        if self.engine == 'my':
            sql = "select column_type, data_type, character_maximum_length, \
                   numeric_precision from information_schema.columns \
                   where table_schema = '{}' and table_name = '{}' \
                   and column_name = '{}'".format(self.database, table, column)
            done, type, char, num = self.get_one(sql)
            length, precision, scale = None, None, None
        elif self.engine == 'ora':
            if not owner:
                owner, table = self.get_table_owner(table, dblink=dblink)
            dblink_txt = "@{}".format(dblink.upper()) if dblink else ""
            sql = "select data_type, data_length, data_precision, data_scale \
                   from all_tab_columns{} \
                   where owner = '{}' and table_name = '{}' \
                   and column_name = '{}'".format(dblink_txt, owner.upper(),
                                                  table.upper(),
                                                  column.upper())
            type, length, precision, scale = self.get_one(sql)
            done, char, num = None, None, None
            words_in = ('DAT', 'VAL_D_V')
            words_out = ('EDAT',)
            if type == 'NUMBER' and \
               any([word in column.upper() for word in words_in]) and \
               not any([word in column.upper() for word in words_out]):
                type = 'DATE_J'
            if column.upper() == "VISI_DATA_UPDA":
                type = "DATETIME"
        param = {'column': column, 'length': length,
                 'precision': precision, 'scale': scale,
                 'done': done, 'char': char, 'num': num}
        resul = {key: column for key in ('create', 'query')}
        return resul

    def set_statistics(self, table):
        """Calcula les estadístiques d'una taula d'Oracle."""
        pass

    def set_grants(self, grants, tables, users, inheritance=True):
        """Estableix grants."""
        pass

    def disconnect(self):
        """Desconnecta de la base de dades."""
        pass

    def __enter__(self):
        """Context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager."""
        self.disconnect()
