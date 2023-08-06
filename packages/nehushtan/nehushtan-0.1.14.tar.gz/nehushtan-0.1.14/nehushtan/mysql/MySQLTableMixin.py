#  Copyright (c) 2020. Sinri Edogawa


from abc import ABC
from typing import Iterable, List

import pymysql

from nehushtan.mysql import constant
from nehushtan.mysql.MySQLCondition import MySQLCondition
from nehushtan.mysql.MySQLQueryResult import MySQLQueryResult
from nehushtan.mysql.MySQLViewMixin import MySQLViewMixin


class MySQLTableMixin(MySQLViewMixin, ABC):

    def insert_one_row(
            self,
            row_dict: dict,
            commit_immediately: bool = False,
            on_duplicate_key_update_rows: dict = None,
            with_ignore: bool = False
    ):
        return self._write_one_row(row_dict, 'INSERT', commit_immediately, on_duplicate_key_update_rows, with_ignore)

    def replace_one_row(self, row_dict: dict, commit_immediately: bool = False):
        return self._write_one_row(row_dict, 'REPLACE', commit_immediately)

    @staticmethod
    def _build_on_duplicate_key_update_sql(on_duplicate_key_update_rows: dict):
        sql_parts = []
        for field, value in on_duplicate_key_update_rows.items():
            sql_parts.append(f'{field}={value}')
        sql_parts = ", ".join(sql_parts)
        return f'ON DUPLICATE KEY UPDATE {sql_parts}'

    def _write_one_row(
            self,
            row_dict: dict,
            write_type: str,
            commit_immediately: bool = False,
            on_duplicate_key_update_rows: dict = None,
            with_ignore: bool = False
    ):
        fields = []
        values = []
        for k, v in row_dict.items():
            fields.append('`' + k + '`')
            values.append(self.get_mysql_kit().quote(v))
        fields = ",".join(fields)
        values = ",".join(values)
        ignore = ''
        if with_ignore:
            ignore = ' IGNORE'
        sql = f"{write_type}{ignore} INTO {self.get_table_expression()} ({fields}) VALUES ({values})"

        if type(on_duplicate_key_update_rows) is dict:
            sql_parts = self._build_on_duplicate_key_update_sql(on_duplicate_key_update_rows)
            sql = f'{sql} {sql_parts}'

        return self._modify_with_sql(sql, commit_immediately)

    def insert_many_rows_with_dicts(
            self,
            row_dicts: List[dict],
            commit_immediately: bool = False,
            on_duplicate_key_update_rows: dict = None,
            with_ignore: bool = False
    ):
        return self._write_many_rows_with_dicts(
            row_dict_array=row_dicts,
            write_type='INSERT',
            commit_immediately=commit_immediately,
            on_duplicate_key_update_rows=on_duplicate_key_update_rows,
            with_ignore=with_ignore
        )

    def replace_many_rows_with_dicts(self, row_dicts: List[dict], commit_immediately: bool = False):
        return self._write_many_rows_with_dicts(
            row_dict_array=row_dicts,
            write_type='REPLACE',
            commit_immediately=commit_immediately
        )

    def insert_many_rows_with_matrix(
            self,
            fields: Iterable[str],
            row_matrix: Iterable[Iterable],
            commit_immediately: bool = False,
            on_duplicate_key_update_rows: dict = None,
            with_ignore: bool = False
    ):
        return self._write_many_rows_with_matrix(
            fields=fields,
            row_matrix=row_matrix,
            write_type='INSERT',
            commit_immediately=commit_immediately,
            on_duplicate_key_update_rows=on_duplicate_key_update_rows,
            with_ignore=with_ignore
        )

    def replace_many_rows_with_matrix(
            self,
            fields: Iterable[str],
            row_matrix: Iterable[Iterable],
            commit_immediately: bool = False
    ):
        return self._write_many_rows_with_matrix(
            fields=fields,
            row_matrix=row_matrix,
            write_type='REPLACE',
            commit_immediately=commit_immediately
        )

    def _write_many_rows_with_dicts(
            self,
            row_dict_array: List[dict],
            write_type: str,
            commit_immediately: bool = False,
            on_duplicate_key_update_rows: dict = None,
            with_ignore: bool = False
    ):
        if len(row_dict_array) <= 0:
            return MySQLQueryResult.create_error_result('Rows Empty')

        sample_row = row_dict_array[0]

        fields = []
        for k, v in sample_row.items():
            fields.append(f'`{k}`')
        fields = ",".join(fields)

        row_sql = []
        for row in row_dict_array:
            values = []
            for k, v in row.items():
                values.append(self.get_mysql_kit().quote(v))
            values = ",".join(values)
            row_sql.append(f'({values})')
        if len(row_sql) <= 0:
            raise ValueError("You are trying to write zero rows!")
        row_sql = ",".join(row_sql)

        ignore = ''
        if with_ignore:
            ignore = ' IGNORE'

        sql = f"{write_type}{ignore} INTO {self.get_table_expression()} ({fields}) VALUES {row_sql}"

        if type(on_duplicate_key_update_rows) is dict:
            sql_parts = self._build_on_duplicate_key_update_sql(on_duplicate_key_update_rows)
            sql = f'{sql} {sql_parts}'

        return self._modify_with_sql(sql, commit_immediately)

    def _write_many_rows_with_matrix(
            self,
            fields: Iterable[str],
            row_matrix: Iterable[Iterable],
            write_type: str,
            commit_immediately: bool = False,
            on_duplicate_key_update_rows: dict = None,
            with_ignore: bool = False
    ):
        fields_sql = ",".join([f"`{x}`" for x in fields])
        row_sql = []
        for row in row_matrix:
            values = []
            for v in row:
                values.append(self.get_mysql_kit().quote(v))
            values = ",".join(values)
            row_sql.append(f'({values})')
        if len(row_sql) <= 0:
            raise ValueError("You are trying to write zero rows!")
        row_sql = ",".join(row_sql)

        ignore = ''
        if with_ignore:
            ignore = ' IGNORE'

        sql = f"{write_type}{ignore} INTO {self.get_table_expression()} ({fields_sql}) VALUES {row_sql}"

        if type(on_duplicate_key_update_rows) is dict:
            sql_parts = self._build_on_duplicate_key_update_sql(on_duplicate_key_update_rows)
            sql = f'{sql} {sql_parts}'

        return self._modify_with_sql(sql, commit_immediately)

    def write_rows_with_raw_selection_sql(
            self,
            write_type: str,
            fields: Iterable[str],
            selection_sql: str,
            with_ignore: bool = False,
            on_duplicate_key_update_rows: dict = None,
            commit_immediately: bool = False
    ):
        """
        < Experimental Method, Since 0.1.10>
        It is a low level method for
        [INSERT ... SELECT Statement](https://dev.mysql.com/doc/refman/8.0/en/insert-select.html)
        and [REPLACE Statement](https://dev.mysql.com/doc/refman/8.0/en/replace.html)
        Be Careful when use this.
        :param write_type: INSERT or REPLACE
        :param fields:
        :param selection_sql: 'SELECT ...' If select from one table, you may use MySQLTableSelection::generate_sql()
        :param with_ignore:
        :param on_duplicate_key_update_rows:
        :param commit_immediately:
        :return:
        """
        ignore = ''
        if with_ignore:
            ignore = ' IGNORE'

        fields_sql = ",".join([f'`{x}`' for x in fields])

        sql = f"{write_type}{ignore} INTO {self.get_table_expression()} ({fields_sql}) {selection_sql}"

        if type(on_duplicate_key_update_rows) is dict:
            sql_parts = self._build_on_duplicate_key_update_sql(on_duplicate_key_update_rows)
            sql = f'{sql} {sql_parts}'

        return self._modify_with_sql(sql, commit_immediately)

    def _modify_with_sql(self, sql: str, commit_immediately: bool = False):
        result = MySQLQueryResult()
        cursor = None

        try:
            result.set_sql(sql)
            cursor = self.get_mysql_kit().get_raw_connection().cursor()
            cursor.execute(sql)
            result.set_status(constant.MYSQL_QUERY_STATUS_EXECUTED)
            result.set_last_inserted_id(cursor.lastrowid)
            result.set_affected_rows(cursor.rowcount)
            if commit_immediately:
                self.get_mysql_kit().get_raw_connection().commit()

        except pymysql.MySQLError as e:
            result.set_status(constant.MYSQL_QUERY_STATUS_ERROR)
            result.set_error(f"MySQL Error {e.__class__}: [{e.args[0]}] {e.args[1]}")

        except Exception as pe:
            result.set_status(constant.MYSQL_QUERY_STATUS_ERROR)
            result.set_error(f"Python Error {pe.__class__}: {pe}")

        finally:
            if cursor is not None:
                cursor.close()
            return result

    def update_rows(
            self,
            conditions: Iterable[MySQLCondition],
            modifications: dict,
            commit_immediately: bool = False,
            with_ignore: bool = False,
            sort_expression: str = '',
            limit: int = 0
    ):
        """
        [UPDATE Statement](https://dev.mysql.com/doc/refman/8.0/en/update.html)
        :param conditions:
        :param modifications:
        :param commit_immediately:
        :param with_ignore:
        :param sort_expression:
        :param limit:
        :return:
        """
        condition_sql = MySQLCondition.build_sql_component(conditions)

        modify_pairs = []
        for k, v in modifications.items():
            modify_pairs.append(f'`{k}`=' + self.get_mysql_kit().quote(v))
        modify_pairs = ",".join(modify_pairs)

        ignore = ''
        if with_ignore:
            ignore = ' IGNORE'

        sql = f"UPDATE{ignore} {self.get_table_expression()} SET {modify_pairs} WHERE {condition_sql}"

        if len(sort_expression) > 0:
            sql = f"{sql} ORDER BY {sort_expression}"

        if limit > 0:
            sql = f"{sql} LIMIT {limit}"

        return self._modify_with_sql(sql, commit_immediately)

    def delete_rows(
            self,
            conditions: Iterable[MySQLCondition],
            commit_immediately: bool = False,
            with_ignore: bool = False,
            sort_expression: str = '',
            limit: int = 0
    ):
        """
        [DELETE Statement](https://dev.mysql.com/doc/refman/8.0/en/delete.html)
        :param conditions:
        :param commit_immediately:
        :param with_ignore:
        :param sort_expression:
        :param limit:
        :return:
        """
        condition_sql = MySQLCondition.build_sql_component(conditions)

        ignore = ''
        if with_ignore:
            ignore = ' IGNORE'

        sql = f"DELETE{ignore} FROM {self.get_table_expression()} WHERE {condition_sql}"

        if len(sort_expression) > 0:
            sql = f"{sql} ORDER BY {sort_expression}"

        if limit > 0:
            sql = f"{sql} LIMIT {limit}"

        return self._modify_with_sql(sql, commit_immediately)
