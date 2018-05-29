from db import first_login, fetch_data, save_data
from ui import print_info, get_user_input
from datetime import datetime

#----------------------------------------------------------------------------------#
class User():

    #---------------------------------------------------------#
    def __init__(self):
        self.login_flag, self.db = first_login()
        print_info("1st login: " + str(self.login_flag))

        if self.login_flag:
            self.following = []
            self.my_posts = []
            self.others_posts = [] 

        else:
            self.email, self.following, \
            self.my_posts, self.others_posts = fetch_data(self.db)

    #---------------------------------------------------------#
    def make_post(self):
        text = get_user_input("Write New Post: ")
        post = {"from": self.email, \
                "date": datetime.now(), \
                "text": text}

        self.my_posts.append(post)
        return post

    #---------------------------------------------------------#
    def follow(self):
        email = get_user_input("Insert User Email: ")

        if email in self.following:
            print_info("Failure: Already following " + email)
            return False, ""

        else:
            self.following.append(email)
            print_info("Sucess: Now following " + email)
            return True, email

    #---------------------------------------------------------#
    def unfollow(self):
        email = get_user_input("Insert User Email: ")

        if email in self.following:
            self.following.remove(email)
            print_info("Success: Unfollowed " + email)

        else:
            print_info("Failure: Not following " + email)

    #---------------------------------------------------------#
    def save(self):
        d_email = {"email": self.email}
        
        d_following = []
        for f in self.following:
            d_following.append({"email": f})

        save_data(self.db, d_email, d_following, \
                  self.my_posts, self.others_posts)
