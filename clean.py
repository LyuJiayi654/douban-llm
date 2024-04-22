import re
import emoji
import pandas as pd
import numpy as np
import pickle as pkl
import jieba


def preprocess_text(text):
    # 去除指定字符串 申删 已删 申请删除 申请删帖 已解决
    text = text.replace(r"[内容不可见]", "")
    text = text.replace(r"[该条回应已被删除]", "")
    text = text.replace(r"申删", "")
    text = text.replace(r"已删", "")
    text = text.replace(r"申请删除", "")
    text = text.replace(r"已解决", "")
    text = text.replace(r"nan", "")
    text = text.replace(r"deleted", "")
    text = text.replace(r"delete", "")
    text = re.sub(r'\s+', ' ', text)

    return text


def remove_duplicates():
    data = []
    file = pd.read_csv("pc豆瓣5个组/豆瓣评论1.csv")
    print(len(file['条']))
    for i in range(len(file['条'])):
        if file['评论ID'][i] != '无':
            data.append((file['条'][i], file['评论ID'][i], file['评论内容'][i], file['针对'][i], file['是否楼主'][i],
                         file['名字'][i], file['IP'][i], file['点赞数'][i]))

    print(len(file['是否楼主']), len(list(set(data))))
    print(len(file['是否楼主']), len(list(set(file['评论ID']))))
    x = pd.Series(data).unique()
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    h = []
    j = []
    for i in x:
        a.append(i[0])
        b.append(i[1])
        c.append(i[2])
        d.append(i[3])
        e.append(i[4])
        f.append(i[5])
        h.append(i[6])
        j.append(i[7])
    print(len(x))
    df = pd.DataFrame({'条': a, '评论ID': b, '评论内容': c, '针对': d, '是否楼主': e, '名字': f, 'IP': h, '点赞数': j})
    df.to_csv("pc豆瓣5个组/豆瓣评论1_.csv", index=False, sep=',', encoding='utf-8-sig')
    return 0


def gen_id_id_id_file():
    post = []
    comment = []
    review = []
    file = pd.read_csv("pc豆瓣5个组/豆瓣评论1_.csv")
    for i in range(len(file['是否楼主'])):
        if file['是否楼主'][i] == "是":
            if str(file['针对'][i]) != '0':
                post.append(file['条'][i])
                comment.append(file['针对'][i])
                review.append(file['评论ID'][i])

    p = list(set(post))
    print("有楼主回复的帖子：", len(p))
    print("楼主的回复：", len(post))
    df = pd.DataFrame({'postID': post, 'comment': comment, 'review': review})
    df.to_csv("medium data/rswtyjs_id_id_id.csv", index=False, sep=',', encoding='utf-8-sig')


def gen_postid_pre():
    file = pd.read_csv("medium data/rswtyjs_id_id_id.csv")
    post_c = pd.read_csv("pc豆瓣5个组/豆瓣1_1.csv")
    postdict = {}
    for i in range(len(post_c['条'])):
        postdict[str(post_c['条'][i])] = i
    cp = {}
    postid = list(set(file['postID']))
    for i in range(len(postid)):
        cp[str(postid[i])] = str(post_c['标题'][postdict[str(postid[i])]]) + str(
            post_c['正文'][postdict[str(postid[i])]])

    post_id = []
    post_content = []
    for i in cp.keys():
        post_id.append(i)
        post_content.append(preprocess_text(cp[i]))
    df = pd.DataFrame({'postID': post_id, 'postkey': post_content})
    df.to_csv("medium data/rswtyjs_postid.csv", index=False, sep=',', encoding='utf-8-sig')


def gen_id_c_c_file():
    file = pd.read_csv("medium data/rswtyjs_id_id_id.csv")
    comment_c = pd.read_csv("pc豆瓣5个组/豆瓣评论1_.csv")

    commentdict = {}
    for i in list(set(comment_c['针对']) - set(comment_c['评论ID'])):
        commentdict[str(i)] = ''
    for i in range(len(comment_c['评论ID'])):
        commentdict[str(comment_c['评论ID'][i])] = comment_c['评论内容'][i]

    comment = []
    review = []
    for i in file['comment']:
        if pd.isna(commentdict[str(i)]):
            comment.append(' ')
        else:
            comment.append(preprocess_text(commentdict[str(i)]))
    print("comment finish")
    for i in file['review']:
        if pd.isna(commentdict[str(i)]):
            review.append(' ')
        else:
            review.append(preprocess_text(commentdict[str(i)]))

    df = pd.DataFrame({'postID': file['postID'], 'comment': comment, 'review': review})
    df.to_csv("medium data/rswtyjs_id_c_c.csv", index=False, sep=',', encoding='utf-8-sig')


