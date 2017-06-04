from firebase import FirebaseAuthentication, FirebaseApplication, firebase
from User import User
import operator


class Firebase:
    def __init__(self, user_id):
        auth = FirebaseAuthentication('kUFM5wAt2CkXtfKrglMjLPgNsuWsO33j1uKHMRyn', 'dhdepddl@gmail.com', True, True)
        self.db = firebase.FirebaseApplication('https://pickme-f283e.firebaseio.com', auth)
        self.user_id = user_id
        self.posts = {}
        self.votes = {}
        self.hearts = {}
        self.comments = {}
        self.bookmarks = {}
        self.user_cards = {}
        self.user_hearts = {}
        self.user_bookmarks = {}

    def get_all_data(self):
        total_data = self.db.get('/', None)
        self.posts = total_data['cards']['data']
        self.votes = total_data['item-selected']
        self.hearts = total_data['card-hearts']
        self.comments = total_data['card-comments']
        self.bookmarks = total_data['card-bookmarks']
        try:
            self.user_cards = total_data['user-cards'][self.user_id]
            self.user_hearts = total_data['user-hearts'][self.user_id]
            self.user_bookmarks = total_data['user-bookmarks'][self.user_id]
        except:
            self.user_cards = {}
            self.user_hearts = {}
            self.user_bookmarks = {}

    def is_deleted(self, post_info):
        if u'deleted' in post_info[1].keys():
            return True
        return False

    def vote_info(self, user_id, post_id):
        try:
            votes = self.votes[post_id]
            voted_1 = 0
            voted_2 = 0
            selected = 0
            for item in votes.items():
                uid = item[0]
                choice_num = item[1]
                if user_id == uid:
                    selected = choice_num
                if choice_num == 1:
                    voted_1 += 1
                elif choice_num == 2:
                    voted_2 += 1
        except KeyError:
            return {"voted_1": 0, "voted_2": 0, "selected": 0}
        else:
            return {"voted_1": voted_1, "voted_2": voted_2, "selected": selected}

    def heart_info(self, user_id, post_id):
        try:
            hearts_dic = self.hearts[post_id]
            hearts = 0
            heart_state = 0
            for item in hearts_dic.items():
                uid = item[0]
                if uid == user_id:
                    heart_state = 1
                hearts += 1
        except KeyError:
            return {"hearts": 0, "heart_state": 0}
        else:
            return {"hearts": hearts, "heart_state": heart_state}

    def comment_info(self, user_id, post_id):
        info = {"comments": 0}
        try:
            comments_dic = self.comments[post_id]['ids']
        except KeyError:
            return {"comments": 0}
        return {"comments": len(comments_dic)}

    def bookmark_info(self, user_id, post_id):
        try:
            bookmarks_dic = self.bookmarks[post_id]
            bookmarks = 0
            bookmark_state = 0
            for item in bookmarks_dic.items():
                uid = item[0]
                if uid == user_id:
                    bookmark_state = 1
                bookmarks += 1
        except KeyError:
            return {"bookmarks": 0, "bookmark_state": 0}
        else:
            return {"bookmarks": bookmarks, "bookmark_state": bookmark_state}

    def get_card(self, user_id, card_info):
        result = card_info
        post_id = card_info['id']
        result.update(self.vote_info(user_id, post_id))
        result.update(self.heart_info(user_id, post_id))
        result.update(self.comment_info(user_id, post_id))
        result.update(self.bookmark_info(user_id, post_id))
        return result

    def get_card_with_id(self, user_id, card_id):
        self.get_all_data()
        post_id = card_id
        try:
            result = self.posts[post_id]
        except:
            return {}
        else:
            result.update(self.vote_info(user_id, post_id))
            result.update(self.heart_info(user_id, post_id))
            result.update(self.comment_info(user_id, post_id))
            result.update(self.bookmark_info(user_id, post_id))
            return result

    def get_cards(self, user_id, num_of_recommend):
        result = []

        self.get_all_data()

        # For each card
        for post in self.posts.items():
            if self.is_deleted(post):
                continue
            post_info = post[1]
            result.append(self.get_card(user_id, post_info))

        result.sort(key=operator.itemgetter('created'))
        result += self.recommend(user_id, num_of_recommend)

        return {'cards': result}

    def recommend(self, user_id, num_of_cards):

        result = []
        return result