import json
import requests
from typing import Tuple
import time
import dimod
import enum

from requests.exceptions import HTTPError

class APIStatus(enum.Enum):
    SUCCESS = 'SUCCESS'
    PENDING = 'PENDING'
    FAILED = 'FAILED'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'


POST_SOLVER = {
    "hardware": str,
    "algorithm": str,
    "num_variables": int,
    "problem": dict,
    "problem_type": str,
    "parameters": dict,
    "info": dict
}

def post_instance(url: str, token: str, instance: dict)->dict:
    endpoint = url if url[-1] != '/' else url[:-1]
    endpoint += '/jijcloudpostinstance/JijCloudPostInstance/'
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": token
    }
    json_data = json.dumps(instance)
    res = requests.post(endpoint, headers=headers, data=json_data)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        try:
            res = e.response
            res_body = res.json()
            error_message = "\n" + res_body['message']
        except:
            error_message = e
        raise requests.exceptions.HTTPError(e, error_message)

    return res.json()


def solver_api(url: str, token: str, parameters: dict, cachekey: str):
    endpoint = url if url[-1] != '/' else url[:-1]
    endpoint += '/jijcloudquery/JijCloudQuery/'
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": token
    }


    json_data = json.dumps({
        'instance_key': cachekey,
        'solver_param': parameters['parameters'],
        'solver': parameters['solver']
    })


    res = requests.post(endpoint, headers=headers, data=json_data)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        try:
            res = e.response
            res_body = res.json()
            error_message = "\n" + res_body['message']
        except:
            error_message = e
        raise requests.exceptions.HTTPError(e, error_message)

    return res.json()


def fetch_api(url: str, token: str, cachekey: str):
    endpoint = url if url[-1] != '/' else url[:-1]
    endpoint += '/jijcloudquery/JijCloudQuery/'
    headers = {
        "Ocp-Apim-Subscription-Key": token
    }

    params = {
        'cachekey': cachekey,
    }

    res = requests.get(endpoint, headers=headers, params=params)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # TODO: set error logger
        if res.text != 'Internal Server Error':
            print('error object', res.text)
        raise requests.exceptions.HTTPError(e)

    json_obj = res.json()
    if json_obj is None:
        raise HTTPError('Cache key is not found')

    return json_obj



def post_instance_and_query(instance_url, solver_url, token, instance, parameters, sync:bool=True):
    # Instance を投げる
    instance_key = post_instance(instance_url, token, instance)

    # Solverにqueryをなげる
    solver_res = solver_api(solver_url, token, parameters, instance_key['cachekey'])

    # 同期モードで解を取得
    status = 'PENDING'
    if sync:
        while status == APIStatus.PENDING.value:
            response = fetch_api(solver_url, token, solver_res['cachekey'])
            status = response['status']
            if response['status'] == APIStatus.SUCCESS.value:
                break
            elif response['status'] == APIStatus.FAILED.value:
                return _empty_resopnse(APIStatus.FAILED, solver_url, token, solver_res['cachekey'])

            elif response['status'] == APIStatus.UNKNOWN_ERROR.value:
                return _empty_resopnse(APIStatus.UNKNOWN_ERROR, solver_url, token, solver_res['cachekey'])

    else:
        return _empty_resopnse(APIStatus.PENDING, solver_url, token, solver_res['cachekey'])

    res_json = response['response']
    res_obj = Response.from_serializable(res_json)
    res_obj.set_status(APIStatus.SUCCESS)
    return res_obj



def _empty_resopnse(status, solver_url, token, cache):
    response: Response = Response.from_samples([], 'BINARY', 0)
    response._set_config(solver_url, token, cache)
    response.set_status(status)
    return response

class Response(dimod.SampleSet):

    def _set_config(self, solver_url, token, solver_cache):
        self._solver_url = solver_url
        self._token = token
        self._solver_cache = solver_cache

    def set_status(self, status):
        self._status = status

    @property
    def status(self):
        if hasattr(self, '_status'):
            return self._status
        else:
            return APIStatus.PENDING

    def get_result(self):
        if self.status == APIStatus.PENDING:
            response = fetch_api(self._solver_url, self._token, self._solver_cache)
            if response['status'] == APIStatus.SUCCESS.value:
                self = _empty_resopnse(APIStatus.SUCCESS, self._solver_url, self._token, self._solver_cache)
                return self
            elif response['status'] == APIStatus.FAILED.value:
                self.set_status(APIStatus.FAILED)
                return self
            else:
                return self
        else:
            return self

