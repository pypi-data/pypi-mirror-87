__version__ = '2.5.1rc1'


def default_user_pool_handler():
    from chalice_cognito_auth.userpool import UserPoolHandler
    return UserPoolHandler.from_env()
