# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graiax', 'graiax.msgparse']

package_data = \
{'': ['*']}

install_requires = \
['graia-application-mirai>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'graiax-msgparse',
    'version': '0.0.2',
    'description': 'A argparse for MessageChain in Graia Framework',
    'long_description': "# graiax-msgparse\n\n### 这是什么\n这是一个为匹配[graia-application-mirai](https://github.com/GraiaProject/Application)中MessageChain的设计创造出来的一个为匹配MessageChain做出的argparse\n\n#### 安装\n``` bash\npip install graiax-msgparse\n# 或使用 poetry\npoetry add graiax-msgparse\n```\n\n### 如何使用\n注意：在查看示例代码前，个人建议先查看以下文档\n[graia-document中对Application的介绍](https://graia-document.vercel.app/)\n[Python-document中对argparse模块的介绍](https://docs.python.org/zh-cn/3.8/library/argparse.html)\n``` python\nfrom graiax.msgparse import MessageChainParser, ParserExit, Element2Msg, Element2Mirai\n\n@bcc.receiver(GroupMessage, dispatchers = [Kanata([RegexMatch('parse.*')])])\nasync def parse_test(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):\n\tparser = MessageChainParser(start_string = 'parse', description='parse测试')\n\tparser.add_argument('-r')\n\ttry:\n\t\tparser.parse_obj(message, space_in_gap = True)\n\texcept ParserExit as e:\n\t\tawait app.sendGroupMessage(group, MessageChain.create([\n\t\t\tPlain(str(parser.usage) if e.status == 0 else '参数不足或不正确，请使用 --help 参数查询使用帮助')\n\t\t\t]))\n```\n方法几乎跟python自带的ArgumentParser使用方法如出一辙(毕竟是继承于此)\n我们就先看看二者不同的区别\n\n`parser = MessageChainParser(start_string = 'parse')`\n\n`start_string`是你的`listener`的触发条件，`MessageChainParser`将会检查message开头时候为`start_string`中的文字并去除\n\n`parser.parse_obj(message, space_in_gap = True)`\n\n`space_in_gap`参数是用于给各个非Plain之间添加缝隙的，因为MessageChainParser的内部处理机制是先将MessageChain转换为字符串，然后再通过`shlex.split`方法对转换过的字符串进行处理。所以可能会出现一些问题\n\n如(At(123),Plain('-s'))\n\n当`sapce_in_gap`为True时，将会自动在俩个element之间添加空格\n\n#### 用Element2Msg, Element2Mirai转换非纯Plain消息\n由于MessageChainParser中将会把除了Plain以外的元素进行特殊处理，所以假设你的参数中带有At,AtAll,Image参数，那么可能会返回这么一串奇怪的东西\n`[json_element:eyJ0eXBlIjoiQXQiLCJ0YXJnZXQiOjEyMywiZGlzcGxheSI6bnVsbH0=]`\n如果需要将这串玩意变成MessageChain或者是Mirai码\n你就会需要\n`Element2Msg`和`Element2Mirai`\n``` python\nfrom graiax.msgparse import MessageChainParser, Element2Msg, Element2Mirai\n...\nparser.add_argument('-r',type = Element2Msg())#将接收到的信息转换为MessageChain的形式\nparser.add_argument('-s',type = Element2Mirai())#将接收到的信息转换为Mirai码的形式\nparser.parse_obj(message)\n```\n",
    'author': 'I_love_study',
    'author_email': '1450069615@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/I-love-study/graiax-msgparse',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
