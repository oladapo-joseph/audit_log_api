# audit_log_api

## A RESTFUL API that logs transactions per staff, using JWT authentication and mongoengine on MongoDB database



## To run it on Ubuntu

> $ export FLASK_APP=__int__.py

> $ flask run


## Curl commands for testing


## How to use:

### 1. To register as a new staff 
    
    curl -i http:localhost:5000/register
    -X POST
     --header   "Authorization: {admin}"     #if admin else blank
    --header   "Accept=application/json"
    --header  "Content-Type: application/json"
    -d '{     "first_name" : "firstName",
                ""last_name"" : "lastName",
                "password" : "<password>",
                "secret_key" = "<your secret key>"
              }'


### 2. Login as a user

    curl -i http:localhost:5000/staff/login   \
    -X POST \
     --header   "Authorization: {secret_key}"
    --header   "Accept=application/json"
    --header  "Content-Type: application/json"
     -d '{"username" : "lead_test@subi.com",
                "password" : <password>
              }'  



### 3 Transaction CRUD
    
> 1. Log new Transaction

    curl -i http:localhost:5000/staff/log
    -X POST
     --header   "Authorization: {token}"
    --header   "Accept=application/json"
    --header  "Content-Type: application/json"
  -d  '{      "customer_name": "joe",
                "purchased": "powder",
                "quantity": "3",
                "total": 1200
                     }' 


> 2. Get All Transaction
    curl -i http:localhost:5000/staff/log
    -X GET
    --header   "Authorization: {token}"
    --header   "Accept=application/json"
    --header  "Content-Type: application/json"



### 3. Single Transaction
> 1. GET single

    curl -i http:localhost:5000/staff/log/<id>
    -X GET
    --header   "Authorization: {token}"
    --header   "Accept=application/json"
    --header  "Content-Type: application/json"

>2.Update Single Template

    curl -i http:localhost:5000/staff/log/<log_id> \    
        -X PUT    \
    --header   "Authorization: {token}"
    --header   "Accept=application/json"
    --header  "Content-Type: application/json"
    -d '{     "customer_name": "joe",
                "purchased": "powder",
                "quantity": "3",
                "total": 1200    }'


 > 3. DELETE Single Transaction
    
    curl http:localhost:5000/staff/log/<log_id>
    -X DELETE
    --header   "Authorization: {token}"
    --header   "Accept=application/json"
    --header  "Content-Type: application/json"



### 4. Admin 
    
    curl -i http:localhost:5000/admin/checklog/<string:who>
    -X GET
    --header "Authorization: {admin_secret_key}"
    --header  "Accept": "application/json"
    --header  "Content-Type": "application/json" 

> With admin privilege you dont need to login and you can get the report on both customers and staff, so you can specify "c" or "s" as "who"
