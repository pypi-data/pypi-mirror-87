import urllib

import requests
from dateutil import parser

from ._klasifikasi_model import KlasifikasiModel
from ._settings import BASE_URL


class Klasifikasi:
    def __init__(self, creds, url=BASE_URL):
        if not isinstance(creds, list):
            raise Exception(
                "Creds must be a list of dict contain client_id & client_secret"
            )

        self.__model_mapping = {}
        for data in creds:
            if (not isinstance(data, dict) or data.get("client_id") is None
                    or data.get("client_secret") is None):
                raise Exception(
                    "Creds must be a list of dict contain client_id & client_secret"
                )

            model = KlasifikasiModel(data.get("client_id"),
                                     data.get("client_secret"), url)
            self.__model_mapping[model.public_id] = model

        self.url = url

    def get_models(self):
        return self.__model_mapping

    def classify(self, public_id, query):
        if self.__model_mapping.get(public_id) is None:
            raise Exception("Model not found !")
        model = self.__model_mapping.get(public_id)

        headers = {"Authorization": "Bearer {}".format(model.get_token())}
        payload = {"query": query}
        response = requests.post(
            "{}/api/v1/classify/{}".format(self.url, public_id),
            headers=headers,
            json=payload,
        )
        response_json = response.json()

        if response.status_code != 200:
            error = "Failed to classify into klasifikasi-api"
            if response_json.get("error"):
                error = response_json.get("error")
            raise Exception(error)

        return response_json

    def logs(self, public_id, query):
        if self.__model_mapping.get(public_id) is None:
            raise Exception("Model not found !")

        model = self.__model_mapping.get(public_id)

        if query.get("started_at") is None or query.get("ended_at") is None:
            raise Exception("Date filter is required")

        query_string = {}
        started_at = parser.parse(query.get("started_at"))
        query_string["startedAt"] = started_at.isoformat()

        ended_at = parser.parse(query.get("ended_at"))
        query_string["endedAt"] = ended_at.isoformat()

        if query.get("skip"):
            query_string["skip"] = query.get("skip")

        if query.get("take"):
            query_string["take"] = query.get("take")

        headers = {"Authorization": "Bearer {}".format(model.get_token())}
        full_url = "{}/api/v1/history/{}?{}".format(
            self.url, public_id, urllib.parse.urlencode(query_string))
        response = requests.get(full_url, headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            error = "Failed to classify into klasifikasi-api"
            if response_json.get("error"):
                error = response_json.get("error")
            raise Exception(error)

        return response_json
