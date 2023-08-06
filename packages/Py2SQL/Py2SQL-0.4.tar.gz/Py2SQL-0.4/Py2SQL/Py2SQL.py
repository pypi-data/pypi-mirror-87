import inspect
import fdb
import os
from Py2SQL.generators.FileGenerator import FileGenerator
from Py2SQL.entities.Object import Object


class Py2SQL(object):
    __DBMS_name = "Firebird"

    def __init__(self):
        self.__connection = None
        self.__db_info = None

    def db_connect(self, db):
        self.__connection = fdb.connect(
            host=db.host,
            port=db.port,
            database=db.name,
            user=db.username,
            password=db.password
        )

        self.__db_info = db

    def db_disconnect(self):
        self.__connection.close()

    def db_engine(self):
        sql = """select rdb$get_context('SYSTEM', 'ENGINE_VERSION')
                 from rdb$database"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        version = cursor.fetchone()[0]
        cursor.close()

        return f"{self.__DBMS_name} version {version}"

    def db_name(self):
        return os.path.split(self.__db_info.name)[1].split('.')[0]

    def db_size(self):
        sql = """select ((select count(*) from rdb$pages)) * 
                 (select mon$page_size from mon$database) / 1
                  from rdb$database;"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        size = cursor.fetchone()[0] / 1000000
        cursor.close()

        return f"{size} MB"

    def db_tables(self):
        sql = """select a.RDB$RELATION_NAME
                 from RDB$RELATIONS a
                 where coalesce(RDB$SYSTEM_FLAG, 0) = 0 and RDB$RELATION_TYPE = 0"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        tables = [x[0].strip() for x in cursor.fetchall()]
        cursor.close()

        return tables

    def db_table_structure(self, table):
        sql = f"""select row_number() over(), trim(rrf."RDB$FIELD_NAME"), trim(rt."RDB$TYPE_NAME") 
                  from RDB$RELATION_FIELDS rrf 
	                inner join RDB$FIELDS rf on rrf.RDB$FIELD_SOURCE = rf."RDB$FIELD_NAME" 
	                inner join RDB$TYPES rt on rf."RDB$FIELD_TYPE" = rt.RDB$TYPE 
                  where rt."RDB$FIELD_NAME" = 'RDB$FIELD_TYPE' and rrf."RDB$RELATION_NAME" = '{table}';"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        columns = cursor.fetchall()
        cursor.close()

        return columns

    def db_table_size(self, table):
        sql = f"""select ((select count(*) from rdb$pages
                           where rdb$relation_id = (select rdb$relation_id
                                                    from rdb$relations
                                                    where rdb$relation_name = '{table}'))
                          ) * (select mon$page_size from mon$database) / 1
                  from rdb$database;"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        size = cursor.fetchone()[0] / 1000000
        cursor.close()

        return f"{size} MB"

    def find_object(self, table, py_object):
        object_attributes = py_object.__dict__
        sql = f"""select * 
                  from {table}
                  where """

        i = 0
        for key in object_attributes:
            val = f"'{object_attributes[key]}'" if type(object_attributes[key]) == type("str") else object_attributes[
                key]
            and_str = "and" if i > 0 else ""
            sql += f"{and_str} {key} = {val} "
            i += 1

        main_sql = f"""select trim(rrf."RDB$FIELD_NAME"), trim(rt."RDB$TYPE_NAME") 
                      from RDB$RELATION_FIELDS rrf 
	                    inner join RDB$FIELDS rf on rrf.RDB$FIELD_SOURCE = rf."RDB$FIELD_NAME" 
	                    inner join RDB$TYPES rt on rf."RDB$FIELD_TYPE" = rt.RDB$TYPE 
                      where rt."RDB$FIELD_NAME" = 'RDB$FIELD_TYPE' and rrf."RDB$RELATION_NAME" = '{table}'
                            and exists ({sql});"""

        cursor = self.__connection.cursor()

        try:
            cursor.execute(main_sql)
        except:
            return []

        attributes = cursor.fetchall()
        cursor.close()

        result = []
        for attr in attributes:
            if attr[0].lower() in object_attributes:
                result.append((*attr, object_attributes[attr[0].lower()]))

        return result

    def find_objects_by(self, table, attributes):
        sql = f"""select * 
                          from {table}
                          where """
        where = ""

        i = 0
        for attr in attributes:
            val = f"'{attr[1]}'" if type(attr[1]) == str else attr[1]
            and_str = "and" if i > 0 else ""
            where += f"{and_str} {attr[0]} = {val} "
            i += 1

        sql += where
        main_sql = f"""select trim(rrf."RDB$FIELD_NAME"), trim(rt."RDB$TYPE_NAME") 
                              from RDB$RELATION_FIELDS rrf 
        	                    inner join RDB$FIELDS rf on rrf.RDB$FIELD_SOURCE = rf."RDB$FIELD_NAME" 
        	                    inner join RDB$TYPES rt on rf."RDB$FIELD_TYPE" = rt.RDB$TYPE 
                              where rt."RDB$FIELD_NAME" = 'RDB$FIELD_TYPE' and rrf."RDB$RELATION_NAME" = '{table}'
                                    and exists ({sql});"""

        cursor1 = self.__connection.cursor()

        try:
            cursor1.execute(main_sql)
        except:
            return []

        fields = cursor1.fetchall()
        cursor1.close()

        sql_results_count = f"""select count(id)
                              from {table}
                              where {where}"""
        cursor2 = self.__connection.cursor()

        try:
            cursor2.execute(sql_results_count)
        except:
            return []

        results_count = cursor2.fetchone()[0]
        cursor2.close()


        result = []
        for i in range(0, results_count):
            row_res = []
            for field in fields:
                sql_res = f"""select {field[0]}
                             from {table}
                             where {where}"""
                curr_cursor = self.__connection.cursor()
                curr_cursor.execute(sql_res)
                curr_res = curr_cursor.fetchall()[i][0]
                curr_cursor.close()
                row_res.append((*field, curr_res))
            result.append(row_res)

        return result

    def find_class(self, py_class):
        sql_classes = """select trim("RDB$RELATION_NAME") from RDB$RELATIONS 
                         where "RDB$RELATION_NAME" not like 'RDB$%' 
                            and "RDB$RELATION_NAME" not like 'MON$%' 
                            and "RDB$RELATION_NAME" not like 'SEC$%'"""

        cursor1 = self.__connection.cursor()
        cursor1.execute(sql_classes)
        classes = [x[0] for x in cursor1.fetchall()]
        cursor1.close()

        class_attrs = self.getAttributes(py_class)
        seeken_class = None
        table_name = None
        for clss in classes:
            main_sql = f"""select trim(rrf."RDB$FIELD_NAME"), trim(rt."RDB$TYPE_NAME") 
                                  from RDB$RELATION_FIELDS rrf 
            	                    inner join RDB$FIELDS rf on rrf.RDB$FIELD_SOURCE = rf."RDB$FIELD_NAME" 
            	                    inner join RDB$TYPES rt on rf."RDB$FIELD_TYPE" = rt.RDB$TYPE 
                                  where rt."RDB$FIELD_NAME" = 'RDB$FIELD_TYPE' and rrf."RDB$RELATION_NAME" = '{clss}'"""

            curr_cursor = self.__connection.cursor()
            curr_cursor.execute(main_sql)
            db_class_attrs = curr_cursor.fetchall()
            curr_cursor.close()

            right_attrs_count = 0
            for attr in class_attrs:
                for db_attr in db_class_attrs:
                    if attr.lower() == db_attr[0].lower():
                        right_attrs_count += 1

            if right_attrs_count == len(db_class_attrs) and right_attrs_count == len(class_attrs):
                seeken_class = db_class_attrs
                table_name = clss

        if seeken_class is None:
            return []

        sql_results_count = f"""select count(id)
                                from {table_name}"""
        cursor2 = self.__connection.cursor()
        cursor2.execute(sql_results_count)
        results_count = cursor2.fetchone()[0]
        cursor2.close()

        result = []
        for i in range(0, results_count):
            row_res = []
            for field in seeken_class:
                sql_res = f"""select {field[0]}
                             from {table_name}"""
                curr_cursor = self.__connection.cursor()
                curr_cursor.execute(sql_res)
                curr_res = curr_cursor.fetchall()[i][0]
                curr_cursor.close()
                row_res.append((*field, curr_res))
            result.append(row_res)

        return result

    def find_classes_by(self, attributes):
        sql_classes = """select trim("RDB$RELATION_NAME") from RDB$RELATIONS 
                         where "RDB$RELATION_NAME" not like 'RDB$%' 
                            and "RDB$RELATION_NAME" not like 'MON$%' 
                            and "RDB$RELATION_NAME" not like 'SEC$%'"""

        cursor1 = self.__connection.cursor()
        cursor1.execute(sql_classes)
        classes = [x[0] for x in cursor1.fetchall()]
        cursor1.close()

        seeken_classes = []
        table_names = []
        for clss in classes:
            main_sql = f"""select trim(rrf."RDB$FIELD_NAME"), trim(rt."RDB$TYPE_NAME") 
                                  from RDB$RELATION_FIELDS rrf 
            	                    inner join RDB$FIELDS rf on rrf.RDB$FIELD_SOURCE = rf."RDB$FIELD_NAME" 
            	                    inner join RDB$TYPES rt on rf."RDB$FIELD_TYPE" = rt.RDB$TYPE 
                                  where rt."RDB$FIELD_NAME" = 'RDB$FIELD_TYPE' and rrf."RDB$RELATION_NAME" = '{clss}'"""

            curr_cursor = self.__connection.cursor()
            curr_cursor.execute(main_sql)
            db_class_attrs = curr_cursor.fetchall()
            curr_cursor.close()

            right_attrs_count = 0
            for attr in attributes:
                for db_attr in db_class_attrs:
                    if attr.lower() == db_attr[0].lower():
                        right_attrs_count += 1

            if right_attrs_count == len(attributes):
                seeken_classes.append(db_class_attrs)
                table_names.append(clss)

        if len(seeken_classes) == 0:
            return []

        return seeken_classes

    def create_object(self, table, id):
        attributes = [x[1] for x in self.db_table_structure(table)]
        attrs_sql = ""
        i = 0
        for attr in attributes:
            koma = ", " if i > 0 else ""
            attrs_sql += f"{koma}{attr}"
            i += 1

        sql = f"""select {attrs_sql}
                  from (
                        select row_number() over() as row_number, {attrs_sql}
                        from {table})   
                  where row_number = {id}"""

        curr_cursor1 = self.__connection.cursor()
        curr_cursor1.execute(sql)
        entity = curr_cursor1.fetchone()
        curr_cursor1.close()

        obj = Object()
        for j in range(0, len(attributes)):
            setattr(obj, attributes[j].lower(), entity[j])

        return obj

    def create_objects(self, table, fid, lid):
        objects = []

        for id in range(fid, lid+1):
            obj = self.create_object(table, id)
            objects.append(obj)

        return objects

    def getAttributes(self, clss):
        attrs = {}
        for name in vars(clss):
            if name.startswith("__") or name.endswith("__"):
                continue
            attr = getattr(clss, name)
            if callable(attr):
                continue
            attrs[name] = attr
        return attrs

    def create_class(self, table, module):
        attributes = [x[1] for x in self.db_table_structure(table)]
        class_name = table[:len(table)-1] if table.lower().endswith('s') else table
        class_name = class_name.lower().capitalize()

        file_content = FileGenerator.get_python_class(class_name, attributes)
        created = FileGenerator.create_class(module, file_content)

        frame = inspect.stack()[1]
        mod = inspect.getmodule(frame[0])
        filename = mod.__file__
        FileGenerator.import_module(filename, module, class_name, created)

    def create_hierarchy(self, table, package):
        package_created = FileGenerator.create_package(package)

        if package_created:
            tables = self.with_linked_tables(table)

            frame = inspect.stack()[1]
            mod = inspect.getmodule(frame[0])
            filename = mod.__file__

            for tab in tables:
                attributes = [x[1] for x in self.db_table_structure(tab)]
                class_name = tab[:len(tab) - 1] if tab.lower().endswith('s') else table
                class_name = class_name.lower().capitalize()

                module_content = FileGenerator.get_python_class(class_name, attributes)
                created = FileGenerator.create_package_module(package, class_name.lower(), module_content)

                FileGenerator.import_package_module(filename, package, class_name, created)

    def with_linked_tables(self, table, already_found = None):
        sql_linked = f"""select trim("RDB$RELATION_NAME") 
                         from RDB$INDICES ri 
                         where "RDB$INDEX_NAME" in (
                            select RDB$FOREIGN_KEY 
                            from RDB$INDICES ri 
                            where "RDB$RELATION_NAME" = '{table}' and RDB$FOREIGN_KEY is not null)"""

        sql_linked2 = f"""select trim("RDB$RELATION_NAME") 
                          from RDB$INDICES ri 
                          where RDB$FOREIGN_KEY in (
                            select "RDB$INDEX_NAME" 
                            from RDB$INDICES ri 
                            where "RDB$RELATION_NAME" = '{table}' and RDB$UNIQUE_FLAG = 1)"""

        curr_cursor = self.__connection.cursor()
        curr_cursor.execute(sql_linked)
        tables_list = [x[0] for x in curr_cursor.fetchall()]
        curr_cursor.close()

        curr_cursor2 = self.__connection.cursor()
        curr_cursor2.execute(sql_linked2)
        tables_list = tables_list + [x[0] for x in curr_cursor2.fetchall()]
        curr_cursor2.close()

        if already_found is not None:
            for tabl in tables_list:
                if tabl in already_found:
                    tables_list.remove(tabl)
                else:
                    already_found.append(tabl)
        else:
            already_found = []
            already_found = already_found + tables_list
            already_found.append(table)

        all_trans_tables = []
        for tabl in tables_list:
            trans_tables = self.with_linked_tables(tabl, already_found)
            all_trans_tables = all_trans_tables + trans_tables

        tables_list = tables_list + all_trans_tables
        tables_list.append(table)

        unique_set = set(tables_list)
        unique_list = list(unique_set)

        return unique_list

class Database(object):
    def __init__(self, host, port, name, username, password):
        self.__host = host
        self.__port = port
        self.__name = name
        self.__username = username
        self.__password = password

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def name(self):
        return self.__name

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password
