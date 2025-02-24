#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @IDE       :PyCharm
# @Project   :apikey_query
# @FileName  :QueryCost.py
# @Time      :2025/2/24 15:03
# @Author    :Hacon


import os
import yaml

from .tools import load_yaml


class QueryCost:
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_type = load_yaml(os.path.join(project_root, "model_type.yaml"))
    model_info = load_yaml(os.path.join(project_root, "model_info.yaml"))
    unit = model_info["unit"]

    def __init__(self):
        self.input_token = []
        self.output_token = []
        self.cost = []
        self.input_token_sum = 0
        self.output_token_sum = 0
        self.cost_sum = 0

    @classmethod
    def get_model_type(cls, response) -> str:
        """ Get type of model by response.
        :param response: Return body from LLM
        :return: True or False
        """
        r_type = str(type(response)).split("'")[-2].split(".")[-1]
        if r_type not in QueryCost.model_type:
            raise RuntimeError(f"Unable to process return body of type {r_type}. Please expand the model list.")

        model_type = QueryCost.model_type[r_type]
        if model_type not in QueryCost.model_info:
            raise RuntimeError(f"No model list for {model_type} was found. Please expand the model list.")
        return model_type

    @classmethod
    def get_model_name(cls, response) -> str:
        """ Get name of specific model by response.
        :param response: Return body from LLM
        :return: True or False
        """
        model_type = QueryCost.get_model_type(response)
        model_name = None
        if model_type in ["OpenAIChat", "OpenAIEmbeddings"]:
            model_name = response.model
        elif model_type in ["GoogleGemini"]:
            model_name = response.model_version
        if not model_name:
            raise RuntimeError(
                f"Unable to find the specific {model_type} model name from the return body. Please update the code.")

        if model_name not in QueryCost.model_info[model_type]:
            raise RuntimeError(f"No model named {model_name} was found. Please expand the model list.")

        return model_name

    @classmethod
    def get_input_token(cls, response) -> int:
        """
        Get the num of input tokens by response.
        :param response: Return body from LLM
        :return: The num of input tokens
        """
        model_type = QueryCost.get_model_type(response)
        try:
            if model_type in ["OpenAIChat", "OpenAIEmbeddings"]:
                return response.usage.prompt_tokens
            elif model_type in ["GoogleGemini"]:
                return response.usage_metadata.prompt_token_count
        except Exception as e:
            print(f"Error. {e}")
        raise RuntimeError(
            f"Unable to count the input tokens of {model_type} from the return body. Please update the code.")

    @classmethod
    def get_output_token(cls, response) -> int:
        """
        Get the num of output tokens by response.
        :param response: Return body from LLM
        :return: The num of output tokens
        """
        model_type = QueryCost.get_model_type(response)
        try:
            if model_type in ["OpenAIChat", "OpenAIEmbeddings"]:
                return response.usage.completion_tokens
            elif model_type in ["GoogleGemini"]:
                return response.usage_metadata.candidates_token_count
        except Exception as e:
            print(f"Error. {e}")
        raise RuntimeError(
            f"Unable to count the output tokens of {model_type} from the return body. Please update the code.")

    @classmethod
    def get_cost_one(cls, response) -> dict:
        """
        Calculate input token, output token and cost from one response
        :param response: Return body from LLM
        :return: Input token, output token and cost
        """
        model_type = QueryCost.get_model_type(response)
        model_name = QueryCost.get_model_name(response)
        input_token = QueryCost.get_input_token(response)
        output_token = QueryCost.get_output_token(response)
        input_price = QueryCost.model_info[model_type][model_name]["input"]
        output_price = QueryCost.model_info[model_type][model_name]["output"]

        cost = input_token * input_price / QueryCost.unit + output_token * output_price / QueryCost.unit
        result = {"input_token": input_token, "output_token": output_token, "cost": cost}
        return result

    def get_cost(self, *args) -> dict:
        """
        Calculate input token, output token and cost from responses
        :param args: one response, multi responses or response list
        :return: Input token, output token and cost in sum
        """
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        responses = args
        # print(responses)
        for r in responses:
            result = QueryCost.get_cost_one(r)
            self.input_token.append(result["input_token"])
            self.output_token.append(result["output_token"])
            self.cost.append(result["cost"])
        self.input_token_sum = sum(self.input_token)
        self.output_token_sum = sum(self.output_token)
        self.cost_sum = sum(self.cost)
        result = {"input_token": self.input_token_sum, "output_token": self.output_token_sum, "cost": self.cost_sum}
        return result

    def clear(self):
        """
        Clear old data
        :return: None
        """
        self.input_token = []
        self.output_token = []
        self.cost = []
        self.input_token_sum = 0
        self.output_token_sum = 0
        self.cost_sum = 0
