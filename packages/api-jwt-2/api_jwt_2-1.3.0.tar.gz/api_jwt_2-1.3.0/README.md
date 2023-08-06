# README and Getting Started

This Python library is a wrapper around pyjwt to support JWT creation and validation as well
as payload handling (scopes, auth level, etc).

## Use case

The typical use is a micro services architecture where a single auth service is responsible for issuing JWT tokens for clients you may or may not trust. 
In order to scale without a central point of failure, the JWT token should contain all necessary information for each micro service
to trust the identity of the requestor, as well what the requestor can access. This is done through embedding meta information in the
JWT token and signing it with a private key only known to the authn/authz service.

With only knowledge of the public key, any service can verify the signature of the JWT and thus prove it's authenticity.

**NOTE!!!** Do not store secrets in the payload, it is not encrypted and can easily be decoded and read.

## Typical use

Make your own wrapper through sub-classing the APIJwt class. In the initialisation, load the private key (for the
authn/authz service) and public key(s) for the all other services. In the authn/authz service that encodes JWTs, set all the extra payload keys that should be 
allowed (i.e. info you want to convey to the other services receiving the JWT), and then set the allowed values for each
of the keys. The decode does not validate the payload, just the signature, so these configurations are thus not
needed.

You can now use the encode() and decode() functions inherited from APIJwt to encode (and sign) the JWT, as well as
decode.

## Example use

Example wrapper where you add set your own configuration parameters

    from api_jwt import APIJwt 
    class HudyaJWT(APIJwt):
        def __init__(self, *args, **kwargs):
            if settings.JWT_KEY_PRIVATE:  # This could be loaded from os.env(), it should be base64 encoded
                                          # It should be in pem format and not be encrypted
                privkey = base64.b64decode(settings.JWT_KEY_PRIVATE).decode('utf-8')
            else:
                privkey = None
            if settings.JWT_KEY_PUBLIC:   # This could be loaded from os.env(), it should be base64 encoded in pem format
                pubkey = base64.b64decode(settings.JWT_KEY_PUBLIC).decode('utf-8')
            else:
                pubkey = None
            super().__init__(
                public_keys=pubkey,
                private_key=privkey,
                ttl=int(settings.JWT_TOKEN_TTL),  # This is in seconds
                *args, **kwargs)
    
            # The below is only required for encoding
            self.set_allowed('level', [
                0.0,  # Level 0, no authentication
                1.0,  # External auth
                2.0,  # Password/single-factor
                3.0,  # Multi-factor
                3.1,  # Yubikey
                3.5,  # External multi-factor
                4.0   # Certificate-level
            ])
            self.set_allowed('keys', {
                'user': 'auth_user',
                'support': 'auth_support',
                'admin': 'auth_admin'
            })
            self.set_allowed('scopes', {
                'PER_KEY': {  # Use single key with 'PER_KEY' to set allowed values based on key
                    'user': ['user:all', 'NO', 'SE', 'DK'],
                    'support': [
                        'support:all',
                        'support:insurance',
                        'support:power',
                        'support:mobile'
                    ],
                    'admin': ['admin:all', 'user:all']
                }
            })

With this class, you can encode a JWT:

    jwt_obj = HudyaJWT()
    token = jwt_obj.encode(
        subject='user@domain.com',
        level='3.1',
        factor='yubikey',
        target='user@domain.com',  # Used if the target of the scopes is different from subject
        key='support,
        exp=3600,
        scopes=['support:mobile'],
        dnt=0,  # Normal user, full tracking
    )
    if token is None:
        raise
        
Decoding is super-simple:

    jwt_data = HudyaJWT()
    payload = jwt_data.decode(token)
    if not jwt_data.is_valid:
        raise ValidationError("JWT is not valid")
    if 'support:mobile' in payload['scope']:
        print("Access granted!")

## How to release

Remember to update version in setup.py.

Running `docker-compose up -d` without env var COMMAND set will start up the container and run run.sh, which
will result in the tests being run and the container be kept running for subsequent docker exec commands.

To do a test build and release, run docker-compose with `COMMAND="build"` as an env variable (which will be passed into run.sh as a parameter).
In this case, the .pypirc file in the root dir of the docker build will be copied in. A pypitest server entry is expected.

To release, make sure you have the pypi server entry in .pypirc for release and run with COMMAND set to "release", e.g.:

`export COMMAND="release";docker-compose up -d`


**NOTE!!** Due to the volume set up in docker-compose.yml, the sources will be in sync inside and outside of the container, so
there is no need to rebuild the container.

**Do not forget to change CHANGELOG.md.**
