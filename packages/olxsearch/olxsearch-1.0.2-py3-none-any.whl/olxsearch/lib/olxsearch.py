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

""" Search small ad listings on OLX web sites in different countries """


import importlib


__all__ = [
    "OlxSearch"
]


class OlxSearch:
    """ Class factory for obtaining a country-specific class to scrape OLX
        market place web sites.
    """

    def __new__(
            cls,
            country,
            *args,
            **kwargs
    ):
        cls_ = "OlxSearch{:s}".format(country.replace(" ", ""))
        module_ = "olxsearch.lib.{:s}".format(cls_.lower())

        try:
            module = importlib.import_module(module_)
            cls = getattr(module, cls_)
        except ImportError as e:
            raise NotImplementedError(
                """ Could not find country-specific
                    OlxSearch class for {:s} """.format(country)
            ) from e

        instance = cls.__new__(cls, *args, **kwargs)
        instance.__init__(*args, **kwargs)

        return instance
