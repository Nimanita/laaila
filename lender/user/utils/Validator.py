from datetime import date
from django.http import JsonResponse
from rest_framework import status
import re
from bson import ObjectId

class Validator:

    @classmethod
    def validateUser(cls, user):
        
        if not(isinstance(user, dict)):
            return False , "Invalid User type"
        
        if "name" not in user or "phoneNumber" not in user:
            return False , "Incomplete User info"
        
        if len(user["name"]) == 0 or len(user["name"]) > 50 :
            return False , "Invalid User length"
        
        if len(user["phoneNumber"]) < 10 or len(user["phoneNumber"]) > 10 :
            return False , "Invalid User phoneNumber length"
        
        result = re.match(r"^[0-9]*$",user["phoneNumber"])
        if not result:
            return False , "Invalid User phoneNumber"
        
          
        return True , None
    
    @classmethod
    def validateContract(cls, contract):
        
        keys = ["principle" , "lendorId" , "borrowerId" , "loanStartDate" , "loanDueDate" , "isRepaid" , "interestRate"]
        if not(isinstance(contract, dict)):
            return False , "Invalid Contract type"
        
        for key in keys:
            if key not in contract:
                return False , "Incomplete Contract info"
            if key == "principle" and not(isinstance(contract["principle"], int)):
                return False , "Invalid principle type"
            if key == "interestRate" and not(isinstance(contract["interestRate"], int)):
                return False , "Invalid interestRate type"
            if key == "isRepaid" and not(isinstance(contract["isRepaid"], bool)):
                return False , "Invalid isRepaid type"
        
        if not ObjectId.is_valid(contract["borrowerId"]) or not ObjectId.is_valid(contract["lendorId"]):
            return False , "Invalid Contract id type" 
           
        return True , None