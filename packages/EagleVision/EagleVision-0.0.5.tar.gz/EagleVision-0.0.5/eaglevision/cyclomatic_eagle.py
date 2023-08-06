"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
import os
import subprocess
from pathlib import Path
import pandas as pd
from eaglevision.base_eagle import BaseEagle


class CyclomaticEagle(BaseEagle):
    """ To extract the cyclomatic complexity of a repo: """

    def __init__(self):
        """ Constructor for the class """
        super(CyclomaticEagle)
        super().__init__()
        self.cmd = ""
        self.report_path = None

    def __cmd_builder(self):
        """ Function to form the cyclomatic complexity tool (lizard) command to be executed """
        self.cmd = 'python -m lizard "%s" ' % self.get_proj_path()
        args = ""
        if self.get_cyclo_args():
            args = self.get_cyclo_args()
        exclude = ",".join(str(x) for x in self.get_cyclo_exclude() if x is not None)
        if exclude:
            exclude = ','.join(' -x "{0}"'.format(w) for w in exclude.rstrip().split(','))
        self.cmd = self.cmd + args + " " + exclude + " --csv"
        print(self.cmd) # pragma: no mutate

    def __subprocess_out(self):
        """ Function to execute the subprocess with the specified cyclomatic complexity tool """
        file_out = open(os.path.join(self.report_path, "cyclomatic-complexity.csv"), "w")
        status = subprocess.call(r'%s' % self.cmd, stdout=file_out)
        if status:
            print("There was error while processing the sub process command") # pragma: no mutate
        file_out.close()
        return status

    def __report(self):
        """ Function to report the cyclomatic complexity execution report """
        dataframe = pd.read_csv(os.path.join(self.report_path, "cyclomatic-complexity.csv"),
                                names=["NLOC", "CCN", "Token", "Param", "Length", "Location",
                                       "Path", "Function", "Args", "Row", "Col"],
                                sep=',')
        dataframe.drop(['Path', 'Function', 'Row', 'Col'], axis=1, inplace=True)
        dataframe.sort_values('CCN', ascending=False, inplace=True)
        dataframe["Location"] = dataframe["Location"].str.replace('\\', '/')
        self.report_html(os.path.join(self.report_path,
                                      "cyclomatic-complexity-report.html"), dataframe,
                         "Cyclomatic Complexity report")

    def __set_report_path(self):
        """ Function to set the report path for cyclomatic complexity"""
        self.report_path = os.path.join(self.get_report_path(), "cyclomatic_report")
        Path(self.report_path).mkdir(parents=True, exist_ok=True)

    def orchestrate_cyclomatic(self, json):
        """ Function which orchestrate the cyclomatic complexity  execution"""
        print("\n\n=================================")  # pragma: no mutate
        print("Please wait while [Cyclomatic analysis Tool] process your inputs")  # pragma: no mutate
        self.populate_data(json)
        self.__set_report_path()
        self.__cmd_builder()
        if not self.__subprocess_out():
            self.__report()
            print("\n\n[Cyclomatic analysis Tool] saved the reports @ %s" % self.report_path)  # pragma: no mutate
            print("=================================")  # pragma: no mutate
