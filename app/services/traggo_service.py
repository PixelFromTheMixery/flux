import json


from ..models.data_models import NewDoc, UpsertRequest
from ..models.traggo_models import TagUpsert
from ..utils.api_tools import APIRequest, make_call
from ..utils.logger import logger


class TraggoService:
    def __init__(self, traggo_url: str, key: str):
        self.url = traggo_url
        self.key = key

    async def prefilled_request_model(self, info: str, payload: dict):
        request = APIRequest(
            target="traggo",
            category="post",
            url=self.url,
            info=info,
            auth_token=self.key,
            payload=payload,
        )
        return make_call(request)

    def query_builder(self, table: str, args: str, columns: list[str]):
        return {"query": f"{{{table}({args}){{{','.join(columns)}}}}}"}

    def payload_builder(
        self,
        action: str,
        modifiers: dict,
        fields: list[str],
        payload_type: str = "mutation",
    ):
        args = ",".join([f"{k}: {json.dumps(v)}" for k, v in modifiers.items()])

        fields = ",".join(fields if fields else modifiers.keys())

        result = f"{payload_type} {{ {action} ({args}) {{ {fields} }} }}"

        return {"query": result}

    async def connection_check(self) -> dict:

        payload = {"query": self.query_builder("version", "", ["name"])}

        result = await self.prefilled_request_model("check version", payload)

        return result["data"]

    async def search_for_tag(self, tag_key: str):
        existing_tag = None
        found = False

        payload = self.query_builder("suggestTag", 'query: "test"', ["key", "color"])

        result = await self.prefilled_request_model(
            f"filtered tag list for {tag_key}", payload
        )
        if "errors" in result:
            logger.error(result["errors"])
            return result
        tags = result["data"]["suggestTag"]
        for tag in tags:
            if tag["key"] == tag_key:
                found = True
                existing_tag = tag
        logger.info("Tag %s%sfound", tag_key, " not " if not found else " ")
        return existing_tag

    async def get_tags(self) -> dict:
        payload = self.query_builder("tags", "", ["key", "color"])
        result = await self.prefilled_request_model("basic tag fetch", payload)
        return result

    async def upsert_tag(self, tag: TagUpsert) -> dict:
        formatted_key = tag.name.lower().replace(" ", "-")

        existing_tag = await self.search_for_tag(
            tag.old_name if tag.old_name else tag.name
        )

        traggo_action = ""
        if existing_tag:
            tag.color = existing_tag["color"]
            tag.old_name = existing_tag["key"]
            traggo_action = "Updated"

            payload = self.payload_builder(
                "updateTag",
                {"key": tag.old_name, "newKey": formatted_key, "color": tag.color},
                ["key", "color"],
            )
            result = await self.prefilled_request_model(
                f"update tag: {tag.old_name} to {formatted_key}", payload
            )

        else:
            traggo_action = "Created"
            payload = self.payload_builder(
                "createTag",
                {"key": formatted_key, "color": tag.color},
                ["key", "color"],
            )
            result = await self.prefilled_request_model(
                f"create tag: {formatted_key}", payload
            )

        return {traggo_action: result["data"]}
