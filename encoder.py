import jwt
import datetime
from random import randint as rand


def encode_data(json_data, secret):
    """

    Args:
        json_data (dict): details of the user
        secret (str): secret key

    Returns:
        token : JWT generated token for the user
    """
    
    json_data['exp'] = datetime.datetime.utcnow()+datetime.timedelta(seconds=300)
    json_data['data'] = str(datetime.datetime.utcnow())
    return jwt.encode(payload=json_data, key=secret, algorithm='HS256')



def decode_data(token, secret):
    """
    This function decodes the password hash and

    Args:
        token (str): the password hash generated as token
        secret (str): the secret key of the user

    Returns:
        data : Error type if error, else the password of the user
        status (bool): the validity of the token
    """
    try:
        data = jwt.decode(jwt = token, key=secret, algorithms='HS256')
        status = True
    except Exception as e:
        data = e
        status = False
    return data,status


def create_username(first_name, last_name):
    return last_name[:3]+first_name+str(rand(10,99))


        