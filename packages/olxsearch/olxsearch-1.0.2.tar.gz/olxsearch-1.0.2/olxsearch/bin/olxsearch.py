#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.

""" Search small ad listings on OLX market places """


import os.path
import sys

import pandas

from ..lib.olxsearch import OlxSearch


def main():
    try:
        country = sys.argv[1]
        search_term = sys.argv[2]
    except IndexError:
        print(
            "Usage: {:s} country search_term".format(
                os.path.basename(sys.argv[0])
            )
        )
        return

    olx_search = OlxSearch(country, search_term)
    print(pandas.DataFrame(olx_search.listings))


if __name__ == "__main__":
    main()
