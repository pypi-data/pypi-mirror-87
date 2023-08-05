#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import textwrap as _textwrap
from fixalign import run_multiprocess
from fixalign.version import VERSION

class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string

    def _fill_text(self, text, width, indent):
        return ''.join(indent + line for line in text.splitlines(keepends=True))

    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        return _textwrap.wrap(text, 80)


"""
The script is used to import fixalign package and run run_multiprocess function to find and fix small exon missed reads.
"""


def main():
    parser = argparse.ArgumentParser(description="Find and fix small exon missed region in noisy long reads based on transcript annotation.",
                                     formatter_class=CustomHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    # positional arguments
    parser.add_argument("inBam", help="Input original bam file.")
    parser.add_argument(
        "genomeFasta", help="Reference genome fasta file, with fai index under the same directory.")
    parser.add_argument(
        "annotBed", help="Annotated transcripts file in BED12 format.")
    parser.add_argument(
        "outRegion", help="Output Region file, regions contain missed small exons.")
    # optional arguments
    parser.add_argument("-v", "--version", help="Print version and exit.",
                        action="version", version="fixalign {0}".format(VERSION))
    parser.add_argument("-c", "--coreNum", help="The number of cpu cores we used.",
                        default=1, type=int, metavar="N")
    parser.add_argument("-s", "--exonSizeThd", help="The threshold of exons size, ignore exons size > exonSizeThd.",
                        default=80, type=int, metavar="N")
    parser.add_argument("-d", "--deltaRatioThd",
                        help="The threshold of absolute delta ratio, ignore abs(delta ratio) > deltaRatioThd.",
                        default=0.5, type=float, metavar="float")
    parser.add_argument("-f", "--flankLen", help="The extended length on the both sides of realign region.",
                        default=20, type=int, metavar="N")
    parser.add_argument("--ignoreStrand", help="Consider both strands.",
                        action="store_true", default=False)
    parser.add_argument("--detail", help="Return all possible missed exons on different transcripts.",
                        action="store_true", default=False)
    parser.add_argument("--floatFlankLen", help="Flank length can be changed by adjacent indel.",
                        action="store_true", default=False)
    parser.add_argument("--debugMode", help="Won't stop when get a error in one read.",
                        action="store_true", default=False)
    parser.add_argument("--setTag", help="Set fr tags on the realigned reads",
                        action="store_true", default=False)
    group.add_argument(
        "-o", "--outBam", help="Output realigned bam file.", metavar="file")
    group.add_argument("--onlyRegion", help="Only return the Region file without realign process.",
                       action="store_true", default=False)
    # output help message when no param.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    if not args.onlyRegion:
        if args.outBam is None:
            raise Exception(
                "Require -o or --outBam if --onlyRegion flag is not set!")
    run_multiprocess(
        args.inBam, args.genomeFasta, args.annotBed, args.outBam, args.outRegion,
        small_exon_size=args.exonSizeThd, flank_len=args.flankLen,
        ignore_strand=args.ignoreStrand, nprocess=args.coreNum,
        delta_ratio_thd=args.deltaRatioThd, simplify=(not args.detail),
        float_flank_len=args.floatFlankLen, only_region=args.onlyRegion,
        debug_mode=args.debugMode, set_tag=args.setTag
    )
