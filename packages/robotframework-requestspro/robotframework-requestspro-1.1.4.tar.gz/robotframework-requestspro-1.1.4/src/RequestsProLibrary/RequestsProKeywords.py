import json
import copy
import pandas as pd
import ast
from RequestsLibrary import RequestsLibrary
from urllib3.util import Retry
from robot.api import logger


class RequestsProKeywords(RequestsLibrary):
    ROBOT_LIBRARY_SCOPE = 'Global'
    DEFAULT_RETRY_METHOD_LIST = list(copy.copy(Retry.DEFAULT_METHOD_WHITELIST))

    def __init__(self):
        super().__init__()
        for base in RequestsProKeywords.__bases__:
            base.__init__(self)
        self._primers = {}
        self.cookies = None
        self.timeout = 90
        self.verify = False

    def trigger_api(self, test_data_full_path, test_input_path, api_name, base_url, **kwargs):

        global auth
        logger.info('*************************************************************************************************')
        logger.info('Trigger API using the parameters specified in test data sheet - ' + api_name)
        logger.info('*************************************************************************************************')
        logger.info('Step-01: Start - Read and filter test data sheet based on API_NAME')
        test_cases_df = pd.read_csv(str(test_data_full_path), dtype=str)
        # test_cases_df = pd.read_csv(str(test_data_full_path), dytpe=str)
        # Map the lowering function to all column names
        # test_cases_df.columns = map(str.lower, test_cases_df.columns)

        selected_api_df = test_cases_df.loc[test_cases_df['test_name'] == api_name].copy()
        selected_api_df = selected_api_df.loc[selected_api_df['tbe'] == 'YES']
        selected_api_df = selected_api_df.reset_index(drop=True)
        logger.debug('API Name      :' + api_name)
        logger.info('Step-01: End   - Read and filter test data sheet based on API_NAME')

        logger.info('Step-02: Start - Identify the request type')
        request_type = str(selected_api_df['request_type'][0])
        logger.info('Step-02: End   - Identify the request type')

        logger.info('Step-03: Start - Assign default values to None')
        params = None
        data = None
        # auth = None
        files = None
        json_data = None
        cookies = None
        timeout = None
        proxies = None
        verify = False
        logger.info('Step-03: End   - Assign default values to None')

        logger.info('Step-04: Start - Assign project specific values')
        if 'auth' in kwargs:
            for key, value in kwargs.items():
                if key == 'auth':
                    auth = value
        logger.info('Step-04: End   - Assign project specific values')

        logger.info('Step-05: Start - Identify uri')

        # Unique identifier for creating a session
        alias = str(api_name)

        uri = str(selected_api_df['uri'][0])
        logger.info('Step-05: End   - Identify uri')

        logger.info('Step-06: Start - Create the parameter and assign to params')

        # Identify the parameters specific columns and create a separate data frame
        selected_api_flt_df = selected_api_df.filter(regex='_d$', axis=1)

        # Identify the parameters specific for the api
        selected_api_flt_df = selected_api_flt_df.dropna(axis='columns')

        # Params value which needs to be passed should be as dictionary
        if selected_api_flt_df.empty:
            params = None
        else:
            params_list = selected_api_flt_df.to_dict('records')[0]

            # Remove _d from the parameter name
            params = {x.replace('_d', ''): v for x, v in params_list.items()}
        logger.info('Step-06: End   - Create the parameter and assign to params')

        logger.info('Step-07: Start - Extract other additional information required - data, auth, headers, files')

        # Check if data level json is required (body)
        if pd.isna(selected_api_df.loc[0, 'data']):
            data = None
        else:
            file_name = str(selected_api_df['data'][0])
            with open(test_input_path + api_name + '/' + file_name + '.JSON') as f:
                data = json.load(f)

        # Check if authorization is required
        if auth is not None:
            auth = auth.split(',')
            logger.debug(auth)
        elif pd.isna(selected_api_df.loc[0, 'auth']):
            auth = None
        else:
            auth = str(selected_api_df['auth'].item()).split(',')

        # Check if headers is required
        headers = {}
        if pd.isna(selected_api_df.loc[0, 'headers']):
            headers = {}
        else:
            headers = {'Content-Type': 'values', 'Accept': 'values'}
            headers_type = str(selected_api_df['headers'].item())
            headers['Content-Type'] = headers_type
            headers['Accept'] = headers_type

        # Check if files is required
        files_str = ''
        if pd.isna(selected_api_df.loc[0, 'files']):
            files = None
        else:
            # Extract the files column content
            files_str = str(selected_api_df['files'][0])

            # Convert the variable to dict
            files = ast.literal_eval(files_str)

            # Iterate through the dict and open the files specified in the data sheet
            # Files will be opened in binary mode and passed to post
            for k, value in files.items():
                f = open(test_input_path + api_name + '/' + value, 'rb')
                files[k] = f

        # List of parameters required for any type of API
        logger.info('type      :' + request_type)
        logger.info('url       :' + base_url)
        logger.info('uri       :' + uri)
        logger.info('params    :' + str(params))
        logger.info('data      :' + str(data))
        logger.info('auth      :' + str(auth))
        logger.info('headers   :' + str(headers))
        logger.info('files     :' + str(files_str))

        # Static variables for the request
        max_retries = 3
        backoff_factor = 0.1
        disable_warnings = 0
        debug = 0

        logger.info('Step-07: End   - Extract other additional information required - data, auth, headers, files')

        logger.info('Step-08: Start - Trigger the API, extract the response and status code')

        # Condition to check GET/POST method
        if request_type == 'GET':

            # Response with status code, response content and api name will be returned as data frame
            # Create Session
            super(RequestsLibrary, self).create_session(alias=alias, url=base_url, headers=headers, cookies=cookies,
                                                        auth=auth, timeout=timeout, proxies=proxies, verify=verify,
                                                        debug=debug, max_retries=max_retries,
                                                        backoff_factor=backoff_factor,
                                                        disable_warnings=disable_warnings)
            # Trigger Get method
            response = super(RequestsLibrary, self).get_request(alias=alias, uri=uri, headers=headers, json=data,
                                                                params=params, allow_redirects=None, timeout=timeout)
        elif request_type == 'PUT':

            # Response with status code, response content and api name will be returned as data frame
            # Create Session
            super(RequestsLibrary, self).create_session(alias=alias, url=base_url, headers=headers, cookies=cookies,
                                                        auth=auth, timeout=timeout, proxies=proxies, verify=verify,
                                                        debug=debug, max_retries=max_retries,
                                                        backoff_factor=backoff_factor,
                                                        disable_warnings=disable_warnings)
            # Trigger Get method
            response = super(RequestsLibrary, self).put_request(alias=alias, uri=uri, data=data, json=json_data,
                                                                params=params, files=files, headers=headers,
                                                                allow_redirects=None, timeout=timeout)
        else:
            # Create Session
            super(RequestsLibrary, self).create_session(alias=alias, url=base_url, headers=headers, cookies=cookies,
                                                        auth=auth, timeout=timeout, proxies=proxies, verify=verify,
                                                        debug=debug, max_retries=max_retries,
                                                        backoff_factor=backoff_factor,
                                                        disable_warnings=disable_warnings)
            # Trigger Get method
            response = super(RequestsLibrary, self).post_request(alias=alias, uri=uri, data=data, json=json_data,
                                                                 params=params, headers=headers, files=files,
                                                                 allow_redirects=None, timeout=timeout)

        selected_api_df.loc[0, 'API_Response_Code'] = response.status_code
        if response.text != '':
            response_string = str(response.content.decode("utf-8"))
            selected_api_df.loc[0, 'API_Response_Content'] = response_string
        else:
            selected_api_df.loc[0, 'API_Response_Content'] = ''
        logger.info('Step-08: End   - Trigger the API, extract the response and status code')
        logger.info('*************************************************************************************************')

        return selected_api_df

    def api_test_cases_list(self, test_data_full_path):
        """
        Opens the api test data file from the test inputs
        API test data file name should always be api_test_data. File format should be csv

        Aruguments:
                | Test Data Full Path   | Full path of test data file with file name    |
        Example:

        |*Keywords*             |   *Parameters*                                        |
        |*Api Test Cases List*  |   *C:\\Automation_Repository\\Project_Name\\Test_Inputs\\Project_Name_api_test_data.csv|

        """
        logger.info('*************************************************************************************************')
        logger.info('Reading API Test Data File and return the APIs to be executed')
        logger.info('*************************************************************************************************')
        logger.info('Step-01: Start - Read and filter based on tbe')
        test_cases_df = pd.read_csv(str(test_data_full_path))
        test_cases_df = test_cases_df.loc[test_cases_df['tbe'] == 'YES']
        test_cases_dict = test_cases_df.to_dict('records')
        logger.info('Step-01: End   - Read and filter based on tbe')
        logger.info('*************************************************************************************************')
        return test_cases_dict
