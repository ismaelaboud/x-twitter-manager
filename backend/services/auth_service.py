import secrets
from typing import Dict, Optional
from cryptography.fernet import Fernet
import os

class AuthService:
    def __init__(self):
        # Generate or load encryption key
        self.encryption_key = self._load_or_generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # In-memory storage for encrypted credentials (can be replaced with database)
        self.credentials: Dict[str, Dict[str, str]] = {}

    def _load_or_generate_key(self):
        """
        Load existing encryption key or generate a new one
        """
        key_path = os.path.join(os.path.dirname(__file__), 'encryption.key')
        
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            return key

    def encrypt_credentials(self, credentials: Dict[str, str]) -> str:
        """
        Encrypt Twitter API credentials
        
        :param credentials: Dictionary of API credentials
        :return: Encrypted token
        """
        credentials_str = str(credentials).encode()
        encrypted_credentials = self.cipher_suite.encrypt(credentials_str)
        return encrypted_credentials.decode()

    def decrypt_credentials(self, encrypted_token: str) -> Optional[Dict[str, str]]:
        """
        Decrypt Twitter API credentials
        
        :param encrypted_token: Encrypted credentials token
        :return: Decrypted credentials dictionary
        """
        try:
            decrypted = self.cipher_suite.decrypt(encrypted_token.encode())
            return eval(decrypted.decode())
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

    def add_account_credentials(self, username: str, credentials: Dict[str, str]):
        """
        Add encrypted credentials for a Twitter account
        
        :param username: Unique username for the account
        :param credentials: Twitter API credentials
        """
        encrypted_token = self.encrypt_credentials(credentials)
        self.credentials[username] = {
            'encrypted_token': encrypted_token,
            'added_at': secrets.token_hex(8)  # Timestamp-like identifier
        }
        return True

    def get_account_credentials(self, username: str) -> Optional[Dict[str, str]]:
        """
        Retrieve decrypted credentials for a Twitter account
        
        :param username: Username to retrieve credentials for
        :return: Decrypted credentials or None
        """
        account = self.credentials.get(username)
        if account:
            return self.decrypt_credentials(account['encrypted_token'])
        return None

    def remove_account_credentials(self, username: str):
        """
        Remove credentials for a Twitter account
        
        :param username: Username to remove
        """
        if username in self.credentials:
            del self.credentials[username]
            return True
        return False

    def list_accounts(self):
        """
        List all stored account usernames
        
        :return: List of account usernames
        """
        return list(self.credentials.keys())
