import json
import math
import time
import requests
from collections import OrderedDict
from random import uniform
from oauth2client.service_account import ServiceAccountCredentials
from urllib.parse import urlencode, quote
from requests import HTTPError


def initialize_app(config):
    return Firebase(config)


def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except HTTPError as e:
        # raise detailed error message
        # TODO: Check if we get a { "error" : "Permission denied." } and handle automatically
        raise HTTPError(e, request_object.text)


def convert_to_pyre(items):
    pyre_list = []
    for item in items:
        pyre_list.append(Pyre(item))
    return pyre_list


def convert_list_to_pyre(items):
    pyre_list = []
    for item in items:
        pyre_list.append(Pyre([items.index(item), item]))
    return pyre_list


class Firebase:
    """ Firebase Interface """
    def __init__(self, config):
        self.api_key = config["apiKey"]
        self.auth_domain = config["authDomain"]
        self.database_url = config["databaseURL"]
        self.storage_bucket = config["storageBucket"]
        self.credentials = None
        self.requests = requests.Session()
        if config.get("serviceAccount"):
            scopes = [
                'https://www.googleapis.com/auth/firebase.database',
                'https://www.googleapis.com/auth/userinfo.email',
                "https://www.googleapis.com/auth/cloud-platform"
            ]
            service_account_type = type(config["serviceAccount"])
            if service_account_type is str:
                self.credentials = ServiceAccountCredentials.from_json_keyfile_name(config["serviceAccount"], scopes)
            if service_account_type is dict:
                self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(config["serviceAccount"], scopes)

        adapter = requests.adapters.HTTPAdapter(max_retries=3)

        for scheme in ('http://', 'https://'):
            self.requests.mount(scheme, adapter)


    def database(self):
        return Database(self.credentials, self.api_key, self.database_url, self.requests)


