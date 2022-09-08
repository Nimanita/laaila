from lender.database.MongoConnection import MongoConnection

class userDao(MongoConnection):

    def __init__(self):
        super(userDao, self).__init__()
        self.get_collection("user")
    
    def addUser(self, name , phoneNumber):
        result = self.collection.insert_one({"name" : name , "phoneNumber" : phoneNumber})
        return result.acknowledged
    
    def getUser(self):
        cursor = self.collection.find()
        return list(cursor)
    
    def findUser(self , user):
        count = self.collection.count_documents({"name" : user["name"] , "phoneNumber" : user["phoneNumber"]})
        return count
    
    def findUserId(self , id):
        count = self.collection.count_documents({"_id" : { "$toObjectId": id}})
        return count