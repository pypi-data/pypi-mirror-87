import requests


def http_get(**params):
    res = requests.get(**params)
    return res


def http_post(**params):
    res = requests.post(**params)
    return res


if __name__ == "__main__":
    print('### bone http ###')
