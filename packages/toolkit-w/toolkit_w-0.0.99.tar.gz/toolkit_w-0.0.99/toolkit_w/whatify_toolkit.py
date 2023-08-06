import json
import allure
import boto3
import pandas as pd
import time, os
import logging
import s3fs
from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.token_json import UserToken
from toolkit_w.internal.vars_global import ProblemType, TargetMetric, FeatureType
from toolkit_w.internal.vars_global import InterpretabilityLevel as Interpt
import toolkit_w as my_toolkit
from ast import literal_eval

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

#############################
########    SDK      ########
#############################
#############################
###    Functionality      ###
#############################

class MyWhatify:
    #############################
    #######    API's      #######
    #############################
    user_token = None

    @classmethod
    def __init__(cls):
        pass

    #############################
    ###    user management    ###
    #############################
    @classmethod
    def authenticate(cls, username, password):
        cls.login(email=username, password=password)

    @classmethod
    def login(cls, email, password, user_id: str = None, imp_email: str = None):
        """
        login to Whatify system

        :param email: the user email
        :param password: the user password
        :param user_id: user ID to do impersonate
        :param imp_email: user email to do impersonate
        """
        with allure.step('login with user: ' + str(email)):
            my_toolkit.UserManagement.login(email=email, password=password)

            if user_id or imp_email:
                cls.impersonate(user_id=user_id, email=imp_email)

            cls.user_token = UserToken(my_toolkit.token)

    @classmethod
    def get_user_id(cls, email: str = None):
        """
        get the user ID of email - works only for Admin users

        :param email: user email to return the ID

        :return: user ID or -1 if not exist
        """
        user_id = -1
        if email:
            user_id = my_toolkit.UserManagement.get_user_id(email=email)
        else:
            user_id = cls.user_token.get_user_id()
        return user_id

    @classmethod
    def get_account_id(cls, email: str = None):
        """
        get the account ID of account name\email - works only for Admin users

        :param email: account name\email to return the ID

        :return: account ID or -1 if not exist
        """
        return my_toolkit.UserManagement.get_account_id(email=email)

    @classmethod
    def impersonate(cls, user_id=None, email: str = None, admin_token: str = None):
        """
        doing impersonate for user ID or email - only works for admin users

        :param user_id: the user ID to do impersonate
        :param email: the user email to do impersonate
        :param admin_token: the admin token to do impersonate
        """
        with allure.step(' '.join(['impersonate to user_ID:', str(user_id)])):
            if email:
                with allure.step('getting user ID from email'):
                    user_id = cls.get_user_id(email=email)

            with allure.step(' '.join(['impersonate to user_ID:', str(user_id)])):
                my_toolkit.UserManagement.impersonate(user_id=user_id, admin_token=admin_token)



    #############################
    #######    API's      #######
    #############################
    @classmethod
    def mark_ensemble_in_production(cls, ensemble_id, mark_production=True):
        """
        mark ensemble ID as in production and vice versa

        :param ensemble_id: the ensemble ID to change
        :param mark_production: True - mark as in production, False - mark as not in production
        """
        with allure.step('setting ensemble_id: ' + str(ensemble_id) + ' as in production: ' + str(mark_production)):
            logging.info('setting ensemble_id: ' + str(ensemble_id) + ' as in production: ' + str(mark_production))
            if mark_production:
                my_toolkit.Ensemble.set_ensemble_in_production(ensemble_id=ensemble_id)
            else:
                my_toolkit.Ensemble.remove_ensemble_in_production(ensemble_id=ensemble_id)

    @classmethod
    def run_prediction(cls, data_name, ensemble_id, data_file=None, wait=True, file_path=None, header=None,
                       data_id=None, skip_if_exist=False):
        with allure.step('running prediction on data name: ' + data_name + ' with ensemble id: ' + str(ensemble_id) + ' and wait is: ' + str(wait)):
            print('running prediction on data name: ' + data_name + ' with ensemble id: ' + str(ensemble_id) +
                  ' and wait is: ' + str(wait) + ' with skip_if_exist: ' + str(skip_if_exist))
            logging.info('running prediction on data name: ' + data_name + ' with ensemble id: ' + str(ensemble_id) + ' and wait is: ' + str(wait) )
            status = True
            predict_id = None
            message = None
            # data_file.drop(data_file.columns[len(df.columns) - 1], axis=1, inplace=True)
            if skip_if_exist:
                ret_list = cls.get_prediction_list(search_term=data_name)
                if len(ret_list) > 0:
                    for pred_check in ret_list:
                        if pred_check['ensemble_id'] == ensemble_id and pred_check['datasource_name'] == data_name:
                            return int(pred_check['id']), True, None
            try:
                if not (file_path or data_id):
                    data_id = my_toolkit.Datasource.create_from_dataframe(df=data_file, data_source_name=data_name,
                                                                          wait=True, skip_if_exists=True)['id']
                predict_id = my_toolkit.Prediction.create(ensemble_id=ensemble_id, data_id=data_id, data_name=data_name,
                                                          file_path=file_path, header=header, wait=wait)['id']
            except Exception as ex:
                message = ex.args
                status = False
        return predict_id, status, message

    @classmethod
    def run_ice(cls, pred_id):
        return my_toolkit.Prediction.run_ice(pred_id=pred_id)

    @classmethod
    def run_prescriptive(cls, pred_id, features, target_value='YES'):
        return my_toolkit.Prediction.run_prescriptive(pred_id=pred_id, features=features, target_value=target_value)

    @classmethod
    def upload_data_file(cls, data_name, data_file=None, wait=True, skip_if_exists=True, na_values=None):
        with allure.step('uploading csv name: ' + data_name + ' with wait= ' + str(wait) +
                         ' and skip if exist= ' + str(skip_if_exists)):
            source_id = -1
            try:
                if data_file is None:
                    data_file = cls.get_data_file_s3(file_name=data_name)
                source_id = my_toolkit.Datasource.create_from_dataframe(df=data_file, data_source_name=data_name,
                                                                        wait=wait, skip_if_exists=skip_if_exists,
                                                                        na_values=na_values)['id']
                print("\nYour Source ID for {} is: {}".format(data_name, source_id))
            except Exception as e:
                print(e)
        return source_id

    @classmethod
    def create_data_set(cls, source_id, data_set_name, problem_type=ProblemType.CLASSIFICATION, target='class',
                        not_used=None, na_values=None, retype_columns=None, rename_columns=None, sample_id=None,
                        datetime_format=None, time_axis=None, block_id=None, subdataset_id=None, sample_weight=None,
                        header: bool = True, hidden=None, skip_if_exists=True, wait=True):
        with allure.step('Preparing Dataset name: ' + str(data_set_name) + ' source_id= ' + str(source_id) +
                         ' problem_type: ' + str(problem_type) + ' target: ' + str(target) + ' wait: ' + str(wait)):
            dataset_id = -1
            # task_type = eval(problem_type.value)

            try:
                dataset_id = my_toolkit.Dataset.create(datasource_id=source_id, dataset_name=data_set_name,
                                                       problem_type=problem_type, target=target, not_used=not_used,
                                                       na_values=na_values,  skip_if_exists=skip_if_exists,
                                                       sample_id=sample_id, retype_columns=retype_columns,
                                                       rename_columns=rename_columns, datetime_format=datetime_format,
                                                       time_axis=time_axis, block_id=block_id, hidden=hidden,
                                                       sample_weight=sample_weight, subdataset_id=subdataset_id,
                                                       header=header, wait=True)['id']
                print("Dataset {} id is {}".format(data_set_name, dataset_id))
            except Exception as e:
                logging.exception('failed creating data set' + data_set_name + ' got error: ' + e)
        return dataset_id

    @classmethod
    def train_model(cls, data_name, dataset_id, target_metric=TargetMetric.RECALL_MACRO, training_time_in_minutes=6,
                    cv_folds=3, ensemble_size=5, interpt_level=Interpt.EXPLAINABLE, max_models_num=None,
                    leaky_features=[], wait=True, skip_if_exists=True):
        with allure.step('On data_name: ' + data_name + ' ID: ' + str(dataset_id)
                         + ' training a model with target_metric: ' + str(target_metric.value)
                         + ' cv_folds: ' + str(cv_folds) + ' ensemble_size: ' + str(ensemble_size)
                         + ' interpt_level: ' + str(interpt_level) + ' training_time_in_minutes:'
                         + str(training_time_in_minutes)):
            task_id = None
            ret_dict = None
            # target_metric_eval = eval(target_metric.value)
            # @markdown * Allocate training time
            # Training_time_in_minutes = training_time_in_minutes  # @param {type:'number'}

            # @markdown * Data partitioning
            # @markdown * Hold-out // Cross-Validation

            pipeline = cls.get_pipeline_estimators_list(dataset_id, True, interpt_level)
            estimators = cls.get_pipeline_estimators_list(dataset_id, False, interpt_level)
            if interpt_level == Interpt.EXPLAINABLE:
                interpretability_level = my_toolkit.vars_global.InterpretabilityLevel.EXPLAINABLE
            else:
                interpretability_level = my_toolkit.vars_global.InterpretabilityLevel.PRECISE

            # print('The training time is:', Training_time_in_minutes)
            # print ('The selected Target Metric is:', Target_metric.value)

            try:
                task = my_toolkit.Dataset.train(
                    task_name=data_name + " " + interpretability_level.name,
                    estimators=estimators,
                    pipeline=pipeline,
                    target_metric=target_metric,
                    dataset_id=dataset_id,
                    # splitting_strategy=firefly.enums.SplittingStrategy.STRATIFIED,
                    notes='created from Automation, run minutes: ' + str(training_time_in_minutes),
                    ensemble_size=ensemble_size,
                    n_folds=cv_folds,
                    max_models_num=int(max_models_num) if max_models_num else max_models_num,
                    interpretability_level=interpretability_level,
                    leaky_features=leaky_features,
                    timeout=int(training_time_in_minutes) * 60, wait=wait, skip_if_exists=skip_if_exists
                )
                task_id = task['id']
                ret_dict = task.to_dict()
            except Exception as e:
                logging.exception('Failed to train model on data_name: ' + str(data_name)
                                  + ' dataset_id: ' + str(dataset_id)
                                  # + ' target_metric_eval ' + str(target_metric_eval)
                                  + 'in Time: ' + str(training_time_in_minutes)
                                  + ' interpretability_level ' + str(interpretability_level))
        return task_id, ret_dict

    @classmethod
    def model_sensitivity_report(cls, ensemble_id, alg='Permutation', max_iteration=10):
        logging.info('running model sensitivity report for ensemble_id: ' + str(ensemble_id) + ' alg: ' + str(alg) +
                     ' max iter: ' + str(max_iteration))
        df = pd.DataFrame()
        n = 4
        # alg = 'Permutation'  # @param['Permutation', 'NA value']

        sens = None

        while max_iteration > 0:
            max_iteration = max_iteration - 1
            try:
                sens = my_toolkit.Ensemble.get_model_sensitivity_report(id=ensemble_id)
                if sens is not None:
                    break
                time.sleep(5)
            except Exception as e:
                print(e)
                break

        return sens[alg]

    @classmethod
    def feature_importance_report(cls, ensemble_id):
        logging.info('getting feature_importance report for ensemble_id: ' + str(ensemble_id))
        return my_toolkit.Ensemble.get_feature_importance_report(id=ensemble_id)

    @classmethod
    def get_report_by_type(cls, report_type: str, entity_id: int):
        logging.info(' '.join('getting report type:', str(report_type), 'for entity_id:', str(entity_id)))
        return my_toolkit.Report.get_report(report_type=report_type, entity_id=entity_id)

    @classmethod
    def run_sensitivity(cls, ensemble_id):
        logging.info('running model sensitivity for ensemble_id: ' + str(ensemble_id))
        status = None
        ensemble_id = int(ensemble_id)
        if ensemble_id > 0:
            status = my_toolkit.Ensemble.run_model_sensitivity(ensemble_id=ensemble_id)
        else:
            logging.info('invalid model sensitivity ensemble_id: ' + str(ensemble_id))
        return status

    @classmethod
    def search_act_base(cls, searchfunc=None, search_term=None, len=10, action_func=None):
        delete_list = searchfunc(search_term=search_term, len=len)
        if delete_list is not None and not delete_list.empty:
            [action_func(data_id) for data_id in delete_list]

    @classmethod
    def delete_data_source_by_name(cls, data_name=None, len=10):
        logging.info('deleting data Source with data_name: ' + str(data_name))
        cls.search_act_base(searchfunc=cls.get_data_source_list, search_term=data_name, len=len,
                            action_func=my_toolkit.Datasource.delete)

    @classmethod
    def delete_data_source_by_id(cls, data_id):
        logging.info('deleting data Source data_id: ' + str(data_id))
        # cls.delete_base(func=my_toolkit.Datasource.delete, file_id=data_id)
        my_toolkit.Datasource.delete(data_id)

    @classmethod
    def delete_data_set_by_name(cls, data_name=None, len=10):
        logging.info('deleting data Source with data_name: ' + str(data_name))
        cls.func_base(serachfunc=cls.get_datasets_list, search_term=data_name, len=len,
                      action_func=my_toolkit.Dataset.delete)

    @classmethod
    def delete_data_set_by_id(cls, data_id):
        logging.info('deleting dataset data_id: ' + str(data_id))
        my_toolkit.Dataset.delete(data_id)

    @classmethod
    def delete_task_by_name(cls, task_name=None, len=10):
        logging.info('deleting task with task_name: ' + str(task_name))
        cls.func_base(serachfunc=cls.get_tasks_list, search_term=task_name, len=len,
                      action_func=my_toolkit.Task.delete)

    @classmethod
    def delete_task_by_id(cls, task_id):
        logging.info('deleting task_id: ' + str(task_id))
        my_toolkit.Task.delete(task_id)

    @classmethod
    def cancel_task_by_id(cls, task_id):
        logging.info('canceling task_id: ' + str(task_id))
        my_toolkit.Task.cancel_task(task_id=task_id)

    @classmethod
    def delete_prediction_by_name(cls, prediction_name=None, len=10):
        logging.info('deleting prediction with prediction_name: ' + str(prediction_name))
        cls.func_base(serachfunc=cls.get_prediction_list, search_term=prediction_name, len=len,
                      action_func=my_toolkit.Prediction.delete)

    @classmethod
    def delete_prediction_id(cls, pred_id):
        logging.info('deleting pred_id: ' + str(pred_id))
        my_toolkit.Prediction.delete(pred_id)

    # def delete_user(cls, email=None, password=None, delete_user_id=None):
    #     with allure.step('Marking user email ' + str(email) + ' or user_id:' + str(delete_user_id) + ' as Deleted in the DB with API'):
    #         logging.info('deleting user email: ' + str(email))
    #         if not delete_user_id:
    #             cls.login(email=email, password=password)
    #             delete_user_id = cls.user_token.get_user_id()
    #
    #         if delete_user_id:
    #             cls.login(email=vars_global.Users.AUTO_QA_ADMIN.get_email(), password=vars_global.Users.AUTO_QA_ADMIN.get_password())
    #             #TODO move to test
    #             # cls.umClient = UMClient(host=conf_server['USERM_HOST'], port=conf_server['USERM_PORT'])  # , use_https=True)
    #             # cls.umClient.delete_user(jwt=cls.user_token.get_token(), user_id=delete_user_id)

    #############################
    ###        Gettrs         ###
    #############################
    @classmethod
    def api_get(cls, url, headers=None, body=None, params=None, user_token=None):
        return APIRequestor().get(url=url, headers=headers, body=body, params=params, api_key=user_token)

    @classmethod
    def api_post(cls, url, headers=None, body=None, params=None, user_token=None):
        return APIRequestor().post(url=url, headers=headers, body=body, params=params, api_key=user_token)

    @classmethod
    def api_put(cls, url, headers=None, body=None, params=None, user_token=None):
        return APIRequestor().put(url=url, headers=headers, body=body, params=params, api_key=user_token)

    @classmethod
    def api_patch(cls, url, headers=None, body=None, params=None, user_token=None):
        return APIRequestor().patch(url=url, headers=headers, body=body, params=params, api_key=user_token)

    @classmethod
    def send_api(cls, url, method, headers=None, body=None, params=None, user_token=None):
        switcher = {
            'GET': cls.api_get,
            'POST': cls.api_post,
            'PUT': cls.api_put,
            'PATCH': cls.api_patch
        }
        func = switcher.get(method.upper(), lambda: "Invalid api method")
        return func(url=url, headers=headers, body=body, params=params, user_token=user_token)

    @classmethod
    def test_api(cls, url, method, expected_response, headers=None, body=None, params=None, user_token=None):
        expected_payload, expected_status_code = expected_response

        with allure.step('checking endpoint (url): ' + str(url)):
            print(url)

        with allure.step('sending the API with method: ' + str(method)):
            response = cls.send_api(url=url, method=method, headers=headers, body=body, params=params, user_token=user_token)

        with allure.step('validating the expected response'):
            assert response.status_code == expected_status_code, f"Status code is not as expected: {response.status_code} instead of {expected_status_code}"

        with allure.step('validating response json'):
            assert str(expected_payload) == str(response), f"Response is not as expected: {response}, instead of {expected_payload}"

    #############################
    ###     DATA_SOURCE       ###
    #############################
    @classmethod
    def get_data_source_by_id(cls, data_id):
        with allure.step('getting the data source for data ID: ' + str(data_id)):
            ret_val = my_toolkit.Datasource.list(filter_={'id': [data_id]})['hits']
            return ret_val[0] if ret_val else {}

    @classmethod
    def get_data_source_by_name(cls, data_name):
        logging.info('getting the DataSource list for data_name: ' + str(data_name))
        ret_val = my_toolkit.Datasource.list(search_term=data_name)['hits']
        return ret_val[0] if ret_val else {}

    @classmethod
    def get_data_source_list(cls, search_term=None, len=10):
        with allure.step('getting the DataSource list with len: ' + str(len)):
            list_sources = my_toolkit.Datasource.list(search_term=search_term)
            sources = pd.DataFrame(list_sources['hits'][0:len])
        return sources[['creation_date', 'data_size', 'id', 'name', 'row_count', 'state']] if not sources.empty else sources

    @classmethod
    def get_data_set(cls, data_name):
        logging.info('getting the DataSet list for data_name: ' + str(data_name))
        return my_toolkit.Dataset.list(search_term=data_name)['hits']

    #############################
    ###        DATASET        ###
    #############################
    @classmethod
    def get_datasets_list(cls, len=10, search_term=None):
        with allure.step('getting the Dataset list with len: ' + str(len)):
            list_datasets = my_toolkit.Dataset.list(search_term=search_term)
            datasets = pd.DataFrame(list_datasets['hits'][0:len])
            datasets.set_index('creation_date')
        return datasets[['creation_date', 'id', 'name', 'problem_type', 'row_count', 'state']]

    @classmethod
    def get_tasks(cls, data_name):
        logging.info('getting the Tasks list for data_name: ' + str(data_name))
        return my_toolkit.Task.list(search_term=data_name)['hits']

    @classmethod
    def get_tasks_list(cls, len=10, search_term=None):
        with allure.step('getting the tasks list with len: ' + str(len)):
            list_tasks = my_toolkit.Task.list(search_term=search_term)
            tasks = pd.DataFrame(list_tasks['hits'][0:len])
        return tasks[['creation_date', 'dataset_id', 'name', 'notes', 'problem_type', 'state', 'target_metric']]

    @classmethod
    def get_ensemble_list(cls, task_id):
        with allure.step('getting the Ensemble list for task ID: ' + str(task_id)):
            # get list of ensembles
            return my_toolkit.Ensemble.list(filter_={'task_id': [task_id], 'stage': ['TASK', 'REFIT']})['hits']

    @classmethod
    def get_ensemble_id(cls, task_name):
        with allure.step('getting the ensemble ID of task name: ' + str(task_name)):
            task_id = my_toolkit.Task.get_task_id(task_name=task_name)
            return my_toolkit.Ensemble.get_ensemble_id(task_id=task_id)

    @classmethod
    def get_pipeline_list(cls, dataset_id, interpt_level=Interpt.PRECISE):
        return cls.get_pipeline_estimators_list(dataset_id, True, interpt_level)

    @classmethod
    def get_estimators_list(cls, dataset_id, interpt_level=Interpt.PRECISE):
        return cls.get_pipeline_estimators_list(dataset_id, False, interpt_level)

    @classmethod
    def get_pipeline_estimators_list(cls, dataset_id, is_pipeline=True, interpt_level=Interpt.PRECISE):
        """
        getting the Dataset pipeline or estimators list for dataset_id
        :param dataset_id: Dataset ID
        :param is_pipeline: get pipeline (default True) or estimators (False)
        :param interpt_level:
        :return:
        """
        with allure.step('getting the Dataset pipeline or estimators list for dataset_id: ' + str(dataset_id)
                     + ' is_pipeline: ' + str(is_pipeline) + ' interpt_level: ' + str(interpt_level)):
            ret_list = None
            if is_pipeline:
                ret_list = my_toolkit.Dataset.get_available_pipeline(inter_level=interpt_level, id=dataset_id)
            else:
                ret_list = my_toolkit.Dataset.get_available_estimators(inter_level=interpt_level, id=dataset_id)
        return ret_list

    @classmethod
    def get_prediction_list(cls, len=10, search_term=None):
        """
        get prediction list by search term
        :param len: len of the return prediction list
        :param search_term: search term to filter the prediction list
        :return: list of prediction for search term or by len
        """
        with allure.step('getting the prediction list limit by len for the prediction_name: ' + str(search_term)):
            return my_toolkit.Prediction.list(search_term=search_term)['hits'][0:len]

    @classmethod
    def get_prediction(cls, predict_id, len=None):
        """
        get prediction list for predict ID
        :param predict_id: prediction ID
        :param len: len of the return prediction list (None for all)
        :return: list of prediction limit by len (None = no limit) for predict ID
        """
        with allure.step('getting prediction list for predict_id: ' + str(predict_id) + ' len: ' + str(len)):
            ret_prediction = None
            predict_results = my_toolkit.Prediction.get(predict_id)

            download_url = predict_results['result_path']

            if download_url is not None:
                df_predict = pd.read_csv(download_url)
                ret_prediction = df_predict.head(len) if len else df_predict

        return ret_prediction

    @classmethod
    def get_prediction_error(cls, predict_id):
        """
        get error for prediction ID
        :param predict_id:prediction ID
        :return: error message for predict ID
        """
        with allure.step('getting prediction error for predict_id: ' + str(predict_id)):
            error_message = None
            predict_results = my_toolkit.Prediction.get(predict_id)
            error_message = predict_results['error_message']
        return error_message

    @classmethod
    def get_metadata_datasource(cls, data_id):
        """
        get_metadata for given datasource ID
        :param data_id: datasource ID
        :return: mapping of metadata
        """
        with allure.step('getting metadata for data id: ' + str(data_id)):
            metadata_results = my_toolkit.Datasource.get_metadata(data_id)
        return metadata_results

    @classmethod
    def get_metadata_dataset(cls, data_id):
        """
        get_metadata for given dataset ID
        :param data_id: dataset ID
        :return: mapping of metadata
        """
        with allure.step('getting metadata for data id: ' + str(data_id)):
            metadata_results = my_toolkit.Dataset.get_metadata(data_id)
        return metadata_results
    #############################
    ###        Wisdoms        ###
    #############################

    @classmethod
    def create_wisdom(cls, name: str, template_id: int, user_input: str, user_id: int = None, user_token: str = None):
        """
        create wisdom

        :param name (str): new name of the wisdom
        :param template_id (int): the template number for the new wisdom
        :param user_input (Dict): contain the wisdom data
        :param user_id (Optional [int]) : user id to set the wisdom, else we take from the exist user
        :param user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
        :return:

        wisdom ID
        """
        with allure.step(' '.join(['creating wisdom name:', str(name), 'template_id:', str(template_id), 'user_input:',
                                   str(user_input)])):
            wisdom_id = my_toolkit.Wisdom.create_wisdom(name=name, user_id=user_id if user_id else cls.get_user_id(),
                                                        template_id=template_id, user_input=literal_eval(str(user_input)),
                                                        api_key=user_token)
        return wisdom_id

    @classmethod
    def update_wisdom(cls, wisdom_id: int, wisdom_data: str, user_token: str = None):
        """
        update wisdom with given wisdom data

        :param wisdom_id (int): the id of the wisdom we want to change
        :param wisdom_data (str): the content we want to change in the wisdom
        :param user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
        :return:
        respone Succeed \ Failed
        """
        with allure.step(' '.join(['updating wisdom ID:', str(wisdom_id), 'with:', str(wisdom_data)])):
            response = my_toolkit.Wisdom.update_wisdom(id=wisdom_id, data=wisdom_data, api_key=user_token)
        return response

    @classmethod
    def copy_wisdom(cls, base_wisdom_id: int, target_wisdom_id: int, user_token: str = None):
        """
        copy from base_wisdom_id to target_wisdom_id
        :param base_wisdom_id: base wisdom id to copy from
        :param target_wisdom_id: target wisdom id to change
        :param user_token: Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
        """
        with allure.step(' '.join(['copying wisdom ID:', str(base_wisdom_id), 'to wisdom ID:', str(target_wisdom_id)])):
            logging.info(' '.join(['Copying wisdom date from wisdom ID:', str(base_wisdom_id), 'to wisdom ID:', str(target_wisdom_id)]))
            base = cls.get_wisdom(wisdom_id=base_wisdom_id).to_dict()
            base.pop('id')
            cls.update_wisdom(wisdom_id=target_wisdom_id, wisdom_data=base, user_token=user_token)

    @classmethod
    def delete_wisdom(cls, wisdom_id: int, user_token: str = None):
        """
        delete wisdom by given wisdom ID

        :param wisdom_id (int): the wisdom ID to delete
        :param user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
        :return:
        respone Succeed \ Failed
        """
        with allure.step(' '.join(['Deleting wisdom ID:', str(wisdom_id)])):
            response = my_toolkit.Wisdom.delete_wisdom(id=wisdom_id, api_key=user_token)
        return response

    @classmethod
    def get_wisdom_list(cls, search_term: str = None):
        """
        get wisdom list for current user
        :return:
        wisdom object list
        """
        with allure.step('getting wisdom list with search term: ' + str(search_term)):
            my_list = my_toolkit.Wisdom.get_wisdom_list_with_demo(search_term=search_term)
        return my_list

    @classmethod
    def get_suggest_wisdom_list(cls, search_term: str = None):
        """
        get suggest wisdom list for current user
        :return:
        suggest wisdom list
        """
        with allure.step('getting suggest wisdom list with search term: ' + str(search_term)):
            my_list = my_toolkit.Wisdom.get_suggest_wisdom_list(search_term=search_term)
        return my_list

    @classmethod
    def get_wisdom(cls, wisdom_id: int):
        """
        get wisdom for current user by ID
        :param wisdom_id:
        :return:
        wisdom object
        """
        with allure.step(' '.join(['getting wisdom ID:', str(wisdom_id)])):
            return my_toolkit.Wisdom.get_wisdom(id=wisdom_id)

    @classmethod
    def get_perturbations_download_link(cls, pred_id: int, features: str = None):
        """
        get perturbations download link for prediction
        :param pred_id:prediction ID to get the download link
        :param features: relvant features
        :return: download link
        """
        with allure.step(' '.join(['getting perturbations download link for prediction ID:', str(pred_id), 'With Features: ', str(features)])):
            return my_toolkit.Prediction.get_perturbations_download_link(pred_id=pred_id, features=features)

    #############################
    ###       Connector       ###
    #############################

    @classmethod
    def ls_client(cls, path: bool = False, user_token: str = None):
        """
        Lists the existing files on S3
        Args:
            user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
            path (Optional[bool]): True to include all path in folder, False just the files
        Returns:
            List of the files in S3, empty list if not found or not exist any file
        """
        return my_toolkit.Connector.get_client_path(path, user_token=user_token)

    @classmethod
    def get_credentials(cls, user_token: str = None, renew: bool = False):
        """
        get and set the user credentials in MyWhatify

        Args:
            user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
            renew (Optional[bool]): if we need to renew the credentials in MyWhatify
        Returns:
            The user credentials
        """
        return my_toolkit.Connector.get_credentials(user_token=user_token, renew=renew)

    @classmethod
    def get_s3_path(cls, user_token: str = None):
        """
        get user S3 path
        Args:
            user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
        Returns:
            path to user directory in s3
        """
        return my_toolkit.Connector.get_s3_path(user_token=user_token)

    @classmethod
    def read_to_pandas_df(cls, file_name: str):
        logging.info("Deprecated func: read_to_pandas_df, please use get_data_file_s3 function")
        return cls.get_data_file_s3(file_name=file_name)

    @classmethod
    def get_data_file_s3(cls, file_name: str, user_token: str = None, **kwargs):
        """
        read s3 to panda
        Args:
            file_name (str): the file name to read in the user bucket
            user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
        Returns:
            panda var with the file
        """
        logging.info('getting csv of data file from S3 for file_name: ' + str(file_name))
        return my_toolkit.Connector.read_to_pandas_df(file_name=file_name, user_token=user_token, **kwargs)

    @classmethod
    def write_pandas_df_to_s3(cls, df, file_name: str, user_token: str = None, **kwargs):
        """
        write panda to s3
        Args:
            df (panda): panda file to be written into s3
            file_name (str): the file name to name the file in the user bucket
            user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior
        Returns:
            None
        """
        return my_toolkit.Connector.write_pandas_df_to_s3(df=df, file_name=file_name, user_token=user_token, **kwargs)

    #############################
    ###   old data_file       ###
    #############################

    @classmethod
    def get_data_file(cls, data_name='car_sdk_demo.csv'):
        with allure.step('getting csv from data file for data_name: ' + str(data_name)):
            path = os.path.join(os.path.dirname(__file__))
            list_dir = os.listdir(path)
            with allure.step("looking inside path: " + str(path) + " the dir name list: " + str(list_dir)):
                logging.info("looking at the dir name list: " + str(list_dir))
                path = os.path.join(os.path.dirname(__file__), 'data_source')
                list_dir = os.listdir(path)
                with allure.step("looking inside path " + str(path) + " the data_source in dir name list: " + str(list_dir)):
                    logging.info("looking inside the data_source in dir name list: " + str(list_dir))

            # script_dir = os.getcwd()
            # script_dir = os.path.dirname(__file__)
            # os.path.dirname()
            path = os.path.join(os.path.dirname(__file__), 'data_source/', data_name)
        return pd.read_csv(path)

    # @classmethod
    # def get_created_data_file(cls, data_name='temp.csv'):
    #     df_data = cls.get_data_file(data_name='car_sdk_demo_test_no.csv')
    #     data = df_data.get_values()
    #     script_dir = os.path.dirname(__file__)
    #     path = os.path.join(script_dir, '../data_source/') + data_name
    #     with open(path, 'a') as f:
    #         f.write('car_id,buying,maint,doors,persons,lug_boot,junk_feature,safety')
    #         for i in range(1):
    #             for row in data:
    #                 text = ''
    #                 for index in range(row.__len__()):
    #                     text += str(row.tolist().pop(index)) + ","
    #                 f.write('\n' + text[:-1])
    #         f.close()

    #############################
    ###      Validation       ###
    #############################

# """
# Lists the existing Datasources - supports filtering, sorting and pagination.
#
# Args:
#     search_term (Optional[str]): Return only records that contain the `search_term` in any field.
#     page (Optional[int]): For pagination, which page to return.
#     page_size (Optional[int]): For pagination, how many records will appear in a single page.
#     sort (Optional[Dict[str, Union[str, int]]]): Dictionary of rules  to sort the results by.
#     filter_ (Optional[Dict[str, Union[str, int]]]): Dictionary of rules to filter the results by.
#     user_token (Optional[str]): Explicit `user_token`, not required, if `MyWhatify.login()` was run prior.
#
# Returns:
#     WhatifyResponse: Datasources are represented as nested dictionaries under `hits`.
# """