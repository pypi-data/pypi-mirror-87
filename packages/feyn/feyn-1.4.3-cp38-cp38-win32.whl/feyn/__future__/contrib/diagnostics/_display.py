import numpy as np
from os import path
import pathlib
from io import StringIO


def _to_string_table(table):
    lens = dict()
    size = len(table[list(table.keys())[0]])
    for key, value in table.items():
        max_len = max([len(str(v)) for v in value])
        lens[key] = max(max_len+2, len(key)+2)

    total_len = np.sum(list(lens.values())) + len(lens.keys())

    file_str = StringIO()
    file_str.write('-'*total_len+'\n')
    file_str.write('|'.join([f"{key}".center(lens[key]) for key in table.keys()]) + '\n')
    file_str.write('-'*total_len + '\n')
    for i in range(size):
        file_str.write('|'.join([f"{table[key][i]}".center(lens[key]) for key in table.keys()]) + '\n')
    file_str.write('-'*total_len + '\n')

    return file_str.getvalue()


def print_tables(diagnostics, filepath=None, silent=False):
    """ Prints a list of diagnostics objects as a table. Can either print to stdout or to a file

    Arguments:
        diagnostics {list(dict(str, str))} -- Your list of graph diagnostics

    Keyword Arguments:
        filepath {str} -- file to save the results to (default: {None})
        silent {bool} -- whether to print the first table or not when saving to a file. (default: {False})

    Raises:
        ValueError: Raises ValueError if no diagnostics are supplied, or if silent=True when writing to stdout.
    """
    if len(diagnostics) == 0:
        raise ValueError("No diagnostics to save")

    if filepath is None:
        if silent:
            raise ValueError("Silent output only supported when writing to file")

        table_string = StringIO()
        for table in diagnostics:
            table_string.write(_to_string_table(table))

        print(table_string.getvalue())
    else:
        import json
        table_json = json.dumps(diagnostics)

        dirname = path.dirname(filepath)
        if not path.exists(dirname):
            pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)

        with open(filepath, mode='w') as fd:
            fd.write(table_json)

        if not silent:
            print(f"File {filepath} successfully written.")
            print("First table: \n", _to_string_table(diagnostics[0]))
