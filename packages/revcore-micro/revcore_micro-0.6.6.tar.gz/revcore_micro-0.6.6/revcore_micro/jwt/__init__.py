import boto3
import random
from jwt.algorithms import Algorithm
from jwt.api_jwt import PyJWT


class KMSAlgorithm(Algorithm):
    region = 'ap-northeast-1'

    def get_client(self):
        client = boto3.client('kms', self.region)
        return client

    def prepare_key(self, key):
        return key

    def sign(self, msg, key):
        client = self.get_client()
        resp = client.sign(KeyId=key, Message=msg, SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256')
        return resp['Signature']


class JWT(PyJWT):
    def __init__(self, algorithms=None, options=None):
        super().__init__(algorithms, options)
        self._algorithms = {'RS256': KMSAlgorithm()}


_jwt = JWT()
encode = _jwt.encode


class JWTEncoder:
    default_payload_classes = None
    key_class = None

    def __init__(self, client):
        self.client = client

    def get_payload_classes(self):
        return self.default_payload_classes.__members__.items()

    def get_private_key(self):
        keys = self.key_class.query(alg='RSA256', status='enabled', index_name='alg-status-index')
        key = random.choice(keys)
        return key['id']

    def build_payload(self, user):
        payload_classes = self.get_payload_classes()
        payload = {}
        for name, member in payload_classes:
            builder = member.value(client=self.client)
            payload[name] = builder.build_payload(user)

        return payload

    def encode(self, user):
        key = self.get_private_key()
        data = self.build_payload(user)
        headers = {'kid': key}
        encoded = encode(data, key=key, algorithm='RS256', headers=headers)
        return encoded.decode()
