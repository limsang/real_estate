# -*- coding: utf-8 -*-
import json
import os
from collections import OrderedDict
import sys
import pandas as pd
import time
import matplotlib.pyplot as plt
#todo manage with config.json
fileLocation = "estate_sample_test.json"
# fileLocation = "config.json"

class Calculator(object):

    def __init__(self):
        self._fileLocation = "estate_sample_test.json"
        self._raw = dict()
        self.filtered_data = dict()
        self.readFiles()
        self.calc_()



    def calc_(self):


        # todo 조건값들 config로 관리, None값들 처리 어떻게 할지???
        try:
            for key in self._raw:
                if (self._raw[key]["gin_trade"] < 50000) and (self._raw[key]["house_cnt"] > 0) and (self._raw[key]["gin_rent_per"] > 60) :
                    print(self._raw[key]["bldg_nm"])
        except Exception as e:
            print("calc_ error", e)
            sys.exit()

    def save_as_csv(self):
        try:
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            filename = "/"+ today + "location.tsv"
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
