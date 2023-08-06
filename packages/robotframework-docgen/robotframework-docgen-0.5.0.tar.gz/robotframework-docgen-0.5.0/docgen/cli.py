#!/usr/bin/env python3
"""Robot Framework documentation finder and generator.

Example usage:
> docgen -f html Process
> docgen RPA.*

"""
import argparse
import fnmatch
import logging
import sys
from pathlib import Path

from docgen import finder, loader, patcher, converter
from docgen.utils import timed, debug_traceback


DEFAULT_EXCLUDE = (
    r"_*",
    r"*.setup",
    r"*.main",
    r"antigravity",
    r"robot.libraries.Remote",
    r"robot.libraries.Reserved",
)


def filter_include(matches, patterns):
    output = []
    for match in matches:
        for pattern in patterns:
            if fnmatch.fnmatch(match, pattern):
                output.append(match)
                break
    return output


def filter_exclude(matches, patterns):
    output = []
    for match in matches:
        for pattern in patterns:
            if fnmatch.fnmatch(match, pattern):
                logging.debug("Ignoring %s", match)
                break
        else:
            output.append(match)
    return output


def create_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("pattern", help="library name pattern", nargs="?", default="*")
    parser.add_argument(
        "-o", "--output", help="output directory", type=Path, default="dist"
    )
    parser.add_argument(
        "-f",
        "--format",
        help="output format",
        choices=converter.CONVERTERS,
        default="json-html",
    )
    parser.add_argument(
        "--no-patches",
        action="store_true",
        help="Don't apply automatic patches to generated output",
    )
    parser.add_argument(
        "--no-curdir",
        action="store_true",
        help="Don't parse resources from current directory",
    )
    parser.add_argument(
        "-v", "--verbose", help="be more talkative", action="store_true"
    )
    return parser


def run(raw_args=None):
    parser = create_parser()
    args = parser.parse_args(raw_args)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
    )

    with timed("All"):
        with timed("Find"):
            if args.pattern == "robotframework":
                matches = finder.builtins()
                include = "*"
            elif args.pattern == "rpaframework":
                matches = finder.rpaframework()
                include = "*"
            else:
                matches = finder.find_all(curdir=(not args.no_curdir))
                include = args.pattern
            matches.sort()

        with timed("Filter"):
            matches = filter_include(matches, [include])
            matches = filter_exclude(matches, DEFAULT_EXCLUDE)

        with timed("Load"):
            libraries = []
            for match in matches:
                try:
                    lib = loader.load(match)
                    libraries.append(lib)
                except ImportError:
                    debug_traceback()

        if not args.no_patches:
            with timed("Patch"):
                for lib in libraries:
                    patcher.apply_all(lib)

        args.output.mkdir(parents=True, exist_ok=True)
        with timed("Convert"):
            for lib in libraries:
                converter.convert(lib, args.format, args.output)

    logging.info("Created %d file(s)", len(libraries))
