import os
import re
import csv
import datetime
import json
import pyarrow.parquet as pq
from pandas import DataFrame


def read_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        s = f.read()
        return s


def read_string_default(file_name='x.json'):
    file_path = os.path.join(os.path.expanduser('~'), 'Downloads',
                             file_name)
    return read_string(file_path)


def read_json(file_path):
    with open(file_path) as f:
        s = f.read()
        jstr = json.loads(s)
        return jstr


def read_json_default(file_name='x'):
    file_path = os.path.join(os.path.expanduser('~'), 'Downloads',
                             '{}.json'.format(file_name))
    return read_json(file_path)


def read_lines(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        return lines


def read_csv_list(file_path):
    with open(file_path) as f:
        return f.readlines()


def read_csv_list_default(file_name='x'):
    file_path = os.path.join(os.path.expanduser('~'), 'Downloads',
                             '{}.csv'.format(file_name))
    return read_csv_list(file_path)


def read_csv_dict_list(file_path):
    """
    Return list of dict.
    """
    with open(file_path, encoding='utf-8-sig') as f:
        row_list = []
        lines = list(csv.reader(f, skipinitialspace=True))
        row_list = []
        headers = [x.strip() for x in lines[0]]
        for i in range(1, len(lines)):
            row_dict = {}
            row_values = lines[i]
            for j in range(0, len(row_values)):
                if not row_values[j] or row_values[j].lower() == 'null':
                    continue
                row_dict[headers[j]] = row_values[j]
            row_list.append(row_dict)
        return row_list


def read_csv_dict_list_default(file_name='x'):
    file_path = os.path.join(os.path.expanduser('~'), 'Downloads',
                             '{}.csv'.format(file_name))
    return read_csv_dict_list(file_path)


def write_string(s, file_path):
    with open(file_path, 'w') as f:
        f.write(s)


def write_string_default(s, file_name='x.json'):
    file_path = os.path.join(os.path.expanduser('~'), 'Downloads',
                             file_name)
    write_string(s, file_path)


def write_json(j_str, file_path):
    with open(file_path, 'w') as f:
        f.write(json.dumps(j_str, default=_datetime_handler,
                           sort_keys=False, indent=2))


def write_json_default(j_str, file_name='x'):
    file_path = os.path.join(os.path.expanduser('~'), 'Downloads',
                             '{}.json'.format(file_name))
    write_json(j_str, file_path)


def write_csv(j_str, file_path):
    with open(file_path, 'w') as f:
        csv_writer = csv.writer(f)
        cnt = 0
        for row in j_str:
            if cnt == 0:
                headers = row.keys()
                csv_writer.writerow(headers)
                cnt += 1
            csv_writer.writerow(row.values())


def write_csv_default(j_str, file_name='x'):
    file_path = os.path.join(os.path.expanduser('~'), 'Downloads',
                             '{}.csv'.format(file_name))
    write_csv(j_str, file_path)


def write_lines(lines, file_path):
    with open(file_path, 'w') as f:
        f.write('')
    with open(file_path, 'a') as f:
        for line in lines:
            f.write(line)


def write_file(f_bytes, file_path):
    with open(file_path, 'wb') as f:
        f.write(f_bytes)


def append_line(line, file_path):
    with open(file_path, 'a') as f:
        f.write(line)


def transform_parquet_to_json(src_file_path, dest_file_path):
    """
    Convert parquet to json file, and return json data.
    """
    parquet_data = pq.read_table(src_file_path)
    pandas_data = parquet_data.to_pandas()
    df_data = DataFrame(pandas_data)
    return df_data.to_json(dest_file_path, orient='records')


def transform_parquet_to_json_default(src_name='x', dest_name='x'):
    """
    Convert parquet to json file, and return json data.
    """
    src_file_path = mkdownloadspath(f'{src_name}.parquet')
    dest_file_path = mkdownloadspath(f'{dest_name}.out.json')
    return transform_parquet_to_json(src_file_path, dest_file_path)


def mkpath(*dirs):
    """ Return dir path with splat(*) dir components. """
    file_path = os.path.join(*dirs)
    return file_path


def mkdownloadspath(*dirs):
    """ Return dir path under default Downloads with splat(*) dir components. """
    file_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    return os.path.join(file_path, *dirs)


def mkuserpath(*dirs):
    """ Return dir path under default user path with splat(*) dir components. """
    file_path = os.path.join(os.path.expanduser('~'))
    return os.path.join(file_path, *dirs)


def mkdir(file_path):
    """ Generate dir with given file path. """
    try:
        os.makedirs(file_path, exist_ok=True)
    except OSError:
        print('Directory {} can not be created.'.format(file_path))


def _datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()


if __name__ == "__main__":
    print('### bon file ###')