def gen_c_c_c_file_remove_mutiple():
    file = pd.read_csv("rswtyjs_id_c_c.csv")
    file_post = pd.read_csv("rswtyjs_postid_pre.csv")
    post_label = []
    for i in range(len(file['postID'])):
        post_label.append(' ')

    for i in range(len(file_post['postID'])):
        post_label[int(file_post['postID'][i])] = file_post['postkey'][i]
    print(len(file['postID']))
    print(len(file_post['postID']))

    post_id = []
    post = []
    comment = []
    review = []

    for i in range(len(file['postID'])):
        if pd.isna(file['postID'][i]):
            print("!!!!!!!")
            post_label[int(file['postID'][i])] = ' '
            post.append(' ')
            post_id.append(-1)
        else:
            post_id.append(int(file['postID'][i]))
            post.append(post_label[int(file['postID'][i])])
    for i in range(len(file['postID'])):
        if pd.isna(file['comment'][i]):
            comment.append(' ')
        else:
            comment.append(file['comment'][i])
        if pd.isna(file['review'][i]):
            review.append(' ')
        else:
            review.append(file['review'][i])

    for i in range(len(comment)):
        if pd.isna(comment[i]):
            print("!!!!!!!")
        else:
            comment[i] = preprocess_text(comment[i])
    for i in range(len(review)):
        if pd.isna(review[i]):
            print("!!!!!!!")
        else:
            review[i] = preprocess_text(review[i])
    print(len(post), len(comment), len(review))
    postid_ = []
    multi_result = []
    post_result = []
    post_ = []
    comment_ = []
    review_ = []
    for i in range(len(post)):
        if len(post[i]) > 9 and len(comment[i]) > 5 and len(review[i]) > 1 and post_id[i] > 0:
            multi_result.append((int(post_id[i]), post[i], comment[i], review[i]))
            post_result.append((int(post_id[i]), post[i]))
            postid_.append(post_id[i])

    print(len(postid_), len(post_), len(comment_), len(review_))
    post_id_final = []
    post_content_final = []

    x = list(set(multi_result))
    x.sort()
    y = list(set(post_result))
    y.sort()
    for i in y:
        post_id_final.append(i[0])
        post_content_final.append(i[1])
    for i in x:
        post_.append(i[1])
        comment_.append(i[2])
        review_.append(i[3])
    print(len(post_), len(comment_), len(review_))
    print(len(post_id_final), len(post_content_final), len(list(set(post_))), len(list(set(postid_))))
    df1 = pd.DataFrame({'postID': post_id_final, 'postkey': post_content_final})
    df1.to_csv("rswtyjs_postid_pre_final.csv", index=False, sep=',', encoding='utf-8-sig')

    df = pd.DataFrame({'post': post_, 'comment': comment_, 'review': review_})
    df.to_csv("rswtyjs_c_c_c.csv", index=False, sep=',', encoding='utf-8-sig')


