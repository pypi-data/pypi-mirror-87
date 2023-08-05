import typing

_user_cas_attributes = None


class UserCasAttributes:
    def __init__(self, user_cas_attributes_payload):
        self._payload = user_cas_attributes_payload
        self.is_from_new_login: typing.Sequence[bool] = user_cas_attributes_payload.get('isFromNewLogin')
        self.mail: typing.Sequence[bool] = user_cas_attributes_payload.get('mail')
        self.authentication_date: typing.Sequence[int] = user_cas_attributes_payload.get('authenticationDate')
        self.sam_account_name: typing.Sequence[str] = user_cas_attributes_payload.get('sAMAccountName')
        self.display_name: typing.Sequence[str] = user_cas_attributes_payload.get('displayName')
        self.given_name: typing.Sequence[str] = user_cas_attributes_payload.get('givenName')
        self.successful_authentication_handlers: typing.Sequence[str] = \
            user_cas_attributes_payload.get('successfulAuthenticationHandlers')
        self.distinguished_name: typing.Sequence[str] = user_cas_attributes_payload.get('distinguishedName')
        self.cn: typing.Sequence[str] = user_cas_attributes_payload.get('cn')
        self.title: typing.Sequence[str] = user_cas_attributes_payload.get('title')
        self.saml_authentication_statement_auth_method: typing.Sequence[str] = \
            user_cas_attributes_payload.get('samlAuthenticationStatementAuthMethod')
        self.credential_type: typing.Sequence[str] = user_cas_attributes_payload.get('credentialType')
        self.authentication_method: typing.Sequence[str] = user_cas_attributes_payload.get('authenticationMethod')
        self.long_term_authentication_request_token_used: typing.Sequence[bool] = \
            user_cas_attributes_payload.get('longTermAuthenticationRequestTokenUsed')
        self.member_of: typing.Sequence[str] = user_cas_attributes_payload.get('memberOf')
        self.department: typing.Sequence[str] = user_cas_attributes_payload.get('department')
        self.user_principal_name: typing.Sequence[str] = user_cas_attributes_payload.get('userPrincipalName')


def save_user_cas_attributes(user_cas_attributes_payload):
    """
    Saves CAS user attributes in-memory
    """
    global _user_cas_attributes

    _user_cas_attributes = UserCasAttributes(user_cas_attributes_payload)


def get_user_cas_attributes() -> UserCasAttributes:
    """
    :return: CAS user attributes in-memory
    """
    global _user_cas_attributes

    return _user_cas_attributes
