# zhiwang_spider
## 爬取到知网期刊类下对应的数据


### 介绍
入口地址（期刊类高级检索界面）: http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ
#### 表单填写
包括日期、期刊内容（后期也可以通过自动化的方式，自动填入表单）
- （1）设置检索的日期（年份）
- （2）设置对应的查找期刊（分为精确搜索和模糊搜索）
#### 设置headers，cookies
- 知网的headers属性基本不变
- cookies帮助保持访问者的身份

### 目录结构
- 框架:Scrapy
