class ViewUtils:

    
    @classmethod
    def getIsUIFlag(cls, request):
        isUI = request.GET.get('isUI', None)
        if isUI and isUI.lower() == 'true':
            return True
        return False
    
   