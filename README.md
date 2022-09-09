# laaila
| Api Name | Method | Response | Use
| --- | --- | --- | --- | 
| ngrokpath/**api-token-auth/** | POST | {<br/> "token": "XXXXX" }<br/> | To get token which you need to add under authorisation header to use the api 
| ngrokpath/**user** | POST | {<br/> "message": "User added successfully and user id is XXXX" }<br/> | To add the user
| ngrokpath/**user** | GET | list of all user along with their id , name and phone number | To get list of all user (Created for testing)
| ngrokpath/**contracts** | POST | {<br/> "message": "Contracts added successfully" }<br/><br/> | To add the contract
| ngrokpath/**contracts** | GET | list of all contracts with their relation with lendor , borrowers , amount they have lended or borrowed,their names etc | It shows the relation between different user(if relation of lending and borrowing exists and only if amount is yet to paid) 

There are certain validation.This will be checked if you want to add new user or contract
| No | Condition | Example
| --- | --- | --- |
| 1 | There should be unique pair of userName and phoneNumber | if you have added (Ram , 1234567890) in user than you cannot again add it.But the name "Ram" can come with any other "phoneNumber" and viceversa
| 2 | length of userName should be greater than 0 and less than 50 and phoneNumber length should be 10 | Ram , 1234567890
| 3 | All the parameters in requestbody(given below) along with its respective type is mandatory |
| 4 | You cannot add "lendorId" or "borrowerId" which don't exist in user collection(To know your id you can make use of 3rd api in above table)Request

Expected RequestBody 
1.User #(should be dict)
{
    "name" : "balu",
    "phoneNumber" : "8992637382" #(only integer needed)
}

2.Contract #(should be dict)<br/>
{<br/>
    "lendorId" : "631ae604582e80a20b11afb0", #(should be objectId)<br/>
    "borrowerId" : "631ae15c12f5bcf59ae195b3", #(should be objectId)<br/>
    "isRepaid" : false, #(only bool needed)<br/>
    "principle" : 400,  #(only integer needed)<br/>
    "interestRate" : 6, #(only integer needed)<br/>
    "loanStartDate" : "23/6/2022",<br/>
    "loanDueDate" : "12/8/2022"<br/>
}<br/>
