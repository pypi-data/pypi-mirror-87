from graia.application.message.elements.internal import Plain, Image, At, AtAll, Voice
from graia.application.message.chain import MessageChain
from argparse import *
import pickle
import base64
import shlex
import regex

try:
	import ujson as json
except ImportError:
	import json

class Element2Msg:
	"""
	将String转化为MessageChain
	使用方法
	>>> message = MessageChain.create([Plain('-s '), At(123)])
	>>> parser = MessageChainParser()
	>>> parser.add_argument('-s', type = String_To_Msg())
	>>> args = parser.parse_args(message)
	>>> args.s
	__root__ = [At(123)]

	method默认为'json'(可选'pickle'，前提是parse_obj的method也为'pickle')
	"""

	def __init__(self, method: str = 'json'):
		method_type = {'json': self._json_msg, 'pickle': self._pickle_msg}
		if method in method_type:
			self.method = method_type[method]
		else:
			raise ValueError(f'no such a method:{method}')

	def __call__(self, string: str) -> MessageChain:
		return self.method(string)

	def _json_msg(self, string: str) -> MessageChain:
		result = []
		for match in regex.split(r'(\[json_element:.+?\])', string):
			if element := regex.fullmatch(r'(\[json_element:(.+?)\])', match):
				result.append(json.loads(base64.b64decode(element.group(2))))
			elif match:#去除空字符串
				result.append({'type': 'Plain', 'text': match})
		return MessageChain.parse_obj(result)

	def _pickle_msg(self, string: str) -> MessageChain:
		result = []
		for match in regex.split(r'(\[pickle_element:.+?\])', string):
			if element := regex.fullmatch(r'(\[pickle_element:(.+?)\])', match):
				result.append(pickle.loads(base64.b64decode(element.group(2))))
			elif match:#去除空字符串
				result.append(Plain(match))
		return MessageChain.create(result)

class Msg2Element:

	def __init__(self, method: str = 'json'):
		method_type = {'json': self._json_string, 'pickle': self._pickle_string}
		if method in method_type:
			self.method = method_type[method]
		else:
			raise ValueError(f'no such a method:{method}')

	def __call__(self, string: str, space_in_gap: bool) -> MessageChain:
		return self.method(string, space_in_gap)

	def _json_string(self, message_arg: MessageChain, space_in_gap: bool) -> list:
		str_input = ''
		gap = ' ' if space_in_gap else ''
		hyper_message = message_arg.dict()['__root__']
		for n, element in enumerate(hyper_message):
			if element.get('type') == 'Plain':
				if (last_mes := hyper_message[n-1]).get('type') != 'Plain':
					str_input += gap
				str_input += element.get('text','')
			else:
				json_element = base64.b64encode(json.dumps(element).encode('UTF-8'))
				if (last_mes := hyper_message[n-1]).get('type') == 'Plain':
					str_input += '' if last_mes.get('text','').endswith(' ') else gap
				else:
					str_input += gap
				str_input += '[json_element:{}]'.format(
					json_element.decode("ascii"))
		return shlex.split(str_input)

	def _pickle_string(self, message_arg: MessageChain, space_in_gap: bool) -> list:
		str_input = ''
		gap = ' ' if space_in_gap else ''
		hyper_message = message_arg.__root__
		for n, element in enumerate(hyper_message):
			if type(element) is Plain:
				if not type(last_mes := hyper_message[n-1]) is Plain:
					str_input += gap
				str_input += element.text
			else:
				pickle_element = base64.b64encode(pickle.dumps(element))
				if type(last_mes := hyper_message[n-1]) is Plain:
					str_input += '' if last_mes.text.endswith(' ') else gap
				else:
					str_input += gap
				str_input += '[pickle_element:{}]'.format(
					pickle_element.decode("ascii"))
		return shlex.split(str_input)

class Element2Mirai:
	def __init__(self, method: str = 'json'):
		if method in ('json', 'pickle'):
			self.method = Element2Msg(method)
		else:
			raise ValueError(f'no such a method:{method}')

	def __call__(self, string: str):
		return self.method(string).asSerializationString()

class MessageChainParser(ArgumentParser):
	"""
	为MessageChain设计的Parser
	继承自标准库的ArgumentParser
	注:此模块仅验证了add_argument和parse_args的部分功能
	　　其他功能暂未验证其是否能够正常工作
	"""

	def __init__(self, *args, **kwargs):
		self.start = kwargs.pop('start_string', None)
		self.method = kwargs.pop('method', 'json')
		if self.method not in ('json', 'pickle'):
			raise ValueError('Unsupport method')
		super().__init__(*args, **kwargs)

	def parse_args(self, message: MessageChain, space_in_gap: bool = False):
		if self.start:
			if not message.asDisplay().startswith(self.start):
				raise ValueError()
			message_arg = message.asMerged().asHypertext()[(0,len(self.start)):]
		else:
			message_arg = message.asMerged().asHypertext()
		shell_like_list = Msg2Element(self.method)(message_arg, space_in_gap)
		print(Element2Msg(self.method)(shell_like_list[0]))
		try:
			return super().parse_args(shell_like_list)
		except ParserExit as e:
			if e.status == 0:
				print(0)
			else:
				print(e.status)