import os
import socket
import threading
from time import sleep
from coverage import Coverage
from coverage.data import CoverageData, CoverageDataFiles
from coverage.files import abs_file, PathAliases
from coveragePy.multiproc import patch_multiprocessing
import multiprocessing as mp

cov = Coverage(config_file=True, data_suffix=True)
cov.config.omit = ['*.py']
if cov.config.omit is None:
    cov.config.omit = []
# cov.config.omit += ['*multiproc.py', '*coverage_logger.py', '*flash.py']
cov.config.omit += ['*.py']
cov.config.parallel = True
cov.start()
patch_multiprocessing(cov.config_file)

DEBUG = True


def get_data_dict(d):
    """Return a dict like d, but with keys modified by `abs_file`."""
    res = {}
    keys = list(d.keys())
    for k in keys:
        a = {}
        lines = list(d[k].keys())
        for l in lines:
            v = d[k].pop(l)
            a[l] = v
        res[abs_file(k)] = a
    return res


class CoverageLoggerThread(threading.Thread):
    _kill_now = False
    _delay = 10

    def __init__(self, main=True):
        self.main = main
        self._data = CoverageData()
        self._fname = cov.config.data_file
        self._suffix = ".{}.{}".format(socket.gethostname(), os.getpid())
        self._data_files = CoverageDataFiles(basename=self._fname,
                                             warn=cov._warn)
        self._pid = os.getpid()
        super(CoverageLoggerThread, self).__init__()

    def shutdown(self):
        self._kill_now = True

    def combine(self):
        aliases = None
        if cov.config.paths:
            # from coverage.aliases import PathAliases
            aliases = PathAliases()
            for paths in self.config.paths.values():
                result = paths[0]
                for pattern in paths[1:]:
                    aliases.add(pattern, result)

        self._data_files.combine_parallel_data(self._data, aliases=aliases)

    def export(self, new=True):
        cov_report = cov
        if new:
            # cov_report = Coverage(config_file=True)
            # 不显示原有文件
            cov_report = Coverage(omit=['main.py', 'multiproc.py', 'coverage_logger.py'])
            cov_report.load()
        self.combine()
        self._data_files.write(self._data)
        cov_report.data.update(self._data)
        cov_report.combine()
        cov_report.xml_report(outfile="coverage_report_data_new.html\\report.xml")
        cov_report.html_report(directory="coverage_report_data_new.html")
        cov_report.report(show_missing=True)

    def _collect_and_export(self):
        new_data = get_data_dict(cov.collector.data)
        print(new_data)
        if cov.collector.branch:
            self._data.add_arcs(new_data)
        else:
            self._data.add_lines(new_data)
        self._data.add_file_tracers(get_data_dict(cov.collector.file_tracers))
        self._data_files.write(self._data, self._suffix)

    def run(self):
        while True:
            sleep(CoverageLoggerThread._delay)
            if self._kill_now:
                break
            if DEBUG:
                print(mp.current_process().name, cov.collector.data)

            self._collect_and_export()

            if self.main:
                self.export()

        cov.stop()

        if not self.main:
            self._collect_and_export()
            return
        print("Main ok")

        self.export(new=False)
        print("End of the program. I was killed gracefully :)")
