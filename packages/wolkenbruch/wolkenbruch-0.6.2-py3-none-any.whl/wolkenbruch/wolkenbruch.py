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

""" Reminds me if it rains """

import statistics
import sys

import geocoder

from .lib import (
    Config,
    EMailSender,
    PrecipitationChecker
)


__all__ = [
    "remind_me_if_it_rains"
]

# How many hours to look into the future?
N_HOURS = 14


def remind_me_if_it_rains():
    """ Remind me if rain is forecast """
    config = Config()

    try:
        verbose = config["verbose"]
    except KeyError:
        verbose = False

    lat, lon = geocoder.osm(config["place"]).latlng

    hourly_precipitation_rates = \
        PrecipitationChecker(lat, lon).hourly_precipitation_rates[:N_HOURS]

    average_precipitation_rate = \
        statistics.fmean(hourly_precipitation_rates)
    max_precipitation_rate = \
        max(hourly_precipitation_rates)

    if verbose:
        print(
            (
                "Average precipitation rate in {place:s} is {a:0.2f} mm/h " +
                "over the next 14 hours, maximum {m:0.2f}. "
            ).format(
                place=config["place"],
                a=average_precipitation_rate,
                m=max_precipitation_rate
            ),
            file=sys.stderr,
            end=""
        )

    if (
            average_precipitation_rate
            > config["average_precipitation_rate_threshold"]

            or max_precipitation_rate
            > config["max_precipitation_rate_threshold"]
    ):
        EMailSender(
            config["email"]["from"],
            config["email"]["to"],
            config["email"]["subject"],
            config["email"]["message"].format(
                a=average_precipitation_rate,
                m=max_precipitation_rate
            ),
            config["smtp"]["host"],
            config["smtp"]["user"],
            config["smtp"]["password"]
        ).send_message()

        if verbose:
            print(
                "Sending reminder to {:s} ".format(config["email"]["to"]),
                file=sys.stderr
            )
    else:
        if verbose:
            print(
                "NOT sending reminder to {:s} ".format(config["email"]["to"]),
                file=sys.stderr
            )
