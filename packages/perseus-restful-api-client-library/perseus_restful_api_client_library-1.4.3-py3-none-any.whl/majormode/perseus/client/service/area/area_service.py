# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from majormode.perseus.client.service.base_service import BaseService
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.obj import Object


class AreaService(BaseService):
    def __init__(self, session):
        super(AreaService, self).__init__(session)

    def get_area_boundaries(self, area_id, sync_time=None):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/area/(area_id)/boundaries',
                url_bits={
                    'area_id': area_id
                },
                arguments={
                    'sync_time': sync_time
                },
                authentication_required=False,
                signature_required=True))

    def get_areas_by_ip_address(
            self,
            ip_address,
            highest_area_level=None,
            locale=DEFAULT_LOCALE,
            lowest_area_level=None,
            minimal_area_surface=None):
        """
        Return the geographic areas that encompass the location determined
        from the specified IP address.


        @param ip_address: a dotted-decimal notation of an IPv4 address,
            consisting of four decimal numbers, each ranging from ``0`` to
            ``255``, separated by dots.

        @param lowest_area_level: the level of the smallest administrative
            area to start with.

            As a reminder, for clarity and convenience the standard neutral
            reference for the largest administrative subdivision of a country
            is called the "first-level administrative division" or "first
            administrative level". Next smaller is called "second-level
            administrative division" or "second administrative level", etc.

            Note: the smallest the area, the fastest the function returns
            result.

        @param highest_area_level: the level of the largest administrative
            area to finish with.

        @param locale: a ``Locale`` instance that specifies the locale of the
            area labels to be returned.

        @param minimal_area_surface: minimal surface in square meter of the
            geographical area that are returned.


        @return: a list of instances containing the following members:

            * ``area_id`` (required): identification of the geographic area.

            * ``area_label`` (required): an instance ``Label`` corresponding to the
              name of this area in the specified locale, or the closest locale if
              no name is defined for this particular locale, which is, at least,
              English by default.

            * ``area_level`` (required): administrative level of this geogaphic area.
              For clarity and convenience the standard neutral reference for the
              largest administrative subdivision of a country is called the "first-
              level administrative division" or "first administrative level".  Next
              smaller is called "second-level  administrative division" or "second
              administrative level".

            * ``area_type`` (optional): symbolic name of the type of this geographic
              area.

            * ``bounding_box`` (required): an instance ``BoundingBox`` representing
              the maximum extents of the geographical area.

            * ``centroid`` (required): an instance ``GeoPoint`` representing the
              centroid of this area.

            * ``parent_area_id`` (optional): identification of the parent geographic
              area or ``None`` if none defined.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/area',
                arguments={
                    'ip_address': '.'.join([str(byte) for byte in ip_address]),
                    'highest_area_level': highest_area_level,
                    'locale': locale,
                    'lowest_area_level': lowest_area_level,
                    'minimal_area_surface': minimal_area_surface
                },
                authentication_required=False,
                signature_required=True))

    def get_areas_by_keywords(
            self, keywords,
            highest_area_level=None,
            limit=None,
            locale=DEFAULT_LOCALE,
            lowest_area_level=None,
            minimal_area_surface=None,
            offset=0):
        """
        Return the geographic areas that match the specified keywords.


        @param keywords: a list of one or more keywords.

        @param highest_area_level: the level of the largest administrative
            area to finish with.

        @param limit: constrain the number of areas that are returned to the
            specified number.

        @param lowest_area_level: the level of the smallest administrative
            area to start with.

            As a reminder, for clarity and convenience the standard neutral
            reference for the largest administrative subdivision of a country
            is called the "first-level administrative division" or "first
            administrative level". Next smaller is called "second-level
            administrative division" or "second administrative level", etc.

            Note: the smallest the area, the fastest the function returns
            result.

        @param minimal_area_surface: minimal surface in square meter of the
            geographical area that are returned.

        @param offset: require to skip that many areas before beginning to
            return them.  If both ``limit`` and ``offset`` are specified, then
            ``offset`` areas are skipped before starting to count the
            `limit`` areas that are returned.  The default value is ``0``.

        @param locale: a ``Locale`` instance that specifies the locale of the
             area labels to be returned.


        @return: an instance containing the following members:

            * ``area_id``: identification of the geographic area.

            * ``area_type``: symbolic name of the type of the geographic area.

            * ``area_label``: label in the specified locale, or the closest locale
              if no label is defined for this particular locale, which is, at
              least, English by default.

            * ``parent_area_id``: identification of the parent geographic area or
              ``None`` if none defined.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/area',
                arguments={
                    'highest_area_level': highest_area_level,
                    'keywords': ','.join(keywords),
                    'limit': limit,
                    'locale': locale,
                    'lowest_area_level': lowest_area_level,
                    'minimal_area_surface': minimal_area_surface,
                    'offset': offset
                },
                authentication_required=False,
                signature_required=True))

    def get_areas_by_location(
            self,
            location,
            highest_area_level=None,
            locale=DEFAULT_LOCALE,
            lowest_area_level=None,
            minimal_area_surface=None):
        """
        Return the geographic areas that encompass the specified location.


        @param location: a ``GeoPoint`` instance that specifies a location.

        @param lowest_area_level: the level of the smallest administrative
            area to start with.

            As a reminder, for clarity and convenience the standard neutral
            reference for the largest administrative subdivision of a country
            is called the "first-level administrative division" or "first
            administrative level". Next smaller is called "second-level
            administrative division" or "second administrative level", etc.

            Note: the smallest the area, the fastest the function returns
            result.

        @param highest_area_level: the level of the largest administrative
            area to finish with.

        @param locale: a ``Locale`` instance that specifies the locale of the
            area labels to be returned.

        @param minimal_area_surface: minimal surface in square meter of the
            geographical area that are returned.


        @return: a list of instances containing the following members:

            * ``area_id`` (required): identification of the geographic area.

            * ``area_label`` (required): an instance ``Label`` corresponding to the
              name of this area in the specified locale, or the closest locale if
              no name is defined for this particular locale, which is, at least,
              English by default.

            * ``area_level`` (required): administrative level of this geogaphic area.
              For clarity and convenience the standard neutral reference for the
              largest administrative subdivision of a country is called the "first-
              level administrative division" or "first administrative level".  Next
              smaller is called "second-level  administrative division" or "second
              administrative level".

            * ``area_type`` (optional): symbolic name of the type of this geographic
              area.

            * ``bounding_box`` (required): an instance ``BoundingBox`` representing
              the maximum extents of the geographical area.

            * ``centroid`` (required): an instance ``GeoPoint`` representing the
              centroid of this area.

            * ``parent_area_id`` (optional): identification of the parent geographic
              area or ``None`` if none defined.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/area',
                arguments={
                    'highest_area_level': highest_area_level,
                    'll': '%s,%s' % (location.longitude, location.latitude),
                    'locale': locale,
                    'lowest_area_level': lowest_area_level,
                    'minimal_area_surface': minimal_area_surface
                },
                authentication_required=False,
                signature_required=True))

    def get_areas_in_bounding_box(self, bounds, locale=DEFAULT_LOCALE):
        """

        @param bounds: a tuple of two instances ``GeoPoint`` that represent
            the north-east corner and the south-west corners of the rectangle
            area to search geographical areas in.

        @param locale: an instance ``Locale`` to return textual information of
            the places.


        @return:
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/area',
                arguments={
                    'bounds': bounds and '%s,%s,%s,%s' % (
                        bounds[0].longitude, bounds[0].latitude,
                        bounds[1].longitude, bounds[1].latitude),
                    'locale': locale
                },
                authentication_required=False,
                signature_required=True))
