import functools
import typing

import requests
from flask import request, abort, redirect

from .variables import cas_url
from .user_cas_attributes import save_user_cas_attributes, get_user_cas_attributes
from .user_role import UserRole


cas_service_validation_url = f'{cas_url}/cas/p3/serviceValidate?format=json&service=%(service)s&ticket=%(ticket)s'
cas_redirect_url = f"{cas_url}/cas/login?service=%(service)s"


def determine_roles():
    """
    Determine the roles that a user can have according to their CAS user attributes
    :return: role_value
    """
    assert get_user_cas_attributes(), "No CAS Attribute found"

    user_cas_attributes = get_user_cas_attributes()
    member_of_attributes = "".join([
        member_of_attribute.lower() for member_of_attribute in user_cas_attributes.member_of
    ])
    distinguished_name_attributes = "".join([
        distinguished_name_attribute.lower() for distinguished_name_attribute in user_cas_attributes.distinguished_name
    ])
    joined_attributes = member_of_attributes + distinguished_name_attributes
    role_value = 0

    if "ou=students" in joined_attributes:
        role_value = role_value | UserRole.STUDENT.value
    if "ou=academic" in joined_attributes:
        role_value = role_value | UserRole.LECTURER.value
    if "ou=academic administration" in joined_attributes:
        role_value = role_value | UserRole.ADMIN.value
    if "ou=centre of technology and innovation (cti)" in joined_attributes:
        role_value = role_value | UserRole.CTI.value

    return role_value


def has_roles(roles: typing.Sequence[UserRole]) -> bool:
    """
    Check if the current user has any role within given list of UserRole

    Keyword arugments:

    roles -- A list of UserRole to check against
    """
    UserRole.assert_user_roles(roles)

    current_user_role = determine_roles()
    combined_accepted_role_value = 0

    for role in roles:
        combined_accepted_role_value = combined_accepted_role_value | role.value

    return current_user_role & combined_accepted_role_value


def validate_service_ticket():
    ticket = request.args.get('ticket', None)

    if ticket is None:
        return False

    response = requests.get(
        cas_service_validation_url % {"service": request.base_url, "ticket": ticket}
    ).json()['serviceResponse']

    if 'authenticationSuccess' not in response:
        return False

    return response['authenticationSuccess']['attributes']


def require_service_ticket(
        _function: typing.Optional[typing.Callable] = None,
        *,
        restricted_to_roles: typing.Optional[typing.Sequence[UserRole]] = None,
        deny_for_roles: typing.Optional[typing.Sequence[UserRole]] = None,
):
    """
    Makes decorated endpoint to require CAS service ticket as query string parameter

    Keyword arguments:

    _function -- The function to be decorated

    restricted_to_roles -- A list of UserRole to be allowed access 
                           (default None, allowing access to everyone) 

    deny_for_roles -- A list of UserRole to be denied access (default None) 
                      This will explicitly deny anyone with the any UserRole in the list
    """
    restricted_to_roles = restricted_to_roles if restricted_to_roles else []
    deny_for_roles = deny_for_roles if deny_for_roles else []

    for restricted_to_role in restricted_to_roles:
        UserRole.assert_user_role(restricted_to_role)
    for deny_for_role in deny_for_roles:
        UserRole.assert_user_role(deny_for_role)

    @functools.wraps(_function)
    def require_service_ticket_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            user_cas_attributes = validate_service_ticket()

            if not user_cas_attributes:
                return redirect(
                    cas_redirect_url % {"service": request.base_url}
                )

            save_user_cas_attributes(user_cas_attributes)

            if len(restricted_to_roles) > 0 and not has_roles(restricted_to_roles):
                abort(403, "The current user does not have the allowed role(s)")
            if len(deny_for_roles) > 0 and has_roles(deny_for_roles):
                abort(403, "The current user has role that is denied access")

            return function(*args, **kwargs)

        return wrapper

    if _function is None:
        return require_service_ticket_decorator
    else:
        return require_service_ticket_decorator(_function)


def has_role(role: UserRole) -> bool:
    """
    Check if the current user has the given role
    """

    return has_roles([role])
