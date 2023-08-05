This is a library for Flask for developers from Centre of Technology and Innovation (CTI) from Asia Pacific University
to be able to simply implement CAS (Central Authentication Service) by annotating their view functions with the
decorators provided in this library.

## Quickstart
```
from flask import Flask
from apu_cas import require_service_ticket 
app = Flask(__name__)

@app.route('/')
@require_service_ticket
def hello_world():
    return 'Hello, World!'
```

This will secure the endpoints with CAS Authentication and consumer of the secured endpoints will have to pass a valid string
of service ticket through as query parameter, 'ticket'.

For example:
```
GET http://localhost:5000?ticket="ST-575303-I0RYRmVuzlRb4cCkD6jYyw3ISV8ip-172-32-13-200"
```

The above method is related to CAS REST Protocol, for more information such as how to authenticate with CAS REST protocol,
please visit the [documentation](https://apereo.github.io/cas/5.3.x/protocol/REST-Protocol.html)

## Getting Authenticated User Attributes
```
from flask import Flask
from apu_cas import require_service_ticket 
app = Flask(__name__)

@app.route('/')
@require_service_ticket
def user_attribute():
    attr = get_user_cas_attributes()
    return {
        'is_from_new_login': attr.is_from_new_login[0],
        'mail': attr.mail[0],
        'authentication_date': attr.authentication_date[0],
        'sam_account_name': attr.sam_account_name[0],
        'display_name': attr.display_name[0],
        'given_name': attr.given_name[0],
        'successful_authentication_handlers': attr.successful_authentication_handlers[0],
        'distinguished_name': attr.distinguished_name[0],
        'cn': attr.cn[0],
        'title': attr.title or None,
        'saml_authentication_statement_auth_method': attr.saml_authentication_statement_auth_method[0],
        'credential_type': attr.credential_type[0],
        'authentication_method': attr.authentication_method[0],
        'long_term_authentication_request_token_used': attr.long_term_authentication_request_token_used[0],
        'member_of': attr.member_of or None,
        'department': attr.department,
        'user_principal_name': attr.user_principal_name[0]
    }
```

This is returning the CAS Attributes of the authenticated User. `get_user_cas_attributes()` function plays the major role of collecting all the attributes and returning through the function.

## Determining User Role
```
from flask import Flask
from apu_cas import require_service_ticket 
app = Flask(__name__)

@app.route('/')
@require_service_ticket
def determine_role():
    return {
        'role': determine_roles()
    }
```

This is returning the Role which is being determined by Bitwise Calculation. The roles are pre-defined as below:
STUDENT = 1 << 0
LECTURER = 1 << 1
ADMIN = 1 << 2
CTI = 1 << 3

## Has a Role
```
from flask import Flask
from apu_cas import require_service_ticket 
app = Flask(__name__)

@app.route('/')
@require_service_ticket
def has_role():
    return {
        'permission': 'Yes, you are from CTI.' if has_role(UserRole.CTI) else 'No'
    }
```

This uses the same Bitwise Operation as above, but this function returns (bool) if the Role is matching the User permission level.

## Restrict Endpoint to a specific role
```
from flask import Flask
from apu_cas import require_service_ticket 
app = Flask(__name__)

@app.route('/')
@require_service_ticket(restricted_to_roles=[UserRole.CTI])
def restricted():
    return {
        'message': 'Yes, only CTI can access this Endpoint!'
    }
```

This function uses the `@require_service_ticket` decorator with a new parameter `restricted_to_roles`. In this parameter, we need to pass in the User Role. In this example, we're passing in CTI as the Role. Hence, any Staff with their Account parked under CTI would have access to this Endpoint. Access is determined by the OU (Organisation/Functional Unit). 

## Deny Endpoint to a specific role
```
from flask import Flask
from apu_cas import require_service_ticket 
app = Flask(__name__)

@app.route('/')
@require_service_ticket(deny_for_roles=[UserRole.CTI])
def restricted():
    return {
        'message': 'Yes, any other role than CTI can access this Endpoint!'
    }
```
This function uses the `@require_service_ticket` decorator with a new parameter `deny_for_roles`. In this parameter, we need to pass in the User Role. In this example, we're passing in CTI as the Role. Hence, any Staff with their Account parked any other than under CTI would have access to this Endpoint. Access is determined by the OU (Organisation/Functional Unit). 
