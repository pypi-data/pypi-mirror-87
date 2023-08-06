from pandas_profiling import ProfileReport
import pandas as pd
import sys


def main():
    pickle_path = sys.argv[1]
    report_path = sys.argv[2]
    report_title = sys.argv[3]
    data = pd.read_pickle(pickle_path)
    report = ProfileReport(data, title=report_title)
    report.to_file(report_path)
