# Copyright (C) 2019 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from majormode.perseus.client.service.base_service import BaseService
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.obj import Object


class SchoolService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def get_bus_stops(
            self,
            school_id,
            include_ignored=False,
            include_suggested=False,
            limit=None,
            locale=None,
            offset=0,
            sync_time=None):
        """
        Return a list of bus stops where school buses pick up and drop off
        children of a school.


        :param school_id: Identification of a school.

        :param include_ignored: Indicate whether to return bus stops that have
            been automatically detected but ignored by an administrator of an
            organization managing the transportation for this school.

        :param include_suggested: Indicate whether to return bus stops which
            changes been automatically detected (new bus stops, bus stops
            which location has slightly changed, unused bus stops).

        :param limit: Constrain the number of bus stops to return to the
            specified number.  If not specified, the default value is `10`.
            The maximum value is `100`.

        :param locale: The locale to return textual information, such as the
             name of the bus stop, its address.  By default, textual
             information is returned in English.

        :param offset: Require to skip that many bus stops before beginning to
            return bus stops to the client.  Default value is `0`.  If both
            `offset` and `limit` are specified, then `offset` bus stops are
            skipped before starting to count the limit bus stops that are
            returned.

        :param sync_time: Earliest time to return bus stops based on the time
            of the most recent modification of one of their attributes.  If
            not specified, the platform returns all the bus stops.


        :return: A list of objects containing the following attributes:

            * `address` (required): Postal address of the school, composed of one or
              more address components, which textual information is written in the
              specified locale. An address component is defined with a component
              type and its value.

            * `location` (required): Geographical location of the bus stop.

              * `altitude` (required): Altitude in meters of the bus stop's location.

              * `latitude` (required): Latitude-angular distance, expressed in decimal
                degrees (WGS84 datum), measured from the center of the Earth, of a
                point north or south of the Equator corresponding to the bus stop's
                location.

              * `longitude` (required): Longitude-angular distance, expressed in
                decimal degrees (WGS84 datum), measured from the center of the Earth,
                of a point east or west of the Prime Meridian corresponding to the bus
                stop's location.

              * `radius` (optional): Radius in meters of the surface area of the
                circle that contains the bus stop.

            * `stop_id` (required): Identification of the bus stops.

            * `update_time` (required): Time of the most recent modification of an
              attribute of this bus stop.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/school/(school_id)/bus-stop',
                url_bits={
                    'school_id': school_id
                },
                arguments={
                    'include_ignored': include_ignored,
                    'include_suggested': include_suggested,
                    'limit': limit,
                    'locale': locale,
                    'offset': offset,
                    'sync_time': sync_time,
                },
                authentication_required=True,
                signature_required=True))

    def get_school_buses_locations(self, school_id):
        """

        :param school_id: Identification of a school.


        :return: A list of objects containing the following attributes:

* `account_id` (required): Identification of the attendant who is using
  the tracker device.

* `accuracy` (optional): Accuracy in meters of the location.

* `altitude` (optional):

* `bearing` (optional): Bearing is the horizontal direction of travel
  of the mobile tracker device, and is not related to the device's
  orientation.  It is guaranteed to be in the range `[0.0, 360.0]`.

* `fix_time` (required): Time when the mobile tracker device determined
  the information of this fix.

* `full_name` (required): Full name by which the attendant is known.

* `latitude` (required):

* `longitude` (required):

* `speed` (optional): Speed in meters/second over the ground.


* `team_id` (required): Identification of the team that the attendant
  belongs to.

* `team_name` (required): Name of the team that the attendant belongs to.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/school/(school_id)/bus/location',
                url_bits={
                    'school_id': school_id,
                },
                authentication_required=True,
                signature_required=True))

    def search_schools(
            self,
            area_id=None,
            include_education_grades=False,
            ip_address=None,
            keywords=None,
            location=None,
            limit=None,
            locale=DEFAULT_LOCALE,
            offset=0):
        """
        Return a list of schools that have joined the School Bus Program and
        that correspond to the specified criteria.


        :param area_id: Identification of a geographical area to return
            schools.

        :param include_education_grades: Indicate whether to include the
            education grades that this school supports.

        :param ip_address: IPv4 address of the machine of the user, a tuple
            consisting of four decimal numbers, each ranging from ``0`` to
            ``255``.

        :param keywords: A list of keywords to search schools for.

        :param limit: Constrain the number of places to return to the
            specified number.  If not specified, the default value is
            ``BaseService.DEFAULT_RESULT_SET_SIZE``.  The maximum value is
            ``BaseService.MAXIMUM_RESULT_SET_LIMIT``.

        :param locale: An instance ``Locale`` to return textual information,
            such as the names of countries and the names of schools.

        :param location: An instance ``GeoPoint`` that indicates the user's
            location.

        :param offset: Require to skip that many records before beginning to
            return records to the client.  Default value is ``0``.  If both
            ``offset`` and ``limit`` are specified, then ``offset`` records
            are skipped before starting to count the limit records that are
            returned.


        @return: An object containing the following attributes:

        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/school',
                arguments={
                    'area_id': area_id,
                    'include_education_grades': include_education_grades,
                    'ip_address': ip_address and '.'.join([str(byte) for byte in ip_address]),
                    'keywords': keywords and ','.join(keywords if isinstance(keywords, (list, set, tuple)) else [keywords]),
                    'limit': limit,
                    'll': location and f'{location.latitude},{location.longitude}',
                    'locale': locale,
                    'offset': offset,
                },
                authentication_required=False,
                signature_required=True))
