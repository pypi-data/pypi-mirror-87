# graiax-msgparse

### 这是什么
这是一个为匹配[graia-application-mirai](https://github.com/GraiaProject/Application)中MessageChain的设计创造出来的一个为匹配MessageChain做出的argparse

#### 安装
``` bash
pip install graiax-msgparse
# 或使用 poetry
poetry add graiax-msgparse
```

### 如何使用
注意：在查看示例代码前，个人建议先查看以下文档
[graia-document中对Application的介绍](https://graia-document.vercel.app/)
[Python-document中对argparse模块的介绍](https://docs.python.org/zh-cn/3.8/library/argparse.html)
``` python
from graiax.msgparse import MessageChainParser, Element2Msg, Element2Mirai

@bcc.receiver(GroupMessage, dispatchers = [Kanata([RegexMatch('parse.*')])])
async def parse_test(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
	parser = MessageChainParser(start_string = 'parse', description='parse测试')
	parser.add_argument('-r')
	parser.parse_obj(message, space_in_gap = True)
```
方法几乎跟python自带的ArgumentParser使用方法如出一辙(毕竟是继承于此)
我们就先看看二者不同的区别

`parser = MessageChainParser(start_string = 'parse')`

`start_string`是你的`listener`的触发条件，`MessageChainParser`将会检查message开头时候为`start_string`中的文字并去除

`parser.parse_obj(message, space_in_gap = True)`

`space_in_gap`参数是用于给各个非Plain之间添加缝隙的，因为MessageChainParser的内部处理机制是先将MessageChain转换为字符串，然后再通过`shlex.split`方法对转换过的字符串进行处理。所以可能会出现一些问题

如(At(123),Plain('-s'))

当`sapce_in_gap`为True时，将会自动在俩个element之间添加空格

#### 用Element2Msg, Element2Mirai转换非纯Plain消息
由于MessageChainParser中将会把除了Plain以外的元素进行特殊处理，所以假设你的参数中带有At,AtAll,Image参数，那么可能会返回这么一串奇怪的东西
`[json_element:eyJ0eXBlIjoiQXQiLCJ0YXJnZXQiOjEyMywiZGlzcGxheSI6bnVsbH0=]`
如果需要将这串玩意变成MessageChain或者是Mirai码
你就会需要
`Element2Msg`和`Element2Mirai`
``` python
from graiax.msgparse import MessageChainParser, Element2Msg, Element2Mirai
...
parser.add_argument('-r',type = Element2Msg())#将接收到的信息转换为MessageChain的形式
parser.add_argument('-s',type = Element2Mirai())#将接收到的信息转换为Mirai码的形式
parser.parse_obj(message)
```
