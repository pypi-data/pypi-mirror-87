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

""" Search small ad listings on OLX Indonesia
    and save them in a local PostGIS/PostgreSQL database """


import argparse
import os
import os.path

import psycopg2
import psycopg2.extras
import psycopg2.sql
import requests

from ..lib.olxsearch import OlxSearch


def _save_listing_to_database(listing, connection_string, table_name):
    """ Save an OLX listing to a PostgreSQL database """
    with psycopg2.connect(connection_string) as connection:
        with connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                psycopg2.sql.SQL(
                    """
                        INSERT INTO
                            {table_name}
                                (
                                    id,
                                    title,
                                    description,
                                    created_at,
                                    created_at_first,
                                    republish_date,
                                    price,
                                    price_currency,
                                    images,
                                    geom
                                )
                            VALUES (
                                %(id)s,
                                %(title)s,
                                %(description)s,
                                %(created_at)s,
                                %(created_at_first)s,
                                %(republish_date)s,
                                %(price)s,
                                %(price_currency)s,
                                %(images)s,
                                ST_SetSRID(
                                    ST_Point(%(lon)s, %(lat)s),
                                    4326
                                )
                            )
                        ON CONFLICT (id)
                            DO UPDATE
                                SET
                                    title=EXCLUDED.title,
                                    description=EXCLUDED.description,
                                    created_at=EXCLUDED.created_at,
                                    created_at_first=EXCLUDED.created_at_first,
                                    republish_date=EXCLUDED.republish_date,
                                    price=EXCLUDED.price,
                                    price_currency=EXCLUDED.price_currency,
                                    images=EXCLUDED.images,
                                    geom=EXCLUDED.geom;
                    """
                ).format(
                    table_name=psycopg2.sql.Identifier(table_name)
                ),
                {
                    "id": listing["id"],
                    "title": listing["title"],
                    "description": listing["description"],
                    "created_at": listing["created_at"],
                    "created_at_first": listing["created_at_first"],
                    "republish_date": listing["republish_date"],
                    "price": listing["price"][0],
                    "price_currency": listing["price"][1],
                    "images": listing["images"],
                    "lon": listing["lon"],
                    "lat": listing["lat"]
                }
            )


def _download_listing_images(listing, media_directory):
    """ Download all images attached to an OLX listing """
    destination_directory = os.path.join(
        media_directory,
        listing["id"]
    )
    os.makedirs(
        destination_directory,
        exist_ok=True
    )
    for url in listing["images"]:
        filename = os.path.join(
            destination_directory,
            "{:s}.jpg".format(
                url.split('/')[-2]
            )
        )
        _download_file(url, filename)


def _download_file(url, filename):
    with requests.get(
            url,
            stream=True
    ) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=None):
                f.write(chunk)


def _create_tables(connection_string, table_name):
    """ Create the tables to store OLX listings in a PostgreSQL database """
    with psycopg2.connect(connection_string) as connection:
        with connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                psycopg2.sql.SQL(
                    """
                        CREATE EXTENSION IF NOT EXISTS
                            postgis;

                        CREATE TABLE IF NOT EXISTS
                            {table_name}
                        (
                            row BIGSERIAL PRIMARY KEY,
                            id BIGINT UNIQUE,
                            title TEXT,
                            description TEXT,
                            created_at TIMESTAMP,
                            created_at_first TIMESTAMP,
                            republish_date TIMESTAMP,
                            price NUMERIC,
                            price_currency CHAR(3),
                            images TEXT[],
                            geom GEOMETRY('POINT', 4326)
                        );

                        CREATE INDEX IF NOT EXISTS
                            {geom_index}
                        ON
                            {table_name}
                        USING
                            GIST(geom);

                    """
                ).format(
                    table_name=psycopg2.sql.Identifier(table_name),
                    geom_index=psycopg2.sql.Identifier(
                        "{:s}_geom_idx".format(table_name)
                    )
                )
            )
            connection.commit()


def main():
    """ Search small ad listings on OLX Indonesia
        and save them in a local PostGIS/PostgreSQL database """
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-c",
        "--country",
        help="""Query the OLX market place for COUNTRY.
                Specify more than one country using multiple switches
                (-c COUNTRY1 -c COUNTRY2) """,
        choices=(
            "Argentina",
            "Bulgaria",
            "Colombia",
            "Costa Rica",
            "Ecuador",
            "Guatemala",
            "India",
            "Indonesia",
            "Kazakhstan",
            "Pakistan",
            "Panama",
            "Peru",
            "Poland",
            "Portugal",
            "Romania",
            "San Salvador",
            "South Africa",
            "Ukraine",
            "Uzbekistan"
        ),
        action="append",
        required=True
    )
    argparser.add_argument(
        "search_terms",
        help="""Query the titles and descriptions of the listings
                on the OLX market place for this""",
        nargs="+"
    )
    argparser.add_argument(
        "-p",
        "--postgresql-connection-string",
        help="""Store the retrieved data in this PostgreSQL data base
                (default: "dbname=olx") """,
        default="dbname=olx"
    )
    argparser.add_argument(
        "-t",
        "--table",
        help="""Store the data in a PostgreSQL table with this name
                (default: same as the first search_term)""",
        default=None
    )
    argparser.add_argument(
        "-m",
        "--media-directory",
        help="""Download images to this directory""",
        default="./media"
    )
    args = argparser.parse_args()

    if args.table is None:
        args.table = args.search_terms[0]

    _create_tables(args.postgresql_connection_string, args.table)
    for search_term in args.search_terms:
        for country in args.country:
            for listing in OlxSearch(country, search_term).listings:
                _save_listing_to_database(
                    listing,
                    args.postgresql_connection_string,
                    args.table
                )
                _download_listing_images(
                    listing,
                    args.media_directory
                )


if __name__ == "__main__":
    main()
