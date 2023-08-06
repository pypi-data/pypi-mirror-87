#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script extract options for scalafmt from the HTML documentation on
# https://scalameta.org/scalafmt.
# scalafmt use HOCON syntax for the configuration which supports nesting
# options. We only extract the simple options that can be expressed as
# key-value pairs.
# ---------------------------------------------------------------------

from __future__ import print_function

import os
import re
import sys
from os.path import abspath, basename, dirname, join


re_option = re.compile(r'([a-z]\w\w+(\.\w\w\w+(\.\w\w\w+)?)?)\s*=\s*[0-9a-zA-Z]+')


def main():
    if len(sys.argv) != 2:
        print('Usage: %s <path to Scalafmt.html>')
        sys.exit(1)
    htmlfile = sys.argv[1]
    with open(htmlfile) as fp:
        lines = fp.readlines()
    options = []
    ready = False
    for line in lines:
        # Begin in the configuration section
        if '#Configuration' in line:
            ready = True
        # Stop at gotchas
        if '#Gotchas' in line:
            ready = False
        if not ready:
            continue

        m = re_option.search(line)
        if m:
            options.append(m.group(0))
    print('\n'.join(sorted(options)))


if __name__ == '__main__':
    sys.exit(main())