def gen_c_c_c_file():
    file = pd.read_csv("medium data/rjqlgc_id_c_c.csv")
    file_post = pd.read_csv("medium data/rjqlgc_postid.csv")
    post_label = []
    for i in range(len(file['postID'])):
        post_label.append(' ')

    for i in range(len(file_post['postID'])):
        post_label[int(file_post['postID'][i])] = file_post['postkey'][i]
    print(len(file['postID']))
    print(len(file_post['postID']))

    post_id = []
    post = []
    comment = []
    review = []

    for i in range(len(file['postID'])):
        if pd.isna(file['postID'][i]):
            print("!!!!!!!")
            post_label[int(file['postID'][i])] = ' '
            post.append(' ')
            post_id.append(-1)
        else:
            post_id.append(int(file['postID'][i]))
            post.append(post_label[int(file['postID'][i])])
    for i in range(len(file['postID'])):
        if pd.isna(post[i]):
            post[i] = ' '
        if pd.isna(file['comment'][i]):
            comment.append(' ')
        else:
            comment.append(file['comment'][i])
        if pd.isna(file['review'][i]):
            review.append(' ')
        else:
            review.append(file['review'][i])

    print(len(post), len(comment), len(review))
    post_result = []
    postid_ = []
    post_ = []
    comment_ = []
    review_ = []
    for i in range(len(post)):
        if len(post[i]) > 9 and len(comment[i]) > 5 and len(review[i]) > 1 and post_id[i] > 0:
            post_result.append((int(post_id[i]), post[i]))
            postid_.append(int(post_id[i]))
            post_.append(post[i])
            comment_.append(comment[i])
            review_.append(review[i])

    print(len(postid_), len(post_), len(comment_), len(review_))
    post_id_final = []
    post_content_final = []

    y = list(set(post_result))
    y.sort()
    for i in y:
        post_id_final.append(i[0])
        post_content_final.append(i[1])

    print(len(post_id_final), len(post_content_final), len(list(set(post_))))

    # df1 = pd.DataFrame({'postID': post_id_final, 'postkey': post_content_final})
    # df1.to_csv("medium data/rswtyjs_postid_pre_final.csv", index=False, sep=',', encoding='utf-8-sig')

    # df = pd.DataFrame({'post': post_, 'comment': comment_, 'review': review_})
    # df.to_csv("medium data/rswtyjs_c_c_c.csv", index=False, sep=',', encoding='utf-8-sig')

    df = pd.DataFrame({'postID': postid_, 'post': post_, 'comment': comment_, 'review': review_})
    df.to_csv("medium data/rjqlgc_id_c_c_c.csv", index=False, sep=',', encoding='utf-8-sig')


def show_len():
    file = pd.read_csv("medium data/rswtyjs_id_c_c_c.csv")
    file_post = pd.read_csv("medium data/rswtyjs_postid_pre_final.csv")
    post_len = []
    comment_len = []
    review_len = []
    for i in file_post['postkey']:
        post_len.append(len(i))
    for i in file['comment']:
        if len(i) == 6:
            print(i)
        comment_len.append(len(i))
    for i in file['review']:
        if len(i) == 2:
            print(i)
        review_len.append(len(i))
    post_len.sort()
    comment_len.sort()
    review_len.sort()

    print(len(post_len))
    print(np.mean(post_len), np.mean(comment_len), np.mean(review_len))
    print(len(post_len))
    print(len(file['post']), len(list(set(file['post']))), len(list(set(file['postID']))))


def gen_id_c():
    post = []
    comment = []
    file = pd.read_csv("pc豆瓣5个组/豆瓣评论1_.csv")
    print(len(file['是否楼主']), len(list(set(file['评论ID']))))
    for i in range(len(file['是否楼主'])):
        post.append(file['条'][i])
        comment.append(file['评论内容'][i])

    for i in range(len(comment)):
        if pd.isna(comment[i]):
            comment[i] = ' '
        else:
            comment[i] = preprocess_text(comment[i])
    print(len(comment))
    df = pd.DataFrame({'postID': post, 'comment': comment})
    df.to_csv("medium data/rswtyjs_id_c.csv", index=False, sep=',', encoding='utf-8-sig')


def gen_id_c_label():
    post = []
    comment = []
    label = []
    file = pd.read_csv("pc豆瓣5个组/豆瓣评论1_.csv")
    print(len(file['是否楼主']), len(list(set(file['评论ID']))))
    relation = {}
    for i in range(len(file['是否楼主'])):
        # dic[file['评论ID'][i]] = file['是否楼主'][i]
        relation[str(file['评论ID'][i])] = '0'
    for i in range(len(file['是否楼主'])):
        if file['是否楼主'][i] == '是':
            relation[str(file['针对'][i])] = str(file['评论ID'][i])
    for i in range(len(file['是否楼主'])):
        post.append(file['条'][i])
        comment.append(file['评论内容'][i])
        if relation[str(file['评论ID'][i])] =='0':
            label.append(0)
        else:
            label.append(1)

    for i in range(len(comment)):
        if pd.isna(comment[i]):
            comment[i] = ' '
        else:
            comment[i] = preprocess_text(comment[i])
    print(len(comment))
    df = pd.DataFrame({'postID': post, 'comment': comment, 'label': label})
    df.to_csv("medium data/rswtyjs_id_c_label.csv", index=False, sep=',', encoding='utf-8-sig')


