# coding: utf-8

"""
    Foxtail Trainer

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import foxtail_trainer_api
from foxtail_trainer_api.models.training_history import TrainingHistory  # noqa: E501
from foxtail_trainer_api.rest import ApiException

class TestTrainingHistory(unittest.TestCase):
    """TrainingHistory unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TrainingHistory
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = foxtail_trainer_api.models.training_history.TrainingHistory()  # noqa: E501
        if include_optional :
            return TrainingHistory(
                id = '0', 
                metric_name = '0'
            )
        else :
            return TrainingHistory(
        )

    def testTrainingHistory(self):
        """Test TrainingHistory"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
