#!/usr/bin/env python
# -*- coding: utf-8 -*-

from babynames.utils import csv2json


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="input file path")
    parser.add_argument(
        "-o", "--output", dest="output", help="output file path"
    )

    args = parser.parse_args()

    csv2json(input=args.input, output=args.output)
