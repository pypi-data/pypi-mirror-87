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
        - Bulgaria
        - Kazakhstan
        - Poland
        - Portugal
        - Romania
        - Ukraine
        - Uzbekistan
"""


import json
import sys

import bs4
import dateparser.search
import geocoder
import requests

from .olxsearchbase import OlxSearchBase

__all__ = ["OlxSearchBaseB"]


class OlxSearchBaseB(OlxSearchBase):
    """Base class for searching OLX listings in various countries,
    also see country-specific classes
    """

    @classmethod
    def _filter_record(cls, record):
        filtered_record = {}
        try:
            filtered_record["id"] = record.div.table["data-id"]
            filtered_record["title"] = record.div.table.h3.get_text().strip()
            details_href = record.div.table.h3.a["href"]

            with requests.get(details_href) as response:
                details = bs4.BeautifulSoup(response.text, "html.parser")
                metadata = cls._find_js_metadata_in_details_page(details)

                offer = details.find("div", id="offerdescription")

                filtered_record["description"] = (
                    offer.find("div", id="textContent").get_text().strip()
                )
                filtered_record["created_at"] = dateparser.search.search_dates(
                    offer.find("div", class_="offer-titlebox__details").get_text(),
                    languages=[cls.LANGUAGE],
                )[0][1]
                filtered_record["created_at_first"] = None
                filtered_record["republish_date"] = None
                try:
                    filtered_record["images"] = [
                        img_item.div.img["src"]
                        for img_item
                        in offer.find_all("div", class_="img-item")
                    ]
                except TypeError:
                    filtered_record["images"] = []
                filtered_record["price"] = (
                    metadata["pageView"]["ad_price"],
                    metadata["pageView"]["price_currency"]
                )

                try:
                    (lat, lon) = geocoder.osm(
                        details.find("a", class_="locationbox")
                        .span
                        .span
                        .span
                        .get_text()
                        .strip()
                    ).latlng
                except TypeError:
                    lat, lon = None, None

                filtered_record["lat"] = lat
                filtered_record["lon"] = lon

        except (KeyError, TypeError):
            filtered_record = None

        return filtered_record

    @staticmethod
    def _find_js_metadata_in_details_page(details):
        metadata = {}
        for script in details.find_all("script"):
            if "trackingData" in script.get_text():
                s_text = script.get_text()
                metadata = json.loads(
                    s_text[s_text.find("'{") + 1 : s_text.find("}'") + 1]
                )
                break
        return metadata

    def _download_listings(self):
        """ Download all listings for `search_term` """
        # don’t run the base class
        try:
            self.BASE_URL
        except AttributeError as exception:
            raise NotImplementedError(
                "Use a country-specific OlxSearch class"
            ) from exception

        page = 1
        while True:
            try:
                params = {
                    "search[description]": 1
                }
                if page > 1:
                    params["page"] = page

                print(params)

                data = requests.get(
                    self.BASE_URL.format(query=self.search_term),
                    params=params
                ).text
            except requests.RequestException as exception:
                print(exception, file=sys.stderr)
                break

            data = bs4.BeautifulSoup(data, "html.parser")

            for record in data.find_all("td", class_="offer"):
                record = self._filter_record(record)
                if record is None:
                    continue
                yield record

            # test whether there’s another page
            next_page_link = data.find("span", class_="pageNextPrev").a
            if next_page_link is None:
                break

            page += 1
