import pyodbc


def sql_query_rows(connection_string, query,
                   query_size=100000):
    """Return dict list."""
    with pyodbc.connect(connection_string) as cnxn:
        cursor = cnxn.cursor()
        cursor.execute(query)
        rows = cursor.fetchmany(query_size)
        full_query_result = {'description': cursor.description, 'rows': rows}
        return _extract_dict_list_from_sql_query_result(full_query_result)


def sql_query_cell(connection_string, query):
    return sql_execute_query(connection_string, query)


def sql_execute_query(connection_string, query):
    with pyodbc.connect(connection_string) as cnxn:
        cursor = cnxn.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.commit()
        return res[0]


def _extract_dict_list_from_sql_query_result(full_query_result):
    dict_rows = []
    if full_query_result['rows']:
        for query_row in full_query_result['rows']:
            row = {}
            for i in range(len(full_query_result['description'])):
                row[full_query_result['description'][i][0]] = query_row[i]
            dict_rows.append(row)
    return dict_rows


if __name__ == "__main__":
    print('### bon sql ###')
