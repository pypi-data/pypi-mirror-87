# -*- coding: utf-8 -*-

import unittest
from authlib.jose import jwt, jwk
from eve import Eve
from eve_jwt import JWTAuth
from flask import g
from . import test_routes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
   key_size=2048,
)
public_key = private_key.public_key()

alt_private_key = rsa.generate_private_key(
    public_exponent=65537,
   key_size=2048,
)
alt_public_key = private_key.public_key()
# pem = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
#  )
header = {'alg': 'RS256', 'kid':'default'}

settings = {
    'JWT_DEFAULT_KEY': jwk.dumps(public_key),
    'JWT_KEY_URL': '',
    'JWT_TTL': 600,
    'JWT_ISSUER': 'https://domain.com/token',
    'JWT_ROLES_CLAIM': 'roles',
    'JWT_SCOPE_CLAIM': 'scope',
    'JWT_AUDIENCES': [],
    'DOMAIN': {
        'foo': {
            'schema': {
                'name': {},
            },
            'audiences': ['aud1'],
            'resource_methods': ['POST', 'GET'],
        },
        'bar': {
            'audiences': ['aud2'],
        },
        'baz': {
            'audiences': ['aud1'],
            'allowed_roles': ['role1', 'role2'],
        },
        'bad': {
        },
        'bag': {
            'audiences': ['aud1'],
            # 'authentication': JWTAuth(jwk.dumps(alt_public_key)),
        },
    },
}


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = Eve(settings=settings, auth=JWTAuth(default_key=public_key))
        test_routes.register(self.app)
        self.test_client = self.app.test_client()

    def test_restricted_access(self):
        r = self.test_client.get('/foo')
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.headers['WWW-Authenticate'], 'Bearer realm="eve_jwt"')

    def test_token_error(self):
        r = self.test_client.get('/foo?access_token=invalid')
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.headers['WWW-Authenticate'], 'Bearer realm="eve_jwt", error="invalid_token"')

    def test_valid_token_header(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        auth = [('Authorization', 'Bearer {}'.format(token.decode('utf-8')))]
        r = self.test_client.get('/foo', headers=auth)
        self.assertEqual(r.status_code, 200)

    def test_valid_token_query(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/foo?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200)

    def test_token_claims_context(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        with self.app.test_client() as client:
            client.get('/foo?access_token={}'.format(token.decode('utf-8')))
            self.assertEqual(g.get('authen_claims'), claims)

    def test_invalid_token_secret(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, alt_private_key)
        r = self.test_client.get('/foo?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401)

    def test_missing_token_subject(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/foo?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200)

    def test_invalid_token_issuer(self):
        claims = {'iss': 'https://invalid-domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/foo?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401)

    def test_invalid_token_audience(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud2',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/foo?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401)

    def test_valid_token_resource_audience(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud2',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/bar?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200)

    def test_invalid_token_resource_audience(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/bar?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401)

    def test_valid_token_role(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'roles': ['role1']}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/baz?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200)

    def test_invalid_token_role(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/baz?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401)

    def test_token_role_context(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'roles': ['role1']}
        token = jwt.encode(header, claims, private_key)
        with self.app.test_client() as client:
            client.get('/baz?access_token={}'.format(token.decode('utf-8')))
            self.assertEqual(g.get('authen_roles'), ['role1'])

    def test_token_role_context_always(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'roles': ['role1']}
        token = jwt.encode(header, claims, private_key)
        with self.app.test_client() as client:
            client.get('/foo?access_token={}'.format(token.decode('utf-8')))
            self.assertEqual(g.get('authen_roles'), ['role1'])

    def test_token_scope(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'scope': 'user'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/foo?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200)

    def test_token_scope_viewer_read(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'scope': 'viewer'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/foo?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200)

    def test_token_scope_viewer_write(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'scope': 'viewer'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.post('/foo?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401)

    def test_requires_token_success(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'roles': ['super'],
                  'scope': 'user'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/token/success?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200, r.data)

    def test_requires_token_failure_audience(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud2',
                  'sub': '0123456789abcdef01234567',
                  'roles': ['super'],
                  'scope': 'user'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/token/failure?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401, r.data)

    def test_requires_token_failure_roles(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'roles': [],
                  'scope': 'user'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/token/failure?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401, r.data)

    def test_auth_header_token_success(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567',
                  'roles': ['super'],
                  'scope': 'user'}
        token = jwt.encode(header, claims, private_key)
        headers = {'Authorization': 'Bearer {}'.format(token.decode('utf-8'))}
        r = self.test_client.get('/token/success', headers=headers)
        self.assertEqual(r.status_code, 200)

    def test_auth_header_token_failure(self):
        r = self.test_client.get('/token/failure')
        self.assertEqual(r.status_code, 401, r.data)

    def test_no_audience_token_success(self):
        claims = {'iss': 'https://domain.com/token'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/bad?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200)

    def test_no_audience_token_failure(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'sub': '0123456789abcdef01234567'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/bad?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 401)

    def test_endpoint_level_auth_with_different_secret(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1'}
        token = jwt.encode(header, claims, private_key)
        r = self.test_client.get('/bag?access_token={}'.format(token.decode('utf-8')))
        self.assertEqual(r.status_code, 200)

    def test_auth_header_token_success_with_different_secret(self):
        claims = {'iss': 'custom_issuer',
                  'aud': 'aud1',
                  'roles': ['super']}
        token = jwt.encode(header, claims, private_key)
        headers = {'Authorization': 'Bearer {}'.format(token.decode('utf-8'))}
        r = self.test_client.get('/custom/success', headers=headers)
        self.assertEqual(r.status_code, 200)

    def test_auth_header_token_failure_with_wrong_issuer(self):
        claims = {'iss': 'https://domain.com/token',
                  'aud': 'aud1',
                  'roles': ['super']}
        token = jwt.encode(header, claims, private_key)
        headers = {'Authorization': 'Bearer {}'.format(token.decode('utf-8'))}
        r = self.test_client.get('/custom/success', headers=headers)
        self.assertEqual(r.status_code, 401)


if __name__ == '__main__':
    unittest.main()
