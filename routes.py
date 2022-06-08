import encodings
from pandas import json_normalize
from api import app
from documents import Staff ,Transactions, Login_status
from flask import request, jsonify, make_response, Response
from werkzeug.security import check_password_hash, generate_password_hash
from encoder import encode_data,decode_data, create_username
from datetime import datetime
import logging


logging.basicConfig(filename='example.log', level=logging.DEBUG)      
        
@app.route('/staff/register', methods=['POST'])
def register():
    """
        This function registers new member of staff and saves their details in the staff document
    
    """
    details = request.json
    
    try:
        header = request.headers['Authorization']
    except:
        header = ''
    admin = lambda x: True if x=='admin' else False
    new_staff = Staff(
                        first_name= details['first_name'],
                        last_name = details['last_name'],
                        username = create_username(details['first_name'], details['last_name']),
                        password = generate_password_hash(details['password'], 'sha256'),
                        secret_key = details['secret_key'],
                        timestamp = datetime.utcnow(),
                        admin = admin(header)
                        )
    new_staff.save()
    return jsonify(new_staff.to_json())




@app.route('/staff/login', methods=['POST'])
def login():
    login = request.json   # loads the request data
    user = Staff.objects(username=login['username']).first()   
    if not user and check_password_hash(user.password, login['password']):   # # checks if email exists and password is correct
        return jsonify({
                        'error': 'Kindly register or retype password',
                        })
    
    else:
        SECRET_KEY = request.headers['Authorization']   # carries te secret key from the header 
        token = encode_data(json_data= login ,secret = SECRET_KEY)          # encoding the secret key
        login = Login_status(username =user.username, token=token )              # saving the token generated to be accessed later
        login.save()
        
        
        return jsonify(
                        {
                            'message': 'Login Successful, kindly save token, expires after 5 mins',
                            'token' : f'{token}'
                        }
                       ) 


@app.route('/staff/log', methods=['POST', 'GET'])
def transactions():
    """ 
        This function manages the transactions logged by the user
        A POST request logs transaction per staff
        A GET request fetches all the transactions by the requesting staff

    Returns:
        json
    """
    
    token = request.headers['Authorization']            # to check for token
    
    login = Login_status.objects(token=token).first()
    if login:                                                                # checks if token exists'      
     # checks if the token is valid, returns true or false and e==
        auth, valid = decode_data(token, Staff.objects(username=login.username).first().secret_key)
        if valid: 
            if request.method=='POST':                                      # if user wants to post a transaction      
                transaction = request.json
                new_transaction = Transactions( staff_username = login.username,
                                                customer_username =transaction['customer_name'],
                                                purchase = transaction['purchased'],
                                                quantity = transaction['quantity'],
                                                total_paid = transaction['total'],
                                                timestamp = datetime.utcnow()
                                                )
                new_transaction.save()                          # saves a new transaction 
                message = {
                            'message': 'Transaction logged successfully'
                                }
                
            else:                                                                       # else a GET request
                # to get the list of all transactions by the staff
                all_transactions = Transactions.objects(staff_username=login.username).all()       
                # to get them in a disctionary format
                list_of_transactions = {str(index+1):temp.to_json() for index,temp in enumerate(all_transactions)}        
                message = {'transactions': list_of_transactions}
            
        else:
            message = {'message':f'{auth}, Kindly /login again'}
    else:
        message = {'message':'Token doesnt exist'}
    return jsonify(message)
    
  
        
@app.route('/staff/log/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_template(log_id):
    """
        This allows user to update, delete and fetch a transaction.
    """
    token = request.headers['Authorization']
    # to check for token
    login= Login_status.objects(token=token).first()
    if login:    
        auth, valid = decode_data(token, Staff.objects(username=login.username).first().secret_key )    
        message = ''
        if valid: 
            temps = request.json
            try:
                selected_transaction = Transactions.objects(staff_username=login.username)[int(log_id)-1]
            
                if request.method=='PUT':            
                    selected_transaction.update( customer_= temps['customer_name'],
                                                purchase = temps['purchased'],
                                                quantity = temps['quantity'],
                                                total_paid = temps['total'],
                                                timestamp = datetime.utcnow()
                                                ) 
                    message = {"message":"Transaction updated successfully"}
                    
                elif request.method =='GET':
                    message = selected_transaction.to_json()
                else:
                    selected_transaction.delete()
                    message = {
                                'message':'Deleted successfully'
                                }
            except Exception as e:
                message = {'message' : f"{e} , Kindly select a valid number from 1 "}
        else:
            message = {'message':f'{auth}, Kindly login again'}
    else:
        message = {"No authorisation, token doesn't exist"}
            
    return jsonify(message)
    

@app.route('/admin/checklog/<string:who>', methods = ['GET'])
def admin(who):
    """
    This can only be done using admin rights
    To gain admin right, when registering add 'Bearer admin' to authorization header
    
    
    Keyword arguments:
        who : _string_
                depends on the statistics the admin wants to check, 
                "c": 'customers' or "s":'staff'
                
    Return: 
        message :json 
                containing the details based on request
    
    """

    try:
        SECRET_KEY = request.headers['Authorization']
        admin = Staff.objects(secret_key=SECRET_KEY).first().admin
        all_report = {}
        if admin:
            if who=='c':
                all_customers = set([each.customer_username  for each in Transactions.objects])
                
                for n, customer in enumerate(all_customers):
                    report = {'Name': f'{customer}'}
                    logging.info(f'{customer}')
                    details = [item.total_paid for item in Transactions.objects(customer_username=customer)]
                    logging.info(f'{details}')
                    report['summary']  = {'total purchases': sum(details),
                                        'no of patronage': len(details),
                                        'first transaction': Transactions.objects(customer_username= customer).first().timestamp,
                                    "last_transaction": Transactions.objects(customer_username=customer)[len(details)-1].timestamp
                                    }
                    all_report[n+1] = report

            if who == 's':
                staff_list = set([staff.username for staff in Staff.objects])
                for s_no, name in enumerate(staff_list):
                    report = {'Staff username':f'{name}'}
                    details = [item.total_paid for item in Transactions.objects(staff_username=name)]
                    report['summary'] = { 'total_sales': sum(details),
                                            'count': len(details),
                                    }
                    all_report[s_no+1] = report
                    
        return jsonify({'Report': all_report})
    except Exception as error:
        return jsonify({'Error': f'{error}',
                        "author": f"{request.headers['Authorization']}"
                        })