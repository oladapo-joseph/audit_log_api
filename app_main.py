from datetime import datetime
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from werkzeug.security import check_password_hash, generate_password_hash
from token_generator import generate_token
from encoder import encode_data,decode_data, create_username

import os

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = { #'connect':False,
                                  "host" : 'mongodb://localhost:27017/test'
                                    #   f"mongodb+srv://joseph:{os.environ.get('password')}@cluster-test.hnakk.mongodb.net/test?retryWrites=true&ssl=true&tlsAllowInvalidCertificates=true"
                                  }
                            #    
db = MongoEngine()
db.init_app(app)



class Staff(db.Document):
    
    """
            This document stores the staff records and keeps them for reference
    
    """
    first_name = db.StringField()
    last_name = db.StringField()
    username = db.StringField()
    password = db.StringField(required=True)
    secret_key = db.StringField()
    timestamp = db.DateTimeField()
    admin = db.BooleanField(default=False)
    
    def to_json(self):
        return {
                "username": self.username,
                "message": 'Account Successfully created',
                "To login": "Add secret key to your authorization header to login. Mode 'Bearer <secret_key>'"}


class Login_status(db.Document):
    
    """
        This Documents keeps record of the login token given to a user that logs in
        It saves the email and token, so that the user can use his token to create, view templates
        
    """
    
    username = db.StringField()
    token = db.StringField()
        
class Transactions(db.Document):
    """
        Stores all the templates posted by users
    """
    staff_username =  db.StringField()
    customer_username = db.StringField()
    purchase= db.StringField()
    quantity = db.StringField()
    total_paid = db.IntField()
    timestamp = db.DateTimeField()
    
    
    def to_json(self):
        return        {"_customer": self.customer_username,
                        "paid": self.total_paid,
                        'bought':self.purchase
                        }
    
                    
        
# the routes
        
@app.route('/staff/register', methods=['POST'])
def register():
    """
        This function registers new member of staff and saves their details in the staff document
        
    """
    details = request.json
    pwd = generate_password_hash(details['password'], 'sha256')
    try:
        header = request.headers['Authorization'].split(' ')[1][:-1]
    except:
        header = ''
    admin = lambda x: True if x=='admin' else False
    new_staff = Staff(
                        first_name= details['first_name'],
                        last_name = details['last_name'],
                        username = create_username(details['first_name'], details['last_name']),
                        password = pwd,
                        secret_key = details['secret_key'],
                        timestamp = datetime.utcnow(),
                        admin = admin(header)
                        )
    new_staff.save()
    return new_staff.to_json()



@app.route('/staff/login', methods=['POST'])
def login():
    login = request.json   # loads the request data
    user = Staff.objects(username=login['username']).first()   
    if not user and check_password_hash(user.password, login['password']):   # # checks if email exists and password is correct
        return jsonify({
                        'error': 'Kindly register or retype password',
                        })
    
    else:
        SECRET_KEY = request.headers['Authorization'].split(' ')[1][:-1]   # carries te secret key from the header 
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
    token = request.headers['Authorization'].split(' ')[1][:-1]             # to check for token
    
    login = Login_status.objects(token=token).first()
    if login:                                                                # checks if token exists'      
     # checks if the token is valid, returns true or false and e==
        auth, valid = decode_data(token, Staff.objects(username=login.username).first().secret_key)
        if valid: 
            if request.method=='POST':                                      # if user posts a transaction      
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
                
                all_transactions = Transactions.objects(staff_username=login.username).all()       # to get the list of all transactions
                list_of_transactions = {str(index+1):temp.to_json() for index,temp in enumerate(all_transactions)}              # to get them in a disctionary format
                message = {'transactions': list_of_transactions}
            
        else:
            message = {
                            'message':f'{auth}, Kindly /login again',
                           }
    else:
        message = {'message':'Token doesnt exist'}
    return jsonify(message)
    
  
        
@app.route('/staff/log/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_template(log_id):
    """
        This allows user to update, delete and fetch a template.
    """
    token = request.headers['Authorization'].split(' ')[1][:-1]
    # to check for token
    login= Login_status.objects(token=token).first()
    if login:    
        auth, valid = decode_data(token, Staff.objects(username=login.username).first().secret_key )    
        message = ''
        if valid: 
            temps = request.json
            try:
                selected_transaction = Transactions.objects(customer_username=login.username)[int(log_id)-1]
            
                if request.method=='PUT':            
                    selected_transaction.update( customer_= temps['customer_name'],
                                                purchase = temps['purchased'],
                                                quantity = temps['quantity'],
                                                total_paid = temps['total'],
                                                timestamp = datetime.utcnow()
                                                ) 
                    message = {
                                "message":"Transaction updated successfully"
                                }
                    
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
            message = {
                        'message':f'{auth}, Kindly login again'
                        }
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
    SECRET_KEY = request.headers['Authorization'].split(' ')[1][:-1]
    admin = Staff.objects(secret_key=SECRET_KEY).first().admin
    all_report = {}
    if admin:
        if who=='c':
            all_customers = set([each.customer_username  for each in Transactions.objects]) 
            for n, customer in enumerate(all_customers):
                
                report = {'Name': f'{customer}'}
                details = [item.total_paid for item in Transactions.objects(customer_username=customer)]
                report['body']  = {'total purchases': sum(details),
                                    'no of patronage': len(details),
                                    'first transaction': Transactions.objects(customer_username= customer).first().timestamp,
                                  "last_transaction": Transactions.objects(customer_username=customer)[len(details)-1].timestamp
                                   }
                all_report[n+1] = report
                
        if who == 's':
            staff_list = [staff.username for staff in Staff.objects]
            
            for s_no, name in enumerate(staff_list):
                report = {'Staff username':f'{name}'}
                details = [item.total_paid for item in Transactions.objects(staff_username=name)]
                report['body'] = { 'total_sales': sum(details),
                                  'count': len(details),
                                  'first transaction': Transactions.objects(staff_username=name).first().timestamp,
                                  "last_transaction": Transactions.objects(staff_username=name)[len(details)-1].timestamp
                                  }
                all_report[s_no+1] = report
                
    return jsonify({'Report': all_report})

if __name__ == "__main__":
    app.run(debug=True)
    db.disconnect()