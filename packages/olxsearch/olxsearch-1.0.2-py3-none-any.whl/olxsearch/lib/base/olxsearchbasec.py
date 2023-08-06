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
        - Egypt
        - Oman
        - Lebanon
"""


import json
import re
import sys

import bs4
import dateparser.search
import fake_useragent
import geocoder
import requests

from .olxsearchbase import OlxSearchBase

__all__ = [
    "OlxSearchBaseC"
]


class OlxSearchBaseC(OlxSearchBase):
    """ Base class for searching OLX listings in various countries,
        also see country-specific classes
    """
    _useragent = fake_useragent.UserAgent(
        fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 "
        + "Safari/537.36"
    ).random

    @classmethod
    def _filter_record(cls, record):
        filtered_record = {}
        try:
            details_href = \
                record.find("a", class_="ads__item__ad--title")["href"]

            with requests.get(
                    details_href,
                    headers={
                        "User-Agent": cls._useragent
                    }
            ) as response:
                details = bs4.BeautifulSoup(response.text, "html.parser")
                metadata = \
                    cls._find_js_metadata_in_details_page(details)

                offer = details.find("div", class_="content")

                filtered_record["id"] = metadata["adID"]
                filtered_record["title"] = metadata["ad_title"]
                filtered_record["description"] = \
                    offer.find("div", id="textContent").get_text().strip()

                filtered_record["created_at"] = dateparser.search.search_dates(
                    offer.find("div", class_="offerheadinner").get_text(),
                    languages=[cls.LANGUAGE]
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
                    metadata["itemPrice"],
                    metadata["defaultCurrency"]
                )

                try:
                    (lat, lon) = geocoder.osm(
                        details.find("a", class_="locationbox")
                        .find("span", class_="address")
                        .span
                        .get_text()
                        .strip()
                    ).latlng
                except TypeError:
                    lat, lon = None, None

                filtered_record["lat"] = lat
                filtered_record["lon"] = lon

        except (
                KeyError,
                TypeError
        ):
            filtered_record = None

        return filtered_record

    @staticmethod
    def _find_js_metadata_in_details_page(details):
        metadata = {}
        for script in details.find_all("script"):

            if script.has_attr("src"):
                continue

            # expanding the filter of text types to
            # get to bs4.Comment and bs4.Script
            # Otherwise this does yields an empty string
            s_text = script.get_text(
                types=(
                    bs4.NavigableString,
                    bs4.CData,
                    bs4.Comment,
                    bs4.Script
                )
            )

            if "window.dataLayer.push" in s_text:
                for line in s_text.splitlines():
                    if (
                            "window.dataLayer.push" in line
                            and "cleanup" not in line
                    ):
                        metadata.update(
                            json.loads(
                                line[line.find("{"):line.find("}") + 1]
                            )
                        )

            elif "window.suggestmeyes_loaded" in s_text:
                js_var_parser = \
                    re.compile(
                        r"""var (?P<name>[^=\s]*)\s*=\s*(?P<value>[^;]*)\s*;"""
                    )
                for match in js_var_parser.finditer(s_text):
                    metadata[match["name"]] = match["value"].strip("\"'")

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
                params = {}
                if page > 1:
                    params["page"] = page

                data = requests.get(
                    self.BASE_URL.format(query=self.search_term),
                    headers={
                        "User-Agent": self._useragent
                    },
                    params=params
                ).text
            except requests.RequestException as exception:
                print(exception, file=sys.stderr)
                break

            data = bs4.BeautifulSoup(data, "html.parser")

            for record in data.find_all("div", class_="ads__item"):
                record = self._filter_record(record)
                if record is None:
                    continue
                yield record

            # test whether there’s another page
            next_page_link = data.find("a", class_="pageNextPrev")
            if next_page_link is None:
                break

            page += 1
