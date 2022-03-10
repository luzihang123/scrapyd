=======
Scrapyd
=======
|PyPI Version| |Build Status| |Coverage Status| |Python Version| |Pypi Downloads|

Scrapyd is a service for running `Scrapy`_ spiders.

It allows you to deploy your Scrapy projects and control their spiders using an
HTTP JSON API.

The documentation (including installation and usage) can be found at:
http://scrapyd.readthedocs.org/


.. |PyPI Version| image:: https://img.shields.io/pypi/v/scrapyd.svg
   :target: https://pypi.org/project/scrapyd/
.. |Build Status| image:: https://github.com/scrapy/scrapyd/workflows/Tests/badge.svg
.. |Coverage Status| image:: https://codecov.io/gh/scrapy/scrapyd/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/scrapy/scrapyd
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/scrapyd.svg
   :target: https://pypi.org/project/scrapydt/
.. |Pypi Downloads| image:: https://img.shields.io/pypi/dm/scrapyd.svg
   :target: https://pypi.python.org/pypi/scrapyd/
.. _Scrapy: https://github.com/scrapy/scrapy



=======
修改部分
=======


Feature:
--------

1、通过配置文件scrapyd.conf，log_suffix配置项，可以自定义日志格式，方便被公司elk收集

2、前端增加UTF_8视窗，解决乱码问题，方便查看中文日志


TODO:
-----

1、日志大小控制
应对长任务，海量数据抓取的log大小问题


Install:
-----
1、安装
无需登录git

码云：pip install git+https://gitee.com/WoAiChiZhuSun/scrapyd.git

github：pip install git+https://github.com/luzihang123/scrapyd.git

2、添加 scrapyd/scripts/logs/UTF-8.html 文件，到scrapyd 配置文件指定的logs_dir下
