# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


def count_word_in_topic(doc, words):
    cnt = 0
    for noun in doc:
        for word in words:
            if noun == word:
                cnt += 1
    return cnt


def rating_doc(doc, topic_set):
    rst_topics = []
    tp_len = len(topic_set)
    for i in range(tp_len):
        rst_topics.append(0)

    sum = 0
    for i in range(tp_len):
        word_cnt = count_word_in_topic(doc, topic_set[i])
        rst_topics[i] += word_cnt
        sum += word_cnt

    return rst_topics


class Post(models.Model):
    user = models.ForeignKey('auth.User')
    post_id = models.CharField(db_index=True, max_length=30)
    title = models.CharField(max_length=100)
    item_1 = models.CharField(max_length=20)
    item_2 = models.CharField(max_length=20)
    created = models.DateTimeField()
    topic = []
    #
    # def __init__(self, postId, user, title, item1, item2):
    #     import os
    #     self.user = user
    #     self.post_id = postId
    #     self.title = title
    #     self.item_1 = item1
    #     self.item_2 = item2
    #     self.topic = []
    #     if os.name == 'posix' or 'mac':
    #         from konlpy.tag import Mecab
    #         self.noun_set = Mecab().nouns(title)
    #     else:
    #         from konlpy.tag import Twitter
    #         self.noun_set = Twitter().nouns(title)

    def get_topic(self, topic_set, numOftopic):
        try:
            cnt_list = rating_doc(self.noun_set, [x.words for x in topic_set])
        except AttributeError as e:
            print (str(e) + '. first parameter must be a list of Topic class instance')
        else:
            self.topic = []
            topic_cnts = cnt_list[:]
            topic_cnts.sort()
            topic_cnts.reverse()
            topNval = topic_cnts[:numOftopic]
            for i in range(numOftopic):
                self.topic.append({'topic': cnt_list.index(topNval[i]), 'count': topNval[i]})
                cnt_list[cnt_list.index(topNval[i])] = 0

    def printpost(self):
        user = self.user
        if self.user is None: user = u''
        text = self.title
        if self.title is None: text = u''
        top = [str(x['topic']) for x in self.topic]
        print u'user: ' + user + u'\ntext: ' + text + u'\ntopic: ' + u', '.join(top).encode('utf-8').strip()

    def json(self):
        import json
        return json.dumps({"user": self.user, "title": self.title, "topic": self.topic})
