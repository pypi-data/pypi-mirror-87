import re


def regex_modify_string(s, pattern, repl, flags=0):
    sr = re.sub(pattern, repl, s, flags=flags)
    return sr


if __name__ == "__main__":
    print('### bon string ###')
