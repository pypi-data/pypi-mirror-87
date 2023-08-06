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


class BusRouteService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def accept_bus_stop_suggestion(
            self,
            suggestion_id,
            bus_stop=None):
        """
        Accept a bus stop suggestion that the server platform automatically
        made based on the Ci/Co operation activities of the pupils of a school.


        :param suggestion_id: Identification of the bus stop suggestion.

        :param bus_stop: An object `BusStop` that provides the information of
            the bus stop to create.  This argument MUST be passed when the
            suggestion corresponds to the creation of a bus stop.


        :return: An object containing the following attributes:

            * ``stop_id`` (required): Identification of the bus stop.

            * ``update_time`` (required): Time of the most recent modification of
                the information of this bus stop.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/bus-stop/suggestion/(suggestion_id:uuid)/acceptance',
                url_bits={
                    'suggestion_id': suggestion_id
                },
                message_body=bus_stop,
                authentication_required=True,
                signature_required=True))

    def get_bus_routes(
            self,
            school_id,
            include_path=False,
            locale=DEFAULT_LOCALE):
        """
        Return a list of children that have joined the School Bus Program and
        that correspond to the specified criteria.


        :param school_id: Identification of the school to return the list of
            bus routes.

        :param include_path: Indicate whether the path of the route needs to
            be returned.

        :param locale: A `Locale` object to return textual information,
            such as the names of countries and the names of children.


        :return: A list of objects containing the following attributes:

                {
                  "routes": [
                    {
                      "creation_time": timestamp,
                      "stops": [
                        {
                          "stop_id": string,
                          "position": integer,
                          "arrival_time": time,
                          "departure_time": time
                        },
                        ...
                      ],
                      "journey_type": string,
                      "object_status": string,
                      "path": [
                        [latitude, longitude, altitude],
                        ...
                      ],
                      "route_id": string,
                      "update_time": timestamp,
                      "visibility": string
                    },
                    ...
                  ],
                  "stops": [
                    {
                      "address": {
                        component_type: string,
                        ...
                      },
                      "creation_time": timestamp,
                      "locale": string,
                      "location": {
                        "altitude": decimal,
                        "latitude": decimal,
                        "longitude": decimal
                      },
                      "object_status": string,
                      "stop_id": string,
                      "update_time": timestamp
                    }
                  ]
                }

            where:

            * `routes` (required): The list of routes of the school buses:

              * `creation_time` (required): The time when this route has been
                created.

              * `stops` (required): The list of stops along the route:

                * `stop_id` (required): Identification of a bus stop used to board or
                  alight children when taking them to school (outward journey) or taking
                  them back to home from their school (inward journey).

                * `position` (required): Position of the bus stop along this route,
                  starting from `0`.

                * `arrival_time` (optional): Time when the school bus pulls up to the
                  bus stop's area.  This time is possibly not defined for the first bus
                  stop of the route.

                * `departure_time` (optional): Time whe the school bus leaves the bus
                  stop's area.  This time is possibly not defined for the last bus stop
                  of the route.

              * `journey_type`: Indicate the direction of the journey:

                * `outward`: From children's homes to the school.

                * `inward`: From the school to children's homes.

              * `object_status`: Current status of this route.

              * `path` (optional): A list of geographic coordinates defining the
                path of the route through the bus stops.

              * `route_id`: Identification of the route.

              * `update_time`: Time of the most recent modification of an
                information regarding this route.

              * `visibility`: Indicate the visibility to users:

                * `private`: This route is only visible to members of organization
                  responsible for managing the bus transportation service of the school
                  that this route takes children to or from, and parents whose children
                  are registered to this route.

                * `public`: This route is visible to any authenticated or anonymous
                  users.

                * `team`: This route is visible to any users registered to the school
                  that this route takes children to or from.

              * `stops` (required): The list of the places where buses of the school
                stop for children to get on or get off the bus.

              * `address` (optional): Postal address of the place corresponding to
                the bus stop.  This address is composed of one or more address
                components, which textual information is written in the specified
                locale.  An address component is defined with a component type and its
                value (refer to the `Place Service` documentation for the complete
                list of address components).

              * `creation_time` (required): Time when this bus stop has been created.

              * `locale` (required): Locale in which the values of each address
                component of the bus stop are written.

              * `location` (required): Information about the geographic location of
                the bus stop:

                * `altitude` (optional): Altitude in meters of the geographic location
                  of the bus stop.

                * `latitude` (required): Latitude-angular distance, expressed in
                  decimal degrees (WGS84 datum), measured from the center of the Earth,
                  of a point north or south of the Equator corresponding to the
                  geographic location of the bus stop.

                * `longitude` (required): Longitude-angular distance, expressed in
                  decimal degrees (WGS84 datum), measured from the center of the Earth,
                  of a point east or west of the Prime Meridian corresponding to the
                  geographic location of the bus stop.

              * `object_status` (required): Current status of this bus stop.

              * `stop_id` (required): Identification of the bus stop.

              * `update_time` (required): Time of the most recent modification of
                an attribute of the bus stop.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/school/(school_id)/bus-route',
                url_bits={
                    'school_id': school_id
                },
                arguments={
                    'include_path': include_path,
                    'locale': locale
                },
                authentication_required=False,
                signature_required=True))

    def add_bus_line(
            self,
            school_id,
            bus_line):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/school/(school_id)/bus-line',
                url_bits={
                    'school_id': school_id
                },
                message_body=bus_line,
                authentication_required=True,
                signature_required=True))

    def add_bus_stops(
            self,
            school_id,
            bus_stops):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/school/(school_id)/bus-stop',
                url_bits={
                    'school_id': school_id
                },
                message_body=bus_stops,
                authentication_required=True,
                signature_required=True))

    def reject_bus_stop_suggestion(
            self,
            suggestion_id):
        """
        Reject a bus stop suggestion that the server platform automatically
        made based on the Ci/Co operation activities of the pupils of a school.


        :param suggestion_id: Identification of a bus stop suggestion.


        :raise DeletedObjectException: If the bus stop suggestion has been
            already reviewed and deleted.

        :raise DisabledObjectException: If the bus stop suggestion has been
            already reviewed and ignored.

        :raise IllegalAccessException: If the user is not granted access to
            bus stop suggestions of this school.

        :raise UndefinedObjectException: If the bus stop suggestion does not
            exist.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/bus-stop/suggestion/(suggestion_id:uuid)/rejection',
                url_bits={
                    'suggestion_id': suggestion_id
                },
                authentication_required=True,
                signature_required=True))
