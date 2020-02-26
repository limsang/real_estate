# -*- coding: utf-8 -*-
import json
import os
from collections import OrderedDict
import sys
import pandas as pd
import time
from config import config
import matplotlib.pyplot as plt


class Calculator(object):

    def __init__(self):
        self._fileLocation = config()._json_data["raw_data"]["location"]["성동구"]
        self._raw = dict()
        self.filtered_data = dict()

        self.readFiles()
        self.calc_()
        self.save_as_json("성동구", self._raw)

    """
    key = raw_data
    condition = treating condition of value "null"  
    """
    def filter(self, key, condition):
        # 조건주고 맞으면 True, 아니면 False 리턴하도록
        PRIVATE_EXTENT = config()._json_data["filter_table"]["전용면적"]
        GIN_TRADE_RENT_CAL = config()._json_data["filter_table"]["매전차액"]
        GIN_RENT_PER = config()._json_data["filter_table"]["전세가율"]

        if condition is True:
            if self._raw[key]["private_extent"] is not None and self._raw[key]["gin_trade_rent_cal"] is not None and self._raw[key]["gin_rent_per"] is not None:
                if (self._raw[key]["private_extent"] > PRIVATE_EXTENT) and (self._raw[key]["gin_trade_rent_cal"] < GIN_TRADE_RENT_CAL) and (self._raw[key]["gin_rent_per"] > GIN_RENT_PER):
                    return True
                else:
                    return False
        else:
            return True

    # todo "구" 단위로 mp 사용해서 데이터 처리
    def calc_(self):
        # todo 조건값들 config로 관리, None값들 처리 어떻게 할지???
        try:
            idx = 0
            for key in self._raw:
                if self.filter(key, True):
                    tmp = dict()
                    tmp["total_num_of_family"] = self._raw[key]['total_num_of_family']
                    tmp["gin_trade_flag"] = self._raw[key]['gin_trade_flag']
                    tmp["gin_rent_per"] = self._raw[key]['gin_rent_per']
                    tmp["house_cnt"] = self._raw[key]['house_cnt']
                    tmp["bldg_nm"] = self._raw[key]['bldg_nm']
                    tmp["gin_trade"] = self._raw[key]['gin_trade']
                    tmp["gin_rent_per"] = self._raw[key]['gin_rent_per']
                    tmp["year_diff"] = self._raw[key]['year_diff']
                    tmp["gin_trade_cal"] = self._raw[key]['gin_trade_cal']
                    tmp["unsold_cnt"] = self._raw[key]['unsold_cnt']
                    tmp["gin_rent"] = self._raw[key]['gin_rent']
                    tmp["gin_rent_cal"] = self._raw[key]['gin_rent_cal']
                    self.filtered_data[str(idx)] = tmp
                    idx += 1

        except Exception as e:
            print("calc_ error", e)
            sys.exit()

    def save_as_json(self, location, raw_data):
        try:
            pwd = os.getcwd()
            today = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            filename = "/report/" + today + location + ".json"
            dir = pwd + filename

            with open(dir, 'w', encoding="utf-8") as f:
                json.dump(self.filtered_data, f, ensure_ascii=False, indent="\t")

            # mapogu_table.to_csv(dir, sep='\t', encoding='utf-8')
        except Exception as e:
            print("save_as_json error", e)

    def save_as_csv(self, location):
        try:
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            filename = "/" + today + location + ".tsv"
            pwd = os.getcwd()
            dir = pwd + filename

            ## tsv file로 저장
            # mapogu_table.to_csv(dir, sep='\t', encoding='utf-8')
        except Exception as e:
            print("save_as_csv error", e)

    """
    부동산 지인의 raw data는 크게 데이터와 데이터 config의 리스트로 구성됨
    [0]가 데이터, [1]가 #row를 담고있음, 우린 [0]만 쓴다.
    """
    def readFiles(self):

        try:
            with open(self._fileLocation, 'r') as f:
                json_data = json.load(f)
                json_data = json_data[0]
                for idx, data in enumerate(json_data):
                    tmp = dict()
                    tmp["total_num_of_family"] = data['total_num_of_family']
                    tmp["gin_trade_flag"] = data['gin_trade_flag']
                    tmp["gin_rent_per"] = data['gin_rent_per']
                    tmp["house_cnt"] = data['house_cnt']
                    tmp["gin_rent_flag"] = data['gin_rent_flag']
                    tmp["bldg_nm"] = data['bldg_nm']
                    tmp["gin_trade"] = data['gin_trade']
                    tmp["gin_rent_per"] = data['gin_rent_per']
                    tmp["year_diff"] = data['year_diff']
                    tmp["gin_trade_cal"] = data['gin_trade_cal']
                    tmp["unsold_cnt"] = data['unsold_cnt']
                    tmp["gin_rent"] = data['gin_rent']
                    tmp["gin_rent_cal"] = data['gin_rent_cal']
                    self._raw[str(idx)] = tmp
            return self._raw

        except Exception as e:
            print("readFiles error", e)
            sys.exit()
