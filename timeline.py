
#----------------------------------------------------------------------------------#
class User():

    #---------------------------------------------------------#
    def __init__(self, login_flag):
        self.login_flag = login_flag

        if login_flag:
            self.following, self.my_posts, self.others_posts = fetch_data()

    #---------------------------------------------------------#
    def make_post(self):
        #user_input = input('Insert text: ')
        user_input = "Pru!"
        print('Your post: %s' % (user_input))
        # add post to my_posts
        return(user_input)

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
        save_data(self.following, self.my_posts, self.others_posts)

