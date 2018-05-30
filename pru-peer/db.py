from pymongo import MongoClient
from datetime import datetime

'''
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/
sudo service mongod start
sudo service mongod stop
sudo service mongod restart
mongo --host 127.0.0.1:27017
cat /var/log/mongodb/mongod.log
'''

#----------------------------------------------------------------------------------#
def fetch_data(db):

    #---------------------------------------------------------#
    def fetch_id():
        return db.id.find_one()['id']

    #---------------------------------------------------------#
    def fetch_email():
        return db.email.find_one()['email']

    #---------------------------------------------------------#
    def fetch_following():
        following = {}

        for f in db.following.find():
            following[f['email']] = f['id']

        return following

    #---------------------------------------------------------#
    def fetch_my_posts():
        my_posts = []

        for p in db.my_posts.find():
            my_posts.append({"from": p['from'],\
                             "id": p['id'],\
                             "date": p['date'],\
                             "text": p['text']})
        return my_posts

    #---------------------------------------------------------#
    def fetch_others_posts():
        others_posts = []

        for p in db.others_posts.find():
            others_posts.append({"from": p['from'],\
                                 "id": p['id'],\
                                 "date": p['date'],\
                                 "text": p['text']})
        return others_posts

    #---------------------------------------------------------#
    id = fetch_id()
    email = fetch_email()
    following = fetch_following()
    my_posts = fetch_my_posts()
    others_posts = fetch_others_posts()

    return email, id, following, my_posts, others_posts


#----------------------------------------------------------------------------------#
def save_data(db, email, id, following, my_posts, others_posts):

    #---------------------------------------------------------#
    def save_id(id):
        if db.id.find().count() == 0:
            db.id.insert(id)

    #---------------------------------------------------------#
    def save_email(email):
        if db.email.find().count() == 0:
            db.email.insert(email)

    #---------------------------------------------------------#
    def save_following(following):
        for f in following:
            if db.following.find(f).count() == 0:
                db.following.insert_one(f)

    #---------------------------------------------------------#
    def save_my_posts(my_posts):
        for p in my_posts:
            if db.my_posts.find(p).count() == 0:
                db.my_posts.insert_one(p)

    #---------------------------------------------------------#
    def save_others_posts(others_posts):
        # dont save if the posts are too old
        for p in others_posts:
            if db.others_posts.find(p).count() == 0:
                db.others_posts.insert_one(p)

    #---------------------------------------------------------#
    save_id(id)
    save_email(email)
    save_following(following)
    save_my_posts(my_posts)
    save_others_posts(others_posts)


#----------------------------------------------------------------------------------#
def first_login():
    client = MongoClient('localhost', 27017)
    db = client['pru-user']

    names = client.database_names()
    if 'pru-user' in names:
        return False, db
    else:
        return True, db

#----------------------------------------------------------------------------------#
def drop_db():
    client = MongoClient('localhost', 27017)
    client.drop_database('pru-user')

'''
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['pru-user']
for p in db.followers.find():
    print(p)


client.database_names()
client.drop_database('pru-user')
'''
