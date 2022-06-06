import os

class DevConfig:
   MONGODB_SETTINGS = { 
                        "host" : 'mongodb://localhost:27017/test'
                   #   f"mongodb+srv://joseph:{os.environ.get('password')}@cluster-test.hnakk.mongodb.net/test?retryWrites=true&ssl=true&tlsAllowInvalidCertificates=true"
                        }
    
    
 