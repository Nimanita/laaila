from lender.database.MongoConnection import MongoConnection

class contractsDao(MongoConnection):

    def __init__(self):
        super(contractsDao, self).__init__()
        self.get_collection("contracts")
    
    def addContracts(self, contract):
        result = self.collection.insert_one(contract)
        return result.acknowledged
    
    def getSortDictForGroupingQuery(self, sortQuery, countKey):
        if sortQuery and sortQuery[0]:
            if sortQuery[0][0] == countKey:
                return {countKey: sortQuery[0][1]}
            return {"_id."+str(sortQuery[0][0]): sortQuery[0][1]}

    def getDistributionForLendor(self, filterQuery, sortQuery, skip, limit):
      
        lendors = self.collection.aggregate(
            [{
                "$match": filterQuery
            },
                {
                    "$group": {
                        "_id": {"lendorId": "$lendorId"},
                        "count": {
                            "$sum": 1
                        },
                       
                        "borrowerDetails" : {"$push" : {
                        "principle" : "$principle",
                        "borrowerId" : "$borrowerId",
                        "loanStartDate" : "$loanStartDate",
                        "loanDueDate" : "$loanDueDate"
                        }},
                       "avg": { "$avg" : "$principle" }
                      
                    }
                },
                {
                    "$sort": self.getSortDictForGroupingQuery(sortQuery, countKey="count")
                },
                {
                    '$skip': skip
                },
                {
                    '$limit': limit
                }
            ]
        )
        
        
        count = self.collection.aggregate(
            [
                {
                    "$match": filterQuery
                },
                {
                    "$group": {
                        "_id": {"lendorId": "$lendorId"}
                    }
                },
                {
                    "$count": "totalCount"
                }
            ]
        )
        
        lendors = list(lendors)
        counterCursor = list(count)
        
        totalResults = counterCursor[0]["totalCount"] if counterCursor else 0
       
        return lendors, totalResults
    
    def getDistributionForBorrower(self, filterQuery, sortQuery, skip, limit):
      
        lendors = self.collection.aggregate(
            [{
                "$match": filterQuery
            },
                {
                    "$group": {
                        "_id": {"borrowerId": "$borrowerId"},
                        "count": {
                            "$sum": 1
                        },
                       "lendorDetails" : {"$push" : {
                        "principle" : "$principle",
                        "lendorId" : "$lendorId",
                        "loanStartDate" : "$loanStartDate",
                        "loanDueDate" : "$loanDueDate"
                        }},
                       "avg": { "$avg" : "$principle" }
                        
                      
                    }
                },
                {
                    "$sort": self.getSortDictForGroupingQuery(sortQuery, countKey="count")
                },
                {
                    '$skip': skip
                },
                {
                    '$limit': limit
                }
            ]
        )
        
        
        count = self.collection.aggregate(
            [
                {
                    "$match": filterQuery
                },
                {
                    "$group": {
                        "_id": {"borrowerId": "$borrowerId"}
                    }
                },
                {
                    "$count": "totalCount"
                }
            ]
        )
        
        lendors = list(lendors)
        counterCursor = list(count)
        
        totalResults = counterCursor[0]["totalCount"] if counterCursor else 0
       
        return lendors, totalResults
   
    def findContract(self , contract):
        count = self.collection.count_documents({"borrowerId" : contract["borrowerId"] , "lendorId" : contract["lendorId"]})
        return count
    
    