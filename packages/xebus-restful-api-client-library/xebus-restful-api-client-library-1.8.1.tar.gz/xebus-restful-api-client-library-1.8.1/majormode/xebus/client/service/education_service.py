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
from majormode.perseus.model.obj import Object


class EducationService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def get_school_grades(self, country_code):
        """
        Return the list of subdivisions of formal learning for the specified
        country.  They are known as school grades (US), school years or levels
        (UK).


        :param country_code: An ISO 3166-1 alpha-2 code representing the
            country to return school grades from.


        :return: A list of instances containing the following attributes:

            * `grade_level` (required): Number of the year a pupil has reached in
              his given educational stage for this grade

            * `grade_name` (required): Name given to this grade.

            * `start_age` (required): Age at which pupils usually begin this grade.

            * `end_age` (required): Age at which pupils usually complete this grade.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/school_grades/(country_code)',
                url_bits={
                    'country_code': country_code
                },
                authentication_required=False,
                signature_required=True))
