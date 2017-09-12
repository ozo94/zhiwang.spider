# coding=utf-8
import urllib
from urlparse import urljoin

import requests
from PIL import Image
from scrapy import Spider
from scrapy.http import Request

from captcha_recognition.recognition_img import distinguish_captcha
from zhiwangspider.items import ZhiwangspiderItem

# 第二次跳转
# http://kns.cnki.net/kns/brief/brief.aspx?
formdata1=urllib.urlencode({
    't':'1488268898493',
    'S':'1',
    'research':'off',
    'pagename':'ASP.brief_result_aspx',
    'dbPrefix':'CJFQ',
    'dbCatalog':'中国学术期刊网络出版总库',
    'ConfigFile':'CJFQ.xml'
})

# 第三次跳转 结果页面
# http://kns.cnki.net/kns/brief/result.aspx?
formdata2=urllib.urlencode(
    {
        'pagename':'ASP.brief_result_aspx',
        'dbPrefix':'CJFQ',
        'dbCatalog':'中国学术期刊网络出版总库',
        'ConfigFile':'CJFQ.xml',
        'research':'off',
        'recordsperpage':'50',
        't':'1488184668147',
        'S':'1',
        'queryid':'5',
        'skuakuid':'5',
        'turnpage':'1',
        'keyValue':''
    }
)





class zwspider(Spider):
    name = 'zw'
    allowed_domains = []
    start_urls = ['http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'kns.cnki.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
    }

    # cookies是存在时间限制的，可以尝试使用动态获取cookie的方式
    cookies = {
        'Ecp_ClientId': '1170508144702006262',
        'cnkiUserKey': '35b8f401-5acc-d2ad-1b1a-bc71854695ba',
        'RsPerPage': '50',
        'ASP.NET_SessionId': 'tgz0kchpbtr4ujwxzdupkc4r',
        'Ecp_IpLoginFail': '17052258.211.96.227',
        'SID_kns': '123118',
        'SID_klogin': '125141',
        'SID_kinfo': '125102',
        'SID_kredi': '125144',
        'SID_krsnew' : '125132',
    }

    def __init__(self, query='', time=''):
        # 第一次链接
        # http://kns.cnki.net/kns/request/SearchHandler.ashx?

        # magazine_special1, '=' -> 精确搜索, '%' -> 模糊搜索
        self.formdata = urllib.urlencode(
            {'magazine_value1': '计算机学报',
             'year_from': '2010',
             'year_to': '2016',
             'NaviCode': '*',
             'ua': '1.21',
             'PageName': 'ASP.brief_result_aspx',
             'DbPrefix': 'CJFQ',
             'DbCatalog': '中国学术期刊网络出版总库',
             'ConfigFile': 'CJFQ.xml', 'db_opt': 'CJFQ',
             'db_value': '中国学术期刊网络出版总库',
             'magazine_special1': '=',
             'year_type': 'echar',
             'his': '0',
             '__': 'Mon Feb 27 2017 16:37:42 GMT+0800 (中国标准时间)',
             'action': ''
             })

    # 处理response，并返回处理的数以及跟进的url,但是在response 没有指定函数的情况下的默认处理方法
    def parse(self, response):
        return Request("http://kns.cnki.net//kns/request/SearchHandler.ashx?"+self.formdata,
                       headers=self.headers,
                       cookies=self.cookies,
                       callback=self.Search1
                       )

    def Search1(self,response):
        filename = 'tmp_htmls/search1.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        return Request("http://kns.cnki.net/kns/brief/brief.aspx?"+formdata1,
                       headers=self.headers,
                       cookies=self.cookies,
                       callback=self.Search2
                       )

    def Search2(self,response):
        filename = 'tmp_htmls/search2.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        return Request("http://kns.cnki.net/kns/brief/brief.aspx?"+formdata2,
                       headers=self.headers,
                       cookies=self.cookies,
                       callback=self.Search3)


    def Search3(self,response):
        filename = 'tmp_htmls/result.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        if 'CheckCodeImg' in response.body:
            print 'need check code!'

            # 带cookie获取验证码图片，防止下载时图片的刷新，影响识别
            img = requests.get('http://kns.cnki.net/kns/checkcode.aspx?t=%27+Math.random()',
                               stream=True,
                               headers=self.headers ,
                               cookies = self.cookies)
            code_path = 'tmp_code_img/code.gif'
            with open(code_path, 'wb') as f:
                f.write(img.content)
            img = Image.open(code_path)
            img.show()
            checkcode = distinguish_captcha(img)
            print 'checkcode',checkcode

            # 获取验证码的跳转地址
            rurl = response.url.split('rurl=')[1].split('&vericode')[0]
            veriform = 'rurl=' + rurl + '&vericode=' + checkcode
            print 'response.url', response.url
            print 'rurl', rurl
            print 'veriform',veriform

            # 返回验证码后的跳转地址，dont_filter参数，防止用户被服务器踢出去
            yield Request(
                "http://kns.cnki.net/kns/brief/vericode.aspx?" + veriform,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.Search3,
                dont_filter=True)
        else:
            next_pages = response.xpath('//a[@id="Page_next"]/@href').extract_first()
            for tr in response.css('table.GridTableContent').xpath('tr[position()>1]'):
                paper = ZhiwangspiderItem()
                paper['title'] = [tr.xpath('td[2]/a//text()').extract()[0].split('\'')[0]]
                # paper['author'] = tr.xpath('td[3]/a/text()').extract()
                # paper['journal'] = tr.xpath('td[4]/a//text()').extract()

                # print  paper
                yield  paper

            next_url = urljoin('http://kns.cnki.net/kns/brief/brief.aspx',next_pages)
            if next_url:
                yield  Request(next_url,
                               headers=self.headers,
                               cookies=self.cookies,
                               callback=self.Search3)


