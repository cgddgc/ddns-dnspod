#!python 3
# -*-coding:utf-8-*-

'''
1. 安装 python3 库
pip3 install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python
pip3 install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python-dnspod

2. linux 加入定时任务:
crontab -e
*/5 * * * * python3 tx_ddns.py

3.自建 nginx 获取本机公网 ip

公网服务器的 nginx 加入下面的配置：

location /getip {
default_type  text/plain;
return        200 $remote_addr;
}

使用脚本或浏览器访问 http://server/getip ，就可以返回本机的公网地址
'''

import json
import urllib.request

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client, models


class dnspod():
    def __init__(self, SecretId, SecretKey):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
            # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
            cred = credential.Credential(secretId, secretKey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            self.client = dnspod_client.DnspodClient(cred, "", clientProfile)
            # 上面有可能是可以公用的
        except TencentCloudSDKException as err:
            print(err)

    def get_ip(self, url=''):
        ip = str(urllib.request.urlopen(url).read(), encoding='utf-8')
        # encoding 修改类型 b'' 为 r''
        # print(ip)
        return ip

    def query_record_List(self, Domain, Subdomain='', keyword='', recordType="A"):
        '''
        :param Domain:
        :param keyword:
        :param recordType:
        :return:RecordList
        '''
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.DescribeRecordListRequest()
            params = {
                "Domain": Domain,
                "Subdomain": Subdomain,
                "RecordType": recordType,
                "Keyword": keyword,
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个DescribeRecordListResponse的实例，与请求对象对应
            resp = self.client.DescribeRecordList(req)
            # 输出json格式的字符串回包
            print((resp.RecordList))
            return resp.RecordList
            # print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)
            return False

    def add_record(self, Domain, SubDomain, Value, recordType="A", recordLine="默认"):
        '''
        :param Domain:
        :param SubDomain:
        :param Value:
        :param recordType:
        :param recordLine:
        :return:
        '''
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.CreateRecordRequest()
            params = {
                "Domain": Domain,
                "SubDomain": SubDomain,
                "Value": Value,
                # value 是记录值
                "RecordType": recordType,
                "RecordLine": recordLine,
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个CreateRecordResponse的实例，与请求对象对应
            resp = self.client.CreateRecord(req)
            # 输出json格式的字符串回包
            print("添加1条记录，子域名是：",SubDomain ,"记录值是：",Value,resp.to_json_string())
        except TencentCloudSDKException as err:
            print(err)

    def modify_record(self, Domain, SubDomain, Value, RecordId: int, RecordType="A", RecordLine="默认"):
        '''
        修改1个解析记录
        :param domain:
        :param subdomain:
        :param value:
        :param recordType:
        :param recordLine:
        :return:
        '''
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.ModifyRecordRequest()
            params = {
                "Domain": Domain,
                "SubDomain": SubDomain,
                "Value": Value,
                "RecordId": RecordId,
                "RecordType": RecordType,
                "RecordLine": RecordLine,
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个ModifyRecordResponse的实例，与请求对象对应
            resp = self.client.ModifyRecord(req)
            # 输出json格式的字符串回包
            print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)

    def modify_record_batch(self, RecordIdList: list, Change: str, ChangeTo: str):
        '''
        批量修改域名解析
        :param RecordIdList:要修改的 recordid 的列表，比如 [1233530942, 975621755]
        :param Change: 要修改的字段，可选值为 [“sub_domain”、”record_type”、”area”、”value”、”mx”、”ttl”、”status”] 中的某一个。
        :param ChangeTo: 修改为，具体依赖 change 字段，必填参数。
        :return:
        '''

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ModifyRecordBatchRequest()
        params = {
            "RecordIdList": RecordIdList,
            "Change": Change,
            "ChangeTo": ChangeTo
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ModifyRecordBatchResponse的实例，与请求对象对应
        resp = self.client.ModifyRecordBatch(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())


if __name__ == '__main__':

    # 腾讯云->访问管理->API密钥管理，新建密钥，获取 SecretId 和 secretKey
    secretId = ''
    secretKey = ''

    # 要操作的域名，例如 domain = 'baidu.com'
    domain = ''

    # 二级域名列表
    subdomains = ['s1', 's2', ]

    # 可以获取本地公网 ip 的 url
    getip_url = 'http://server/getip'

    r = dnspod(secretId, secretKey)
    # 下面是以修改单条记录的方式更新 ip
    ip = r.get_ip(url=getip_url)
    for subdomain in subdomains:
        record_info = r.query_record_List(Domain=domain, Subdomain=subdomain)
        # [{"RecordId": 1233530942, "Value": "8.8.8.8", "Status": "ENABLE", "UpdatedOn": "2022-10-31 12:00:28", "Name": "qqq", "Line": "默认", "LineId": "0", "Type": "A", "Weight": null, "MonitorStatus": "", "Remark": "", "TTL": 600, "MX": 0}]
        if record_info:
            if record_info[0].Value == ip:
                print("ip没变，不用更新")
            else:
                r.modify_record(Domain=domain, SubDomain=subdomain, Value=ip, RecordId=record_info[0].RecordId)
                print("ip更新了", ip)
        else:
            r.add_record(Domain=domain, SubDomain=subdomain, Value=ip)

    # # 使用举例：
    # r = dnspod(secretId, secretKey)

    # r.query_record_List(Domain=domain)
    # r.query_record_List(Domain=domain,Subdomain='qqq')
    # r.query_record_List(Domain=domain,keyword='qqq')
    # r.add_record(Domain=domain,SubDomain='qqq',Value=r.get_ip())
    # r.modify_record(Domain=domain,SubDomain='dm',Value=r.get_ip(),RecordId='1233530942')
    # r.modify_record_batch(RecordIdList=[1233530942, 975621755],Change='value',ChangeTo='8.8.8.8')
