from firebase import FirebaseAuthentication, FirebaseApplication, firebase
from User import User


class Firebase:
    def __init__(self):
        auth = FirebaseAuthentication('kUFM5wAt2CkXtfKrglMjLPgNsuWsO33j1uKHMRyn', 'dhdepddl@gmail.com', True, True)
        self.db = firebase.FirebaseApplication('https://pickme-f283e.firebaseio.com/', auth)

    def get_initial_users(self, user_list):
        users = list(self.db.get('/user-profiles/data', None, {'print': 'pretty'}))
        for user in users:
            user_list.append(User(user))

    def get_initial_posts(self):
        posts = self.db.get('cards/data', None)
        return posts
