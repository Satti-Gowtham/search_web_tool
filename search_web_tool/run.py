#!/usr/bin/env python
from dotenv import load_dotenv
from typing import Dict
from naptha_sdk.schemas import ToolRunInput, ToolDeployment
from naptha_sdk.user import sign_consumer_id
from naptha_sdk.utils import get_logger
from search_web_tool.schemas import InputSchema
import os, requests, json

load_dotenv()

logger = get_logger(__name__)

class SearchNewsTool:
    def __init__(self, tool_deployment: ToolDeployment):
        self.tool_deployment = tool_deployment
        self.api_key = os.environ['SERPER_API_KEY']
        self.serper_url = "https://google.serper.dev"

        if self.api_key is None:
            raise ValueError("API key is not set")

    def search_news_tool(self, inputs: InputSchema):
        """Run the module to search news from the prompt using SerperAI API"""
        logger.info(f"Getting news from the prompt: {inputs.query}")

        return self.request_serper(inputs, "news").get("news", [])
    
    def search_web_tool(self, inputs: InputSchema):
        """Run the module to search web from the prompt using SerperAI API"""
        logger.info(f"Getting web results from the prompt: {inputs.query}")

        return self.request_serper(inputs, "search").get("organic", [])

    def request_serper(self, inputs: InputSchema, type: str):
        if not inputs.query:
            raise ValueError("Query cannot be empty")

        # Prepare the payload data
        payload_data = {
            "q": inputs.query
        }

        # Include "gl" only if location is not empty
        if inputs.location:
            payload_data["gl"] = inputs.location

        # Include "tbs" only if date is not empty
        if inputs.date:
            payload_data["tbs"] = f"qdr:{inputs.date}"

        payload = json.dumps(payload_data)

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            f"{self.serper_url}/{type}", 
            headers=headers, 
            data=payload
        )

        return response.json()

def run(module_run: Dict, *args, **kwargs):
    module_run = ToolRunInput(**module_run)
    module_run.inputs = InputSchema(**module_run.inputs)
    search_news_tool = SearchNewsTool(module_run)
    method = getattr(search_news_tool, module_run.inputs.tool_name, None)

    if not method:
        raise ValueError(f"Method {module_run.inputs.tool_name} not found")

    return method(module_run.inputs)


if __name__ == "__main__":
    import asyncio
    from naptha_sdk.client.naptha import Naptha
    from naptha_sdk.configs import setup_module_deployment
    import os

    naptha = Naptha()

    deployment = asyncio.run(setup_module_deployment("tool", "search_web_tool/configs/deployment.json", node_url = os.getenv("NODE_URL")))

    input_params = {
        "tool_name": "search_web_tool",
        "query": "Naptha AI",
    }

    module_run = {
        "inputs": input_params,
        "deployment": deployment,
        "consumer_id": naptha.user.id,
        "signature": sign_consumer_id(naptha.user.id, os.getenv("PRIVATE_KEY"))
    }

    response = run(module_run)

    if input_params["tool_name"] == "search_news_tool":
        for article in response:
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}")
            print(f"Snippet: {article['snippet']}")
            print(f"Source: {article['source']}")
            print(f"Date: {article['date']}")
            print("-" * 50)
    elif input_params["tool_name"] == "search_web_tool":
        for result in response:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print("-" * 50)