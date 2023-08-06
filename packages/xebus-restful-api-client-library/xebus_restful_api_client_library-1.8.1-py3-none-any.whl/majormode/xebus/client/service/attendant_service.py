# Copyright (C) 2020 Majormode.  All rights reserved.
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


class AttendantService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def get_trackers_locations(
            self,
            team_id,
            end_time=None,
            limit=None,
            max_fix_age=None,
            sort_order=None,
            start_time=None):
        """
        Return lists of geographic location updates of tracker mobile devices
        used by the attendants of a school transport organization.

        :note: The user on behalf of whom this function is called must be an
            administrator of the school transport organization.


        :param team_id: Identification of a school transport organization.

        :param end_time: Latest inclusive time to filter location updates
            based on their fix time.

        :param limit: Constrain the number of locations per tracker mobile
            device to return to the specified number.  The default value is
            `AttendantService.DEFAULT_LIMIT`.  The maximum value is
            `AttendantService.MAXIMUM_LIMIT`.

        :param max_fix_age: Maximum difference, expressed in seconds, between
            the time when a tracker mobile device calculated the location fix
            and the current time on the server platform.  This duration
            corresponds to the current age of the location fix.

        :param sort_order: An item of the enumeration `SortOrder` that
            indicates the order to sort location updates:

            * `SortOrder.ascending` (default): The location updates of a tracker
              mobile device are sorted by ascending order of their fix time.

            * `SortOrder.descending`: The location updates of a tracker mobile
              device are sorted by descending order of their fix time.

        :param start_time: Earliest non-inclusive time to filter location
            updates based on their fix time.


        :return: A list of objects containing the following attributes:

            * `account_id` (required): Identification of the account of an
              attendant belonging to the specified school transport organization.

            * `battery_level` (required): Current level in percentage of the
              battery of the tracker mobile device.

            * `device_id` (required): Identification of the tracker mobile device
              currently used by the attendant.

            * `is_battery_plugged` (required): Indicate if the internal battery of
              the tracker mobile device is plugged to a power source.

            * `locations` (optional): A list of geographic locations reported by
              the tracker mobile device:

              * `accuracy` (required): Accuracy in meters of the location.

              * `altitude` (required): Altitude in meters of the location.

              * `bearing` (optional): Bearing in degrees.  Bearing is the horizontal
                direction of travel of the tracker mobile device, and is not related
                to the device orientation.  It is guaranteed to be in the range
                `[0.0, 360.0]`.

              * `fix_time` (required): Time when the tracker mobile device determined
                the information of this fix.

              * `latitude` (required): Latitude-angular distance, expressed in decimal
                degrees (WGS84 datum), measured from the center of the Earth, of a
                point north or south of the Equator corresponding to the location.

              * `longitude` (required): Longitude-angular distance, expressed in
                decimal degrees (WGS84 datum), measured from the center of the Earth,
                of a point east or west of the Prime Meridian corresponding to the
                location.

              * `provider` (required): Type of the location provider that reported
                this geographical location:

                * `gps`: This provider determines location using satellites (Global
                  Positioning System (GPS)).

                * `network`: This provider determines location based on availability of
                  cell towers and Wi-Fi access points.  Results are retrieved by means
                  of a network lookup.

                * `passive`: A special location provider for receiving locations without
                  actually initiating a location fix.  This provider can be used to
                  passively receive location updates when other applications or services
                  request them without actually requesting the locations yourself.  This
                  provider will return locations generated by other providers.

              * `speed` (optional): Speed in meters/second over the ground.


        :raise DeletedObjectException: If the specified team has been deleted.

        :raise DisabledObjectException: If the specified team has been disabled.

        :raise IllegalAccessException: If the account of the user on behalf of
            whom this function is called is not an administrator of the school
             transport organization.

        :raise UndefinedObjectException: If the specified team is not registered.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/attendant/tracker/location',
                arguments={
                    'end_time': end_time,
                    'limit': limit,
                    'max_fix_age': max_fix_age,
                    'sort_order': sort_order,
                    'start_time': start_time,
                    'team_id': team_id,
                },
                authentication_required=True,
                signature_required=True))
