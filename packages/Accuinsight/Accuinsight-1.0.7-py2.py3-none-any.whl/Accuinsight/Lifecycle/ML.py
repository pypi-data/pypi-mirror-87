import os
import inspect
import json
from collections import OrderedDict
import warnings
import sys
import logging
import boto3
from boto3.session import Session
import asyncio
from slack import WebClient
from slack.errors import SlackApiError
from pathlib import Path
from joblib import dump
from Accuinsight.modeler.core import func, path, get
from Accuinsight.modeler.core.func import get_time
from Accuinsight.modeler.core.get_for_visual import roc_pr_curve, get_visual_info_regressor
from Accuinsight.modeler.utils.runs_utils import get_aws_info, ProgressPercentage
from Accuinsight.modeler.core.sklearnModelType import REGRESSION, CLASSIFICATION
from Accuinsight.modeler.core.LcConst.LcConst import ALL_MODEL_PARAMS, SELECTED_PARAMS, SELECTED_METRICS, VALUE_ERROR, \
    LOGGING_TIME, LOGGING_RUN_ID, FITTED_MODEL, RUN_PREFIX_PATH, RUN_MODEL_JSON_PATH, RUN_MODEL_VISUAL_JSON_PATH, \
    RUN_MODEL_HOME_PATH
from Accuinsight.modeler.core.Run.RunInfo.RunInfo import set_current_runs, clear_runs, print_run_info, \
    set_git_meta, set_python_dependencies, set_run_name, set_model_json_path, set_visual_json_path, set_model_file_path, set_prefix_path, set_best_model_joblib_path, _set_result_path
from Accuinsight.modeler.utils.dependency.dependencies import gather_sources_and_dependencies
from Accuinsight.modeler.core.LcConst import LcConst
from Accuinsight.modeler.utils.os_getenv import is_in_ipython, get_current_notebook
from Accuinsight.modeler.clients.modeler_api import LifecycleRestApi


logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

warnings.filterwarnings("ignore")


