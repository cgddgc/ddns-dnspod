#!python 3
#-*-coding:utf-8-*-
import urllib.request, time, json, random, urllib.parse, hmac, base64, binascii, copy
from collections import OrderedDict

class dnspod():
    def __init__(self, SecretId, SecretKey):
        self.reqDomain = 'cns.api.qcloud.com'
        self.reqRoute = '/v2/index.php'
        self.apiUrl = 'https://' + self.reqDomain + self.reqRoute
        self.apiKey = SecretKey     
       
        self.pub = dict({
            'SecretId':SecretId,     
            'SignatureMethod':'HmacSHA1',    #HmacSHA256
            })

    def dictSort(self, data):
        tmp = OrderedDict()
        for d in sorted(data):
            tmp[d] = data[d]
        return tmp

    def sign(self, paramList):
        postParam = self.dictSort(paramList)
        p = urllib.parse.unquote(urllib.parse.urlencode(postParam))
        postStr = 'POST' + self.reqDomain + self.reqRoute + '?' + p
        #print(postStr)
        hashed = hmac.new(self.apiKey.encode(), postStr.encode(), digestmod = 'SHA1')
        signature = binascii.b2a_base64(hashed.digest())[:-1].decode()
        return signature


    def queryDnsList(self, domain):
        dnsList = dict({
            'domain':domain,
            'recordType':'A',
            })

        postData = copy.deepcopy(self.pub)
        postData.update(dnsList)

        postData['Action'] = 'RecordList'
        postData['Timestamp'] = int(time.time())
        postData['Nonce'] = int(random.random() * 100000)
        signature = self.sign(postData)
        postData['Signature'] = signature
        data = urllib.parse.urlencode(postData)
        data = data.encode()
        res = self.sendRequest(data)
        #print(res)
        return res

    def dnsModify(self, recordId,subdomain, ipAddr, domain, recordType = 'A'):
        dnsModify = dict({
            'domain':domain,
            'recordId':recordId,
            'subDomain':subdomain,
            'recordType':recordType,
            'recordLine':'默认',
            'value':ipAddr,
            'ttl':600,
            })

        postData = copy.deepcopy(self.pub)
        postData.update(dnsModify)
        postData['Action'] = 'RecordModify'
        postData['Timestamp'] = int(time.time())
        postData['Nonce'] = int(random.random() * 100000)
        signature = self.sign(postData)
        postData['Signature'] = signature
        data = urllib.parse.urlencode(postData)
        data = data.encode()
        #print(data)
        res = self.sendRequest(data)
        print(res)
        return res

    def addDnsRecord(self, subdomain, ipAddr, domain, recordType = 'A'):
        addRecord = dict({
            'domain':domain,
            'subDomain':subdomain,
            'recordType':recordType,
            'recordLine':'默认',
            'value':ipAddr,
            })

        postData = copy.deepcopy(self.pub)
        postData.update(addRecord)
        postData['Action'] = 'RecordCreate'
        postData['Timestamp'] = int(time.time())
        postData['Nonce'] = int(random.random() * 100000)
        signature = self.sign(postData)
        postData['Signature'] = signature
        data = urllib.parse.urlencode(postData)
        data = data.encode()
        #print(data)
        res = self.sendRequest(data)
        print(res)
        return res


    def getMyIp(self):
        n = 3
        myIp = None
        apiUrl = 'http://ip.taobao.com/service/getIpInfo.php?ip=myip'
        while n:
            try:
                res = urllib.request.urlopen(apiUrl)
                myIp = json.loads(res.read().decode())['data']['ip']
                break
            except Exception as e:
                n -= 1
        #print(myIp)
        return myIp

    def sendRequest(self, data):
        n = 3   #重试次数
        #headers = {'Content-Type':'application/x-www-form-urlencoded'}
        #proxies = {'http':'http:127.0.0.1:8080', 'https':'127.0.0.1:8080'}
        req = urllib.request.Request(url = self.apiUrl, data = data)
        #opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies = proxies))
        result = None
        while n:
            try:
                res = urllib.request.urlopen(req)
                #res = opener.open(req)
                result = json.loads(res.read().decode())
                break
            except Exception as e:
                n -= 1
        return result

    def getByName(self, records, name):
        a = []
        for r in records:
            if r['name'] == name:
                a.append(r)
        return a


if __name__ == '__main__':

    secretId = '{{your SecretId}}'
    secretKey = '{{your SecretKey}}'
    domain = 'your domain'
    subdomains = ['www', 'test', 'test1']
    app = dnspod(SecretId = secretId, SecretKey = secretKey)

    ip = app.getMyIp()
    result = app.queryDnsList(domain)
    records = result['data']['records']
    for subdomain in subdomains:
        ids = app.getByName(records, subdomain)
        
        if ids:
            for i in ids:
                app.dnsModify(i['id'], subdomain, ip, domain)
            print('%s modified'%(subdomain + '.' +domain))
        else:
            app.addDnsRecord(subdomain, ip, domain)
            print('%s created'%(subdomain + '.' +domain))

    


