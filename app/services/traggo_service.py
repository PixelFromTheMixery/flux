from ..models.api_models import APIRequest
from ..utils.api_tools import make_call


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

    def query_builder(self, title: str, body: str, variables_definitions: str = ""):
        return {"query": f"query {title} {variables_definitions}{{{body.strip()}}}"}

    def connection_check(self) -> dict:

        payload = self.query_builder(
            "TraggoVersion",
            "version{name}",
        )

        return self.prefilled_request_model("check traggo version", payload)["data"]
