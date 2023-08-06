#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .api import SaneJS
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description='Run a query against SaneJS')
    parser.add_argument('--url', type=str, help='URL of the instance.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--meta', action='store_true', help='Get meta information (Not implemented).')

    group.add_argument('--sha512', nargs='*', help='Query a hash.')
    group.add_argument('--library', nargs='*', help='Query a library.')
    parser.add_argument('--version', help='Query a library version (only relevant if a library is given).')
    args = parser.parse_args()

    if args.url:
        sanejs = SaneJS(args.url)
    else:
        sanejs = SaneJS()
    if args.meta:
        raise Exception('Not implemented yet.')
        # response = sanejs.meta()
        # print(response)
    elif args.sha512:
        if len(args.sha512) == 1:
            # Test query with single value
            sha512 = args.sha512[0]
        else:
            sha512 = args.sha512
        # print(sha512)
        response = sanejs.sha512(sha512)
    else:
        if args.version:
            response = sanejs.library(args.library[0], args.version)
        else:
            if len(args.library) == 1:
                library = args.library[0]
            else:
                library = args.library
            response = sanejs.library(library)
    print(json.dumps(response, indent=2))