class Database:
    """ Database Service """
    def __init__(self, credentials, api_key, database_url, requests):

        if not database_url.endswith('/'):
            url = ''.join([database_url, '/'])
        else:
            url = database_url

        self.credentials = credentials
        self.api_key = api_key
        self.database_url = url
        self.requests = requests

        self.path = ""
        self.build_query = {}
        self.last_push_time = 0
        self.last_rand_chars = []

    def order_by_key(self):
        self.build_query["orderBy"] = "$key"
        return self

    def order_by_value(self):
        self.build_query["orderBy"] = "$value"
        return self

    def order_by_child(self, order):
        self.build_query["orderBy"] = order
        return self

    def start_at(self, start):
        self.build_query["startAt"] = start
        return self

    def end_at(self, end):
        self.build_query["endAt"] = end
        return self

    def equal_to(self, equal):
        self.build_query["equalTo"] = equal
        return self

    def limit_to_first(self, limit_first):
        self.build_query["limitToFirst"] = limit_first
        return self

    def limit_to_last(self, limit_last):
        self.build_query["limitToLast"] = limit_last
        return self

    def shallow(self):
        self.build_query["shallow"] = True
        return self

    def child(self, *args):
        new_path = "/".join([str(arg) for arg in args])
        if self.path:
            self.path += "/{}".format(new_path)
        else:
            if new_path.startswith("/"):
                new_path = new_path[1:]
            self.path = new_path
        return self

    def build_request_url(self, token):
        parameters = {}
        if token:
            parameters['auth'] = token
        for param in list(self.build_query):
            if type(self.build_query[param]) is str:
                parameters[param] = quote('"' + self.build_query[param] + '"')
            elif type(self.build_query[param]) is bool:
                parameters[param] = "true" if self.build_query[param] else "false"
            else:
                parameters[param] = self.build_query[param]
        # reset path and build_query for next query
        request_ref = '{0}{1}.json?{2}'.format(self.database_url, self.path, urlencode(parameters))
        self.path = ""
        self.build_query = {}
        return request_ref

    def build_headers(self, token=None):
        headers = {"content-type": "application/json; charset=UTF-8"}
        if not token and self.credentials:
            access_token = self.credentials.get_access_token().access_token
            headers['Authorization'] = 'Bearer ' + access_token
        return headers

    def get(self, token=None, json_kwargs={}):
        build_query = self.build_query
        query_key = self.path.split("/")[-1]
        request_ref = self.build_request_url(token)
        # headers
        headers = self.build_headers(token)
        # do request
        request_object = self.requests.get(request_ref, headers=headers)
        raise_detailed_error(request_object)
        request_dict = request_object.json(**json_kwargs)

        # if primitive or simple query return
        if isinstance(request_dict, list):
            return PyreResponse(convert_list_to_pyre(request_dict), query_key)
        if not isinstance(request_dict, dict):
            return PyreResponse(request_dict, query_key)
        if not build_query:
            return PyreResponse(convert_to_pyre(request_dict.items()), query_key)
        # return keys if shallow
        if build_query.get("shallow"):
            return PyreResponse(request_dict.keys(), query_key)
        # otherwise sort
        sorted_response = None
        if build_query.get("orderBy"):
            if build_query["orderBy"] == "$key":
                sorted_response = sorted(request_dict.items(), key=lambda item: item[0])
            elif build_query["orderBy"] == "$value":
                sorted_response = sorted(request_dict.items(), key=lambda item: item[1])
            else:
                sorted_response = sorted(request_dict.items(), key=lambda item: item[1][build_query["orderBy"]])
        return PyreResponse(convert_to_pyre(sorted_response), query_key)

    def push(self, data, token=None, json_kwargs={}):
        request_ref = self.check_token(self.database_url, self.path, token)
        self.path = ""
        headers = self.build_headers(token)
        request_object = self.requests.post(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))
        raise_detailed_error(request_object)
        return request_object.json()

    def set(self, data, token=None, json_kwargs={}):
        request_ref = self.check_token(self.database_url, self.path, token)
        self.path = ""
        headers = self.build_headers(token)
        request_object = self.requests.put(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))
        raise_detailed_error(request_object)
        return request_object.json()

    def update(self, data, token=None, json_kwargs={}):
        request_ref = self.check_token(self.database_url, self.path, token)
        self.path = ""
        headers = self.build_headers(token)
        request_object = self.requests.patch(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))
        raise_detailed_error(request_object)
        return request_object.json()

    def remove(self, token=None):
        request_ref = self.check_token(self.database_url, self.path, token)
        self.path = ""
        headers = self.build_headers(token)
        request_object = self.requests.delete(request_ref, headers=headers)
        raise_detailed_error(request_object)
        return request_object.json()

    def check_token(self, database_url, path, token):
        if token:
            return '{0}{1}.json?auth={2}'.format(database_url, path, token)
        else:
            return '{0}{1}.json'.format(database_url, path)

    def generate_key(self):
        push_chars = '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
        now = int(time.time() * 1000)
        duplicate_time = now == self.last_push_time
        self.last_push_time = now
        time_stamp_chars = [0] * 8
        for i in reversed(range(0, 8)):
            time_stamp_chars[i] = push_chars[now % 64]
            now = int(math.floor(now / 64))
        new_id = "".join(time_stamp_chars)
        if not duplicate_time:
            for i in range(0, 12):
                self.last_rand_chars.append(int(math.floor(uniform(0, 1) * 64)))
        else:
            for i in range(0, 11):
                if self.last_rand_chars[i] == 63:
                    self.last_rand_chars[i] = 0
                self.last_rand_chars[i] += 1
        for i in range(0, 12):
            new_id += push_chars[self.last_rand_chars[i]]
        return new_id

    def sort(self, origin, by_key):
        # unpack pyre objects
        pyres = origin.each()
        new_list = []
        for pyre in pyres:
            new_list.append(pyre.item)
        # sort
        data = sorted(dict(new_list).items(), key=lambda item: item[1][by_key])
        return PyreResponse(convert_to_pyre(data), origin.key())


class PyreResponse:
    def __init__(self, pyres, query_key):
        self.pyres = pyres
        self.query_key = query_key

    def val(self):
        if isinstance(self.pyres, list):
            # unpack pyres into OrderedDict
            pyre_list = []
            # if firebase response was a list
            if isinstance(self.pyres[0].key(), int):
                for pyre in self.pyres:
                    pyre_list.append(pyre.val())
                return pyre_list
            # if firebase response was a dict with keys
            for pyre in self.pyres:
                pyre_list.append((pyre.key(), pyre.val()))
            return OrderedDict(pyre_list)
        else:
            # return primitive or simple query results
            return self.pyres

    def key(self):
        return self.query_key

    def each(self):
        if isinstance(self.pyres, list):
            return self.pyres


class Pyre:
    def __init__(self, item):
        self.item = item

    def val(self):
        return self.item[1]

    def key(self):
        return self.item[0]

