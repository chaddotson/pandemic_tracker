from logging import getLogger
from matplotlib import pyplot as plt
from os import makedirs
from os.path import dirname

logger = getLogger(__name__)


class ReportOutput(object):
    def output(self, *args, **kwargs):
        return None


class DisplayReportOutput(ReportOutput):
    def output(self, *args, **kwargs):
        plt.show()
        return None


class FileReportOutput(ReportOutput):
    def output(self, filename, file_type='png', *args, **kwargs):
        makedirs(dirname(filename), exist_ok=True)
        plt.savefig(filename, format=file_type, bbox_inches='tight')
        return filename
