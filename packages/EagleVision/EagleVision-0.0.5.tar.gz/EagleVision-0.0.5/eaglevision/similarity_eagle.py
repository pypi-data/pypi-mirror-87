"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import os
import os.path
import datetime
import time
from pathlib import Path
import pandas as pd
from functiondefextractor import core_extractor
from functiondefextractor import condition_checker
from similarity.similarity_io import SimilarityIO
from eaglevision.base_eagle import BaseEagle


class SimilarityEagle(BaseEagle):
    """ Class which conducts the Code extraction, Pattern check in the code and similarity analysis """

    def __init__(self):
        """ Constructor for the class """
        super(SimilarityEagle)
        super().__init__()
        self.dataframe = None
        self.report_path = None

    def __code_extraction__(self):
        """ Function to extract code from the folder"""
        val = True
        self.dataframe = core_extractor.extractor(self.get_proj_path(), annot=self.get_annotation(),
                                                  delta=self.get_delta(),
                                                  exclude=r"%s" % self.get_exclude_extraction())
        if self.dataframe.empty:
            print("No functions are extracted. Data frame is empty. Recheck your input arguments")
            val = False
        return val

    @staticmethod
    def get_timestamp():
        """ Function to get timestamp"""
        return str(datetime.datetime.fromtimestamp(time.time()).strftime('%H-%M-%S_%d_%m_%Y'))  # pragma: no mutate

    def __code_pattern_analyzer__(self):
        """" Function to extract patterns from the source code fetched in to the dataframe """

        if self.get_pattern() is not None and len(self.get_pattern()) == len(self.get_pattern_seperator()):
            for i in range(len(self.get_pattern())):
                pattern_sep = str(self.get_pattern_seperator()[i]) if self.get_pattern_seperator()[i] else None
                data, pattern = condition_checker.check_condition(str(self.get_pattern()[i]), self.dataframe,
                                                                  pattern_sep)
                if self.get_run_pattern_match():
                    self.__report_xlsx__(data, "%s_pattern" % self.get_pattern()[i])
                    pattern.to_html("%s.html" % os.path.join(self.report_path, self.get_pattern()[i] + "Pivot_" +
                                                             self.get_timestamp()))
        else:
            print("The pattern input is expected to be list and should be of same length as pattern separators")

    def __code_similarity__(self):
        """ Function to conduct the similarity analysis """
        similarity_io_obj = SimilarityIO(None, None, None)
        similarity_io_obj.file_path = self.report_path  # where to put the report
        similarity_io_obj.data_frame = self.dataframe
        if self.get_similarity_range():
            similarity_io_obj.filter_range = self.get_similarity_range()
        mapping = {similarity_io_obj.data_frame.columns[0]: 'Uniq ID',
                   similarity_io_obj.data_frame.columns[1]: 'Steps'}
        similarity_io_obj.data_frame.rename(columns=mapping, inplace=True)
        similarity_io_obj.uniq_header = "Uniq ID"  # Unique header of the input data frame
        processed_similarity = similarity_io_obj.process_cos_match()
        similarity_io_obj.report(processed_similarity)

    def __report_xlsx__(self, data_f, name):
        """ Function which write the dataframe to xlsx """
        file_path = os.path.join(self.report_path, name)
        # Github open ticket for the abstract method
        writer = pd.ExcelWriter("%s_%s.xlsx" % (file_path, self.get_timestamp()), engine="xlsxwriter")
        data_f.to_excel(writer, sheet_name=name)
        writer.save()

    def __set_report_path__(self):
        """ Function to set the report path"""
        self.report_path = os.path.join(self.get_report_path(), "pattern_and_similarity_report")
        Path(self.report_path).mkdir(parents=True, exist_ok=True)

    def orchestrate_similarity(self, json):
        """ Function which orchestrate the similarity execution"""
        self.populate_data(json)
        print("\n\n=================================")  # pragma: no mutate
        print("Please wait while input is processed")  # pragma: no mutate
        self.__set_report_path__()
        if self.__code_extraction__():
            print("Please wait while [Pattern matching tool] process your inputs")  # pragma: no mutate
            self.__code_pattern_analyzer__()
            print("[Pattern matching tool] have completed extracting the pattern check")  # pragma: no mutate
            if self.get_run_similarity():
                print("Please wait while [Code Similarity Tool]"
                      " process your inputs, This will take a while")  # pragma: no mutate
                self.__code_similarity__()
                print("\n[Code Similarity Tool] have completed Similarity analysis, "  # pragma: no mutate
                      "reports @ %s" % self.report_path)  # pragma: no mutate
            print("=================================")  # pragma: no mutate
