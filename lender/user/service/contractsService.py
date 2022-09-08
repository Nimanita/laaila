from user.dao.contractsDao import contractsDao
import json
import traceback
from user.utils.ResponseFormatter import ResponseFormatter
import logging
from rest_framework import status
from user.service.userService import userService
from user.utils.Validator import Validator

from bson.json_util import dumps
log = logging.getLogger(__name__)

class contractsService:

    contractsDao = contractsDao()
    SEARCHABLE_KEYS = []

    @classmethod
    def addContracts(cls, contract , isUI=False):
        try:
            result , message = Validator.validateContract(contract)
            if not result:
                return ResponseFormatter.formatAndReturnResponse({"message" : message}, status.HTTP_400_BAD_REQUEST, isUI)
            isExist , message = cls.isContractExist(contract)
            if isExist:
                return ResponseFormatter.formatAndReturnResponse({"message" : message}, status.HTTP_500_INTERNAL_SERVER_ERROR, isUI)

   
            result = cls.contractsDao.addContracts(contract)
            print(result)
            return ResponseFormatter.formatAndReturnResponse({"message" : "Contracts added successfully"}, status.HTTP_200_OK, isUI)
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while adding contracts" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            print(message)
            return ResponseFormatter.formatAndReturnResponse({"message" : "Failed to add contracts"}, status.HTTP_500_INTERNAL_SERVER_ERROR, isUI)

    @classmethod
    def getLendorsDistribution(cls, isUI=False):
       
        try:
           
            filterQuery = {"isRepaid" : False}
            
            groupedlendorNames, totalResults = cls.contractsDao.getDistributionForLendor(filterQuery, sortQuery=[("_id", -1)], skip=0, limit=1000)
       
            return groupedlendorNames
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while getting lender distribution" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            return None
        
    @classmethod
    def getBorrowersDistribution(cls, isUI=False):
       
        try:
           
            filterQuery = {"isRepaid" : False}
            
            groupedborrowerNames, totalResults = cls.contractsDao.getDistributionForBorrower(filterQuery, sortQuery=[("_id", -1)], skip=0, limit=1000)
            return groupedborrowerNames
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while getting borrower distribution" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
         
            return None 
        
    @classmethod
    def getUserInfo(cls):
        users = userService.getUsers()
        if users:
            users = json.loads(dumps(users))
            return users
        return None
        
    @classmethod
    def getUserDistributionHistory(cls, isUI=False):
       
        try:
            
            groupedlendorNames = cls.getLendorsDistribution()
            groupedborrowerNames = cls.getBorrowersDistribution()
            users = cls.getUserInfo()
            
            userDistributionHistory = cls.addUserInfoInDistribution(groupedlendorNames , groupedborrowerNames , users)
            return ResponseFormatter.formatAndReturnResponse(userDistributionHistory, status.HTTP_200_OK, isUI)
      
                    
            
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while getting user distribution history" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            print(message)
            return ResponseFormatter.formatAndReturnResponse({"message" : "Failure while getting user distribution history"}, status.HTTP_500_INTERNAL_SERVER_ERROR, isUI)
    
    @classmethod
    def addUserInfoInDistribution(cls, groupedlendorNames , groupedborrowerNames , users):
        groupedlendorNamesMap = {}
        groupedborrowerNamesMap = {}
        userDetailMap = {}
        
        if groupedlendorNames:
            for lendor in groupedlendorNames:
                if "_id" in lendor and "lendorId" in lendor["_id"]:
                    groupedlendorNamesMap[lendor["_id"]["lendorId"]] = lendor
                    
        if groupedborrowerNames:
            for borrower in groupedborrowerNames:
                if "_id" in borrower and "borrowerId" in borrower["_id"]:
                    groupedborrowerNamesMap[borrower["_id"]["borrowerId"]] = borrower
                
        for user in users:
            if "_id" in user and "$oid" in user["_id"]:
                userId = user["_id"]["$oid"]
                userDetailMap[userId] = user
            
        if users:
            
            userdetails = []
            for user in users:
                if "_id" not in user or "$oid" not in user["_id"]:
                    continue
                if "name" not in user:
                    continue
                if "phoneNumber" not in user:
                    continue
                
                userId = user["_id"]["$oid"]
                userdetail = {}
                userdetail["id"] = userId
                userdetail["name"] = user["name"]
                userdetail["phoneNumber"] = user["phoneNumber"]
                
                
                if userId in groupedlendorNamesMap:
                    userdetail["borrowerCount"] = groupedlendorNamesMap[userId]["count"]
                    userdetail["borrowerAverageAmount"] = groupedlendorNamesMap[userId]["avg"]
                    userdetail["borrowerDetails"] = groupedlendorNamesMap[userId]["borrowerDetails"]
                   
                    
                    for borrowerdetail in userdetail["borrowerDetails"]:
                        borrowerId = borrowerdetail["borrowerId"]
                        borrowerdetail["name"]= userDetailMap[borrowerId]["name"]
                        
                        
                else:
                    userdetail["borrowerCount"] = 0
                    
                if userId in groupedborrowerNamesMap:
                    userdetail["lendorCount"] = groupedborrowerNamesMap[userId]["count"]
                    userdetail["lendorAverageAmount"] = groupedborrowerNamesMap[userId]["avg"]
                    userdetail["lendorDetails"] = groupedborrowerNamesMap[userId]["lendorDetails"]
                   
                    for lendordetail in userdetail["lendorDetails"]:
                        
                        lendorId = lendordetail["lendorId"]
                        
                        lendordetail["name"]= userDetailMap[lendorId]["name"]
                else:
                    userdetail["lendorCount"] = 0
                userdetails.append(userdetail)
                
            return userdetails
        
    @classmethod
    def isContractExist(cls , contract):
        isBorrowerIdExist = userService.findUserId(contract["borrowerId"])
        isLendorIdExist = userService.findUserId(contract["lendorId"])
        print(isBorrowerIdExist , "isBorrowerIdExist" ,isLendorIdExist , "isLendorIdExist" )
        if not isBorrowerIdExist or not isLendorIdExist:
            return True , "Invalid User Id"
        
        count = cls.contractsDao.findContract(contract)
        if count :
            return True , "Contract Already exists"
        
        return False , None