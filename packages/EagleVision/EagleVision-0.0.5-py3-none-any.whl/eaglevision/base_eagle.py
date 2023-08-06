"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
import os
import sys
import json
import shutil
import pandas as pd


class BaseEagle:  # pylint: disable=R0902
    """ Base class for the Similarity, Cloc and Cyclomatic complexity
     classes which holds generic data """

    def __init__(self):
        """ Constructor for the class """
        self.input_dict = dict()
        self._proj_path = None
        self._run_pattern_match = None
        self._run_similarity = None
        self._run_cloc_metric = None
        self._run_cyclomatic_complexity = None
        self._annotation = None
        self._pattern = None
        self._pattern_seperator = None
        self._delta = None
        self._exclude_extraction = None
        self._cyclo_exclude = None
        self._report_path = None
        self._cloc_args = None
        self._cyclo_args = None
        self._similarity_range = None
        self._report_folder = None

    # getter methods
    def get_report_folder(self):
        """
        Returns: project path
        """
        return self._proj_path if self._report_folder is None else self._report_folder

    def get_proj_path(self):
        """
        Returns: project path
        """
        return self._proj_path

    def get_run_pattern_match(self):
        """
        Returns:  project extraction yes or no
        """
        ret_val = ""
        if self._run_pattern_match:
            ret_val = "SIMEXE"
        return ret_val

    def get_run_similarity(self):
        """
        Returns: project similarity yes or no
        """
        ret_val = ""
        if self._run_similarity:
            ret_val = "SIMEXE"
        return ret_val

    def get_run_cloc_metric(self):
        """
        Returns: project cloc yes or no
        """
        ret_val = ""
        if self._run_cloc_metric:
            ret_val = "CLOCEXE"
        return ret_val

    def get_run_cyclomatic_complexity(self):
        """
        Returns: project cyclomatic complexity  yes or no
        """
        ret_val = ""
        if self._run_cyclomatic_complexity:
            ret_val = "CYCLOEXE"
        return ret_val

    def get_annotation(self):
        """
        Returns: annotation input
        """
        return self._annotation

    def get_pattern(self):
        """
        Returns: pattern input
        """
        return self._pattern

    def get_pattern_seperator(self):
        """
        Returns: pattern separator
        """
        return self._pattern_seperator

    def get_delta(self):
        """
        Returns: delta lines number
        """
        return self._delta

    def get_exclude_extraction(self):
        """
        Returns: exclude pattern
        """
        return self._exclude_extraction

    def get_cloc_args(self):
        """
        Returns: cloc complexity exclusion extension
        """
        return self._cloc_args

    def get_cyclo_args(self):
        """
        Returns: cyclomatic complexity optional arguments
        """
        return self._cyclo_args

    def get_cyclo_exclude(self):
        """
        Returns: cyclomatic complexity exclusion
        """
        return self._cyclo_exclude

    def get_report_path(self):
        """ Function to set the root level report folder name"""
        self._report_path = os.path.join(self.get_report_folder(), "EagleVisionReport")
        return self._report_path

    def get_similarity_range(self):
        """
        Returns: Similarity range
        """
        return self._similarity_range

    def __validate_inputs_path__(self):
        """This function helps in validating the user inputs"""

        if not os.path.isdir(self.get_proj_path()):
            print("Input path in json file is not correct --> Please recheck your inputs")  # pragma: no mutate
            sys.exit(1)

    @staticmethod
    def validate_path_json(file_path):
        """This function helps in validating the user inputs"""
        if not os.path.isfile(os.path.join(file_path)):
            print("Input path or json file is not correct --> Please recheck your inputs")  # pragma: no mutate
            sys.exit(1)

    def read_json(self, json_path):
        """ Read the input json provided"""
        self.validate_path_json(json_path)
        with open(os.path.join(json_path)) as file_in:
            data = json.load(file_in)
        return data

    def populate_data(self, json_data):
        """ Function to populate the input json data"""
        self.__json_to_var(json_data)
        self.__validate_inputs_path__()

    def __json_to_var(self, input_data):
        """ Function to set the value of the json input to class variable """
        self._proj_path = input_data["path"]
        self._run_pattern_match = input_data["run_pattern_match"]
        self._run_similarity = input_data["run_similarity"]
        self._run_cloc_metric = input_data["run_cloc_metric"]
        self._cyclo_exclude = input_data["cyclo_exclude"]
        self._cloc_args = input_data["cloc_args"]
        self._cyclo_args = input_data["cyclo_args"]
        # Config specific to similarity and pattern checker
        self._run_cyclomatic_complexity = input_data["run_cyclomatic_complexity"]
        self._annotation = input_data["extraction_annotation"]
        self._pattern = input_data["pattern_match"]
        self._pattern_seperator = input_data["pattern_seperator"]
        self._delta = input_data["extraction_delta"]
        self._exclude_extraction = input_data["extraction_exclude"]
        self._similarity_range = input_data["similarity_range"]
        self._report_folder = input_data["report_folder"]

    @staticmethod
    def report_html(file_path, html_data_frame, report_type):
        """ Function which is used to report output """
        folder_path = os.path.dirname(file_path)
        pd.set_option('colheader_justify', 'center')  # pragma: no mutate
        html_string = '''
        <html>
          <head><title>HTML Pandas Dataframe with CSS</title></head>
          <link rel="stylesheet" type="text/css" href="report_style.css"/>
          <h1 style="font-size:50px;">%s</h1>
          <body>
            {table}
          </body>
        </html>
        ''' % report_type  # pragma: no mutate

        with open(file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_string.format(table=html_data_frame.to_html(  # pragma: no mutate
                classes='mystyle')).replace(r'\r\n', "<br>").
                            replace(r'\n', "<br>").replace(r'\r', "<br>"))  # pragma: no mutate
        shutil.copy(os.path.join(os.path.dirname(__file__),
                                 "report_style.css"),
                    os.path.join(folder_path, "report_style.css"))  # pragma: no mutate
