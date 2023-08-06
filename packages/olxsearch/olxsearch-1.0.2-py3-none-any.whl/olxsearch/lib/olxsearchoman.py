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

""" Search small ad listings on OLX web sites in Oman """


from .base.olxsearchbasec import OlxSearchBaseC

__all__ = [
    "OlxSearchOman"
]


class OlxSearchOman(OlxSearchBaseC):
    """
        Search OLX listings on OLX Oman

        Args:
            search_term (str): query OLX listings using this search term
    """
    BASE_URL = "https://www.olx.com.om/ads/q-{query:s}/"
    LANGUAGE = "ar"
