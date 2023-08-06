from cryptography.fernet import Fernet, InvalidToken

class Token:
    
    def __init__(self, secret_key=None):
        self.secret_key = secret_key if secret_key else Token.key(False)
        self._fernet = Fernet(self.secret_key)
        
    def encrypt(self, data, decode=True):
        data = str(data).encode()
        token = self._fernet.encrypt(data)
        return token.decode() if decode else token
    
    def decrypt(self, token, decode=True):
        try:
            if isinstance(token, str):
                token = token.encode()
            data = self._fernet.decrypt(token)
            return data.decode() if decode else data
        except InvalidToken as ex:
            raise Exception('Config token is invalid.')
        
    @property
    def secret_key(self):
        return self._secret_key
    
    @secret_key.setter
    def secret_key(self, value):
        if not isinstance(value, bytes):
            raise ValueError('secret key must be bytes.')
        self._secret_key = value
    
    @staticmethod
    def key(decode=True):
        key = Fernet.generate_key()
        return key.decode() if decode else key