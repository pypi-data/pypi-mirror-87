"""
Wisdom is the user interaction with Whatify wisdom, it contains

"""
# Prediction is the way to productize the Ensemble created in the previous steps. Once an Ensemble is created,
# users can upload additional Datasources that may be used for predictions.
#
# ‘Prediction’ API includes querying of predictions (Get, List and Delete) and creating a Prediction to get predictions
# on existing Ensembles and uploaded Datasources.
import os
from typing import Dict, List

from toolkit_w.internal import utils
from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.errors import APIError
from toolkit_w.internal.whatify_response import WhatifyResponse
from toolkit_w.resources.api_resource import APIResource


class Report(APIResource):
    _CLASS_PREFIX = 'reports'

    @classmethod
    def get_insights_summary(cls, pred_id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets the wisdoms list for the user with the demo wisdoms.

        Args:
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains mapping of wisdoms for the user.
        """
        requestor = APIRequestor()
        url = '/'.join([cls._CLASS_PREFIX, 'predictions/insights/summary', str(pred_id)])
        response = requestor.get(url, api_key=api_key)
        return response

    @classmethod
    def get_insights_list(cls, pred_id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets the wisdoms list for the user with the demo wisdoms.

        Args:
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains mapping of wisdoms for the user.
        """
        requestor = APIRequestor()
        url = '/'.join([cls._CLASS_PREFIX, 'predictions/insights/list', str(pred_id)])
        response = requestor.get(url, api_key=api_key)
        return response

    @classmethod
    def get_top_insights(cls, pred_id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets the wisdoms list for the user with the demo wisdoms.

        Args:
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains mapping of wisdoms for the user.
        """
        requestor = APIRequestor()
        url = '/'.join([cls._CLASS_PREFIX, 'predictions/insights/top', str(pred_id)])
        response = requestor.get(url, api_key=api_key)
        return response

    @classmethod
    def get_download_link(cls, pred_id: int, report_name: str, api_key: str = None) -> WhatifyResponse:
        """
        Gets download link by pred id and report name.

        Args:
            pred_id : the prediction ID
            report_name: the report name
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.
        Returns:
            str: Link to download prediction report, empty string if could not get the link
        """
        requestor = APIRequestor()
        url = '/'.join([cls._CLASS_PREFIX, 'predictions/download', str(pred_id), str(report_name)])
        response = ''
        try:
            response = requestor.get(url, api_key=api_key)['result']
        except APIError as ex:
            print(' '.join(['got Error:', str(ex)]))
        return response

    @classmethod
    def get_report(cls, report_type: str, entity_id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets the Report by Type and entity ID.

        Args:
            report_type: the report type
            entity_id: the entity_id to get report for
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains mapping of the report for entity ID.
        """
        params = {
            'report_type': report_type,
            'entity_id': entity_id
        }
        requestor = APIRequestor()
        url = '/'.join([cls._CLASS_PREFIX])
        response = requestor.get(url, params=params, api_key=api_key)
        return response





