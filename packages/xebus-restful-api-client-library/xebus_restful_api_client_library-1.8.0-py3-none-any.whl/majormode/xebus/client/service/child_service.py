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


class ChildService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def search_children(
            self,
            keywords=None,
            limit=None,
            locale=DEFAULT_LOCALE,
            offset=0):
        """
        Return a list of children that have joined the School Bus Program and
        that correspond to the specified criteria.


        :param keywords: A list of keywords to search children for.

        :param limit: Constrain the number of places to return to the
            specified number.  If not specified, the default value is
            ``BaseService.DEFAULT_RESULT_SET_SIZE``.  The maximum value is
            ``BaseService.MAXIMUM_RESULT_SET_LIMIT``.

        :param locale: An instance ``Locale`` to return textual information,
            such as the names of countries and the names of children.

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
                path='/child',
                arguments={
                    'keywords': keywords and ','.join(keywords if isinstance(keywords, (list, set, tuple)) else [keywords]),
                    'limit': limit,
                    'locale': locale,
                    'offset': offset
                },
                authentication_required=True,
                signature_required=True))
