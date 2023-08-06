import pandas as pd
import numpy as np
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
import asyncio, nest_asyncio
from concurrent import futures
import re


nest_asyncio.apply()
warnings.filterwarnings("ignore")


class KnnMiss(object):
    def __init__(self, datas):
        self.datas = datas
        
    def get_miss(self):
        result = []
        miss_val = 0
        for data in self.datas:
            miss_data = self.datas[data].isnull()
            for i in miss_data:
                if i:
                    miss_val += 1
            print(f"{data}缺失{miss_val}个值！",end="")
            if miss_val:
                result.append(data)
            miss_val = 0
        if result is []:
            print("无缺失值！")

        return result

    def knn(self, miss_val):
        na_index=self.datas[self.datas[miss_val].isnull()].index.values
        normal_index = self.datas[~self.datas[miss_val].isnull()].index.values
        train_x = self.datas.iloc[normal_index]
        train_y = self.datas.iloc[normal_index,10]
        test_x = self.datas.iloc[na_index]
        test_y = self.datas.iloc[na_index,10]
        list(enumerate(train_x.iloc[:,2:3].values))
        distances = []
        for item in test_x.iloc[:,2:3].values: 
            dist = {}
            for index, item1 in enumerate(train_x.iloc[:,2:3].values):  
                distance = np.sqrt(np.sum(np.square(item - item1)))  
                dist[index] = distance 
            distances.append(dist)

        sorted_list = [sorted(item.items(), key = lambda x: x[1])[0:15] for item in distances]
        index_list =  [list(zip(*item_list))[0] for item_list in sorted_list]

        predict_var= {}
        for item in zip(na_index, index_list):
            predict_var[item[0]] = train_y.iloc[list(item[1])].mode()[0]

        self.datas[miss_val].fillna(predict_var,inplace=True)
    

    def deal_knn(self, miss_vals = None):
        miss_vals = self.get_miss()
        for miss_val in miss_vals:
            self.knn(miss_val)
        print(self.datas[1:11])    
        
        


def deal_char_attr(char_attr: str, data: object, atr_val: str) -> str:
    data_list = list((data[atr_val].values))
    abno_index = []
    for i,val in enumerate(data_list):
        is_mxbc = re.findall(string=val, pattern=char_attr)
        if (is_mxbc == []):
            abno_index.append(i)
    if abno_index == []:
        print("\033[1;32m无异常值！\033[0m")
    else:
        print("\033[1;31m含有异常值！\033[0m")
        print("abno_index：", abno_index)
        data.drop(index=abno_index, inplace=True)


def layida_deal(dataset, attr_val: str=None, is_inplace=True, is_return=False, char_attr: str=None) -> all:
    if char_attr:
        deal_char_attr(char_attr=char_attr, data=dataset, atr_val=attr_val)

    else:
        left = int( dataset[attr_val].mean()-3 * dataset[attr_val].std() )
        right = int( dataset[attr_val].mean()+3 * dataset[attr_val].std() )
        abno_index = []
        for i, val in enumerate( list( dataset[attr_val].values) ):
            if val > right or val < left:
                abno_index.append(i)
        if is_inplace:
            deal_data = dataset.drop(index=abno_index, inplace=False)
            dataset.drop(index=abno_index, inplace=True)
            print("\033[1;31m含有异常值！\033[0m")
            print("abno_index：", abno_index)
            return abno_index, deal_data.reset_index(drop=True)
        else:
            return dataset.drop(index=abno_index, inplace=False)


class AbnoDeal(object):
    def __init__(self, dataset: object):
        self.dataset = dataset

    def layida(self, attr_val: str or tuple or list, is_singer: bool=False, is_inplace=True, char_attr: str=None) -> all:
        if isinstance(attr_val, str):
            if is_inplace:
                if char_attr:
                    layida_deal(dataset=self.dataset, attr_val=attr_val, is_inplace=is_inplace, char_attr=char_attr)
                else:
                    layida_deal(dataset=self.dataset, attr_val=attr_val, is_inplace=is_inplace)
            else:
                return layida_deal(dataset=self.dataset, attr_val=attr_val, is_inplace=is_inplace)
        else:
            abno_index = []
            extend_data = []
            for i, val in enumerate(attr_val):
                if not isinstance(list(self.dataset[val])[0], str or list):
                    if i == 0:
                        extend_data = layida_deal(self.dataset, attr_val=val, is_inplace=True, is_return=True)[1]
                    else:
                        extend_data = layida_deal(extend_data, attr_val=val, is_inplace=True, is_return=True)[1]
            return extend_data
                    
            drop_compli = set(abno_index)
            if abno_index != []:
                print("\033[1;31m含有异常值！\033[0m")
                print("abno_index：", list(drop_compli))
            else:
                print("\033[1;32m无异常值！\033[0m")






# This is a example !
# if __name__ == "__main__":

#     datas = pd.read_csv("filepath")
#     knn = KnnMiss(datas)
#     knn.deal_knn()

