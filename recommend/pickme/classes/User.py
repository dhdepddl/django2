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


class UserDB(models.Model):
    user_id = models.CharField(max_length=30, primary_key=True)
    topic_rating = models.CharField(max_length=200)


class User:
    def __init__(self, id):
        self.id = id
        self.similar_users = None
        self.topic_rating = None

    def saveDB(self):
        try:
            user = UserDB.objects.get(user_id=self.id)
        except:
            UserDB(user_id=self.id, topic_rating=str(self.topic_rating)).save()
        else:
            user.topic_rating = self.topic_rating
            user.save()

    def get_topic_rating(self, test_data_path, topic_set):
        import lda_module as lda
        user_contents = lda.get_user_post(test_data_path, self.id)
        doc_user, noun = lda.make_noun_set(user_contents)
        rst_topics = []
        tp_len = len(topic_set)
        for i in range(tp_len):
            rst_topics.append(0)
        for i in range(tp_len):
            for doc in doc_user:
                word_cnt = count_word_in_topic(doc, topic_set[i])
                rst_topics[i] += word_cnt
        self.topic_rating = rst_topics

    def get_similar_users(self, numOfuser, setOfothers):
        from similarity import most_similar_cosine
        target_user_rating = {'user': self.id, 'rating_list': self.topic_rating}
        user_rating = []
        for user in setOfothers:
            try:
                user_rating.append({'user': user.id, 'rating_list': user.topic_rating})
            except TypeError:
                print 'Set of others is not a set of User class'
                exit(-1)
        self.similar_users = most_similar_cosine(target_user_rating, user_rating, numOfuser)
