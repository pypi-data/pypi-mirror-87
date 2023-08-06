"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
import os
import subprocess
from pathlib import Path
import pandas as pd
from eaglevision.base_eagle import BaseEagle


class ClocEagle(BaseEagle): # pylint: disable=R0903
    """ To extract the code matrices of a repo: LOC, Comments, Type of languages etc """

    def __init__(self):
        """ Constructor for the class """
        super(ClocEagle)
        super().__init__()
        self.cmd = ""
        self.report_path = None

    def __cmd_builder(self):
        """ Function to form the cloc command to be executed """
        args = ""
        if self.get_cloc_args():
            args = self.get_cloc_args()
        file_out = os.path.join(self.report_path, "cloc.csv")
        self.cmd = 'cloc "%s" --csv --out="%s" %s' % (
            self.get_proj_path().replace('\\', '/'), file_out.replace('\\', '/'), args) # pragma: no mutate
        print(self.cmd) # pragma: no mutate

    def __write_cmd(self):
        """ Function to create a batch file to execute cloc """
        file_out = open(os.path.join(self.report_path, "cloc.cmd"), "w")
        file_out.write(self.cmd)
        file_out.close()

    def __subprocess_out(self):
        """ Function to execute cloc command """
        self.__write_cmd()
        status = subprocess.call(os.path.join(self.report_path, "cloc.cmd"))
        if status:
            print("There was error while processing the sub process command") # pragma: no mutate
        return status

    def __report(self):
        """ Function to report the execution report of cloc"""
        dataframe = pd.read_csv(os.path.join(self.report_path, "cloc.csv"))
        dataframe.drop(dataframe.columns[len(dataframe.columns) - 1], axis=1, inplace=True)
        self.report_html(os.path.join(self.report_path, "cloc-report.html"), dataframe,
                         "Cloc Report")

    def __set_report_path(self):
        """ Function to set the report path"""
        self.report_path = os.path.join(self.get_report_path(), "cloc_report")
        Path(self.report_path).mkdir(parents=True, exist_ok=True)

    def orchestrate_cloc(self, json):
        """ Function which orchestrate the cloc execution"""
        print("\n\n=================================")  # pragma: no mutate
        print("Please wait while [Cloc analysis Tool] process your inputs")  # pragma: no mutate
        self.populate_data(json)
        self.__set_report_path()
        self.__cmd_builder()
        if not self.__subprocess_out():
            self.__report()
            print("\n\n[Cloc analysis Tool] saved the reports @ %s" % self.report_path)  # pragma: no mutate
            print("=================================")  # pragma: no mutate
