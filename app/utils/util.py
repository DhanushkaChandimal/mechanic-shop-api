from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "super secret, secret key"

def encode_token(user_id): #using unique pieces of info to make our tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1), #Setting the expiration time to an hour past now
        'iat': datetime.now(timezone.utc), #Issued at
        'sub': str(user_id) #This needs to be a string or the token will be malformed and won't be able to be decoded.
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token