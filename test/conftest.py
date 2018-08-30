import json

import pytest


def load_js(fname):
    with open(fname) as fl:
        _js = json.load(fl)
    return _js


@pytest.fixture
def parsed_account_data():
    # return load_js("output/out.json")
    return {
        "2018": {
            "04": {
                "20": [
                    {
                        "account": "NL49INGB0004568299",
                        "amount": 57.9,
                        "other": "NL53RABO0126644401",
                        "desc": "IG Online B.V.",
                    },
                    {
                        "account": "NL49INGB0004568333",
                        "amount": -1.6,
                        "other": "",
                        "desc": "BAX DEFG",
                    },
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -5.67,
                        "other": "NL304RIO0254649718",
                        "desc": "Stg. AVS Proefdiervrij",
                        "label": "charity",
                    },
                ],
                "19": [
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -89.9,
                        "other": "NL13ABNA3505417344",
                        "desc": "ABO B NV",
                        "label": "charity",
                    },
                    {
                        "account": "NL49INGB0004568333",
                        "amount": 6557.91,
                        "other": "NL41I7GB0770934444",
                        "desc": "Huuglaope BV",
                    },
                ],
                "17": [
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -1.6,
                        "other": "",
                        "label": "charity",
                        "desc": "BAX DEFG",
                    }
                ],
            },
            "06": {
                "16": [
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -2000.0,
                        "other": "NL64RABO0144266451",
                        "desc": "KLUSSENBEIAN",
                    },
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -1.6,
                        "other": "",
                        "desc": "BAX DEFG",
                        "label": "charity",
                    },
                    {
                        "account": "NL49INGB0004568333",
                        "amount": -88.52,
                        "other": "NL77RABO0175882910",
                        "desc": "Landal Greenparks",
                    },
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -39.99,
                        "other": "",
                        "desc": "Praxn 068 WIEN NLD",
                    },
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -18.49,
                        "other": "",
                        "desc": "KruiMEGEN NLD",
                        "label": "charity",
                    },
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -18.26,
                        "other": "",
                        "desc": "Albeijn 1514 NIJME",
                    },
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -0.47,
                        "other": "",
                        "desc": "Toolstation AJ ",
                    },
                ]
            },
        },
        "2016": {
            "01": {
                "04": [
                    {
                        "account": "NL49INGB0004568299",
                        "amount": -75.0,
                        "other": "NL85INGB0784830563",
                        "desc": "Cverzekeraar",
                        "label": "taxes",
                    }
                ]
            }
        },
    }



