from ..utils.api_tools import APIRequest, make_call


class TraggoService:
    def __init__(self, traggo_url: str, traggo_key: str):
        self.url = traggo_url
        self.key = traggo_key

    def prefilled_request_model(self, info: str, payload: dict):
        request = APIRequest(
            target="traggo",
            category="post",
            url=self.url,
            info=info,
            auth_token=self.key,
            payload=payload,
        )
        return make_call(request)

    def query_builder(self, body: str, variables_definitions: str = ""):
        return {"query": f"query{variables_definitions}{{{body.strip()}}}"}

    def connection_check(self) -> dict:

        payload = {"query": "{ version { name } }"}

        return self.prefilled_request_model("check version", payload)["data"]
