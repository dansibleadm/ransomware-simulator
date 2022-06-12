import os
import stat
import json
import struct
from logger import Logger, TIMESTAMP, SIMULATION_ID
from hashlib import sha256

log = Logger.create_logger("FileManager")

class List:
    def __init__(self, path_to_list):
        self.path_to_list = path_to_list
        self.content = self.load_list()

    def load_list(self):
        try:
            with open(self.path_to_list, 'r') as file:
                content = json.load(file)
            log.info(f"File {self.path_to_list} was loaded.")
            return content
        except Exception as exc:
            log.error(exc, exc_info=True)
            return 0

class Journal:
    def __init__(self):
        self.content = dict(source_files=[], encrypted_files=[], decrypted_files=[])
        log.info("Journal initiated.")

    def save_into_journal(self, File):
        file = File.__dict__
        if file["is_encrypted"]:
            self.content["encrypted_files"].append(file)
        elif file["is_decrypted"]:
            self.content["decrypted_files"].append(file)
        else:
            self.content["source_files"].append(file)

        log.info(f"File {file['filename']} saved into journal.")

    def save_journal(self):
        try:
            json_content = json.dumps(self.content, indent=4)
            log.info("Journal was dumped.")
            json_filename = f"journal_{TIMESTAMP}_{SIMULATION_ID}.json"
            with open(json_filename, 'w') as json_file:
                json_file.write(json_content)
            log.info(f"Journal {json_filename} was saved into file_manager folder.")
        except Exception as exc:
            log.error(exc, exc_info=True)

class BaseFile:

    def __init__(self, filename, path_to_file, is_encrypted=False, is_decrypted=False):
        self.filename = filename
        self.path_to_file = path_to_file
        self.is_encrypted = is_encrypted
        self.is_decrypted = is_decrypted
        log.info(f"File {self.filename} was initiated.")

    def calc_checksum(self):
        try:
            content = self.read()
            self.checksum = str(sha256(content).hexdigest())
        except Exception as exc:
            log.error(exc, exc_info=True)
            return 0

    def save(self, *content):
        try:
            with open(self.path_to_file, "wb") as file:
                count_chunk = 0
                for chunk in content:
                    count_chunk += 1
                    if count_chunk == len(content):
                        file.write(chunk.rstrip())
                    else:
                        file.write(chunk)
            log.info(f"File {self.filename} was saved to {self.path_to_file}.")
        except Exception as exc:
            log.error(exc, exc_info=True)

    def read(self):
        try:
            if self.is_encrypted:
                chunks = []
                with open(self.path_to_file, "rb") as file:
                    fsz = struct.unpack('<Q', file.read(struct.calcsize('<Q')))[0]
                    file.read(16) # skip iv
                    content = file.read()
            else:
                with open(self.path_to_file, "rb") as file:
                    content = file.read()
            log.info(f"File {self.filename} was readed from {self.path_to_file}.")
            return content
        except Exception as exc:
            log.error(exc, exc_info=True)
            return 0

    def rename(self, new_path_to_file):
        try:
            os.rename(self.path_to_file, new_path_to_file)
            log.info(f"File was renamed into {new_path_to_file}")
        except Exception as exc:
            log.error(exc, exc_info=True)

class File(BaseFile):
    def __init__(self, filename, path_to_file):
        super().__init__(filename, path_to_file)