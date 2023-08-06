import json
import logging
import os
import threading

import gnupg
from redis import StrictRedis

from om.utils import config

_encryption = None


def get_encryption():
    global _encryption
    if not _encryption:
        _encryption = Encryption()
    return _encryption


def encrypt(data, outfile=None, compress=True, key_name="default"):
    return get_encryption().encrypt(data, outfile, compress, key_name)


def encrypt_file(file_name, out_file_name=None, key_name="default",
                 always_delete_unencrypted=False, delete_unencrypted_on_success=True):
    return get_encryption().encrypt_file(file_name, out_file_name=out_file_name, key_name=key_name,
                                         always_delete_unencrypted=always_delete_unencrypted,
                                         delete_unencrypted_on_success=delete_unencrypted_on_success)


class Encryption:
    REDIS_HKEY = "kv"
    REDIS_KEY_PREFIX = "encryption_key-"
    REDIS_DEFAULT_KEY = "encryption_key-default"

    def __init__(self):
        self.redis = StrictRedis(host=config.string("REDIS_HOST", "localhost"),
                                 port=config.int("REDIS_PORT", 6379),
                                 db=config.int("REDIS_DB", 0))
        self.gpg = gnupg.GPG()
        self.gpg.encoding = "utf-8"
        self.lock = threading.RLock()
        self.fingerprints_by_key_name = {}
        self.fingerprint_usage = {}
        self.old_fingerprints = []
        self.init_keys()

    def init_keys(self):
        keys = [x for x in self.redis.hgetall("kv").keys() if x.startswith(b"encryption_key-")]
        for key in keys:
            key_name = key.decode("utf-8").split("-", 1)[1]
            fp = self.get_fingerprint(key_name)
            self.cleanup(fp)

        fingerprints_to_delete = [x["fingerprint"] for x in self.gpg.list_keys()
                                  if x["fingerprint"] not in list(self.fingerprints_by_key_name.values())]
        # remove all unnecessary keys from keyring
        for fp in fingerprints_to_delete:
            self.gpg.delete_keys(fp)

    def cleanup(self, fp, key_name=None):
        if fp:
            with self.lock:
                self.fingerprint_usage[fp] -= 1
                self.remove_old_key(fp, key_name)

    def remove_old_key(self, fp, key_name):
        if fp in self.old_fingerprints:
            if not self.fingerprint_usage.get(fp):
                self.gpg.delete_keys(fp)
                del self.fingerprint_usage[fp]
                self.old_fingerprints.remove(fp)
            if self.fingerprints_by_key_name.get(key_name) == fp:
                self.fingerprints_by_key_name.pop(key_name, None)

    def get_fingerprint(self, key_name="default"):
        redis_key = self.REDIS_KEY_PREFIX + key_name
        data = self.redis.hget(self.REDIS_HKEY, redis_key)

        with self.lock:
            old_fingerprint = self.fingerprints_by_key_name.get(key_name)
            if data:
                new_key = json.loads(data)

                if not new_key.get("fingerprint"):
                    self.redis.hdel(self.REDIS_HKEY, redis_key)
                    return None

                if new_key.get("fingerprint") != old_fingerprint:
                    import_result = self.gpg.import_keys(new_key["pubkey"])
                    if import_result.unchanged or import_result.imported:
                        fp = import_result.fingerprints[0]
                        # multiple fingerprints?
                        if any(x != fp for x in import_result.fingerprints):
                            return None
                        self.fingerprints_by_key_name[key_name] = fp
                        self.fingerprint_usage[fp] = 0
                        if old_fingerprint:
                            self.old_fingerprints.append(old_fingerprint)
                            self.remove_old_key(old_fingerprint, key_name)

            # delete key from key ring, no longer here
            elif old_fingerprint:
                old_fingerprint = self.fingerprints_by_key_name[key_name]
                self.old_fingerprints.append(old_fingerprint)
                self.remove_old_key(old_fingerprint, key_name)

            fp = self.fingerprints_by_key_name.get(key_name)
            if fp:
                self.fingerprint_usage[fp] = self.fingerprint_usage.get(fp, 0) + 1
            return fp

    def encrypt_file(self, file_name, out_file_name=None, key_name="default",
                     always_delete_unencrypted=False, delete_unencrypted_on_success=True, **kwargs):
        new_name = out_file_name or f"{file_name}.pgp"
        if not new_name.endswith(".pgp"):
            new_name = new_name + ".pgp"

        with open(file_name, "rb") as file:
            compress = True
            ending = file_name.rsplit(".", 1)
            if ending in ["gz", "jpg", "jpeg"]:
                compress = False

            success = self.encrypt(file, new_name, compress, key_name, **kwargs)
        if always_delete_unencrypted or (success and delete_unencrypted_on_success):
            os.remove(file_name)

        return False if success is None else True

    def encrypt(self, data, out_file=None, compress=True, key_name="default", **kwargs):
        if out_file is not None and not out_file.endswith(".pgp"):
            out_file += ".pgp"

        extra_args = None
        if compress:
            extra_args = ['-z', '0']

        fp = self.get_fingerprint(key_name)
        if not fp:
            return None

        if isinstance(data, str) or isinstance(data, bytes) or isinstance(data, bytearray):
            result = self.gpg.encrypt(data, fp, always_trust=True, extra_args=extra_args, output=out_file, armor=False,
                                      **kwargs)
        else:
            result = self.gpg.encrypt_file(data, fp, always_trust=True, extra_args=extra_args, output=out_file,
                                           armor=False, **kwargs)
        self.cleanup(fp, key_name=key_name)

        if result.ok:
            return result.data

        logging.warning(f"Decryption error: {result.status}")
        return None

    def decrypt(self, data, passphrase=""):
        if isinstance(data, str) or isinstance(data, bytes) or isinstance(data, bytearray):
            decrypted = self.gpg.decrypt(data, passphrase=passphrase)
        else:
            decrypted = self.gpg.decrypt_file(data, passphrase=passphrase)
        if decrypted.ok:
            return decrypted.data
        return None


if __name__ == "__main__":
    enc = Encryption()

    enc.encrypt_file("/data/asdf", "/data/asdf.pgp", delete_unencrypted_on_success=False)

    with open("/data/asdf.pgp", "rb") as file:
        with open("/data/asdf_decrypted", "wb") as out:
            out.write(enc.decrypt(file, passphrase="arivotest"))

    with open("/data/asdf", "rb") as f1:
        with open("/data/asdf_decrypted", "rb") as f2:
            print(f1.read() == f2.read())
