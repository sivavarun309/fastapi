Implementing authentication and authorization for the requests
and implementing clean code for better understanding for clean code and for better scalability and management

1. Creating seperate file for api endpoints for authentication and todos operation
2 main.py will only contains setup operations and the api operations for endpoint will be managed in seperate file using router

JSON web Token(JWT)
    JSON web token is a self-contained way to securely transmit data and information between two parties using json object
    JSOn web tokens can be trusted because each JWT can be digitally signed which in return allows the server to know
if the JWT has been changed at all
    JWT should be used when dealing with authorization
    JWT is a great way for information to be exchanged between the server and client

JSON web token structure
    a JSON web token is created of three seperate parts seprated by dots(.) which include
        HEADER(a)         |
        Payload(b)        |   (aaaaaaaa.bbbbbbbb.cccccccc) 
        Signature(c)      |

JWT HEADER
    a JWT header usually consits of two parts:
        alg - the algorithm for signing
        typ - the specific type of token
    the JWT header is then encoded using Base64 to create the first part of the JWT(a)

JWT Payload
    JWT payload consits of the data. the payload data contains claims, and there are three different types of claims
        Registered  - predefined but not mandatory this includes
            ISS -issuer - identifies the principle that issue the JWT
            SUB -Subject- holds the statement about the subject. its must be scoped either locally or globally unique. ID of JWT
            EXP -Expiration time - tells when the JWT token will expire. make sure some type of expirtion time attached to JWT
        Public      -
        Private     -
    JWT payload is then encoded using base64 to create the second part of JWT(b)

JWT Signature
    JWT singnature is created by using the algorithum in the header to hash out the encoded header, encoded payload with a secret
    the secret can be anything, but is saved somewhere on the server that the client does not have access to
    - signature = HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payloade), secret)
    signature(the last part of JWT) is created by hashing the encoded header and encoded payload with "." in between with a secret
    This results in a hash value (the signature), which is used to verify the integrity and authenticity of the token.

JWT Example
    JWT header
        {                                   |        JWT header holds the alogrithum and type
            "alg":"HS256",                  |            Here,  algorithum is "HS256" algotithum
            "typ":"JWT"                     |            and    type is "JWT" which is a JSON Web Token Type
        }                                   |               
                                            |
    JWT Payload                             |
        {                                   |
            "sub": "123456789",             |
            "name":  "siva",                |
            "first_name": "siva",           |
            "last_name": "T",               |
            "email": "siva@email.com",      |
            "role": "admin"                 |
        }                                   |
                                            |
    JWT Signature                           |
        HMACSHA256(base64UrlEncode(header)  |       encoded header and encoded payload is combined by "." in between
             + "." +                        |       and hashed with algorithum from header with a secret
             base64UrlEncode(payloade),     |       here the hash algotithum is HS256 from header
             learnonline)                   |       and the secret is the word learnonline 
    
    JSON Web Token
        eyJhbGci0iJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkVyaWMgUm9ieSIsImdpdmVuX25hbW
        UiOiJFcmljIiwiZmFtaWx5X25hbWUiOiJSb2J5IiwiZW1haWwiOiJjb2Rpbmd3aXRocm9ieUBnbWFpbC5jb20iLCJhZG1pbiI6dHJ1Z
        Xo.i8yqz0z-nWr5hwXqRYP18W9igUPoKMZiBZW315tK5g8

        this token is completely unique to client based on the authentication of the user logged in

try https://jwt.io to see if the token and the data is matched

to create and return JWT install python-jose[cryptography]
    - pip install "python-jose[cryptography]"


Creating the JWT, things need to consider
    - the JWT token must have the expire time which makes the access more secured
    - consider the unique identification or some id for the payload of the JWT. 
    so it will be easy to get the user identification directly from token.
    - it is recommended to include the details that we use often in the application.
    like if we are using different function for different roles then we can add roles data into JWT
    by doing that we can get the roles from the JWT instead of quering from DB every time we need 