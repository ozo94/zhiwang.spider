## zhiwang_spider
>爬取到知网期刊类下对应的数据

### 介绍
入口地址（期刊类高级检索界面）: http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ
##### 表单填写
包括日期、期刊内容（后期也可以通过自动化的方式，自动填入表单）
- 设置检索的日期（年份）
- 设置对应的查找期刊（分为精确搜索和模糊搜索）
##### 设置headers，cookies
- 知网的headers属性基本不变
- cookies帮助保持访问者的身份

### 目录结构
- 框架:Scrapy

##### 模块（文件）
- captcha_recognition
  - 知网验证码的验证模块（知网的验证码还是比较简单）
  - 识别效率在70%左右，基本达到标准
  - 技术实现参考地址：https://www.zhihu.com/question/33321954?sort=created
- img
    - 存放获得的验证码图片，并包含训练、测试图集合
- spiders
    - 主爬虫部分

