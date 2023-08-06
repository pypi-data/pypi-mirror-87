import uuid
import pytest
import datetime
import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from api_jwt import APIJwt

logging.basicConfig(level=logging.DEBUG)


def test_new_token():
    new = APIJwt()
    eid = str(uuid.uuid4())
    new.encode(eid)
    assert new.id == eid


@pytest.fixture()
def jwt_token():
    new = APIJwt()
    eid = str(uuid.uuid4())
    new.encode(eid, level=1.0, factor='password', scopes=['user:all'], exp=7200)
    return new


def test_valid(jwt_token):
    assert jwt_token.is_valid is True


def test_not_expired(jwt_token):
    assert jwt_token.is_expired is False


def test_bad(jwt_token):
    assert jwt_token.is_bad is False


def test_jwt(jwt_token):
    assert jwt_token.jwt is not None


def test_decode(jwt_token):
    t = jwt_token.jwt
    new = APIJwt()
    new.decode(t)
    assert new.is_valid is True
    assert new.level == 1.0
    assert 'user:all' in new.scopes
    assert 'fake' not in new.scopes
    with pytest.raises(AttributeError):
        assert 'fake' in new.groups
    assert new.factor == 'password'
    assert new.expiry > datetime.datetime.utcnow() + datetime.timedelta(seconds=7180)
    assert new.expiry < datetime.datetime.utcnow() + datetime.timedelta(seconds=7201)


def test_add_extras():
    new = APIJwt(
        extras={
            'testkey': 'default'
        },
        allowed={
            'testkey': ['default', 'nr2', 'nr3']
        })
    # Alternative approach:
    # new.set_extras('testkey', 'default')
    # new.set_allowed('testkey', ['default', 'nr2', 'nr3'])
    eid = str(uuid.uuid4())
    new.encode(eid)
    new.decode(new.jwt)
    assert new.is_valid is True
    assert new.testkey == 'default'
    try:
        new.encode(eid, testkey='wrong')
    except ValueError:
        pass
    new.encode(eid, testkey='nr3')
    new.decode(new.jwt)
    assert new.is_valid is True
    assert new.testkey == 'nr3'


def test_expired():
    new = APIJwt()
    eid = str(uuid.uuid4())
    new.encode(eid, level=1.0, scopes=['user:all'], exp=-10)
    assert new.is_expired is True
    new2 = APIJwt()
    new2.decode(new.jwt)
    assert new2.is_valid is False
    assert new2.is_expired is True


def test_extra_factor():
    new = APIJwt()
    eid = str(uuid.uuid4())
    new.encode(eid, factor='something', scopes=['user:all'], exp=3600)
    assert new.is_expired is False
    new2 = APIJwt()
    new2.decode(new.jwt)
    assert new2.is_valid is True
    assert new2.factor == 'something'


def test_extra_float_int():
    new = APIJwt()
    eid = str(uuid.uuid4())
    new.encode(eid, level=1.0, dnt=3, scopes=['user:all'], exp=3600)
    assert new.is_expired is False
    new2 = APIJwt()
    new2.decode(new.jwt)
    assert new2.is_valid is True
    assert new2.level == 1.0
    assert new2.dnt == 3


def test_none_values():
    new = APIJwt()
    eid = str(uuid.uuid4())
    new.encode(eid, factor=None, level=None, dnt=None, scopes=['user:all'], exp=3600)
    assert new.is_expired is False
    new2 = APIJwt()
    new2.decode(new.jwt)
    assert new2.is_valid is True
    assert new2.factor == ''
    assert new2.dnt == 0


def test_multiple_scopes():
    new = APIJwt()
    new.set_allowed('scopes',
                    {
                        'PER_KEY': {
                            'user': ['user:all'],
                            'admin': ['admin:all', 'extra']
                        }
                    }
                    )
    eid = str(uuid.uuid4())
    new.encode(eid, key='admin', level=1.0, dnt=3, scopes=['extra', 'admin:all'], exp=3600)
    assert new.is_expired is False
    new2 = APIJwt()
    new2.decode(new.jwt)
    assert new2.is_valid is True
    assert 'admin:all' in new2.scopes
    assert 'extra' in new2.scopes
    assert 'nope' not in new2.scopes


def test_extra_groups():
    new = APIJwt()
    new.set_extras('groups', [])
    new.set_allowed('groups', [
        'group1',
        'group2'
    ])
    eid = str(uuid.uuid4())
    try:
        new.encode(eid, groups='group3', exp=3600)
    except ValueError:
        assert True is True  # noqa
    try:
        new.encode(eid, groups=['group3'], exp=3600)
    except ValueError:
        assert True is True  # noqa
    new.encode(eid, groups=['group2'], exp=3600)
    assert new.is_valid is True
    new2 = APIJwt()
    new2.set_extras('groups', [])
    new2.decode(new.jwt)
    assert new2.is_valid is True
    assert new2.groups == ['group2']


def test_new_keypair(jwt_token):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    priv_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    # Override preset keys with this new keypair, the token should then not validate
    jwt_token.override_keys(public_key, priv_key)
    jwt_token.decode(jwt_token.jwt)
    assert jwt_token.is_valid is False
    # Reset back, now it should validate
    jwt_token.reset_keys()
    jwt_token.decode(jwt_token.jwt)
    assert jwt_token.is_valid is True
    # Add the new key, it should still validate
    jwt_token.add_public_keys([public_key])
    jwt_token.decode(jwt_token.jwt)
    assert jwt_token.is_valid is True
    # Reset, override private, add new public key, it should still validate
    jwt_token.reset_keys()
    jwt_token.override_keys(private_key=priv_key)
    jwt_token.add_public_keys([public_key])
    jwt_token.decode(jwt_token.jwt)
    assert jwt_token.is_valid is True
    # Generate new jwt with new private key, it should validate
    tok1 = jwt_token.jwt
    jwt_token.encode(str(uuid.uuid4()), level=1.0, scopes=['user:all'], exp=3600)
    tok2 = jwt_token.jwt
    jwt_token.decode(tok2)
    assert jwt_token.is_valid is True
    # First jwt should also validate since both public keys are registered
    jwt_token.decode(tok1)
    assert jwt_token.is_valid is True
    # Reset keys, tok2 should fail, tok1 should validate
    jwt_token.reset_keys()
    jwt_token.decode(tok2)
    assert jwt_token.is_valid is False
    jwt_token.decode(tok1)
    assert jwt_token.is_valid is True
