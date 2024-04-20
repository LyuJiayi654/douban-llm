import pickle as pkl
import pandas as pd
import numpy as np
import spacy
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

file = pd.read_csv("medium data/zctytlxz_id_r_chat35.csv")
print(len(file['result']))
candidates = file['result']
references = []
file_re = pd.read_csv("medium data/zctytlxz_id_c_c_c.csv")
dic = {}
for i in file['postID']:
    dic[i] = []
for i in range(len(file_re['postID'])):
    dic[file_re['postID'][i]].append(file_re['comment'][i])

for i in file['postID']:
    references.append(dic[i])

ch_nlp = spacy.load("zh_core_web_sm")
tes_token = []
for ref in references:
    res = []
    for sent in ref:
        t = []
        for token in ch_nlp.tokenizer(sent):
            t.append(token.text)
        res.append(t)
    tes_token.append(res)
cand_token = []
for cand in candidates:
    can = []
    for token in ch_nlp.tokenizer(cand):
        can.append(token.text)
    cand_token.append(can)

smoothie = SmoothingFunction().method1

# 计算 BLEU 得分列表
bleu_scores = [sentence_bleu(ref, cand) for ref, cand in zip(tes_token, cand_token)]

# 计算 BLEU 得分平均值
average_bleu_score = sum(bleu_scores) / len(bleu_scores)

print("BLEU Scores:", bleu_scores)
print("Average BLEU Score:", average_bleu_score)