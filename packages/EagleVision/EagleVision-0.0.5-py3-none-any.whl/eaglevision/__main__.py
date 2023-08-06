"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import sys
from eaglevision.eaglevision import EagleVision
from eaglevision.eaglevision import create_parser


if __name__ == '__main__':
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    EAGLEVISIONOBJ = EagleVision(ARGS.path)
    EAGLEVISIONOBJ.eaglewatch()
