#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import argparse
from pypushflow.representation.scheme.ows_parser import OwsParser
from pypushflow import Workflow
import darfix.version
import pypushflow.version
import os

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def _convert(scheme, output_file, overwrite):
    """

    :param scheme:
    :param scan:
    :param timeout:
    :return:
    """
    _logger.warning("translate {} to {}".format(scheme, output_file))

    if os.path.exists(output_file):
        if overwrite is True:
            os.remove(output_file)
        else:
            raise ValueError("{} already exists.".format(output_file))

    with open(output_file, "w+") as file_:
        file_.write(_dump_info_generation())
        # add import ignore process
        file_.write(
            "{}\n".format("from darfix.core.process import IgnoreProcess")
        )

    workflow = Workflow.ProcessableWorkflow(scheme)
    converter = Workflow.Converter(workflow=workflow, output_file=output_file)
    converter.process()

    # set up workflow
    with open(output_file, mode="a") as file_:
        file_.write(_dump_executable_script_section())
    _logger.info(
        "translation finished. You can execute python {} [scan path] [[--entry]]".format(
            output_file
        )
    )


def _dump_info_generation():
    return (
        "# This file has been generated automatically using \n"
        "# pypushflow {} and darfix {}\n".format(
            pypushflow.version.version, darfix.version.version
        )
    )


def _dump_executable_script_section():
    return """
if __name__ == '__main__':
    import argparse
    import sys
    from darfix.core.dataset import Dataset
    from silx.gui import qt

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'file_directory',
        help='Directory containing images')

    options = parser.parse_args(sys.argv[1:])
    dataset = Dataset(options.file_directory)
    main(input_data=(dataset, None, None, None), channel='dataset')
    """


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workflow_file",
        help="Path to the .ows file defining the workflow to process with the"
        "provided scan",
    )
    parser.add_argument("output_file", help="Output python file")
    parser.add_argument(
        "--overwrite",
        help="Overwrite output file if exists",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )
    options = parser.parse_args(argv[1:])
    if not options.output_file.lower().endswith(".py"):
        options.output_file = options.output_file + ".py"
    # tune the log level
    log_level = logging.INFO
    if options.debug is True:
        log_level = logging.DEBUG

    for log_ in ("darfix", "pypushflow"):
        logging.getLogger(log_).setLevel(log_level)

    scheme = OwsParser.scheme_load(options.workflow_file, load_handlers=True)
    _convert(
        scheme=scheme, output_file=options.output_file, overwrite=options.overwrite
    )


if __name__ == "__main__":
    main(sys.argv)
