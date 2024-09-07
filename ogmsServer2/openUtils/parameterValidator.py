"""
Author: DiChen
Date: 2024-09-07 00:58:14
LastEditors: DiChen
LastEditTime: 2024-09-07 01:07:19
"""

STATUS = ["Model sign"]


class ParameterValidator:
    @staticmethod
    def v_str(param):
        if not isinstance(param, str):
            raise ValueError("Parameter must be a string.")

    @staticmethod
    def v_int(param):
        if not isinstance(param, int):
            raise ValueError("Parameter must be an integer.")

    @staticmethod
    def v_float(param):
        if not isinstance(param, float):
            raise ValueError("Parameter must be a float.")

    @staticmethod
    def v_list(param):
        if not isinstance(param, list):
            raise ValueError("Parameter must be a list.")

    @staticmethod
    def v_dict(param):
        if not isinstance(param, dict):
            raise ValueError("Parameter must be a dictionary.")

    @staticmethod
    def notEmpty(param, name: str):
        try:
            if param is None or param == {} or param == [] or not param.strip():
                if name in STATUS:
                    raise ValueError(f"{name} occurs error, please try again!")
                raise ValueError(f"{name} cannot be empty,plesae check!")
        except ValueError as e:
            print(e)
            exit(1)

    @staticmethod
    def modelStatus