def gen_c_c():
    file = pd.read_csv("medium data/rswtyjs_id_c.csv")
    file_post = pd.read_csv("medium data/rswtyjs_postid_pre_final.csv")
    post_label = []
    for i in range(len(file['postID'])):
        post_label.append(' ')

    for i in range(len(file_post['postID'])):
        post_label[int(file_post['postID'][i])] = file_post['postkey'][i]
    print(len(file['postID']))

    post = []
    comment = []
    postid = []

    for i in range(len(file['postID'])):
        if pd.isna(file['postID'][i]):
            print("!!!!!!!")
            post.append(' ')
            postid.append(-1)
        else:
            postid.append(int(file['postID'][i]))
            post.append(post_label[int(file['postID'][i])])
    for i in range(len(file['postID'])):
        if pd.isna(file['comment'][i]):
            comment.append(' ')
        else:
            comment.append(file['comment'][i])

    for i in range(len(comment)):
        if pd.isna(comment[i]):
            print("!!!!!!!")
        else:
            comment[i] = preprocess_text(comment[i])
    print(len(post), len(comment))
    post_ = []
    comment_ = []
    postid_ = []
    for i in range(len(post)):
        if len(post[i]) > 9 and len(comment[i]) > 5:
            postid_.append(postid[i])
            post_.append(post[i])
            comment_.append(comment[i])
    print(len(postid_), len(post_), len(comment_))
    df = pd.DataFrame({'post': post_, 'comment': comment_})
    df.to_csv("medium data/rswtyjs_c_c.csv", index=False, sep=',', encoding='utf-8-sig')

    df = pd.DataFrame({'postID': postid_, 'post': post_, 'comment': comment_})
    df.to_csv("medium data/rswtyjs_id_c_c.csv", index=False, sep=',', encoding='utf-8-sig')


def gen_id_c_c_label():
    file = pd.read_csv("medium data/rswtyjs_id_c_label.csv")
    file_post = pd.read_csv("medium data/rswtyjs_postid_pre_final.csv")
    post_label = []
    for i in range(len(file['postID'])):
        post_label.append(' ')

    for i in range(len(file_post['postID'])):
        post_label[int(file_post['postID'][i])] = file_post['postkey'][i]
    print(len(file['postID']))

    post = []
    comment = []
    postid = []

    for i in range(len(file['postID'])):
        if pd.isna(file['postID'][i]):
            print("!!!!!!!")
            post.append(' ')
            postid.append(-1)
        else:
            postid.append(int(file['postID'][i]))
            post.append(post_label[int(file['postID'][i])])
    for i in range(len(file['postID'])):
        if pd.isna(file['comment'][i]):
            comment.append(' ')
        else:
            comment.append(file['comment'][i])

    for i in range(len(comment)):
        if pd.isna(comment[i]):
            print("!!!!!!!")
        else:
            comment[i] = preprocess_text(comment[i])
    print(len(post), len(comment))
    post_ = []
    comment_ = []
    postid_ = []
    label = []
    for i in range(len(post)):
        if len(post[i]) > 9 and len(comment[i]) > 5:
            postid_.append(postid[i])
            post_.append(post[i])
            comment_.append(comment[i])
            label.append(file['label'][i])
    print(len(postid_), len(post_), len(comment_), len(label))
    # df = pd.DataFrame({'post': post_, 'comment': comment_, 'label': label})
    # df.to_csv("medium data/zctytlxz_c_c_label.csv", index=False, sep=',', encoding='utf-8-sig')

    df = pd.DataFrame({'postID': postid_, 'post': post_, 'comment': comment_, 'label': label})
    df.to_csv("medium data/rswtyjs_id_c_c_label.csv", index=False, sep=',', encoding='utf-8-sig')


def show_len_comment():
    file = pd.read_csv("medium data/rswtyjs_c_c.csv")
    file_post = pd.read_csv("medium data/rswtyjs_postid_pre_final.csv")
    post_len = []
    comment_len = []
    for i in file_post['postkey']:
        post_len.append(len(i))
    for i in file['comment']:
        if len(i) == 6:
            print(i)
        comment_len.append(len(i))
    post_len.sort()
    comment_len.sort()

    print(len(post_len), len(list(set(file_post['postID']))), len(list(set(file['post']))))
    print(np.mean(post_len), np.mean(comment_len))
    print(len(post_len))
    print(len(file['comment']), len(list(set(file['comment']))))


