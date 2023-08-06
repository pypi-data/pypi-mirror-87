import os
import json
from contextlib import contextmanager


def plant_env(**params):
    if 'kv_dict' not in params:
        params['kv_dict'] = {}
    if 'folder_path' in params:
        with change_dir(params['folder_path']):
            for fp in os.listdir():
                _, fext = os.path.splitext(fp)
                if os.path.isfile(fp) and fext == '.json':
                    print(fp)
                    with open(fp, encoding="utf8") as f:
                        s = f.read()
                        for k, v in json.loads(s).items():
                            params['kv_dict'][k] = v
    for k, v in params['kv_dict'].items():
        k = f'BON_{k}' if not str(k).startswith('BON') else k
        os.environ[k.upper()] = v


def check_env(k=None):
    if k:
        return os.environ.get(k)
    res = {}
    for k, v in os.environ.items():
        if str(k).startswith('BON'):
            res[k] = v
    return res


def clean_up_env():
    for k, v in os.environ.items():
        if str(k).startswith('BON'):
            del os.environ[k]


@contextmanager
def change_dir(destination):
    try:
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)


if __name__ == "__main__":
    print('### ghost ###')
