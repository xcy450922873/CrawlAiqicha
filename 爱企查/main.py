import json
import re
import time

import requests

from utils import save_file, open_file
from db_utils import *

db = CompanyMessage()


class AiQiCHa:
    def __init__(self):
        self.search_message = ""
        self.pid = "57326131141273"
        self.detail_url = "https://aiqicha.baidu.com/company_detail_{0}"
        self.search_url = "https://aiqicha.baidu.com/s?"
        self.search_other_url = "https://aiqicha.baidu.com/s/advanceFilterAjax"
        self.all_search_url = ""
        self.cookies = '填写登录后的cookies'
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,zh-HK;q=0.8",
            "cache-control": "no-cache", "Host": "aiqicha.baidu.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "cookie": self.cookies
        }


def get_detail_message(self):
    resp = requests.get(self.detail_url.format(self.pid), headers=self.headers)
    if resp.status_code == 200:
        save_file("{0}.html".format(self.pid), resp.text)
        result = re.search('window.pageData = (.*?);', resp.text)[1]
        save_file("阿里巴巴.json", result)
        result_json = json.loads(result)
        print(result_json["result"])


def get_search_message(self, search_message):
    self.search_message = search_message
    search_params = {
        "q": self.search_message,
        "t": 0
    }
    resp = requests.get(url=self.search_url, params=search_params, headers=self.headers)
    self.all_search_url = resp.url
    save_file("{0}/search_{0}.html".format(self.search_message), resp.text)
    result = re.search('window.pageData = (.*?);\n', resp.text)[1]
    save_file("{0}/{0}.json".format(self.search_message), result)
    result_json = json.loads(result)
    company_result = result_json['result']

    for i in company_result['resultList']:
        print(i["pid"], i['titleName'], i['entType'], i['validityFrom'], i['domicile'], i['openStatus'],
              i['legalPerson'],
              i["regCap"], i['scope'], i['regNo'], i["email"], i['telephone'])
        result = db.commit("select count(aiqicha_pid) from company where aiqicha_pid = {0}".format(i['pid']),
                           return_type="one")
        if result[0] == 0:
            print(i["pid"], i['titleName'], i['entType'], i['validityFrom'], i['domicile'], i['openStatus'],
                  i['legalPerson'],
                  i["regCap"], i['scope'], i['regNo'], i["email"], i['telephone'])
            print(i["titleName"])
            CompanyMessage().executeWithParams(
                "insert into company (aiqicha_pid,entName,entType,startDate,addr,openStatus,legalPerson,regCapital,scope,unifiedCode,email,telephone) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    i["pid"], i['titleName'], i['entType'], i['validityFrom'], i['domicile'], i['openStatus'],
                    i['legalPerson'],
                    i["regCap"], i['scope'], i['regNo'], i["email"], i['telephone']))
        else:
            print(i['pid'], 'exist')


def search_others_message(self, search_message="", start_num=2, end_num=50, all_search_url=""):
    if search_message != "":
        self.search_message = search_message
    if all_search_url != "":
        self.all_search_url = all_search_url
    for i in range(start_num, end_num):
        params = {
            'q': self.search_message,
            't': '',
            'p': i,
            's': 10,
            'o': 0,
            'f': '{}'
        }
        print(params)
        print(self.search_message, self.all_search_url)
        self.headers["referer"] = self.all_search_url
        resp = requests.get(self.search_other_url, params=params, headers=self.headers)
        if resp.status_code == 200:
            save_file('{0}/search_{0}_{1}.json'.format(self.search_message, i), resp.content.decode('utf-8'))
        else:
            print('错误信息', resp.status_code, resp.text)
        json_message = json.loads(resp.text)
        company_result = json_message['data']

        for i in company_result['resultList']:
            # print(i)
            print(i["pid"], i['titleName'], i['entType'], i['validityFrom'], i['domicile'], i['openStatus'],
                  i['legalPerson'],
                  i["regCap"], i['scope'], i['regNo'], i["email"], i['telephone'])
            result = db.commit("select count(aiqicha_pid) from company where aiqicha_pid = {0}".format(i['pid']),
                               return_type="one")
            if result[0] == 0:
                CompanyMessage().executeWithParams(
                    "insert into company (aiqicha_pid,entName,entType,startDate,addr,openStatus,legalPerson,regCapital,scope,unifiedCode,email,telephone) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        i["pid"], i['titleName'], i['entType'], i['validityFrom'], i['domicile'], i['openStatus'],
                        i['legalPerson'],
                        i["regCap"], i['scope'], i['regNo'], i["email"], i['telephone']))
            else:
                print(i['pid'], 'exist')
        time.sleep(60)



if __name__ == '__main__':
    #     # AiQiCHa().get_search_message("杭州")
    AiQiCHa().search_others_message(search_message="杭州",
                                    all_search_url="https://aiqicha.baidu.com/s?q=%E6%9D%AD%E5%B7%9E&t=0", start_num=6,
                                    end_num=51
                                    )
