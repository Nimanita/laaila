from django.http import JsonResponse
from rest_framework import status
from collections import Mapping

class ResponseFormatter:

    @classmethod
    def formatAndReturnResponse(cls, data, status, isUI, pageInfo=None):
        if isUI:
            response = dict()

            if pageInfo:
                response.update(dict(pageInfo=pageInfo))

            response['data'] = data
            return JsonResponse(response, safe=False, status=status)
        else:
            return JsonResponse(data, safe=False, status=status)

    @classmethod
    def returnUnauthorizedResponse(cls, data, isUI):
        if isinstance(data, Mapping):
            data.setdefault("message", "Unauthorized request")
        return ResponseFormatter.formatAndReturnResponse(data, status=status.HTTP_401_UNAUTHORIZED, isUI=isUI)
