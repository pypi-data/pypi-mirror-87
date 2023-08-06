import os
from array import array
from inspect import isclass
from functools import wraps

import psycopg2


def should_be_connected(func):
    """Method decorator. If py2SQL wasn't connected and was called method with @should_be_connected,
    it will raise RuntimeError"""

    @wraps(func)
    def wrapper(*args):
        if args[0].was_connected():
            return func(*args)
        else:
            raise RuntimeError("wasn't connected")

    return wrapper


class Py2SQL:
    """Py2SQL is class provides access to a PostgreSQL database.
    First of all, you must connect to database by calling db_connect()"""

    def __init__(self):
        __was_connected = False
        __conn = None

    def was_connected(self):
        """Return true, if database was connected"""
        return self.__was_connected

    def db_connect(self, db):
        """Connect to database. db should be a map with keys {'name', 'user', 'password', 'host'}"""
        self.__conn = psycopg2.connect(dbname=db['name'], user=db['user'],
                                       password=db['password'], host=db['host'],
                                       port=db['port'])
        self.__was_connected = True

    @should_be_connected
    def db_disconnect(self):
        """Disconnect from database"""
        self.__was_connected = False
        self.__conn = None

    @should_be_connected
    def db_engine(self):
        """Return version of the database"""
        cursor = self.__conn.cursor()
        cursor.execute("SELECT version()")
        return cursor.fetchone()[0].split(',')[0]

    @should_be_connected
    def db_name(self):
        """Return name of database"""
        cursor = self.__conn.cursor()
        cursor.execute("SELECT current_database()")
        return cursor.fetchone()[0]

    @should_be_connected
    def db_tables(self):
        """Return list of table names"""
        cursor = self.__conn.cursor()
        cursor.execute("""SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'""")
        tables = cursor.fetchall()
        flatten = lambda t: [item for sublist in t for item in sublist]
        return flatten(tables)

    @should_be_connected
    def db_table_structure(self, table):
        """Returns an ordered list of tuples of the form (id, name, type),
        where id is the attribute number of the table 'table',
        name - attribute name, type - attribute type"""
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT ordinal_position, column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE table_name = '{table}'
                        ORDER BY ordinal_position""")
        return cursor.fetchall()

    @should_be_connected
    def db_size(self):
        """Returns the size of the database in Mb"""
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT pg_size_pretty(pg_database_size(db.datname))
                        FROM (SELECT current_database() datname) db""")
        return cursor.fetchone()[0]

    @should_be_connected
    def db_table_size(self, table):
        """Returns the size of the database table 'table'"""
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT pg_size_pretty(pg_total_relation_size('{table}'))""")
        return cursor.fetchone()[0]

    @should_be_connected
    def find_objects_by(self, table, attributes):
        """Returns an ordered list of database table entries containing
        the attributes specified in the sequence * attributes = [(name, value)].
        Each record is represented as a list of tuples of the type (attribute, type, value).
        Added support for comparisons in Py2SQL.find_objects_by (table, * attributes)
        by supporting the parameters field__gt, field__lt, field__gte, field__lte, field__in, field__not_in"""
        params_value = {'field__gt': '>', 'field__lt': '<',
                        'field__gte': '>=', 'field__lte': '<=',
                        'field__in': 'IN', 'field__not_in': 'NOT IN'}
        if not isinstance(attributes, list):
            raise RuntimeError('Attributes type error in find_objects_by')
        for attr in attributes:
            if not isinstance(attr, tuple) or len(attr) not in (2, 3):
                raise RuntimeError('Attribute type error find_objects_by')
        cursor = self.__conn.cursor()
        query = f"SELECT * from {table}"
        if len(attributes) > 0:
            query += " WHERE "

            query_params = []
            for attr in attributes:
                condition = '='
                if len(attr) == 3 and attr[2] in params_value:
                    condition = params_value[attr[2]]
                if 'IN' in condition:
                    query_params.append(f"{attr[0]} {condition} {tuple(attr[1])}")
                else:
                    query_params.append(f"{attr[0]} {condition} '{attr[1]}'")
            query += ' AND '.join(query_params)
        cursor.execute(query)
        return cursor.fetchall()

    @should_be_connected
    def find_class(self, py_class):
        """Returns an ordered list of structural elements of a database table table if it is structurally equivalent
        to the py_class class, provided that such a table exists. The structural elements of the table are represented in
         the form of a tuple (attribute, type)"""
        if not isclass(py_class):
            raise RuntimeError('is not class')
        structure = self.db_table_structure(py_class.__name__.lower())
        columns = list(map(lambda x: x[1], structure))

        result = []
        for key, value in py_class().__dict__.items():
            if key not in columns:
                return
            result.append((key, list(filter(lambda x: x[1] == key, structure))[0][2]))

        if len(result) == len(structure):
            return result

    @should_be_connected
    def find_classes_by(self, attributes):
        """Returns an ordered list of lists of structural elements of database tables that contain
        attributes specified in the sequence *attributes = [(attribute1_name)], provided that such tables exist.
        Each structural element is represented as a tuple of the type (attribute, type)"""
        if not isinstance(attributes, list):
            raise RuntimeError('Attributes type error in find_classes_by')
        for attr in attributes:
            if not isinstance(attr, tuple) or len(attr) != 1:
                raise RuntimeError('Attribute type error find_classes_by')

        result_map = {}
        for table in self.db_tables():
            def add_table_if_need():
                struct = self.db_table_structure(table)
                column_names = list(map(lambda x: x[1], struct))
                for attr in attributes:
                    if attr[0] not in column_names:
                        return
                result_map[table] = list(map(lambda x: (x[1], x[2]), struct))

            add_table_if_need()
        return result_map

    @should_be_connected
    def create_class(self, table, module, _globals=None):
        """Dynamically creates a new class program code based on the table and stores it in the module 'module',
        then dynamically imports the newly created class from the newly created module to the global scope of the running program
        If user will no give global scope, it will be created, but dont imported"""
        structure = self.db_table_structure(table)
        fields = list(map(lambda x: x[1], structure))
        init_list = ''
        for field in fields:
            init_list += ', ' + field
        if not os.path.exists(module):
            os.makedirs(module)
        try:
            file = open(f'./{module}/' + table + '.py', 'x')
            file.write(f'\nclass {table.capitalize()}:\n\n')
            file.write(f'    def __init__(self{init_list}):\n')
            for field in fields:
                file.write(f'        self.{field} = {field}\n')
            file.close()
            exec(f'from {module.replace("/", ".")}.{table} import {table.capitalize()}', _globals)
        except FileExistsError as e:
            raise RuntimeError(e)

    @staticmethod
    def __get_sql_type(py_value):
        if isinstance(py_value, str):
            return 'text'
        if isinstance(py_value, int):
            return 'bigint'
        if isinstance(py_value, float):
            return 'float8'
        if isinstance(py_value, (list, tuple, set, frozenset, array)):
            if len(py_value) == 0:
                raise RuntimeError('size of collection is 0')
            subtype = None
            for el in py_value:
                if subtype is None:
                    subtype = Py2SQL.__get_sql_type(el)
                else:
                    if subtype != Py2SQL.__get_sql_type(el):
                        raise RuntimeError(f'Invalid types in value: {py_value}')
            return f'{subtype}[]'
        if isinstance(py_value, dict):
            if len(py_value) == 0:
                raise RuntimeError('size of collection is 0')
            subtype = None
            for key, value in py_value:
                if subtype is None:
                    subtype = Py2SQL.__get_sql_type(key)
                    if subtype != Py2SQL.__get_sql_type(value):
                        raise RuntimeError(f'Invalid types in value: {py_value}')
                else:
                    if subtype != Py2SQL.__get_sql_type(key) or subtype != Py2SQL.__get_sql_type(value):
                        raise RuntimeError(f'Invalid types in value: {py_value}')
            return f'{subtype}[][2]'
        raise RuntimeError(f'Invalid type in value: {py_value}')

    @should_be_connected
    def _save_class(self, columns_to_add, columns_to_drop, table_name):
        cursor = self.__conn.cursor()
        sub_queries = []
        if len(self.db_table_structure(table_name)) == 0:  # create table
            query = f'CREATE TABLE {table_name}\n(\n'

            for column in columns_to_add:
                sub_queries.append(f'\t{column[0]} {column[1]}')
            end_of_query = ');'

        else:  # update table
            query = f'ALTER TABLE {table_name}\n'

            for column in columns_to_add:
                sub_queries.append(f'\tADD COLUMN {column[0]} {column[1]}')
            for column in columns_to_drop:
                sub_queries.append(f'\tDROP COLUMN {column}')
            end_of_query = ';'
        query += ',\n'.join(sub_queries)
        query += end_of_query
        cursor.execute(query)
        self.__conn.commit()

    @should_be_connected
    def save_class(self, py_class):
        """Creates a class view in the database or updates it if it already exists"""
        if not isclass(py_class):
            raise RuntimeError('is not class')
        table_name = py_class.__name__.lower()
        structure_in_db = self.db_table_structure(table_name)
        columns = list(map(lambda x: x[1], structure_in_db))

        columns_to_add = []
        columns_to_drop = []

        class_items = py_class().__dict__.items()
        class_values = list(map(lambda x: x[0], class_items))
        for key, value in class_items:
            if key not in columns:
                columns_to_add.append((key, Py2SQL.__get_sql_type(value)))

        for column in columns:
            if column not in class_values:
                columns_to_drop.append(column)

        self._save_class(columns_to_add, columns_to_drop, table_name)

    @should_be_connected
    def delete_class(self, py_class):
        """Finds and removes a class view from the database, if it exists"""
        if not isclass(py_class):
            raise RuntimeError('is not class')
        cursor = self.__conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {py_class.__name__.lower()};')
        self.__conn.commit()

    @should_be_connected
    def find_object(self, table, py_object):
        """Returns a table table entry that is equivalent to a py_object object in the form of a list of tuples
        of type (attribute, type, value), if such an entry exists"""
        cursor = self.__conn.cursor()
        query = f"SELECT exists(SELECT 1 FROM {table}"
        params = py_object.__dict__
        if len(params) > 0:
            query += ' WHERE '
            query_params = []
            for key in params:
                query_params.append(f"{key} {'IS' if params[key] is None else '='} %s")
            query += ' AND '.join(query_params)
        query += ')'
        cursor.execute(query, list(params.values()))
        if cursor.fetchone()[0]:
            cursor.execute(f"""SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS
                                    WHERE table_name = '{table}'
                                    ORDER BY ordinal_position""")
            result = cursor.fetchall()
            i = 0
            values = list(params.values())
            while i < len(result):
                result[i] += (values[i],)
                i += 1
            return result

    @should_be_connected
    def create_object(self, table, _id, _globals=None):
        """Dynamically creates a new object based on an entry with the id number from the database table"""
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT *
                                FROM {table}
                                LIMIT 1 OFFSET {_id - 1}""")
        object_params = cursor.fetchone()
        return Py2SQL._create_object(object_params, table, _globals)

    @should_be_connected
    def create_objects(self, table, fid, lid, _globals=None):
        """Dynamically creates a list of new objects that are created based on the records in the table
        of the database starting with the record with the number fid ending with the record with the number lid inclusive"""
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT *
                                FROM {table}
                                LIMIT {lid - fid} OFFSET {fid - 1}""")
        return [Py2SQL._create_object(params, table, _globals) for params in cursor.fetchall()]

    @staticmethod
    def _get_class(table, _globals):
        return _globals.get(table.capitalize())

    @staticmethod
    def _create_object(params, table, _globals):
        _class = Py2SQL._get_class(table, _globals)
        return _class(*params)

    def find_hierarchies(self):
        """Returns all tabular hierarchies of the database in the form of a list of tuple lists
        of the form (parent_table, child_table),
        where each individual list corresponds to a separate tabular hierarchy."""
        tables = self._get_tables_hierarchy()
        return Py2SQL._get_hierarchies(Py2SQL._to_dict(tables), Py2SQL._get_root(tables))

    @should_be_connected
    def _get_tables_hierarchy(self):
        cursor = self.__conn.cursor()
        cursor.execute("""WITH RECURSIVE ref (tbl, reftbl, depth,path, cycle) AS (
                    SELECT pg_class.oid, NULL::oid, 0, ARRAY[pg_class.OID], false
                    FROM pg_class
                             JOIN pg_namespace ON
                        pg_namespace.oid = pg_class.relnamespace
                    WHERE relkind = 'r'
                      AND nspname = 'public'
                      AND NOT EXISTS(
                            SELECT 1
                            FROM pg_constraint
                            WHERE conrelid = pg_class.oid
                              AND contype = 'f'
                        )
                    UNION ALL
                    SELECT conrelid, ref.tbl, ref.depth + 1, path || conrelid, conrelid = ANY (path)
                    FROM ref
                             JOIN pg_constraint ON
                            confrelid = ref.tbl AND
                            contype = 'f'
                    AND NOT cycle
                )
                SELECT tbl::regclass::text                              as tablename,
                       string_agg(DISTINCT reftbl::regclass::text, ',') as reftables,
                       max(depth)
                FROM ref
                GROUP BY tablename
                ORDER BY max(depth) DESC
                """)
        return cursor.fetchall()

    @staticmethod
    def _to_dict(tables):
        dictionary = dict()
        for table in tables:
            dictionary[table[0]] = None if table[1] is None else list(table[1].split(','))
        return dictionary

    @staticmethod
    def _get_root(tables):
        max_depth = tables[0][2]
        root = list()
        for table in tables:
            if table[2] == max_depth:
                root.append(table[0])
        return root

    @staticmethod
    def _get_hierarchies(dictionary, root):
        visited = dict()
        for value in list(dictionary.keys()):
            visited[value] = False
        result = list()
        for value in root:
            if not visited[value]:
                result.extend(Py2SQL._find_hierarchy(value, dictionary, visited))
        return result

    @staticmethod
    def _find_hierarchy(value, dictionary, visited):
        result = list()
        visited[value] = True
        if dictionary[value] is not None:
            for i in dictionary[value]:
                if not visited[i]:
                    visited[i] = True
                    results = Py2SQL._find_hierarchy(i, dictionary, visited)
                    if len(results) == 0:
                        result.append([(value, i)])
                    else:
                        for part_result in results:
                            current_result = [(value, i)]
                            current_result.extend(part_result)
                            result.append(current_result)

        return result

    @should_be_connected
    def create_hierarchy(self, table, package, _globals):
        """Dynamically creates the program code of the new class hierarchy on the basis of the table
        and all tables connected to it (including transitively connected)
        and saves its separate classes in the corresponding modules of the package
        then dynamically imports newly created classes and package to the global scope of the running program."""
        tables = self._get_tables_hierarchy()
        classes = Py2SQL._get_hierarchies(Py2SQL._to_dict(tables), [table])
        self.create_class(table, package, _globals)
        for i in classes:
            self.create_class(i[0][1], package, _globals)

    @should_be_connected
    def delete_hierarchy(self, root_class, _globals):
        """Finds and removes from the database a representation of the class hierarchy,
        where root_class is the root of the hierarchy, if it existed."""
        root = root_class.__name__[0].lower() + root_class.__name__[1:]
        classes = self._get_class_hierarchy(root_class, _globals)
        class_set = set()
        for _class in classes:
            class_set.add(_class)
        if len(class_set) == 0:
            class_set.add(root)
        if len(class_set) > 0:
            cursor = self.__conn.cursor()
            cursor.execute(f"""DROP TABLE IF EXISTS {','.join(class_set)} CASCADE""")
            self.__conn.commit()

    @should_be_connected
    def _get_class_hierarchy(self, root_class, _globals):
        class_items = root_class().__dict__.items()
        classes = [root_class.__name__, ]
        for key, value in class_items:
            current_class = value.__class__.__name__
            if value.__class__.__name__ in _globals and \
                    current_class not in classes:
                classes.extend(self._get_class_hierarchy(current_class))
            elif isinstance(value, list) and len(value) > 0 and value[0].__class__.__name__ in _globals:
                current_class = value[0].__class__
                classes.append(f'{root_class.__name__.lower()}_to_{current_class.__name__.lower()}')
                if current_class not in classes:
                    classes.extend(self._get_class_hierarchy(current_class, _globals))
        return classes

    @should_be_connected
    def _get_primary_keys(self, table_name):
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT c.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
        JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
          AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
        WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '{table_name}'""")
        return cursor.fetchone()

    @should_be_connected
    def save_object(self, _object):
        """Creates a representation of the object in the database or updates it if it already exists"""
        table_name = _object.__class__.__name__.lower()
        primary_keys = self._get_primary_keys(table_name)

        items = _object.__dict__.items()

        cursor = self.__conn.cursor()

        if len(primary_keys) == 0 or \
                len(self.find_objects_by(table_name, [(primary_keys[0], getattr(_object, primary_keys[0]))])) == 0:
            columns_names = list(map(lambda x: x[0], items))
            columns_values = list(map(lambda x: f"'{str(x[1])}'", items))
            cursor.execute(f"""INSERT INTO {table_name} ({', '.join(columns_names)})
                                    VALUES ({', '.join(columns_values)})""")
        else:
            cursor.execute(f"""UPDATE {table_name} SET {', '.join(map(lambda x: x[0] + "='" + str(x[1]) + "'", items))}
                                WHERE {primary_keys[0]}={str(getattr(_object, primary_keys[0]))}""")
        self.__conn.commit()

    @should_be_connected
    def delete_object(self, _object):
        """Finds and removes the object representation from the database, if it exists."""
        table_name = _object.__class__.__name__.lower()
        primary_keys = self._get_primary_keys(table_name)

        if len(primary_keys) > 0:
            cursor = self.__conn.cursor()
            cursor.execute(f"""DELETE FROM {table_name} 
                                WHERE {primary_keys[0]}={str(getattr(_object, primary_keys[0]))}""")
            self.__conn.commit()

    @should_be_connected
    def save_hierarchy(self, root_class, _globals):
        """Creates a representation of the class hierarchy hierarchy, where root_class is the root of the hierarchy,
        in the database, or updates it if it already exists."""
        if not isclass(root_class):
            raise RuntimeError('is not class')
        table_name = root_class.__name__.lower()
        structure_in_db = self.db_table_structure(table_name)
        columns = list(map(lambda x: x[1], structure_in_db))

        columns_to_add = []
        columns_to_drop = []

        class_items = root_class().__dict__.items()
        class_values = list(map(lambda x: x[0], class_items))
        for key, value in class_items:
            if key not in columns:
                if value.__class__.__name__ in _globals:
                    self.save_hierarchy(_globals.get(value.__class__.__name__), _globals)
                    columns_to_add.append((key, 'bigint'))
                elif isinstance(value, list) and len(value) > 0 and value[0].__class__.__name__ in _globals:
                    self.save_hierarchy(_globals.get(value[0].__class__.__name__), _globals)
                    cursor = self.__conn.cursor()
                    cursor.execute(
                        f"CREATE TABLE IF NOT EXISTS {table_name}_to_{value[0].__class__.__name__.lower()} ({table_name}_id bigint, {value[0].__class__.__name__.lower()}_id bigint)")
                    self.__conn.commit()
                else:
                    columns_to_add.append((key, Py2SQL.__get_sql_type(value)))

        for column in columns:
            if column not in class_values:
                columns_to_drop.append(column)
        if len(columns_to_add) > 0 or len(columns_to_drop) > 0:
            self._save_class(columns_to_add, columns_to_drop, table_name)
