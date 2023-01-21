# -*- coding: utf-8 -*

import requests
from lxml import etree
import urllib.parse
import json
from flask import Flask, request, Response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#01.取得cmkey
def getAllCmkeyHtml(co_id):
    url = 'https://www.cmoney.tw/finance/f00025.aspx?s=' + co_id
    encoding = 'utf8'
    r = requests.get(url)
    response_html = r.content.decode(encoding)
    return response_html

def GetAspxFromCmkind(cmkind):
    # aspx = "f000" + cmkind + ".aspx"   # f00029.aspx, f00041.aspx, f00042.aspx, ...
    aspx = "f000" + cmkind
    return aspx

def GetCmkeyFromHtml(co_id, response_html, cmkind):
    html = etree.HTML(response_html)
    #f = open('/home/hcc/桌面/web/response_html.html', 'w')
    #f.write(response_html)
    #f.close()
    aspx = GetAspxFromCmkind(cmkind)
    print('//a[contains(@href, "/finance/' + co_id + '/' + aspx + '")]//@cmkey')
    cmkey = urllib.parse.quote(html.xpath('//a[contains(@href, "/finance/' + co_id + '/' + aspx + '")]//@cmkey')[0]).replace('/','%2F')
    return cmkey

def GetCmkeyArray(co_id, cmkind):
    cmkey_html = getAllCmkeyHtml(co_id)
    #f = open('/home/hcc/桌面/web/cmkey.html', 'w')
    #f.write(cmkey_html)
    #f.close()
    cmkey = []
    for k in cmkind:
        cmkey.append( GetCmkeyFromHtml(co_id, cmkey_html, k) )
    return cmkey

'''測試01.===================================================
cmkey_html = getAllCmkeyHtml('9940')
cmkey = GetCmkeyFromHtml(cmkey_html, '43')
print(cmkey)
'''#=========================================================

#02.取得Cmoney網站回傳的json

def GetActionFromCmkind(cmkind):
    action = ''
    if(cmkind=='29'): #營收盈餘
        action = 'GetStockRevenueSurplus'
    elif(cmkind=='41'):
        action = 'GetIncomeStatement'
    elif(cmkind=='42'):
        action = 'GetCashFlowStatement'
    elif(cmkind=='43'):
        action = 'GetFinancialRatios'
    else:
        action = ''    
    return action

def GetSelectedTypeFromCmkind(cmkind):
    selectedType = ''
    if(cmkind=='29'):
        selectedType = '3'
    elif(cmkind=='41'):
        selectedType = '5'
    elif(cmkind=='42'):
        selectedType = '3'
    elif(cmkind=='43'):
        selectedType = '4'
    else:
        selectedType = ''    
    return selectedType

def GetCmkindJson(co_id, encoding, cmkind, cmkey):
    aspx = GetAspxFromCmkind(cmkind)
    action = GetActionFromCmkind(cmkind)
    selectedType = GetSelectedTypeFromCmkind(cmkind)
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01'
    ,'Accept-Encoding': 'gzip, deflate, br'
    ,'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7'
    ,'Connection': 'keep-alive'
    ,'Cookie': 'ASP.NET_SessionId=ctqssvvtzai0p2kvjcpnhotq; AspSession=mdvoozzev42b31uusx4vvrhy; __asc=4e8696f916c48e61e66f1408c15; __auc=4e8696f916c48e61e66f1408c15; _ga=GA1.2.1802863723.1564591137; _gid=GA1.2.1011884324.1564591137; _gat_UA-30929682-16=1; _gat_UA-30929682-1=1; _gat_UA-30929682-32=1; _fbp=fb.1.1564591136626.1652837942; _hjid=15034f6b-0e42-4286-ac6f-c6d93d8113eb; _gat_UA-30929682-4=1; _gat_real=1; __gads=ID=ea2ab717523664f1:T=1564591149:S=ALNI_MYoFW3-TT75mzfm4InsdSziwLwFwA'
    ,'Host': 'www.cmoney.tw'
    ,'Referer': 'https://www.cmoney.tw/finance/' + aspx + '?s=' + co_id
    ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    ,'X-Requested-With': 'XMLHttpRequest'
    }
    getstring = 'http://www.cmoney.tw/finance/ashx/mainpage.ashx?action=' + action + '&stockId=' + co_id + '&selectedType=' + selectedType + '&cmkey=' + cmkey
    response_json = requests.get(getstring, headers = headers)
    response_json.encoding = encoding
    response_json = response_json.content.decode(encoding)
    return response_json

def ParseJson(data, datacnt,json_key1,json_key2,title,denominator):
    ret = {}
    j = json.loads(data)    
    idx = 0
    for r in j:	
        idx = idx + 1
        if idx > datacnt:
            return ret
        try:
            ret[r[json_key1]] = round(float(r[json_key2])/denominator,2)
        except:
            ret[r[json_key1]] =  float('nan')

@app.route('/sixidx', methods=['POST'])
def sixidx():
    encoding = 'utf8'
    cmkind = ['29','41','42','43']
    cmoney_jsonArray = []
    ret = {}

    try:
        dataDict = request.get_json()
        co_id = dataDict["co_id"]
        cmkey = GetCmkeyArray(co_id, cmkind)
        
        for i in range(0,len(cmkind)):
            cmoney_jsonArray.append( GetCmkindJson(co_id,encoding,cmkind[i],cmkey[i]) )
    
        json1 = ParseJson(cmoney_jsonArray[3], 4,'DateRange', 'OperatingProfitMargin', u'營業利益率',1)
        json2 = ParseJson(cmoney_jsonArray[0], 6,'Date', 'MonthlyRevenueYearGrowth', u'營收單月年增率',1)
        json3 = ParseJson(cmoney_jsonArray[3], 4,'DateRange', 'EPS', u'EPS',1)
        json4 = ParseJson(cmoney_jsonArray[3], 4,'DateRange', 'NetProfitGrowthRatio', u'稅後純益成長率',1)
        json5 = ParseJson(cmoney_jsonArray[2], 4,'DateRange', 'FreeCashFlow', u'自由現金流量(百萬)',1000)
        json6 = ParseJson(cmoney_jsonArray[3], 4,'DateRange', 'InventoryTurnoverRatio', u'存貨週轉率',1)
        
        ret[u'營業利益率'] = json1
        ret[u'營收單月年增率'] = json2
        ret[u'EPS'] = json3
        ret[u'稅後純益成長率'] = json4
        ret[u'自由現金流量(百萬)'] = json5
        ret[u'存貨週轉率'] = json6

    except Exception as e:
        ret = {'error':str(e)}

    print(json.dumps(ret, ensure_ascii=False))
    return Response(json.dumps(ret, ensure_ascii=False),  mimetype='application/json')

if __name__=="__main__":
    #app.run(host='127.0.0.1', debug=True)
    app.run(host='0.0.0.0')


'''
export FLASK_APP=app.py  (linux terminal)
set FLASK_APP=app.py     (windows cmd)

flask run



{
	"co_id":"9940"
}


sudo docker-compose build

sudo docker-compose up
'''