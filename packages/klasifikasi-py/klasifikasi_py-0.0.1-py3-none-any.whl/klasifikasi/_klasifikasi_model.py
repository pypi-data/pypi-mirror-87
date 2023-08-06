import arrow
import requests


class KlasifikasiModel:
    def __init__(self, client_id, client_secret, url):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.__token, expired_after = self.request_token()
        self.__expired_after = arrow.get(expired_after)
        self.public_id, self.name, self.tag = self.request_model_data()

    def request_token(self):
        payload = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }
        response = requests.post("{}/api/v1/auth/token".format(self.url),
                                 json=payload)
        response_json = response.json()
        auth = response_json.get("auth")

        if response.status_code != 200 or auth is None:
            error = "Failed to request token for {}".format(self.client_id)
            if response_json.get("error"):
                error = response_json.get("error")
            raise Exception(error)

        return auth.get("token"), auth.get("expiredAfter")

    def request_model_data(self):
        headers = {"Authorization": "Bearer {}".format(self.__token)}
        response = requests.get("{}/api/v1/auth/activeClient".format(self.url),
                                headers=headers)
        response_json = response.json()
        model = response_json.get("model")

        if response.status_code != 200 or model is None:
            error = "Failed to get model data for {}".format(self.client_id)
            if response_json.get("error"):
                error = response_json.get("error")
            raise Exception(error)

        tags = []
        for data in model.get("tags"):
            tags.append({
                "name": data.get("name"),
                "description": data.get("description"),
                "description_weight": data.get("description_weight"),
            })

        return model.get("publicId"), model.get("name"), tags

    def get_token(self):
        if self.__expired_after < arrow.utcnow():
            self.__token, expired_after = self.request_token()
            self.__expired_after = arrow.get(expired_after)
        return self.__token
