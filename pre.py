# -*- coding: utf-8 -*-
# Author = Linda

import pandas as pd


def xls_to_csv():
    data_xls = pd.read_excel('rsc.xls', index_col=0)
    data_xls.to_csv('rsc.csv', encoding='utf-8')

def csv_IE(): #csv information extraction
    csv = pd.read_csv("rsc.csv")
    csv_1 = csv[["准考证号","姓名","语言级别","学号"]]
    csv_1["总成绩"] = None
    csv_1["听力"] = None
    csv_1["阅读"] = None
    csv_1["写作与翻译"] = None
    csv_1.to_csv("rsc_1.csv")

