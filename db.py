from pymongo import MongoClient

# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/
# sudo service mongod start
# sudo service mongod stop
# sudo service mongod restart
# mongo --host 127.0.0.1:27017
# cat /var/log/mongodb/mongod.log

#----------------------------------------------------------------------------------#
def fetch_data():

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

    following = fetch_following()
    my_posts = fetch_my_posts()
    others_posts = fetch_others_posts()

    return following, my_posts, others_posts


#----------------------------------------------------------------------------------#
def save_data(following, my_posts, others_posts):

    #---------------------------------------------------------#
    def save_following(following):
        print()
        # save to disk

    #---------------------------------------------------------#
    def save_my_posts(my_posts):
        print()
        # save to disk

    #---------------------------------------------------------#
    def save_others_posts(others_posts):
        print()
        # save to disk

    save_following(following)
    save_my_posts(my_posts)
    save_others_posts(others_posts)


client = MongoClient('localhost', 27017)
db = client['test_database']

follower = {"email": "carlos@pru.pru"}

followers = db.followers
id = followers.insert(follower).inserted_id

db.collection_names(include_system_collections=False)