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
from majormode.perseus.model.contact import Contact
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.obj import Object


class XebusService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def activate_account(
            self,
            activation_code,
            fullname,
            password,
            mobile_phone_number):
        """
        Activate the account of a user and automatically sign the user in.


        :param activation_code: Identification of the verification request
            that has been sent to the user.

        :param fullname: Complete full name of the user.

        :param password: Password given by the user to allow him later to
            sign-in with his account.

        :param mobile_phone_number: Mobile phone number of the user.


        :return: a session instance containing the following members:

            * `account_id`: identification of the account of the user.

            * `expiration_time`: time when the login session will expire.

            * `fullname`: complete full name of the user as given by the user
              himself, i.e., untrusted information, or as determined from his
              email address as for a ghost account.

            * `session_id`: identification of the login session of the user.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path=f'/account/activation/{activation_code}',
                message_body={
                    'fullname': fullname,
                    'mobile_phone_number': mobile_phone_number,
                    'password': password
                },
                authentication_required=False,
                signature_required=True))

    def register_user(
            self,
            contact,
            area_id,
            school_id,
            accuracy=None,
            ip_address=None,
            locale=DEFAULT_LOCALE,
            location=None):
        """
        Register the user to the platform with his preferred language and the
        identification of the geographical area where his kid is living/
        studying in.

        Request the platform to send an email address verification to this
        user.


        :param contact: An instance `Contact` corresponding to the contact
            information of the user.  The function will initiate the process
            to verify this contact information.

        :param area_id: Identification of the geographical area where the kid
            of the user is living in.

        :param school_id: Identification of the school the kid of the user is
            studying at.

        :param accuracy: Accuracy in meters of the location of the user when
            he registered to the service.

        :param ip_address: IPv4 address of the machine of the user when he
            registered to the service.

        :param locale: An instance `Locale` representing the preferred
            language of the user.

        :param location: An instance `GeoPoint` representing the location of
            the user when he registered to the service.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account/registration',
                message_body={
                    'accuracy': accuracy,
                    'area_id': area_id,
                    'contact_name': contact.name,
                    'contact_value': contact.value,
                    'ip_address': ip_address and '.'.join([str(byte) for byte in ip_address]),
                    'll': location and f'{location.latitude},{location.longitude}',
                    'locale': locale,
                    'school_id': school_id
                },
                authentication_required=False,
                signature_required=True))

    def sign_in(self, email_address, password):
        """
        Sign-in the user to the platform providing an email address of the
        user and his password.


        :param email_address: email address of the user.

        :param password: password of the user.


        :return: a session instance containing the following members:

            * `account_id`: identification of the account of the user.

            * `expiration_time`: time when the login session will expire.

            * `fullname`: complete full name of the user as given by the user
              himself, i.e., untrusted information, or as determined from his
              email address as for a ghost account.

            * `is_verified`: indicate whether this contact information has been
              verified, whether it has been grabbed from a trusted Social Networking
              Service (SNS), or whether through a challenge/response process.  The
              user should be reminded to confirm his contact information if not
              already verified, or the user would take the chance to have his
              account suspended.

            * `is_primary`: indicate whether this contact information is the
              primary one for the given property.

            * `session_id`: identification of the login session of the user.

            * `username`: also known as screen name or nickname, username is
              chosen by the end user to identify himself when accessing the platform
              and communicating with others online.  A username should be totally
              made-up pseudonym, not reveal the real name of the person.  The
              username is unique across the platform.  A username is not case
              sensitive.


        :raise DeletedObjectException: if the user account has been deleted.

        :raise DisabledObjectException: if the user account has been disabled.

        :raise AuthenticationFailureException: if the given contact
            information and/or password don't match any account registered
            against the platform.
        """
        payload = Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account/session',
                message_body={
                    'email_address': email_address,
                    'password': password
                },
                authentication_required=False,
                signature_required=True))

        self.set_session(self.session.connection.build_session(payload))

        return self.session
