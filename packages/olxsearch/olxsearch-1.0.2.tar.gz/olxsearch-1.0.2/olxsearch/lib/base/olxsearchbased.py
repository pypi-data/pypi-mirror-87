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
        - Brazil
"""


import datetime
import json
import os
import sys
import time

import bs4
import fake_useragent
import geocoder
import requests

from .olxsearchbase import OlxSearchBase

__all__ = [
    "OlxSearchBaseD"
]


class OlxSearchBaseD(OlxSearchBase):
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
            details_href = record.find(
                "a",
                attrs={"data-lurker-detail": "list_id"}
            )["href"]

            with requests.get(
                    details_href,
                    headers={
                        "User-Agent": cls._useragent
                    }
            ) as response:
                details = bs4.BeautifulSoup(response.text, "html.parser")
                metadata = \
                    cls._find_js_metadata_in_details_page(details)

                offer = details.find("div", id="content")
                inner_container = \
                    offer\
                    .find_all("div", recursive=False)[1]\
                    .div\
                    .find_all("div", recursive=False)[1]\
                    .div

                filtered_record["id"] = metadata["listId"]
                filtered_record["title"] = (
                    details
                    .find("title")
                    .get_text()
                    .replace(
                        " - {id:d} | OLX".format(id=filtered_record["id"]),
                        ""
                    )
                )

                filtered_record["description"] = (
                    inner_container.find(
                        "span",
                        string="Descrição"
                    )
                    .parent
                    .parent
                    .get_text()
                    .replace("Descrição", "", 1)
                )

                filtered_record["created_at"] = datetime.datetime.fromtimestamp(
                    metadata["page"]["detail"]["adDate"]
                )
                filtered_record["created_at_first"] = None
                filtered_record["republish_date"] = None
                try:
                    filtered_record["images"] = [
                        img_item.div.img["src"]
                        for img_item
                        in offer.find_all(
                            "div",
                            attrs={"data-testid": "slides-wrapper"}
                        )
                    ]
                except TypeError:
                    filtered_record["images"] = []
                filtered_record["price"] = (
                    metadata["page"]["detail"]["price"],
                    "BRL"  # hard-coded because this base used for brazil only
                )

                municipality = \
                    inner_container\
                    .find("dt", string="Município")\
                    .parent\
                    .dd\
                    .get_text()
                try:
                    neighbourhood = \
                        inner_container\
                        .find("dt", string="Bairro")\
                        .parent\
                        .dd\
                        .get_text()
                except AttributeError:
                    neighbourhood = None
                postcode = \
                    inner_container\
                    .find("dt", string="CEP")\
                    .parent\
                    .dd\
                    .get_text()

                # EASTER EGG!
                # By default, `olxsearch` uses `geocoder.osm` to look up
                # geographic locations, deriving a coordinate pair from
                # neighbourhood and municipality names (in the case of Brazil)
                #
                # OLX ads also contain much preciser post code information.
                # `olxsearch` can also use cepaberto.com to retrieve geographic
                # coordinates for post codes. Register at cepaberto.com and
                # export your API token as an environment variable
                # CEPABERTO_TOKEN.
                #
                # While significantly more precise, this has one dramatic
                # downside, which is cepaberto.com’s rate limiting:
                # max. 1 location per second, max. 10,000 queries per day

                try:
                    assert "CEPABERTO_TOKEN" in os.environ
                    with requests.get(
                            "https://www.cepaberto.com/api/v3/cep",
                            headers={
                                "Authorization": "Token token={:s}".format(
                                    os.environ["CEPABERTO_TOKEN"]
                                )
                            },
                            params={"cep": postcode}
                    ) as response:
                        response = response.json()
                        lat = response["latitude"]
                        lon = response["longitude"]
                        time.sleep(1.0)  # crude way of respecting rate limit
                except (
                        AssertionError,
                        json.decoder.JSONDecodeError,
                        requests.RequestException
                ):
                    try:
                        (lat, lon) = geocoder.osm(
                            "{neighbourhood:s}, {municipality:s}".format(
                                neighbourhood=neighbourhood,
                                municipality=municipality
                            )
                        ).latlng
                    except TypeError:
                        try:
                            (lat, lon) = geocoder.osm(
                                municipality
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

            if "window.dataLayer = " in s_text:
                metadata = \
                    json.loads(
                        s_text[s_text.find("["):]
                    )[0]

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

            for record in data.find("ul", id="ad-list").find_all("li"):
                record = self._filter_record(record)
                if record is None:
                    continue
                yield record

            # test whether there’s another page
            next_page_link = \
                data.find("a", attrs={"data-lurker-detail": "next_page"})
            if next_page_link is None:
                break

            page += 1
