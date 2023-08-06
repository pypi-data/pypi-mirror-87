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


class GuardianService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def get_children(
            self,
            limit=None,
            offset=0):
        """
        Return a list of the children of the specified user (either a legal
        guardian or a childminder).


        :param limit: Constrain the number of records to return to the
            specified number.  If not specified, the default value is
            `BaseService.DEFAULT_RESULT_SET_SIZE`.  The maximum value is
            `BaseService.MAXIMUM_RESULT_SET_LIMIT`.

        :param offset: Require to skip that many records before beginning to
            return records to the client.  Default value is `0`.  If both
            `offset` and `limit` are specified, then `offset` records
            are skipped before starting to count the limit records that are
            returned.


        :return: A list of objects containing the following attributes:

            * `account_id` (required): Identification of the account of a user.

            * `fullname` (required): Personal name by which the user is known.

            * `locale` (optional): A `Locale` object that identifies the
              preferred language of the user.

            * `picture_id` (optional): Identification of the user's picture.

            * `picture_url` (optional): Uniform Resource Locator (URL) that
              specifies the location of the user's picture.

            * `place_id` (optional): Identification of the residence of the parent
              where he puts his child up.  Guardian having the role of parent MUST
              have a residence.

            * `role` (required): Role of this guardian towards the child.

            * `update_time` (required)): Time when the information of this user
              account has been updated for the last time.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/guardian/children',
                arguments={
                    'limit': limit,
                    'offset': offset
                },
                authentication_required=True,
                signature_required=True))

    def get_children_location(self):
        """
        Return the last known location of the guardian's children.

        This function retrieves the list of the guardian's children who are
        currently checked-in in a school bus, and return the location of the
        ID-R devices that were used to check-in these children.


        :return: A list of object containing the following attributes:

            * `account_id` (required): Identification of a child.

            * `accuracy` (required): Accuracy in meters of the last known location
              of the child.

            * `altitude` (optional): Altitude in meters of the last known location
              of the child.

            * `attendant_account_id` (required): Identification of the attendant who
              checked-in the child.

            * `bearing` (optional): Bearing in degrees of the last known location of
              the child.  Bearing is the horizontal direction of travel of the
              child, and is not related to the child orientation.  It is guaranteed
              to be in the range `[0.0, 360.0]`, or not given if the bearing of the
              child at its last known location is not provided.

            * `bus_id` (optional): Identification of the school bus where the child
              has been checked-in.

            * `cico_time` (required): Time when the child has been checked-in.

            * `device_id` (required): Identification of the ID-R device that was
              used to check-in the child.

            * `fix_time` (required): Time when the tracker mobile device determined
              the information of this last known location of the child.

            * `latitude` (required): Latitude-angular distance, expressed in decimal
              degrees (WGS84 datum), measured from the center of the Earth, of a
              point north or south of the Equator corresponding to the last known
              location of the child.

            * `longitude` (required): Longitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the Earth,
              of a point east or west of the Prime Meridian corresponding to the
              last known location of the child.

            * `line_id` (optional): Identification of the school bus line for which
              the child has been checked-in.

            * `speed` (optional): Speed in meters/second over the ground.

            * `stop_id` (optional): Identification of the bus stop where the child
              boarded school bus when the attendant checked-in this child.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/guardian/children/location',
                authentication_required=True,
                signature_required=True))

    def register_child(
            self,
            fullname,
            dob,
            # photo_file,
            school_id,
            grade_level,
            first_name=None,
            get_off_school_bus_unaccompanied=False,
            home_address=None,
            home_id=None,
            last_name=None,
            leave_school_compound_unaccompanied=False):
        """
        Register a child to the bus transportation program of the specified
        school, on behalf of a legal guardian of this child.


        :param fullname: Personal name by which the child is known, generally
            composed of first name, middle names, and surname, written in a
            order that depends on the language/culture of the child.

        :param dob: Date of birth of the child.

        :param photo_file: A file-like object corresponding to the identity
            photo of the child.

        :param school_id: Identification of the school this child attends.

        :param grade_level: Number of the year the child has reached in the
            educational stage of the school.

        :param first_name: Forename (also known as *given name*) of the child.
            The first name of a child is used to alphabetically sort a list of
            guardians.

        :param get_off_school_bus_unaccompanied: Indicate whether the child is
            authorized to alight from the school bus that brings him home
            without the presence of a guardian of him (e.g., legal guardian or
            childminder).

        :param home_address: Information about the child's home.  This
            argument is optional, and is ignored, if the argument `home_id` is
            passed.  This argument corresponds to an object containing the
            following attributes:

            * `formatted_address` (required): Postal address of the child's home as
              entered by the user.

            * `geocoded_address` (required): Human-readable postal address of the
              child's home determined by a geocoder from the geographical location
              of the child's residence that the user has specified by clicking on
              the map and adjusting the position of the marker representing the
              child's residence.

            * `is_address_edited` (optional): Indicate whether the user has
              manually edited the postal address of the child's home.

            * `is_location_edited` (optional): Indicate whether the user has
              manually adjusted the position of the marker that identifies the
              location of the child's home.

            * `locale` (required): An object `Locale` of the language in which
              the values of each address component of the child's home are written.
              If not defined, a default locale is used (more likely American English).

            * `location` (required): An object `GeoPoint` of the geographical
              location of the child's home.

        :param home_id: Identification of the child's home, if already defined.
            This argument is optional if the attribute `home_address` is
            passed.  This argument takes precedence over the attribute
            `home_address` if both are passed.

        :param last_name: Surname (also known as *family name*) of the child.
            The last name of a child is used to alphabetically sort a list of
            guardians.

        :param leave_school_compound_unaccompanied: Indicate whether the child is
            authorized to leave school at the end without the presence of a
            guardian of him (e.g., legal guardian or childminder).


        :return: An object containing the following attributes:

            * `account_id` (required): The identification of the user account of
              this child.

            * `file_name` (required): The original local file name of the child's
              identity photo.

            * `picture_id` (required): Identification of the identity photo of the
              child.

            * `picture_url` (required): Uniform Resource Locator (URL) that
              specifies the location of the child's identity photo.  The client
              application can use this URL and append the query parameter `size`
              to specify a given pixel resolution of the photo, such as `thumbnail`,
              `small`, `medium`, or `large`.

            * `update_time` (required): Time of the most recent modification of the
              child's account attributes.  This information SHOULD be stored by the
              client application to manage its cache of guardians.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/guardianship/child',
                message_body={
                    'dob': dob,
                    'first_name': first_name,
                    'fullname': fullname,
                    'get_off_school_bus_unaccompanied': get_off_school_bus_unaccompanied,
                    'grade_level': grade_level,
                    'home_address': home_address and {
                        'formatted_address': home_address.formatted_address,
                        'geocoded_address': home_address.geocoded_address,
                        'is_address_edited': home_address.is_address_edited,
                        'is_location_edited': home_address.is_location_edited,
                        'locale': home_address.locale,
                        'location': home_address.location and
                            f'{home_address.location.latitude},{home_address.location.longitude}',
                    },
                    'home_id': home_id,
                    'last_name': last_name,
                    'leave_school_compound_unaccompanied': leave_school_compound_unaccompanied,
                    'school_id': school_id,
                },
                # files=[photo_file],
                authentication_required=True,
                signature_required=True))

    def request_guardianship(
            self,
            child_id):
        """
        Request the guardianship towards a child on behalf of the
        authenticated user.

        Guardianship request is required when a child has been previously
        registered by another user.  The latter is the default parent for this
        child.


        :param child_id: Identification of the account of a child whose
            guardianship is requested.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/child/(child_id)/guardianship/request',
                url_bits={
                    'child_id': child_id
                },
                authentication_required=True,
                signature_required=True))

    def search_guardians(
            self,
            keywords=None,
            limit=None,
            locale=DEFAULT_LOCALE,
            offset=0):
        """
        Search for users who could be considered as the guardians of a child
        and whose personal names best match the specified words.

        The function returns users whose set of names (also known as name-
        group, e.g. first name, last name, middle name, etc.) start with one
        or more of these words.


        :param keywords: A list of keywords to search guardians for.

        :param limit: Constrain the number of places to return to the
            specified number.  If not specified, the default value is
            ``BaseService.DEFAULT_RESULT_SET_SIZE``.  The maximum value is
            ``BaseService.MAXIMUM_RESULT_SET_LIMIT``.

        :param locale: An object ``Locale`` to return textual information,
            such as the names of countries and the names of guardians.

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
                path='/guardian',
                arguments={
                    'keywords': keywords and ','.join(keywords if isobject(keywords, (list, set, tuple)) else [keywords]),
                    'limit': limit,
                    'locale': locale,
                    'offset': offset
                },
                authentication_required=True,
                signature_required=True))

    def upload_child_photo(self, child_account_id, file):
        """
        Upload the photo identity of a child on behalf of a legal guardian of
        this child.


        :param child_account_id: Identification of the account of a child.

        :param file: A file-like object to upload to the platform.


        :return: An instance containing the following attributes:

            * ``file_name`` (required): The original local file name as the
            ``filename`` parameter of the ``Content-Disposition`` header.

            * ``picture_id`` (required): Identification of the new avatar of the
                user's account as registered to the platform.

            * ``picture_url`` (required): Uniform Resource Locator (URL) that
              specifies the location of the user's avatar.  The client application
              can use this URL and append the query parameter ``size`` to specify
              a given pixel resolution of the photo, such as ``thumbnail``,
              ``small``, ``medium``, or ``large``.

            * ``update_time`` (required): Time of the most recent modification of
              the attributes of the user's account.  This information should be
              stored by the client application to manage its cache of user
              accounts.


        :raise DeletedObjectException: If the account of the child has been
            deleted.

        :raise DisabledObjectException: If the account of the child has been
            disabled.

        :raise IllegalAccessException: If the user on behalf of whom the
            child's photo identify is uploaded to the platform is not a legal
            guardian of the child, or if the photo has been already added to
            the platform but to another child

        :raise InvalidOperation: If the format of the uploaded image is not
            supported.

        :raise OutdatedPhotoException: If the uploaded photo has been already
            used by the past, and it has been assessed as outdated.

        :raise UndefinedObjectException: If the specified identification
            doesn't refer to the account of a child registered to the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.PUT,
                path=f'/guardian/child/{child_account_id}/photo',
                files=[file],
                authentication_required=True,
                signature_required=True))
