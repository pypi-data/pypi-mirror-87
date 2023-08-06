"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import argparse
from eaglevision.cloc_eagle import ClocEagle
from eaglevision.base_eagle import BaseEagle
from eaglevision.cyclomatic_eagle import CyclomaticEagle
from eaglevision.similarity_eagle import SimilarityEagle


def create_parser(args):
    """ Function which add the command line arguments required for the command line input
    of text similarity index processor"""
    # Create the parser
    cos_parser = argparse.ArgumentParser(description='EagleVision')

    # Add the arguments
    cos_parser.add_argument("--path",
                            metavar="--p",
                            type=str,
                            help="Input file path")
    # ...Create your parser as you like...
    return cos_parser.parse_args(args)


class EagleVision(BaseEagle):
    """ Class which consolidates the matrices on Similarity, Cyclomatic Complexity, Cloc """

    def __init__(self, json_path):
        """ Constructor for the class """
        super(EagleVision)
        super().__init__()
        self.json_path = json_path

    @staticmethod
    def __eaglewatch_cloc__(json):
        """ Function which invokes the Cloc class for analysis """
        cloceagleobj = ClocEagle()
        cloceagleobj.orchestrate_cloc(json)

    @staticmethod
    def __eaglewatch_cyclo__(json):
        """ Function which invokes the Cyclomatic complexity class for analysis """
        cyclomaticeagleobj = CyclomaticEagle()
        cyclomaticeagleobj.orchestrate_cyclomatic(json)

    @staticmethod
    def __eaglewatch_similarity__(json):
        """ Function which invokes the Similarity analysis class for analysis """
        similarityeagleobj = SimilarityEagle()
        similarityeagleobj.orchestrate_similarity(json)

    @staticmethod
    def __empty_call():
        """ Empty call handler"""
        pass # pylint: disable=W0107

    def eaglewatch(self):
        """ Function which orchestrate the execution of  eaglewatch """
        json_data = self.read_json(self.json_path)
        for data in range(len(json_data)):  # pylint: disable=C0200
            self.populate_data(json_data[data])
            try:
                toggle = [self.get_run_cloc_metric(), self.get_run_cyclomatic_complexity(),
                          self.get_run_similarity() or self.get_run_pattern_match()]
                function_dict = {
                    "CYCLOEXE": lambda: self.__eaglewatch_cyclo__(json_data[data]), # pylint: disable=W0640
                    "CLOCEXE": lambda: self.__eaglewatch_cloc__(json_data[data]), # pylint: disable=W0640
                    "SIMEXE": lambda: self.__eaglewatch_similarity__(json_data[data]), # pylint: disable=W0640
                    "": lambda: self.__empty_call() # pylint: disable=W0108
                }
                for i in range(0, 3):
                    func = toggle[i]
                    function_dict[func]()
            except KeyError:
                continue
