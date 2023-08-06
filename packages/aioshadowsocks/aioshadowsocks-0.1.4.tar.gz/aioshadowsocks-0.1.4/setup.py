# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shadowsocks',
 'shadowsocks.gen.async_protos',
 'shadowsocks.gen.sync_protos',
 'shadowsocks.mdb']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.6.2',
 'bloom-filter==1.3',
 'cryptography>=3.2.1,<4.0.0',
 'fire==0.3.1',
 'grpclib==0.4.1',
 'hkdf==0.0.3',
 'peewee==3.13.3',
 'prometheus-async==19.2.0',
 'prometheus-client==0.8.0',
 'protobuf==3.13.0',
 'requests==2.24.0',
 'sentry-sdk==0.18.0']

entry_points = \
{'console_scripts': ['aioss = shadowsocks.__main__:main']}

setup_kwargs = {
    'name': 'aioshadowsocks',
    'version': '0.1.4',
    'description': 'shadowsocks build with asyncio , also support many user in one port',
    'long_description': '# aioshadowsocks\n\n用 asyncio 重写 shadowsocks\n\n![Publish Docker](https://github.com/Ehco1996/aioshadowsocks/workflows/Publish%20Docker/badge.svg?branch=master)\n\n## 视频安装教程\n\n* 面板视频安装教程: [地址](https://youtu.be/BRHcdGeufvY)\n\n* 后端对接视频教程: [地址](https://youtu.be/QNbnya1HHU0)\n\n* 隧道对接视频教程: [地址](https://youtu.be/R4U0NZaMUeY)\n\n## 使用\n\n* 安装\n\n``` sh\npip install aioshadowsocks\n```\n\n* 多用户配置\n\naioshadowsocks 将json作为配置文件, 会读取当前目录下 `userconfigs.json` 作为默认的配置文件\n\n``` json\n{\n    "users": [\n        {\n            "user_id": 1,\n            "port": 2345,\n            "method": "none",\n            "password": "hellotheworld1",\n            "transfer": 104857600,\n            "speed_limit": 0\n        },\n        {\n            "user_id": 2,\n            "port": 2346,\n            "method": "chacha20-ietf-poly1305",\n            "password": "hellotheworld2",\n            "transfer": 104857600,\n            "speed_limit": 384000\n        }\n    ]\n}\n```\n\n同时也支持从http服务器读取配置文件，这时需要注入环境变量 `SS_API_ENDPOINT` 作为读取配置的api地址\n\n* 注入环境变量\n\n `export SS_API_ENDPOINT="https://xxx/com"`\n\n* 启动ss服务器\n\n``` bash\naioss run_ss_server\n```\n\n## Docker Version\n\n1. install docker\n\n``` sh\ncurl -sSL https://get.docker.com/ | sh\n```\n\n2. install docker-compose\n\n``` sh\nsudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose\n```\n\n3. apply executable permissions\n\n``` sh\nsudo chmod +x /usr/local/bin/docker-compose\n```\n\n4. run server\n\n``` sh\ndocker-compose up\n```\n\n## 为什么要重写shadowsocks\n\n主要想通过这个项目的推进来深入了解 `asyncio`\n\n另外我的一个项目: [django-sspanel](https://github.com/Ehco1996/django-sspanel) 依赖 `shadowsocksr`\n\n但该项目已经停止开发了，所以决定重新造个轮子\n\n## 主要功能\n\n* tcp/udp 代理\n* 流量统计\n* 速率控制\n* 开放了grpc接口(类似ss-manager)\n* **单端口多用户（利用AEAD加密在不破坏协议的情况下实现）**\n* **prometheus/grafana metrics监控** （dashboard在项目的static/grafana/文件夹下）\n\n## 监控dashboard\n\n![](static/images/1.png)\n\n![](statoc/images/2.png)\n\n![](static/images/3.png)\n\n## 性能测试\n\n> Shadowsocks本身是一个IO密集行的应用，但是由于加入了AEAD加密，使得SS本身变成了CPU密集行的应用\n> 而Python本身是不太适合CPU密集的场景的，所以在AEAD模式中的表现不佳\n> PS: 当然，其实是我代码写的烂，python不背锅\n\n* Steam-Cipher-None(不加密 高IO)\n\n![](static/images/stream-none.png)\n\n* AEAD-Cipher-CHACHA-20(加密 高CPU)\n\n![](static/images/aead-chacha-20-ietf-poly-1305.png)\n\n## rpc proto\n\n``` protobuf\nsyntax = "proto3";\n\npackage aioshadowsocks;\n\n// REQ\nmessage UserIdReq { int32 user_id = 1; }\nmessage PortReq { int32 port = 1; }\n\nmessage UserReq {\n  int32 user_id = 1;\n  int32 port = 2;\n  string method = 3;\n  string password = 4;\n  bool enable = 5;\n}\n\n// RES\nmessage Empty {}\n\nmessage User {\n  int32 user_id = 1;\n  int32 port = 2;\n  string method = 3;\n  string password = 4;\n  bool enable = 5;\n  int32 speed_limit = 6;\n  int32 access_order = 7;\n  bool need_sync = 8;\n  repeated string ip_list = 9;\n  int32 tcp_conn_num = 10;\n  int64 upload_traffic = 11;\n  int64 download_traffic = 12;\n}\n\n// service\nservice ss {\n  rpc CreateUser(UserReq) returns (User) {}\n  rpc UpdateUser(UserReq) returns (User) {}\n  rpc GetUser(UserIdReq) returns (User) {}\n  rpc DeleteUser(UserIdReq) returns (Empty) {}\n}\n```\n',
    'author': 'ehco1996',
    'author_email': 'zh19960202@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
