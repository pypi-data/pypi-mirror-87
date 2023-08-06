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

""" Common base class for all OlxSearchX classes """


import pandas


__all__ = [
    "OlxSearchBase"
]


class OlxSearchBase:
    """ Base class for searching OLX listings in various countries,
        also see country-specific classes
    """

    def __init__(self, search_term=""):
        super().__init__()
        self.search_term = search_term

    @property
    def search_term(self):
        """ What to search for on OLX """
        return self._search_term

    @search_term.setter
    def search_term(self, value):
        self._search_term = value

    @property
    def listings(self):
        """ An Iterator over items posted for sale
            Raises StopIteration of no new posts available
        """
        try:
            self._listings
        except AttributeError:
            self._listings = self._download_listings()
        return self._listings

    @property
    def listings_as_dataframe(self):
        """
            A Pandas DataFrame containing all items posted for sale
        """
        return pandas.DataFrame(self.listings)

    @staticmethod
    def _filter_record(record):
        raise NotImplementedError("Use a country-specific OlxSearch class")

    def _download_listings(self):
        """ Download all listings for `search_term` """
        raise NotImplementedError("Use a country-specific OlxSearch class")
