from api import db


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
        Stores all the transactions posted by staff
    """
    staff_username =  db.StringField()
    customer_username = db.StringField()
    purchase= db.StringField()
    quantity = db.StringField()
    total_paid = db.IntField()
    timestamp = db.DateTimeField()
    
    
    def to_json(self):
        return        {"customer": self.customer_username,
                        "paid": self.total_paid,
                        'bought':self.purchase
                        }
    