def count_vocabulary1():
    vocabulary_set = set()
    file = pd.read_csv("medium data/zctytlxz_c_c_c.csv")
    file_post = pd.read_csv("medium data/zctytlxz_c_c.csv")
    post_result = []
    comment_result = []
    review_result = []
    post_result_ = []
    comment_result_ = []
    for text in file['post']:
        words = jieba.lcut(text)
        post_result.append(words)
        vocabulary_set.update(words)
    print("zctytlxz post finish")
    for text in file['comment']:
        words = jieba.lcut(text)
        comment_result.append(words)
        vocabulary_set.update(words)
    print("zctytlxz comment finish")
    for text in file['review']:
        words = jieba.lcut(text)
        review_result.append(words)
        vocabulary_set.update(words)
    print("zctytlxz review finish")
    for text in file_post['post']:
        words = jieba.lcut(text)
        post_result_.append(words)
        vocabulary_set.update(words)
    print("zctytlxz post finish")
    for text in file_post['comment']:
        words = jieba.lcut(text)
        comment_result_.append(words)
        vocabulary_set.update(words)
    print("zctytlxz comment finish")
    with open("medium data/zctytlxz_dict.txt", 'w', encoding='utf-8') as f:
        for i in vocabulary_set:
            f.write(i)
            f.write('\n')
    df = pd.DataFrame({'post': post_result, 'comment': comment_result, 'review': review_result})
    df.to_csv("medium data/zctytlxz_voc_c_c_c.csv", index=False, sep=',', encoding='utf-8-sig')
    df = pd.DataFrame({'post': post_result_, 'comment': comment_result_})
    df.to_csv("medium data/zctytlxz_voc_c_c.csv", index=False, sep=',', encoding='utf-8-sig')
    print("zctytlxz", len(vocabulary_set))
    return len(vocabulary_set)


def count_vocabulary2():
    vocabulary_set = set()
    file = pd.read_csv("medium data/zctcdh_c_c_c.csv")
    file_post = pd.read_csv("medium data/zctcdh_c_c.csv")
    post_result = []
    comment_result = []
    review_result = []
    post_result_ = []
    comment_result_ = []
    for text in file['post']:
        words = jieba.lcut(text)
        post_result.append(words)
        vocabulary_set.update(words)
    print("zctcdh post finish")
    for text in file['comment']:
        words = jieba.lcut(text)
        comment_result.append(words)
        vocabulary_set.update(words)
    print("zctcdh comment finish")
    for text in file['review']:
        words = jieba.lcut(text)
        review_result.append(words)
        vocabulary_set.update(words)
    print("zctcdh review finish")
    for text in file_post['post']:
        words = jieba.lcut(text)
        post_result_.append(words)
        vocabulary_set.update(words)
    print("zctcdh post finish")
    for text in file_post['comment']:
        words = jieba.lcut(text)
        comment_result_.append(words)
        vocabulary_set.update(words)
    print("zctcdh comment finish")
    with open("medium data/zctcdh_dict.txt", 'w', encoding='utf-8') as f:
        for i in vocabulary_set:
            f.write(i)
            f.write('\n')
    df = pd.DataFrame({'post': post_result, 'comment': comment_result, 'review': review_result})
    df.to_csv("medium data/zctcdh_voc_c_c_c.csv", index=False, sep=',', encoding='utf-8-sig')
    df = pd.DataFrame({'post': post_result_, 'comment': comment_result_})
    df.to_csv("medium data/zctcdh_voc_c_c.csv", index=False, sep=',', encoding='utf-8-sig')
    print("zctcdh", len(vocabulary_set))
    return len(vocabulary_set)


def count_vocabulary3():
    vocabulary_set = set()
    file = pd.read_csv("medium data/sbzjs_c_c_c.csv")
    file_post = pd.read_csv("medium data/sbzjs_postid_pre_final.csv")
    file_comment = pd.read_csv("medium data/sbzjs_c_c.csv")
    for text in file_post['postkey']:
        words = jieba.lcut(text)
        vocabulary_set.update(words)
    print("sbzjs post finish")
    for text in file_comment['comment']:
        words = jieba.lcut(text)
        vocabulary_set.update(words)
    print("sbzjs comment finish")
    for text in file['review']:
        words = jieba.lcut(text)
        vocabulary_set.update(words)
    print("sbzjs review finish")
    with open("medium data/sbzjs_dict_.txt", 'w', encoding='utf-8') as f:
        for i in vocabulary_set:
            f.write(i)
            f.write('\n')
    print("sbzjs", len(vocabulary_set))
    return len(vocabulary_set)


