# Ransomware Inquisitor

> **Attention! It’s not a real ransomware. Use with care in study and research proposes. Don’t use against real targets as a real attacker!**
> 

**Ransomware Inquisitor** is the full python-based ransomware simulator which provides AES-256 in CBC mode with encryption/decryption functions and possibility of spicifying custom targets via whitelist.  

Can be used on Windows (not tested yet), Linux (tested) and Darwin (not tested yet) systems.

Currently, this ransomware simulator only in MVP status. More things will be develop later. For example (Road map actually):

- [ ]  HTTP REST API for C2-communicating (useful for e.g. intergation in BAS)
- [ ]  Integrate more symmetric crypto algorithms
- [ ]  Evolize to RaaS-model (Ransomware-as-a-Service) for more comfortable management of your simulations
- [ ]  With RaaS will come asymmetric crypto algorithms

## Setup test environment (test example)

From root directory of the project run:

```bash
docker build -t inquisitor -f test_env/Dockerfile .
```

After the successuful building open an interactive shell, run:

```bash
docker run -ti inquisitor /bin/sh
```

## How-To

Run help command:

```bash
python3 [app.py](http://app.py) -h
```

- Available options
    
    “-l”, “—log_level” - you can specify log level for logging module. Choices: DEBUG, INFO, WARNING, ERROR, CRITICAL. Howerer, during process only INFO, WARNING and ERROR messages are written to log-file Default: DEBUG.
    
    “-e”, “—ransomware_extension” - you can specify ransomware extension which will append to filename (e.g. from file.txt to file.txt.crypto and back to file.txt). Default: “.crypto”.
    
    “-d”, “—decrypt_mode” - you can specify this flag for only decryption process. All files with provided ransomware extension will be decrypted. Important! With enabled decrypt mode - key and iv arguments are required! **If turned off - encrypt and decrypt are enabled.** Default: turned off.
    
    “-s”, “—start_path” - you can specify started path where engine will collect files for encrypt/decrypt. Default: 
    
    “-w”, “—whitelist” - you should specify path to file with whitelist for attack specified targets (json required). Please, don't remove 'required'-flag functionality in argparse module or you will shoot yourself in the foot :) Howerer, if you will remove that - use it with care. Check out format of whitelist in the next section or check my sample in root directory of the project (whitelist.json) Required: yes.
    
    “-k”, “—key” -  you can specify secret key for AES. Required with decrypt mode. Without decrypt mode - is optional. Required key with 32 bytes. But you can try another standart values for AES in CBC mode (not tested).
    
    “-i”, “—iv” - you can specify an initialization vector for AES. required with decrypt mode. Without decrypt mode - is optional. Must be 16 bytes.
    

Examples:

```bash
python3 app.py -s / -w /tmp/whitelist.json
```

where, “-s” - started path from “/”-directory and “-w” - path to whitelist on /tmp/whitelist.json.

After that you can find journal_timestamp_simulationId.json with metadata of files during encryption and decryption. Also you can find log-file simulation_timestamp_simulationId.log".

In journal you can find “source_files” (files before encryption, also it can be before decryption if decrypt_mode enabled), “encrypted_files” (files after encryption) and “decrypted_files” (files after decryption). Every section containt “filename”, “path_to_file” (absolute path to file), “is_encrypted” (is encrypted file or not), “is_decrypted” (is decrypted file or not) and “checksum” (checksum of file for comparing source/encrypted/decrypted file).

### Whitelist format (example from whitelist.json):

```json
{
    "dirs": [
		    "tmp",
        "/home"
    ], 
    "files": [
        "test_1.txt",
				"test_2.txt",
				"test_3.txt",
    ]
}
```

Files from “files” will be encrypted in started path, “/home/*” and in “*/tmp/*”. Attention: if you have “/home” (e.g.) in whitelist but your started path is another subdirectory of “/” (e.g. “/tmp” or “/var/log”) - files in “/home” will be never encrypted or decrypted.