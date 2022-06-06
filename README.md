# audit_log_api

## A RESTFUL API that logs transactions per staff, using JWT authentication and the MongoDB database

## How to use 

### 1. To register as a new staff 
    
    <URL : localhost:5000/register
    Method : POST
    Headers : { 'Authorization': 'Bearer <admin>'   #if admin
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {
                'first_name' : 'firstName',
                ''last_name'' : 'lastName',
                "password" : '<password>',
                'secret_key' = '<your secret key>'
              }


### 2. Login as a user

    <URL : localhost:5000/login
      Method : POST
      Headers : {'Authorization': 'Bearer ' + '<secret_key>',
                 'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
     Body :    {
                'username : 'lead_test@subi.com',
                'password' : '<password>'
              }  
    > 


### 3 Transaction CRUD
    
> 1. Log new Transaction

    <URL : locahost:5000/staff/log
    Method : POST
    Headers : {
                'Authorization': 'Bearer <token from login>',
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {
                 "customer_name": "joe",
                "purchased": "powder",
                "quantity": "3",
                "total": 1200
                     }  
>
    
> 2. Get All Template

    <URL : locahost:5000/staff/log
    Method : GET
    Headers : {
                'Authorization': 'Bearer ' + "{token}"
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}      


### 3. Single Transaction
> 1. GET single

    <URL : locahost:5000/staff/log/<id>
    Method : GET
    Headers : {
                'Authorization': 'Bearer ' + "{token}"
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}  >

>2.Update Single Template

    URL : locahost:5000/template/<template_id>
    
    Method : PUT
    Headers : {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {
                 "customer_name": "joe",
                "purchased": "powder",
                "quantity": "3",
                "total": 1200
    }   

 > 3. DELETE Single Template
    
    <URL : locahost:5000/template/<template_id>
    Method : DELETE
    Headers : {
                'Authorization': 'Bearer ' + "{token}"
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}                  


### 4. Admin 
    
    URL : /admin/checklog/<string:who>
    Method: GET
    Headers: {
                'Authorization': 'Bearer ' + "{admin_secret_key}"
                'Accept': 'application/json',
                'Content-Type': 'application/json',    
    }

    body : {}