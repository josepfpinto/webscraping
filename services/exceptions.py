import os
import sys


def simple(string, error):
    print("\n", string, " ", error)


def more_info(string, error):
    print("\n Error | ", string)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, f_name, exc_tb.tb_lineno, " ", error)
