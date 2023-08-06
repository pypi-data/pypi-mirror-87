# This will validate an incoming token and ensure that it is valid, and refresh it if required
#
# It will either return a new access token if it needed to refresh the existing one, None if the token
# was validated and didn't need to be refreshed, or raise an Exception if it can't validate the token
from os import urandom

import base64
import datetime
import json
import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django_cognito.authentication import utils
from django_cognito.authentication.cognito import constants, actions
from django_cognito.authentication.utils import PublicKey


def validate_token(access_token, refresh_token=None):
    try:
        header, payload = decode_token(access_token)
    except Exception as ex:
        # Invalid token or token we can't decode for whatever reason
        raise Exception("Invalid token")

    public_keys = utils.get_public_keys()

    [matching_key] = [key for key in public_keys['keys'] if key['kid'] == header['kid']]

    if matching_key is None:
        raise Exception("Invalid token public key")
    else:
        decode_params = {
            "algorithms": [header['alg']],
            "options": {'verify_exp': False}
        }
        if 'aud' in payload:
            decode_params['audience'] = constants.CLIENT_ID

        # Verify signature using the public key for this pool, as defined the the AWS documentation
        decode = jwt.decode(access_token, PublicKey(matching_key).pem, **decode_params)

    # Verify that the audience matches the Cognito app ID, as defined by the AWS documentation
    audience = payload.get('aud', None)
    if not audience:
        audience = payload.get('client_id')

    if audience != constants.CLIENT_ID:
        raise Exception("Invalid token audience")

    # Verify that the issuer matches the URL for the Cognito user pool, as defined by the AWS documentation
    iss_url = f"https://cognito-idp.{settings.COGNITO_POOL_ID.split('_', 1)[0]}.amazonaws.com/{settings.COGNITO_POOL_ID}"
    if payload['iss'] != iss_url:
        raise Exception("Invalid token issuer")

    # Verify that the token is either not expired, or if expired, that we have a refresh token to refresh it
    if payload['exp'] <= datetime.datetime.timestamp(datetime.datetime.utcnow()):
        if not refresh_token:
            # The current access token is expired and no refresh token was provided, authentication fails
            raise Exception("The access token provided has expired. Please login again.")
        else:
            # This token is expired, potentially check for a refresh token? Return this token in the auth return
            # variable?
            result = actions.initiate_auth(payload['cognito:username'], constants.REFRESH_TOKEN_FLOW,
                                           refresh_token=refresh_token)

            if result['AuthenticationResult']:
                # Return the freshly generated access token as an indication auth succeeded but a new token was
                # required
                #
                # TODO: DON'T return refresh token here, for methods that require a refresh token we should implement
                # them somewhere else, or differently
                return result['AuthenticationResult']['AccessToken'], refresh_token
            else:
                # Something went wrong with the authentication
                raise Exception("An error occurred while attempting to refresh the access token")
    else:
        # The token validated successfully, we don't need to do anything else here
        return None, None


def generate_csrf():
    random_bytes = urandom(64)
    csrf_token = base64.b64encode(random_bytes).decode('utf-8')

    return csrf_token


def decode_token(access_token):
    token_parts = access_token.split(".")

    header = json.loads(
        base64.b64decode(token_parts[0] + "=" * ((4 - len(token_parts[0]) % 4) % 4)).decode('utf-8'))
    payload = json.loads(
        base64.b64decode(token_parts[1] + "=" * ((4 - len(token_parts[1]) % 4) % 4)).decode('utf-8'))

    return header, payload


def process_request(request):
    if getattr(settings, "USE_CSRF", False):
        try:
            csrf_token_cookie = request.COOKIES.get('csrftoken')
            csrf_header = request.META['HTTP_CSRFTOKEN']

            if csrf_token_cookie != csrf_header:
                raise Exception("CSRF Verification failed")
        except Exception as ex:
            raise Exception("CSRF verification failed")

    try:
        access_token = request.META['HTTP_ACCESSTOKEN']
        try:
            refresh_token = request.META['HTTP_REFRESHTOKEN']
        except Exception as ex:
            # A refresh token doesn't have to be passed in, it's optional to auto renew access token
            pass
    except Exception as ex:
        return AnonymousUser(), None, None

    try:
        id_token = request.META['HTTP_IDTOKEN']
    except Exception as ex:
        return AnonymousUser(), None, None

    if not all([access_token, id_token]) or not refresh_token:
        # Need to have this to authenticate, error out
        raise Exception("No valid tokens were found in the request")
    else:
        new_access_token, new_refresh_token = validate_token(id_token, refresh_token)

        header, payload = decode_token(id_token)

        try:
            params = {
                settings.COGNITO_USER_MODEL_FIELD_REF_FIELD: payload[settings.COGNITO_TOKEN_REF_FIELD]
            }

            user = get_user_model().objects.get(**params)
        except Exception as ex:
            if getattr(settings, "AUTO_CREATE_USER", False):
                username = payload.get('username', None)
                if not username:
                    username = payload.get('cognito:username')

                aws_user = actions.admin_get_user(username)

                user_attributes = {k: v for dict in [{d['Name']: d['Value']} for d in aws_user['UserAttributes']]
                                   for k, v in dict.items()}

                data = settings.COGNITO_USER_FIELD_MAPPING.copy()

                for k, v in data.items():
                    data[k] = user_attributes[v]

                user, _ = get_user_model().objects.get_or_create(**data)
            else:
                return AnonymousUser, None, None

        return user, new_access_token, new_refresh_token
