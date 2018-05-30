from db import first_login, fetch_data, save_data
from ui import print_info, get_user_input
from datetime import datetime

#----------------------------------------------------------------------------------#
class User():

    #---------------------------------------------------------#
    def __init__(self):
        self.login_flag, self.db = first_login()
        #self.login_flag = True
        print_info("1st login: " + str(self.login_flag))

        if self.login_flag:
            self.id = 1
            self.following = {}
            self.my_posts = []
            self.others_posts = []

        else:
            self.email, self.id, self.following, \
            self.my_posts, self.others_posts = fetch_data(self.db)

    #---------------------------------------------------------#
    def make_post(self):
        text = get_user_input("Write New Post: ")
        post = {"from": self.email, \
                "id": self.id, \
                "date": datetime.now().strftime("%y/%m/%d %H:%M:%S"), \
                "text": text}
        self.my_posts.append(post)
        self.id += 1
        return post

    #---------------------------------------------------------#
    def follow(self):
        email = get_user_input("Insert User Email")

        if email in self.following:
            print_info("Failures: Already following " + email)

        else:
            self.following[email] = 0
            print_info("Success: Now following " + email)

    #---------------------------------------------------------#
    def unfollow(self):
        email = get_user_input("Insert User Email")

        if email in self.following:
            del self.following[email]
            print_info("Success: Unfollowed " + email)

        else:
            print_info("Failure: Not following " + email)

    #---------------------------------------------------------#
    def save(self):
        d_email = {"email": self.email}
        d_id = {"id": self.id}

        d_following = []
        for key, value in self.following.items():
            d_following.append({"email": key, "id": value})

        save_data(self.db, d_email, d_id, d_following, \
                  self.my_posts, self.others_posts)
