
#----------------------------------------------------------------------------------#
class User():

    #---------------------------------------------------------#
    def __init__(self, login_flag):
        self.login_flag = login_flag

        if login_flag:
            self.followers, self.following, self.my_posts, self.others_posts = fetch_data()

    #---------------------------------------------------------#
    def make_post(self):
        #user_input = input('Insert text: ')
        user_input = "Pru!"
        print('Your post: %s' % (user_input))
        # add post to my_posts
        return(user_input)

    #---------------------------------------------------------#
    def get_followers(self):
        return self.followers

    #---------------------------------------------------------#
    def get_following(self):
        return self.following

    #---------------------------------------------------------#
    def follow(self):
        #email = input('Insert user email: ')
        email = "pru@pru.pru"
        if True: # check if email is in following
            # error message
            return False, ""
        else:
            # add email to following
            return True, "email"

    #---------------------------------------------------------#
    def unfollow(self):
        #email = input('Insert user email: ')
        email = "pru@pru.pru"
        if True: # check if email is in following
            # remove email from following
            return True
        else:
            # error message
            return False

    #---------------------------------------------------------#
    def save(self):
        save_data(self.followers, self.following, self.my_posts, self.others_posts)


#----------------------------------------------------------------------------------#
def fetch_data():

    #---------------------------------------------------------#
    def fetch_followers():
        # fetch from disk
        return 0

    #---------------------------------------------------------#
    def fetch_following():
        # fetch from disk
        return 0

    #---------------------------------------------------------#
    def fetch_my_posts():
        # fetch from disk
        return 0

    #---------------------------------------------------------#
    def fetch_others_posts():
        # fetch from disk
        return 0

    followers = fetch_followers()
    following = fetch_following()
    my_posts = fetch_my_posts()
    others_posts = fetch_others_posts()

    return followers, following, my_posts, others_posts


#----------------------------------------------------------------------------------#
def save_data(followers, following, my_posts, others_posts):

    #---------------------------------------------------------#
    def save_followers(followers):
        print()
        # fetch to disk

    #---------------------------------------------------------#
    def save_following(following):
        print()
        # fetch to disk

    #---------------------------------------------------------#
    def save_my_posts(my_posts):
        print()
        # fetch to disk

    #---------------------------------------------------------#
    def save_others_posts(others_posts):
        print()
        # fetch to disk

    save_followers(followers)
    save_following(following)
    save_my_posts(my_posts)
    save_others_posts(others_posts)
