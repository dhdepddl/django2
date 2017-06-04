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

class PostDB(models.Model):
    user_id = models.ForeignKey('auth.User')
    post_id = models.CharField(primary_key=True, max_length=30)
    topic = models.SmallIntegerField(null=True)
    topic_2 = models.SmallIntegerField(null=True)
    created = models.BigIntegerField(db_index=True)

class Post():
    def __init__(self, postId, user, title, item1, item2, created):
        from konlpy.tag import Twitter
        twitter = Twitter()
        self.user_id = user
        self.post_id = postId
        title = [x[0] for x in twitter.pos(title, norm=True, stem=True) if x[1] == 'Noun' or x[1] == 'Verb']
        item_1 = [x[0] for x in twitter.pos(item1, norm=True, stem=True) if x[1] == 'Noun' or x[1] == 'Verb']
        item_2 = [x[0] for x in twitter.pos(item2, norm=True, stem=True) if x[1] == 'Noun' or x[1] == 'Verb']
        self.topic = []
        self.noun_set = title + item_1 + item_2
        self.created = created

    def __str__(self):
        return self.post_id

    def save_db(self):
        try:
            post = PostDB.objects.get(post_id=self.post_id)
        except:
            PostDB(user_id=self.user_id, post_id=self.post_id, topic=self.topic[0], topic2=self.topic[1], created=self.created).save()
        else:
            post.topic = self.topic[0]
            post.topic2 = self.topic[1]
            post.save()

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
