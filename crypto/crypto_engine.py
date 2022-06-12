import struct
import os
from hashlib import md5
from uuid import uuid4
from logger import Logger
from Crypto.Cipher import AES

class BaseCryptoEngine:
    def __init__(self, extension, key, iv):
        self.log = Logger.create_logger("CryptoEngine")
        self.extension = extension
        self.secret_key = key if key else str(md5(str(uuid4()).encode('utf-8')).hexdigest()).encode("utf-8")
        self.iv = iv if iv else str(md5(str(uuid4()).encode('utf-8')).hexdigest()).encode("utf-8")[-16:]
        self.aes = AES.new(self.secret_key, AES.MODE_CBC, self.iv)

    def init_aes_obj(self):
        self.aes = AES.new(self.secret_key, AES.MODE_CBC, self.iv)

class CryptoEngine(BaseCryptoEngine):

    def __init__(self, extension, key, iv):
        super().__init__(extension, key, iv)
        self.log.info(f"CryptoEngine initiated. Key: {self.secret_key}; IV: {self.iv}")

    def encrypt(self, Target):
        try:
            if Target.is_encrypted:
                self.log.warning(f"File already encrypted! {Target.__dict__}")
                return

            out_path_to_file = f"{Target.path_to_file}{self.extension}"
            source_content = Target.read()

            chunks = []
            filesize = os.path.getsize(Target.path_to_file)
            chunks.append(struct.pack('<Q', filesize))
            chunks.append(self.iv)

            while len(source_content) != 0:
                buff = source_content[:16]
                if len(buff) % 16 != 0:
                    buff += b' ' * (16 - len(buff) % 16)
                chunks.append(self.aes.encrypt(buff))
                source_content = source_content[16:]
                
            Target.save(*chunks)
            self.log.info(f"File {Target.filename} was encrypted into {out_path_to_file}!")
            Target.rename(out_path_to_file)
        except Exception as exc:
            self.log.error(exc, exc_info=True)

    def decrypt(self, Target):
        try:
            if not Target.is_encrypted:
                self.log.warning(f"File already decrypted or never was encrypted! {Target.__dict__}")
                return

            out_path_to_file = f"{Target.path_to_file[:-len(self.extension)]}"
            encrypted_content = Target.read()

            chunks = []

            while len(encrypted_content) != 0:

                buff = encrypted_content[:16]
                chunks.append(self.aes.decrypt(buff))
                encrypted_content = encrypted_content[16:]

            Target.save(*chunks)
            self.log.info(f"File {Target.filename} was decrypted into {out_path_to_file}!")
            Target.rename(out_path_to_file)
        except Exception as exc:
            self.log.error(exc, exc_info=True)