from cachetools import TTLCache
import requests
from authlib.jose import jwt, jwk, util, errors
from expiringdict import ExpiringDict



class ValidatorBase:

    def validate_token(self, token, issuer, method=None, audiences=None, allowed_roles=None):
        raise NotImplementedError


class AsymmetricKeyValidator(ValidatorBase):
    def __init__(self, default_key=None, key_url=None,
                 ttl=3600, scope_claim=None, roles_claim=None):
        self.key_url = key_url
        self.cache = ExpiringDict(max_len=100, max_age_seconds=ttl) #TTLCache(100, ttl)
        self.cache["default"] = default_key
        self.roles_claim = roles_claim
        self.scope_claim = scope_claim

    def validate_token(self, token, issuer, method=None, audiences=None, allowed_roles=None):
        key = self.get_key(token)
        if not key:
            return (False, None, None, None)
        if isinstance(key, dict):
            key = jwk.loads(key)
        options = {}
        if audiences:
            if isinstance(audiences, str):
                options["aud"] = {"essential": True, "value":audiences}
            else:
                options["aud"] = {"essential": True, "values":audiences}
        else:
            options["aud"] = {"essential": False, "values":[]}
            
        if issuer:
            options["iss"] = {"essential": True, "value":issuer}

        try:
            claims = jwt.decode(token, key, claims_options=options)
            claims.validate()
        except:
            return (False, None, None, None)
        
        payload = dict(claims)
        account_id = payload.get('sub')  # Get account id
        roles = None

        # Check scope is configured and add append it to the roles
        if self.scope_claim and payload.get(self.scope_claim):
            scope = payload.get(self.scope_claim)
            # Viewers can only read
            if scope == 'viewer' and method not in ['GET', 'HEAD']:
                return (False, payload, account_id, None)
            roles = ['scope:%s' % scope]

        # If roles claim is defined, gather roles from the token
        if self.roles_claim:
            roles = payload.get(self.roles_claim, []) + (roles or [])

        # Check roles if scope or role claim is set
        if allowed_roles and roles is not None:
            if not any(role in roles for role in allowed_roles):
                return (False, payload, account_id, roles)

        return (True, payload, account_id, roles)

    def get_key(self, token):
        try:
            kid = util.extract_header(token.encode().partition(b".")[0], 
                                        errors.DecodeError).get("kid","default")
        except Exception as e:
            print(e)
            return ""

        if kid not in self.cache:
            self.fetch_keys()
        return self.cache.get(kid, "")

    def fetch_keys(self):
        if not self.key_url:
            return
        response = requests.get(self.key_url)
        if response.ok:
            data = response.json()
            if "keys" in data:
                keys = {d["kid"]: d for d in data["keys"]}
            elif isinstance(data, list):
                keys = {d["kid"]: d for d in data}
            elif isinstance(data, dict) and len(data)>1:
                keys = data
            elif isinstance(data, dict):
                keys = {"default": data}
            self.cache.update(keys)