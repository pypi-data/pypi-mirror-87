# -*- coding: utf-8 -*-

import numpy as np
import torch
from transformers import AutoModelForTokenClassification,AutoTokenizer,AutoConfig
import os
import re
import regex
from tqdm import tqdm
import time
import gc

class Marker:
    """
    自动提取标记信息
    使用Bert模型进行训练
    
    """
    def __init__(self,model_path="../model",device='cpu'):
        """
        初始化模型
        可以从这里下载模型

        https://www.kaggle.com/terrychanorg/bert-title/output
        
        >>> Demo =Bert_clear_title.Marker(model_path="/mnt/data/dev/model/Bert_clear_title/model/")
        
        """
        self.model_path=model_path
        self.labels_file=os.path.join(model_path,"labels.txt")
        self.device=device
        pass
    def __del__(self):
        # self.release()
        pass

    def release(self):
        """
        print("释放显存")

        """
        # 
        self.model.cpu()

        torch.cuda.empty_cache()
        pass
        # torch.cuda.empty_cache()
        del self.model
        del self.tokenizer
        del self.lablels_dict
        gc.collect()
    # @profile
    def load_model(self):
        """
        加载模型数据

        >>> Demo.load_model()
        
        """
        # tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        config = AutoConfig.from_pretrained(self.model_path)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_path,config=config)
        # self.model = AutoModelForTokenClassification.from_pretrained(os.path.join(self.model_path,"labels.txt"))
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path,config=config)
        # self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(self.model_path,"labels.txt"))
        # model.to(self.device)
        f2=open(self.labels_file,'r')
        lablels_dict={}
        for i,line in enumerate(f2):
            # l=line.split(" ")
            l=line.replace("\n",'')
            # print(l)
            lablels_dict[i]=l
        f2.close()
        self.lablels_dict=lablels_dict
        # self.model=model
        # self.tokenizer=tokenizer
        # self.model.eval()
        return self.model,self.tokenizer
    def pre(self,text):
        """
        进行预测

        >>> Demo.pre(text)
        >>> [{'text': ['[CLS]', '可', '见', '其', '成', '是', '什', '么', '意', '思', '-', '百', '度', '知', '道', '[SEP]'], 'label': ['O', 'B-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'M-title', 'E-title', 'O', 'O', 'O', 'O', 'O', 'O']}]

        """
        model=self.model
        tokenizer=self.tokenizer
        model.eval()
        # text=text
        lenth=128
        # all_ms=[]
        datas=[]
        for text_mini in self.cut_text(text,lenth):
            # text_mini=word+"[SEP]"+text_mini
            ids=tokenizer.encode_plus(text_mini,max_length=512, add_special_tokens=True)
            # print(ids)
            input_ids = torch.tensor(ids['input_ids']).unsqueeze(0)  # Batch size 1
            labels = torch.tensor([1] * input_ids.size(1)).unsqueeze(0)  # Batch size 1
            outputs = model(input_ids, labels=labels)
            # print(outputs)
            tmp_eval_loss, logits  = outputs[:2]
            # ids=tokenizer.encode(text)
            # print(ids)

            # print("\n".join([i for i in self.lablels_dict.keys()]))
            # words=[]
            data_one={"text":[],"label":[]}
            for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
                # print(m)
                # print(m,ids[i],tokenizer.convert_ids_to_tokens(ids[i]),self.lablels_dict[m])
                word=tokenizer.convert_ids_to_tokens(ids['input_ids'][i])
                # print(word,self.lablels_dict[m])
                data_one["text"].append(word)
                data_one["label"].append(self.lablels_dict[m])
            datas.append(data_one)
        return datas



    def cut_text(self,obj,sec):
        """
        分割固定长度字符串
        """
    #     textArr = re.findall('.{'+str(lenth)+'}', text)
    #     textArr.append(text[(len(textArr)*lenth):])
    #     return textArr
    # def cut(self,obj, sec):
        return [obj[i:i+sec] for i in range(0,len(obj),sec)]
    def clear_word(self,word):
        return word.replace("##", "")
    # @profile
    def filterPunctuation(self,x):
        x = regex.sub(r'[‘’]', "'", x)
        x = regex.sub(r'[“”]', '"', x)
        x = regex.sub(r'[…]', '...', x)
        x = regex.sub(r'[—]', '-', x)
        x = regex.sub(r"&nbsp", "", x)
        return x

    def get_mark_data(self,data):
        """
        对标记的数据进行提取

        {"text": ["树", "头", "菜", "（", "学", "名", "：", "）", "为", "山", "柑", "科", "鱼", "木", "属", "的", "植", "物", "。"], "label": ["B-实体", "M-实体", "E-实体", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]} 
        返回数据如下
        {'实体': ['美国电视史', '中国人民大学出版社']}
        """
        all_ms={}
        words=[]
        for word,mark_lable in zip(data['text'],data['label']):
            # its.append(line)
            # print(mark_lable)
            if mark_lable.startswith("E-" ) and len(words)>0:
                words.append(word)
                # print(words)
                word_type=mark_lable.replace("E-",'')
                # print("word_type",word_type)
                try:
                    all_ms[word_type].append(self.clear_word("".join(words)))
                except:
                    all_ms[word_type]=[]
                    all_ms[word_type].append(self.clear_word("".join(words)))
                words=[]
            elif mark_lable.startswith("S-"):
                words=[]
                words.append(word)
                word_type=mark_lable.replace("S-",'')
                try:
                    all_ms[word_type].append(self.clear_word("".join(words)))
                except:
                    all_ms[word_type]=[]
                    all_ms[word_type].append(self.clear_word("".join(words)))

                words=[]
            elif mark_lable.startswith("B-"):
                words=[]
                words.append(word)
            elif mark_lable.startswith("M-")  and len(words)>0:
                words.append(word)
            elif  mark_lable.startswith("O") or mark_lable.startswith("X"):
                words=[]
                pass
        return all_ms