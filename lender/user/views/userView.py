from rest_framework.decorators import api_view , permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from user.service.userService import userService
from user.service.contractsService import contractsService

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def handleUserOperation(request):
   
    if request.method == 'POST':
        requestBody = JSONParser().parse(request)
        
        return userService.addUser(requestBody)
    
    if request.method == 'GET':
        return userService.getUsers(True)


@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def handleAdminOperation(request):
    if request.method == 'POST':
        requestBody = JSONParser().parse(request)
        return contractsService.addContracts(requestBody)
    
    if request.method == 'GET':
        return contractsService.getUserDistributionHistory()

