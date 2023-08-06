"""
Ensemble is the entity representing results of the training process (done using the `Task` entity).
It consists of a combination of one or more models, optimized for the dataset and model training configuration.

‘Ensemble’ API includes querying existing Ensembles (Get and List), but also the `refit` method, which allows users to
maintain updated models.
Future explainability features such as ROC curve, confusion matrix and other tools will be available as well.
"""
from typing import Dict

from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.whatify_response import WhatifyResponse
from toolkit_w.resources.api_resource import APIResource


class Ensemble(APIResource):
    _CLASS_PREFIX = 'ensembles'

    @classmethod
    def list(cls, search_term: str = None, page: int = None, page_size: int = None, sort: Dict = None,
             filter_: Dict = None, api_key: str = None) -> WhatifyResponse:
        """
        List the existing Ensembles - supports filtering, sorting and pagination.

        Args:
            search_term (Optional[str]): Return only records that contain the `search_term` in any field.
            page (Optional[int]): For pagination, which page to return.
            page_size (Optional[int]): For pagination, how many records will appear in a single page.
            sort (Optional[Dict[str, Union[str, int]]]): Dictionary of rules  to sort the results by.
            filter_ (Optional[Dict[str, Union[str, int]]]): Dictionary of rules to filter the results by.
            api_key (Optional[str]): Explicit `api_key`, not required, if `fireflyai.authenticate()` was run prior.

        Returns:
            WhatifyResponse: Ensembles are represented as nested dictionaries under `hits`.
        """
        return cls._list(search_term, page, page_size, sort, filter_, api_key)

    @classmethod
    def get(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Get information on a specific Ensemble.

        Information includes the state of the Ensemble and other attributes.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: Information about the Ensemble.
        """
        return cls._get(id, api_key)

    @classmethod
    def delete(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Deletes a specific Ensemble.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit `api_key`, not required, if `fireflyai.authenticate()` was run prior.

        Returns:
            WhatifyResponse: "true" if deleted successfuly, raises FireflyClientError otherwise.
        """
        return cls._delete(id, api_key)

    @classmethod
    def edit_notes(cls, id: int, notes: str, api_key: str = None) -> WhatifyResponse:
        """
        Edits notes of the Ensemble.

        Args:
            id (int): Ensemble ID.
            notes (str): New notes value.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: "submitted" if operation was successful, raises FireflyClientError otherwise.
        """
        requestor = APIRequestor()
        url = "{prefix}/{id}/notes".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.put(url=url, body={'notes': notes}, api_key=api_key)
        return response

    @classmethod
    def get_model_sensitivity_report(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets sensitivity report for Ensemble.

        Contains each feature's sensitivity score for missing values and feature values.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: Score for each feature in every sensitivity test.
        """
        requestor = APIRequestor()
        url = "reports/{prefix}/{id}/sensitivity".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url=url, api_key=api_key)
        result = response.to_dict()
        cls.__cleanup_report(result)
        return WhatifyResponse(data=result)

    @classmethod
    def get_feature_importance_report(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets feature importance report for Ensemble.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: Contains mapping of feature importance for the ensemble_id.
        """
        requestor = APIRequestor()
        url = "reports/{prefix}/{id}/feature_importance".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url=url, api_key=api_key)
        result = response.to_dict()
        cls.__cleanup_report(result)
        return WhatifyResponse(data=result)

    @classmethod
    def set_ensemble_in_production(cls, ensemble_id: int, api_key: str = None) -> WhatifyResponse:
        """
        Mark the Ensemble as in Production.

        Args:
            id (int): ensemble ID.
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains mapping of wisdoms for the user.
        """
        requestor = APIRequestor()
        url = '{prefix}/write/{ensemble_id}/set_in_production'.format(prefix=cls._CLASS_PREFIX, ensemble_id=ensemble_id)
        response = requestor.post(url, api_key=api_key)
        return response

    @classmethod
    def remove_ensemble_in_production(cls, ensemble_id: int, api_key: str = None) -> WhatifyResponse:
        """
        remove in production Mark from Ensemble

        Args:
            id (int): ensemble ID.
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains mapping of wisdoms for the user.
        """
        requestor = APIRequestor()
        url = '{prefix}/write/{ensemble_id}/remove_from_production'.format(prefix=cls._CLASS_PREFIX, ensemble_id=ensemble_id)
        response = requestor.post(url, api_key=api_key)
        return response

    @classmethod
    def get_ensemble_test_prediction_sample(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets prediction samples for Ensemble.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: Prediction samples.
        """
        requestor = APIRequestor()
        url = "reports/{prefix}/{id}/test_prediction_sample".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url=url, api_key=api_key)
        return response

    @classmethod
    def get_ensemble_summary_report(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets summary report for Ensemble.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: Summary report.
        """
        requestor = APIRequestor()
        url = "{prefix}/{id}/summary".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url=url, api_key=api_key)
        return response

    @classmethod
    def get_ensemble_roc_curve(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets ROC curve data for Ensemble.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: ROC curve data.
        """
        requestor = APIRequestor()
        url = "reports/{prefix}/{id}/roc_curve".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url=url, api_key=api_key)
        return response

    @classmethod
    def get_ensemble_confusion_matrix(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets confusion matrix for Ensemble.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: Confusion matrix.
        """
        requestor = APIRequestor()
        url = "reports/{prefix}/{id}/confusion".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url=url, api_key=api_key)
        return response

    @classmethod
    def get_model_architecture(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets architecture of the Ensemble.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: Architecture.
        """
        requestor = APIRequestor()
        url = "reports/{prefix}/{id}/architecture".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url=url, api_key=api_key)
        return response

    @classmethod
    def get_model_presentation(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets presentation of the Ensemble.

        Args:
            id (int): Ensemble ID.
            api_key (Optional[str]): Explicit api_key, not required if `fireflyai.authenticate` was run prior.

        Returns:
            WhatifyResponse: Ensemble's presentation.
        """
        requestor = APIRequestor()
        url = "reports/{prefix}/{id}/presentation".format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url=url, api_key=api_key)
        return response

    @classmethod
    def __cleanup_report(cls, result):
        if result:
            if result.get('NA value', {}).get('_title'):
                result['NA value'].pop('_title')
            if result.get('NA value', {}).get('_description'):
                result['NA value'].pop('_description')
            if result.get('Permutation', {}).get('_title'):
                result['Permutation'].pop('_title')
            if result.get('Permutation', {}).get('_description'):
                result['Permutation'].pop('_description')

    @classmethod
    def get_ensemble_id(cls, task_id) -> WhatifyResponse:
        ensemble_id = cls.list(filter_={'task_id': [task_id], 'stage': ['TASK', 'REFIT']})['hits'][-1]['id']
        return ensemble_id

    @classmethod
    def run_model_sensitivity(cls, ensemble_id: int, api_key: str = None) -> WhatifyResponse:
        """
        run the model sensitivity for Ensemble

        Args:
            id (int): ensemble ID.
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains status of the trigger.
        """
        requestor = APIRequestor()
        url = '{prefix}/{ensemble_id}/sensitivity'.format(prefix=cls._CLASS_PREFIX, ensemble_id=ensemble_id)
        response = requestor.post(url, api_key=api_key)
        return response
