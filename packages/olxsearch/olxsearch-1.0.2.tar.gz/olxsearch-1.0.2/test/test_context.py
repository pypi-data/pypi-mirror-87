#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

sys.argv.append(
    "--config={:s}".format(
        os.path.join(
            os.path.dirname(__file__),
            "test.yml"
        )
    )
)

import olxsearch  # noqa: F401, E402
