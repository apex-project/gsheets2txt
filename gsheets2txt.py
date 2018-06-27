# -*- encoding: utf-8 -*-

import gspread
from sys import exit as _sysexit
import os.path as op
from os import system as os_system
from configparser import ConfigParser
from oauth2client.service_account import ServiceAccountCredentials
from codecs import open as codecs_open
from time import sleep

config_default = {
    "main": {
        'output_file_path': '_output.txt',
        'errors_file_path': '_errors.txt',
        'separator': '\t',
        'line_end': '\t\n',
        'google_credentials_path': 'credentials.json',
        'google_sheet_url': None,
        'columns_count': 3,
        'encoding': 'utf-8',
    }
}


def sysexit(code=0, pause=5):
    print("\n\nThis window will be closed automatically in %d sec..." % pause)
    sleep(pause)
    _sysexit(code)


def read_config(config_default, fp):
    config = ConfigParser()

    if not op.exists(fp):
        print("\n\nConfig file error!\nFile %s not found" % (fp,))
        sysexit(1)

    config.read_file(open(fp))
    config_user = config_default.copy()

    for cg in config_user.keys():
        cgroup = config_user[cg]
        for ck in cgroup.keys():
            try:
                v = config.get(cg, ck, )
                if type(config_default[cg][ck]) == int:
                    v = int(v)
                cgroup[ck] = v
            except Exception as e:
                if cgroup[ck] == None:
                    print("\n\nConfig file error!\nPlease specify parameter '%s' in [%s] group\n\n%s" % (ck, cg, e,))
                    sysexit(1)
                pass

    return config_user


def extend_list(l, c):
    l_c = len(l)
    if l_c < c:
        empty_list = ['' for i in range(c - l_c)]
        return l + empty_list
    else:
        return l[0:c]


def is_empty_list(l):
    for ll in l:
        if ll != None and ll != '':
            return False
    return True


def read_file(filename, line_sep="\n", encoding='utf-8'):
    result = []
    try:
        with open(filename, 'rb') as f:
            lines = f.readlines()
            for l in lines:
                l = l.decode(encoding, "ignore")
                result.append(l.split(line_sep)[0])
        return result
    except Exception as e:
        return None


def read_gsheets(cfg):
    scope = ['https://spreadsheets.google.com/feeds']
    crd_path = cfg['main']['google_credentials_path']

    if not op.exists(crd_path):
        print("Credentials file not found at %s" % crd_path)
        sysexit(1)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(crd_path, scope)

    gc = gspread.authorize(credentials)
    print("Reading url %s" % cfg['main']['google_sheet_url'])
    sh = gc.open_by_url(cfg['main']['google_sheet_url'])
    worksheet = sh.get_worksheet(0)
    columns = worksheet.get_all_values()
    cc = cfg['main']['columns_count']
    sep = cfg['main']['separator']

    result = []

    if len(columns) == 0:
        print('\n\nCurrent spreadsheet is empty')
        sysexit(1)

    for item in columns:
        items = extend_list(item, cc)
        if not is_empty_list(items):
            result.append(sep.join(items))

    return result


def are_equal_lists(x, y):
    return set(x) == set(y)


def alert_errors(lines, filename="_errors.txt"):
    if op.exists(filename):
        if len(lines) == 0:
            with codecs_open(filename, "w", encoding="utf-8") as f:
                f.write("")
            return
        errors_list_last = read_file(filename)
    else:
        errors_list_last = []

    try:
        with codecs_open(filename, "w", encoding="utf-8") as f:
            for ll in lines:
                f.write(ll + "\n")
    except Exception as exc:
        print('Error file writing error', exc)


def write_results(lines, filename, line_sep="\n", encoding="utf-8", errors="replace"):
    errors_list = []
    try:
        with open(filename, "wb") as f:
            i = 0
            for l in lines:
                i += 1
                try:
                    l = (l + line_sep).encode(encoding)
                except:
                    print("Invalid character not %s\n" % encoding, i, l)
                    errors_list.append(str(i) + " " + l)
                    l = (l + line_sep).encode(encoding, errors=errors)

                f.write(l)

    except Exception as e:
        print(l, "\n", e)
        errors_list.append(str(l) + ": " + str(e))


    if len(errors_list) == 0:
        return []
    else:
        return errors_list


def main():
    cfg = read_config(config_default, 'gsheets2txt.ini')
    output_file_path = config_default['main']['output_file_path']
    errors_file_path = config_default['main']['errors_file_path']
    line_sep = cfg['main']['line_end']
    encoding = cfg['main']['encoding']

    gspread_lines = read_gsheets(cfg)

    file_lines = read_file(output_file_path, line_sep, encoding=encoding)

    if file_lines is not None:
        ae = are_equal_lists(file_lines, gspread_lines)
    else:
        ae = False

    if ae:
        print("Spreadsheet has no changes. File not updated")
    else:
        errors_list = write_results(gspread_lines, output_file_path, line_sep, encoding=encoding)

        alert_errors(errors_list, errors_file_path)

        if file_lines:
            print("File %s updated" % output_file_path)
        else:
            print("File %s created" % output_file_path)


if __name__ == '__main__':
    try:
        main()
        sysexit(0)
    except Exception as e:
        print(e)
        sysexit(1)
