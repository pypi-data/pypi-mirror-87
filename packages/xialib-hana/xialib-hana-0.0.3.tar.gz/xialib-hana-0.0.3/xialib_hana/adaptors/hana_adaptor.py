import os
import json
from datetime import datetime
from typing import List
from hdbcli import dbapi
from xialib.adaptor import DbapiQmarkAdaptor

class HanaAdaptor(DbapiQmarkAdaptor):
    type_dict = {
        'NULL': ['null'],
        'NVARCHAR(8)': ['date'],
        'NVARCHAR(6)': ['time'],
        'NVARCHAR({})': ['c_', 'n_'],
        'NVARCHAR(1024)': ['char'],
        'DECIMAL({}, {})': ['real', 'd_'],
        'BOOLEAN': ['bool'],
        'TINYINT': ['i_1'],
        'SMALLINT': ['i_2'],
        'INTEGER': ['i_4'],
        'BIGINT': ['int', 'i_8'],
        'BLOB': ['blob'],
    }

    # Variable Name: @table_name@, @field_types@, @key_list@
    create_sql_template = "CREATE COLUMN TABLE {} ( {}, PRIMARY KEY( {} ))"
    # Variable Name: @table_name@, @columne_name@, @column_type@
    alter_column_template = "ALTER TABLE {} ALTER ({} {})"

    obs_insert_sql = ("(IFNULL(r._SEQ, '') || "
                      "LPAD(IFNULL(TO_NVARCHAR(r._AGE), ''), 10, '0') || "
                      "LPAD(IFNULL(TO_NVARCHAR(r._NO), ''), 10, '0')) > "
                      "(IFNULL(t._SEQ, '') || "
                      "LPAD(IFNULL(TO_NVARCHAR(t._AGE), ''), 10, '0') || "
                      "LPAD(IFNULL(TO_NVARCHAR(t._NO), ''), 10, '0')) "
                      "AND r._OP in ('U', 'D') ")

    def __init__(self, connection: dbapi.Connection, **kwargs):
        super().__init__(connection=connection, **kwargs)
        if not isinstance(connection, dbapi.Connection):
            self.logger.error("HANA Connection Type Error", extra=self.log_context)
            raise TypeError("XIA-000019")

    def _datetime_sql_to_py(self, sql_format: str) -> str:
        return sql_format.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d')\
            .replace('HH24', '%H').replace('MI', '%M').replace('SS', '%S')

    def _get_date_time(self, date_time_str: str, src_sql_format: str, tar_sql_format: str):
        date_time = datetime.strptime(date_time_str, self._datetime_sql_to_py(src_sql_format))
        return datetime.strftime(date_time, self._datetime_sql_to_py(tar_sql_format))

    def _get_field_type(self, type_chain: list):
        search_dict = dict()
        for type in reversed(type_chain):
            for key, ref_chain in self.type_dict.items():
                for ref in ref_chain:
                    if type == ref and type_chain[-1] == type:
                        search_dict['exact_match'] = key
                    elif type == ref and type_chain[-1] != type:
                        search_dict['hiearchy_match'] = key
                    elif '_' in type and '_' in ref and type.split('_')[0] == ref.split('_')[0]:
                        params = type.split('_')[1:]
                        if key.startswith('NVARCHAR') and int(params[0]) > 5000:
                            search_dict['variable_match'] = 'NCLOB'
                        else:
                            search_dict['variable_match'] = key.format(*params)
        if search_dict:
            return search_dict.get('exact_match',
                                   search_dict.get('variable_match',
                                                   search_dict.get('hiearchy_match', '')))
        else:
            self.logger.error("{} Not supported".format(json.dumps(type_chain)), extra=self.log_context)  # pragma: no cover
            raise TypeError("XIA-000020")  # pragma: no cover

    def _get_field_types(self, field_data: List[dict]):
        field_types = list()
        for field in field_data:
            field_line_list = ['"' + self._sql_safe(field['field_name']) + '"']
            field_line_list.append(self._get_field_type(field['type_chain']))
            if field['type_chain'][-1] == 'date':
                if 'format' in field and field.get('default', None) is not None:
                    date_time_str = self._get_date_time(field['default'], field['format'], 'YYYYMMDD')
                else:
                    date_time_str = '00000000'
                field_line_list.append("DEFAULT '" + date_time_str + "'")
            elif field['type_chain'][-1] == 'time':
                if 'format' in field and field.get('default', None) is not None:
                    date_time_str = self._get_date_time(field['default'], field['format'], 'HH24MISS')
                else:
                    date_time_str = '000000'
                field_line_list.append("DEFAULT '" + date_time_str + "'")
            elif field.get('default', None) is not None and isinstance(field['default'], str):
                field_line_list.append("DEFAULT '" + self._sql_safe(field['default']) + "'")
            elif field.get('default', None) is not None and isinstance(field['default'], (int, float)):
                field_line_list.append("DEFAULT " + str(field['default']))
            field_line_list.append("COMMENT '" + field.get('description', '') + "'")
            field_line = ' '.join(field_line_list)
            field_types.append(field_line)
        return ",\n ".join(field_types)

    def _get_value_holders(self, field_data: List[dict]):
        holder_list = list()
        for field in field_data:
            if 'type_chain' not in field:
                holder_list.append("?")
            elif field['type_chain'][-1] == 'date':
                date_format = field.get('format', 'YYYY-MM-DD')
                holder_list.append(r"TO_NVARCHAR(TO_DATE(?, '" + date_format + r"'), 'YYYYMMDD')")
            elif field['type_chain'][-1] == 'time':
                time_format = field.get('format', 'HH24:MI:SS')
                holder_list.append(r"TO_NVARCHAR(TO_DATE(?, '" + time_format + r"'), 'HH24MISS')")
            else:
                holder_list.append("?")
        return ', '.join(holder_list)

    def alter_column(self, table_id: str, field_line: dict):
        alter_sql = self.alter_column_template.format(self._sql_safe(self._get_table_name(table_id)),
                                                      self._sql_safe('"' + field_line['field_name'] + '"'),
                                                      self._sql_safe(self._get_field_type(field_line['type_chain'])))
        cur = self.connection.cursor()
        try:
            cur.execute(alter_sql)
            return True
        except dbapi.NotSupportedError as e:
            self.logger.error("Alter target is not supported", extra=self.log_context)
            return False