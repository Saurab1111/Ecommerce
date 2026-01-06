from rest_framework.decorators import api_view
from rest_framework.response import Response
import hmac,hashlib,base64
import boto3
from pathlib import Path
from os import environ
from dotenv import load_dotenv
path=Path('F:\Workspace\Amazon\.env')
load_dotenv(path)

REGION = 'eu-north-1'
client = boto3.client('cognito-idp', region_name=REGION)

def get_secret_hash(username, client_id, client_secret):
            message = username + client_id
            dig = hmac.new(
            client_secret.encode('utf-8'),
            message.encode('utf-8'),
            digestmod=hashlib.sha256
            ).digest()
            return base64.b64encode(dig).decode()

@api_view(['POST'])
def login(request):
     
     
     try:
        response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': request.data['username'],
            'PASSWORD': request.data['password'],
            'SECRET_HASH': get_secret_hash(request.data['username'], client_id='3ref2vid0ksr0elpgqlo9qauah', client_secret=environ['client_secret'])        
            },
            ClientId='3ref2vid0ksr0elpgqlo9qauah',
            )
        if 'AuthenticationResult' in response:
            return Response({'success': True, 'tokens': response['AuthenticationResult']})

        # Step 3: Handle password challenge
        elif response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
            print("here")
            print(request.data['username'])
            challenge_response = client.respond_to_auth_challenge(
                                ClientId='3ref2vid0ksr0elpgqlo9qauah',
                                ChallengeName='NEW_PASSWORD_REQUIRED',
                                ChallengeResponses={
                                'USERNAME': request.data['username'],
                                'NEW_PASSWORD': request.data['password']+"1",
                                'userAttributes.given_name': request.data['username'],  # ✅ correct key
                                'SECRET_HASH': get_secret_hash(request.data['username'], client_id='3ref2vid0ksr0elpgqlo9qauah', client_secret=environ['client_secret'])
                            },
                            Session=response['Session']
                            )

            # print("************************************************************************************")
            return Response({'success': True, 'tokens': challenge_response['AuthenticationResult']})

        else:
            return Response("Success")
     except client.exceptions.NotAuthorizedException:
        return Response("❌ Incorrect username or password")
        exit()
     except Exception as e:
        return Response(f"❌ Login failed: {str(e)}")
        exit()

@api_view(['POST'])
def signup(request):
    response = client.sign_up(
    ClientId='3ref2vid0ksr0elpgqlo9qauah',
    SecretHash=get_secret_hash(request.data['username'], '3ref2vid0ksr0elpgqlo9qauah', client_secret=environ['client_secret']),
    Username=request.data['username'],
    Password=request.data['password'],
    UserAttributes=[
        {'Name': 'phone_number', 'Value': request.data['phone_number']},
        {'Name': 'given_name', 'Value': request.data['given_name']},
        {'Name': 'birthdate', 'Value': request.data['birth-date']}
        ]
      )
    return Response("Created successfully")


@api_view(['GET'])
def Hello(request):
    
     return Response(f"Hello, {request.sub}")