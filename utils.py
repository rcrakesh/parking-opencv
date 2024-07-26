from pymongo import MongoClient
# def get_db_handle():

client = MongoClient('localhost', 27017)
db = client['usere']
collection = db['subscription_subscription']


# -------------------------just database info -------------------------------------------------------------------------