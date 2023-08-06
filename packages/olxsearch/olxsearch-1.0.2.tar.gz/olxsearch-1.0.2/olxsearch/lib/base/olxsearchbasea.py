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

""" Search small ad listings on OLX web sites in several countries

    This is one of several models of OLX pages, and the one used in
        - Argentina
        - Colombia
        - Ecuador
        - Guatemala
        - India
        - Indonesia
        - Pakistan
        - Panama
        - Peru
        - San Salvador
        - South Africa
"""


import sys

import requests

from .olxsearchbase import OlxSearchBase

__all__ = [
    "OlxSearchBaseA"
]


class OlxSearchBaseA(OlxSearchBase):
    """ Base class for searching OLX listings in various countries,
        also see country-specific classes
    """

    @staticmethod
    def _filter_record(record):
        return {
            "id": record["id"],
            "title": record["title"],
            "description": record["description"],
            "created_at": record["created_at"],
            "created_at_first": record["created_at_first"],
            "republish_date": record["republish_date"],
            "images": [i["url"] for i in record["images"]],
            "price": (None, None) if record["price"] is None else (
                record["price"]["value"]["raw"],
                record["price"]["value"]["currency"]["iso_4217"]
            ),
            # "location_country":
            #     record["locations_resolved"]["COUNTRY_name"],
            # "location_a1":
            #     record["locations_resolved"]["ADMIN_LEVEL_1_name"],
            # "location_a3":
            #     record["locations_resolved"]["ADMIN_LEVEL_3_name"],
            # "location_sublocality":
            #     record["locations_resolved"]["SUBLOCALITY_LEVEL_1_name"],
            "lat": record["locations"][0]["lat"],
            "lon": record["locations"][0]["lon"]
        }

    def _download_listings(self):
        """ Download all listings for `search_term` """
        # don’t run the base class
        try:
            self.BASE_URL
        except AttributeError as e:
            raise NotImplementedError(
                "Use a country-specific OlxSearch class"
            ) from e

        page = 0
        while True:
            try:
                data = requests.get(
                    self.BASE_URL,
                    params={
                        "page": page,
                        "query": self.search_term
                    }
                ).json()
            except requests.RequestException as e:
                print(e, file=sys.stderr)
                break

            page += 1
            if (
                    "data" not in data
                    or not data["data"]
            ):
                break

            for d in data["data"]:
                yield self._filter_record(d)
