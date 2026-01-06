from jose import jwt
import requests
from django.http import JsonResponse
from http import HTTPStatus
from os import environ
from dotenv import load_dotenv
from pathlib import Path
path=Path('F:\Workspace\Amazon\.env')
load_dotenv(path)

region = "eu-north-1"
user_pool_id = environ['USER_POOL_ID']
app_client_id = '3ref2vid0ksr0elpgqlo9qauah'

def get_token(request):
    try:
        header=request.headers.get('Authorization')
        if header and header.startswith('Bearer'):
            token=  header.split(' ')[1]
            return token
        else:
            return False
    except Exception as e:
        return False
        

class CustomAuthMiddleware:

    def __init__(self,get_response):
        
        self.get_response=get_response
    
    def __call__(self,request):
        token= get_token(request)
        try:
  
                headers = jwt.get_unverified_header(token)
                kid = headers['kid']
    
                jwks= f'https://cognito-idp.eu-north-1.amazonaws.com/eu-north-1_5yBdph2Ho/.well-known/jwks.json'
                jwks=requests.get(jwks).json()

                decoded_token = jwt.decode(
                            token,
                            jwks,
                            algorithms=["RS256"],
                            audience=app_client_id,
                            issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
                        )
                request.user_sub=decoded_token['sub']
                print(request.user_sub)
        except Exception as e:
                paths=['/user/login/','/user/signup/']
                if request.path in paths or request.path.startswith('/admin'):
                     return self.get_response(request)
                return JsonResponse({'Error':'User not authorized'},status=HTTPStatus.UNAUTHORIZED)
        return self.get_response(request)
        