def show_voc_len():
    file = pd.read_csv("medium data/zctytlxz_voc.csv")
    file_cp = pd.read_csv("medium data/zctytlxz_voc.csv")
    post_len = []
    comment_len = []
    review_len = []
    for i in set(file['post']):
        post_len.append(len(i))
    for i in file['comment']:
        comment_len.append(len(i))
    for i in file['review']:
        review_len.append(len(i))
    print("post:", np.mean(post_len), "comment:", np.mean(comment_len), "review:", np.mean(review_len))


# vocabulary_count = count_vocabulary(texts)
# print("唯一词汇数:", vocabulary_count)

# remove_duplicates()
# gen_id_id_id_file()
# gen_postid_pre()
# gen_id_c_c_file()
gen_c_c_c_file()
# show_len()
# gen_id_c()
# gen_id_c_label()
# gen_id_c_c_label()
# gen_c_c()
# show_len_comment()
# print(count_vocabulary1())
# print(count_vocabulary2())
# print(count_vocabulary3())
# print(count_vocabulary4())
# print(count_vocabulary5())

# show_voc_len()


# file = pd.read_csv("rswtyjs_postid.csv")
# post = []
# post_len = []
# for i in range(len(file['postkey'])):
#     if pd.isna(file['postkey'][i]):
#         post.append(' ')
#     else:
#         post.append(file['postkey'][i])
# for i in range(len(post)):
#     if pd.isna(post[i]):
#         print("!!!!!!!")
#     else:
#         post[i] = preprocess_text(post[i])
#         # post_len.append(len(file['postkey'][i]))
# dic = {}
# for i in range(len(file['postID'])):
#     if len(post[i]) > 9:
#         dic[file['postID'][i]] = post[i]
# label = []
# content = []
# for i in dic.keys():
#     label.append(i)
#     content.append(dic[i])
#     post_len.append(len(dic[i]))
# post_len.sort()
# # print(post_len)
# print(np.mean(post_len))
# print(post_len)
# df = pd.DataFrame({'postID': label, 'postkey': content})
# df.to_csv("rswtyjs_postid_pre.csv", index=False, sep=',', encoding='utf-8-sig')

# file = pd.read_csv("rswtyjs_postid.csv")
# file_pre = pd.read_csv("rswtyjs_postid_pre.csv")
# print(len(file['postID']), len(file_pre['postID']))
#
# post_len = []
# for i in range(len(file_pre['postkey'])):
#     if pd.isna(file_pre['postkey'][i]):
#         print("!!!!!!!")
#     else:
#         post_len.append(len(file_pre['postkey'][i]))
# post_len.sort()
# print(post_len)
# print(np.mean(post_len))
# print(len(post_len))

# df = pd.DataFrame({'postID': file['postID'], 'postkey': post})
# df.to_csv("rswtyjs_postid_pre.csv", index=False, sep=',', encoding='utf-8-sig')


# dict = {}
# for i in poster:
#     dict[i] = []
# post = []
# comment = []
# review = []
# for i in range(len(file['是否楼主'])):
#     if file['条'][i] in poster:
#         post.append(file['条'][i])
#         comment.append(file['评论ID'][i])
# print(post)
# print(comment)
# for i in comment:
#     if i in file['针对']:
#         index = file['针对'].index(i)
#         review.append(file['评论ID'][i])
#     else:
#         review.append('')
#
# df = pd.DataFrame({'postID': post, 'comment': comment, 'review': review})
# df.to_csv("rswtyjs_id_id_id.csv", index=False, sep=',', encoding='utf-8-sig')

# post_content = []
# comment_content = []
# review_content = []
# for i in comment:
#     index = file['评论ID'].index(i)
#     comment_content.append(file['评论内容'][index])
#
# for i in review:
#     if i != '':
#         index = file['评论ID'].index(i)
#         review_content.append(file['评论内容'][index])
#     else:
#         review_content.append('')

# df = pd.DataFrame({'postID': post, 'comment': comment_content, 'review': review_content})
# df.to_csv("rswtyjs_id_c_c.csv", index=False, sep=',', encoding='utf-8-sig')