class accuinsight(object):
    def __init__(self):
        self.BucketInfo = None
        self.endpoint = None

    def get_file(self, sub_path):
        self.BucketInfo = get_aws_info(sub_path)
        BUCKET_TYPE = self.BucketInfo['bucket_type']
        BUCKET_NAME = self.BucketInfo['bucket_name']
        FILE_PATH = self.BucketInfo['file_path']
        FILE_NAME = self.BucketInfo['file_name']
        FILE_TYPE = self.BucketInfo['file_type']
        FILE_DELIM = self.BucketInfo['file_delim']
        ACCESS_KEY = self.BucketInfo['my_access_key']
        SECRET_KEY = self.BucketInfo['my_secret_key']
        REGION = self.BucketInfo['region']
        URL = self.BucketInfo['endpoint']

        ## path for saving data
        save_dir = os.path.join(Path.home(), 'data_from_catalog')
        if os.path.exists(save_dir) == False:
            os.mkdir(save_dir)
        else:
            pass

        save_path = os.path.join(str(Path.home()), save_dir, FILE_NAME)

        # endpoint
        pre_url = 'https://' + BUCKET_NAME + '.' + URL
        self.endpoint = os.path.join(pre_url, FILE_PATH)

        client = boto3.client(BUCKET_TYPE,
                              aws_access_key_id = ACCESS_KEY,
                              aws_secret_access_key = SECRET_KEY,
                              region_name = REGION)

        transfer = boto3.s3.transfer.S3Transfer(client)

        progress = ProgressPercentage(client, BUCKET_NAME, FILE_PATH)

        sys.stdout.write('%s %s %s' % ('Downloading file...', FILE_NAME,  '\n'))
        transfer.download_file(BUCKET_NAME, FILE_PATH, save_path, callback=progress)
        logging.info(save_path)


    def set_slack(self, token = None, channel_id = None):
        self.token = token
        self.channel_id = channel_id

    def send_message(self, message = None):
        if message is not None:
            try:
                message = message
                response = WebClient(token=self.token).chat_postMessage(channel=self.channel_id, text=message)
            except SlackApiError as e:
                assert e.response["error"]
        else:
            raise ValueError('message를 입력해주세요.')


    class add_experiment(object):
        def __init__(self, model_name, *args):
            self.model_name = model_name
            is_notebook = is_in_ipython()
            if is_notebook == True:
                self.var_model_file_path = get_current_notebook()
                _caller_globals = inspect.stack()[1][0].f_globals
                (
                    self.mainfile,
                    self.sources,
                    self.dependencies
                ) = gather_sources_and_dependencies(
                    globs=_caller_globals,
                    save_git_info=False
                )
            else:
                _caller_globals = inspect.stack()[1][0].f_globals
                (
                    self.mainfile,
                    self.sources,
                    self.dependencies
                ) = gather_sources_and_dependencies(
                    globs=_caller_globals,
                    save_git_info=True
                )
                self.var_model_file_path = self.mainfile['filename']

            self.fitted_model = get.model_type(self.model_name)               # fitted model type
            self.json_path = OrderedDict()                               # path
            self.selected_params = []                                    # log params
            self.selected_metrics = OrderedDict()                        # log metrics
            self.summary_info = OrderedDict()                            # final results
            self.error_log = []                                          # error log
            self.vis_info = None                                         # visualization info - classifier
            self.dict_path = path.get_file_path(self.model_name)

            set_current_runs(get.model_type(self.model_name))
            _set_result_path(self.dict_path)

            # visualization function
            if len(args) == 2:
                self.xtest = args[0]
                self.ytest = args[1]

               # classifier
                if any(i in self.fitted_model for i in CLASSIFICATION):
                    self.vis_info = roc_pr_curve(self.model_name, self.xtest, self.ytest)

               # regressor
                elif any(i in self.fitted_model for i in REGRESSION):
                    self.ypred = get_visual_info_regressor(self.model_name, self.xtest)

            elif len(args) == 3:
                self.xtest = args[0]
                self.ytest = args[1]
                self.ypred = args[2]

            else:
                raise ValueError('Check the arguments of function - add_experiment(model_name, X_test, y_test)')

            # sklearn/xgboost/lightgbm
            get_from_model = get.from_model(self.model_name)
            self.all_model_params = get_from_model.all_params()
            self.model_param_keys = get_from_model.param_keys()

            set_model_file_path(self.var_model_file_path)

            if hasattr(self, 'mainfile'):
                set_git_meta(fileinfo=self.mainfile)
            if hasattr(self, 'dependencies'):
                set_python_dependencies(py_depenpency=self.dependencies)

        def __enter__(self):
            self.start_time = get_time.now()
            self.summary_info[LOGGING_TIME] = get_time.logging_time()
            self.summary_info[LOGGING_RUN_ID] = func.get_run_id()
            self.summary_info[FITTED_MODEL] = self.fitted_model

            set_prefix_path(self.dict_path[LcConst.RUN_PREFIX_PATH])

            set_run_name(self.fitted_model, self.summary_info[LOGGING_RUN_ID])
            return(self)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.summary_info[ALL_MODEL_PARAMS] = self.all_model_params
            self.summary_info[SELECTED_PARAMS] = self.selected_params
            self.summary_info[SELECTED_METRICS] = self.selected_metrics
            self.summary_info[VALUE_ERROR] = self.error_log


            # visualization
            if any(i in self.fitted_model for i in CLASSIFICATION):

                # path for visual.json
                set_visual_json_path(self.dict_path['visual_json'])
                visual_json_full_path = self.dict_path['visual_json_full']

                with open(visual_json_full_path, 'w', encoding='utf-8') as save_file1:
                    json.dump(self.vis_info, save_file1, indent="\t")

            elif any(i in self.fitted_model for i in REGRESSION):
                if len(self.ytest.tolist()) <= 5000:
                    self.summary_info['True_y'] = self.ytest.tolist()
                    self.summary_info['Predicted_y'] = self.ypred.tolist()
                else:
                    self.summary_info['True_y'] = None
                    self.summary_info['Predicted_y'] = None

            self.summary_info['ValueError'] = self.error_log

            if not self.summary_info['ValueError']:

                # path for model_info.json
                model_json_full_path = self.dict_path['model_json_full']
                set_model_json_path(self.dict_path['model_json'])

                with open(model_json_full_path, 'w', encoding='utf-8') as save_file2:
                    json.dump(self.summary_info, save_file2, indent="\t")
            else:
                pass

            # model save
            save_model_path = self.dict_path['save_model_joblib'] + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID] +'.joblib'
            path_for_setting_model_joblib = self.dict_path['save_model_dir'] + '/' + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID] +'.joblib'

            set_best_model_joblib_path(path_for_setting_model_joblib)

            dump(self.model_name, save_model_path)

            start_time = int(self.start_time.timestamp()*1000)
            end_time = int(get_time.now().timestamp()*1000)
            delta_ts = end_time - start_time

            clear_runs(start_time, end_time, delta_ts)

            modeler_rest = LifecycleRestApi(LcConst.BACK_END_API_URL,
                                            LcConst.BACK_END_API_PORT,
                                            LcConst.BACK_END_API_URI)
            modeler_rest.lc_create_run()
            #notifierActor.completed_message(notifierActor.get_notifier(), self.model_name + ' training is done')

        def log_params(self, param = None):
            # sklearn/xgboost/lightgbm
            if param:
                if param in self.model_param_keys:
                    return(self.selected_params.append(param))

                else:
                    self.error_log.append(True)
                    raise ValueError('"' + param + '"' + ' does not exist in the model.')

        def log_metrics(self, metric_name, defined_metric):
            self.selected_metrics[metric_name] = defined_metric

        def log_tag(self, description):
            self.summary_info['tag'] = description
