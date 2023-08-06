from rest_framework_simplejwt.tokens import AccessToken as AT
from rest_framework_simplejwt.exceptions import TokenError, TokenBackendError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.utils import aware_utcnow
from jwcrypto.jwk import JWK
import jwt
import requests
import json


class AccessToken(AT):
    def __init__(self, token=None, verify=True):
        """
        !!!! IMPORTANT !!!! MUST raise a TokenError with a user-facing error
        message if the given token is invalid, expired, or otherwise not safe
        to use.
        """
        if self.token_type is None or self.lifetime is None:
            raise TokenError(_('Cannot create token with no type or lifetime'))

        self.token = token
        self.current_time = aware_utcnow()

        # Set up token
        if token is not None:
            # An encoded token was provided
            header = jwt.get_unverified_header(token)

            unverified = jwt.decode(self.token, verify=False)
            pub = self.get_public_key(header['kid'], unverified)
            token_backend = TokenBackend(api_settings.ALGORITHM, api_settings.SIGNING_KEY,
                                         pub, api_settings.AUDIENCE, api_settings.ISSUER)

            # Decode token
            try:
                self.payload = token_backend.decode(token, verify=verify)
            except TokenBackendError:
                raise TokenError(_('Token is invalid or expired'))

            if verify:
                self.verify()
        else:
            # New token.  Skip all the verification steps.
            self.payload = {api_settings.TOKEN_TYPE_CLAIM: self.token_type}

            # Set "exp" claim with default value
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)

            # Set "jti" claim
            self.set_jti()

    def get_public_key(self, kid, unverified):
        host, version = unverified['iss'].split('/')
        if version == 'v3':
            url = f'https://{host}/{version}/certs'
            resp = requests.get(url).json()['keys']
            key = [key for key in resp if key['kid'] == kid][0]
            key = JWK.from_json(json.dumps(key))
            return key.export_to_pem()
        else:
            return api_settings.VERIFYING_KEY
