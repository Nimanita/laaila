from user.dao.userDao import userDao
import json
import traceback
from user.utils.ResponseFormatter import ResponseFormatter
import logging
from rest_framework import status
from user.utils.Validator import Validator
from bson.json_util import dumps
log = logging.getLogger(__name__)

class userService:

    userDao = userDao()
    SEARCHABLE_KEYS = []

    @classmethod
    def addUser(cls, user, isUI=False):
        try:
            
            result , message = Validator.validateUser(user)
            print(message)
            if not result:
                return ResponseFormatter.formatAndReturnResponse({"message" : message}, status.HTTP_400_BAD_REQUEST, isUI)
            isExist = cls.findUser(user)
            if isExist:
                return ResponseFormatter.formatAndReturnResponse({"message" : "User already exists"}, status.HTTP_500_INTERNAL_SERVER_ERROR, isUI)

            result , userId= cls.userDao.addUser(user["name"] , user["phoneNumber"])
            if result:
                return ResponseFormatter.formatAndReturnResponse({"message" : f"User added successfully and user id is {userId}"}, status.HTTP_200_OK, isUI)
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
            if not isUI:
                return result
            else:
                if result:
                    users = json.loads(dumps(result))
                    return ResponseFormatter.formatAndReturnResponse(users, status.HTTP_200_OK, isUI)

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
            print("inside dao")
            count = cls.userDao.findUserId(userId)
            if count:
                return True
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while finding userId" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            
            return False
