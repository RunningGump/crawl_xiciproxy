## 前言

​	在爬取网站数据的时候，一些网站会对用户的访问频率进行限制，如果爬取过快会被封ip，而使用代理可防止被封禁。本项目使用scrapy框架对[西刺网站](http://www.xicidaili.com/)进行爬取，并验证爬取代理的有效性，最终将有效的代理存储到json文件中。

## 依赖

1. python3.6
2. Scrapy 1.5.0

## 使用方法

只需在命令行中执行以下命令即可：

``` bash
$ scrapy crawl xici -o out.json -a num_pages=10 -a typ=nn
```

其中`out.json`是最终输出有效代理的json文件，`num_pages`是爬取页数，`typ`表示要爬取的代理类型，`nn`是高匿代理，`nt`是普通代理。

爬取网页信息时大多用高匿代理，高匿名代理不改变客户机的请求，这样在服务器看来就像有个真正的客户浏览器在访问它，这时客户的真实IP是隐藏的，不会认为我们使用了代理。

