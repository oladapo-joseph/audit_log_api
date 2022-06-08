from dotenv import load_dotenv, get_key

user = get_key('.env', 'USERNAME')
password = get_key('.env', 'PASSWORD')
cluster = get_key('.env', "CLUSTER")


class DevConfig:
   MONGODB_SETTINGS = { 
                        # "host" : 'mongodb://localhost:27017/test' #for local connection
                     'host' : f"mongodb+srv://{user}:{password}@{cluster}/test?retryWrites=true&ssl=true&tlsAllowInvalidCertificates=true"
                        }
    
    
 