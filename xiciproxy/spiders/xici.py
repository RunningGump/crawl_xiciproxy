import scrapy
import json
'''
scrapy crawl xici -o out.json -a num_pages=50 -a typ=nn
其中`out.json`是输出json文件，`num_pages`是爬取页数，`typ`表示代理类型，`nn`是高匿代理，`nt`是普通代理。

'''

class XiCiSpider(scrapy.Spider):
    name = 'xici'
    # 使用-a选项,可以将命令行参数传递给spider的__init__方法
    def __init__(self, num_pages=5, typ='nn', *args, **kwargs):
        num_pages = int(num_pages)
        self.num_pages = num_pages
        self.typ = typ

    def start_requests(self): 
        for page in range(1, self.num_pages + 1):
            url = 'http://www.xicidaili.com/{}/{}'.format(self.typ, page)
            yield scrapy.Request(url=url)

    # 解析response返回的网页
    def parse(self, response):
        proxy_list = response.xpath('//table[@id = "ip_list"]/tr[position()>1]')  
        for tr in proxy_list:
            # 提取代理的 ip, port, scheme(http or https)
            ip = tr.xpath('td[2]/text()').extract_first()
            port = tr.xpath('td[3]/text()').extract_first()
            scheme = tr.xpath('td[6]/text()').extract_first()

            # 使用爬取到的代理再次发送请求到http(s)://httpbin.org/ip, 验证代理是否可用
            url = '%s://httpbin.org/ip' % scheme
            proxy = '%s://%s:%s' % (scheme, ip, port)


            meta = {
                'proxy': proxy,
                'dont_retry': True,
                'download_timeout': 5,
                # 下面的ip字段是传递给check_available方法的信息,方便检测是否可隐藏ip
                '_proxy_ip':ip,
            }
 
            yield scrapy.Request(url, callback=self.check_available, meta=meta, dont_filter=True)
 

    def check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']

        # 判断代理是否具有隐藏IP功能
        if proxy_ip == json.loads(response.text)['origin']:
            yield{
                'proxy': response.meta['proxy']
            }
