
#encoding=utf-8
from __future__ import unicode_literals
import sys
# 切换到上级目录
sys.path.append("../")
# 引入本地库
import Bert_clear_title

Demo =Bert_clear_title.Marker(model_path="/mnt/data/dev/model/Bert_clear_title/model/")
Demo.load_model()


text="可见其成是什么意思 - 百度知道"

print(Demo.pre(text))
# [{'text': ['[CLS]', '可', '见', '其', '成', '是', '什', '么', '意', '思', '-', '百', '度', '知', '道', '[SEP]'], 'label': ['O', 'B-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'E-title', 'O', 'O', 'O', 'O', 'O', 'O']}]

one=Demo.pre(text)
print(one)

#>>> [{'text': ['[CLS]', '可', '见', '其', '成', '是', '什', '么', '意', '思', '-', '百', '度', '知', '道', '[SEP]'], 'label': ['O', 'B-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'E-title', 'O', 'O', 'O', 'O', 'O', 'O']}]

print(Demo.get_mark_data(one[0]))

{'title': ['可见其成是什么意思']}
# {'title': ['可见其成是什么意思']}


