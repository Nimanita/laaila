# laaila
| Api Name | Method | Response | Use
| --- | --- | --- | --- | 
| ngrokpath/**api-token-auth/** | POST | {<br/> "token": "XXXXX" }<br/> | To get token which you need to add under authorisation header to use the api 
| ngrokpath/**user/** | POST | {<br/> "message": "User added successfully and user id is XXXX" }<br/> | To add the user
| ngrokpath/**user/** | GET | list of all user along with their id , name and phone number | To get list of all user (Created for testing)
| ngrokpath/**contracts/** | POST | {<br/> "message": "Contracts added successfully" }<br/><br/> | To add the contract
| ngrokpath/**contracts/** | GET | list of all contracts with their relation with lendor , borrowers , amount they have lended or borrowed,their names etc | It shows the relation between different user(if relation of lending and borrowing exists and only if amount is yet to paid) 

