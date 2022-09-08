from user.dao.userDao import userDao
import json
import traceback
from user.utils.ResponseFormatter import ResponseFormatter
import logging
from rest_framework import status
from user.utils.Validator import Validator
log = logging.getLogger(__name__)

class userService:

    userDao = userDao()
    SEARCHABLE_KEYS = []

    @classmethod
    def addUser(cls, user, isUI=False):
        try:
            
            result , message = Validator.validateUser(user)
            if not result:
                return ResponseFormatter.formatAndReturnResponse({"message" : message}, status.HTTP_400_BAD_REQUEST, isUI)
            isExist = cls.findUser(user)
            if isExist:
                return ResponseFormatter.formatAndReturnResponse({"message" : "User already exists"}, status.HTTP_500_INTERNAL_SERVER_ERROR, isUI)

            result = cls.userDao.addUser(user["name"] , user["phoneNumber"])
          
            return ResponseFormatter.formatAndReturnResponse({"message" : "User added successfully"}, status.HTTP_200_OK, isUI)
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while adding user" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            print(message)
            return ResponseFormatter.formatAndReturnResponse({"message" : " Failed to add user"}, status.HTTP_500_INTERNAL_SERVER_ERROR, isUI)

    @classmethod
    def getUsers(cls, isUI=False):
        try:
           
            result = cls.userDao.getUser()
            return result
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while adding user" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            
            return None
    
    @classmethod
    def findUser(cls, user):
        try:
           
            count = cls.userDao.findUser(user)
            if count:
                return True
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while finding user" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            
            return False
    
    @classmethod
    def findUserId(cls, userId):
        try:
           
            count = cls.userDao.findUserId(userId)
            if count:
                return True
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while finding userId" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            
            return False
