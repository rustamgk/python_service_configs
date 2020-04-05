import typing
import json
import enum
import hashlib
import os

from .utils import is_entry_match

from .log import logger

__all__ = (
    'StorageType',
    'ConfigRegistry',
    'FileStorage',
)


class StorageType(enum.IntEnum):
    FileStorage = 1
    MongoDBStorage = 2


class ConfigRegistry(object):
    @classmethod
    def get(cls, storage=None):
        # type: (typing.Optional[StorageType]) -> FileStorage
        if storage == StorageType.MongoDBStorage:
            raise NotImplementedError('MongoDB not supported yet')
        elif storage == StorageType.FileStorage:  # pylint: disable=no-else-raise
            pass
        return FileStorage(os.environ.get('STORAGE_PATH', '/data'))


class FileStorage(object):
    """
    This is Config Registry based on files.

    It implements CRUD operations
    """

    def __init__(self, storage_path):
        # type: (str) -> None
        self._hash_algo = 'md5'
        self._path = storage_path

    def is_exists(self, name):
        # type: (str) -> bool
        return os.path.exists(self.get_entry_path(name))

    def _hash(self, key):
        # type: (str) -> str
        return str(hashlib.new(self._hash_algo, bytes(key, encoding='utf-8')).hexdigest())

    def get_entry_path(self, name):
        # type: (str) -> str
        hash_ = self._hash(name)
        return os.path.join(self._path, hash_[0], hash_[1:3], hash_)

    def store(self, config):
        # type: (typing.Dict) -> bool
        fname = self.get_entry_path(config.get('name'))
        try:
            os.makedirs(os.path.dirname(fname), exist_ok=True)
            with open(fname, 'wt') as fp:
                json.dump(config, fp, ensure_ascii=False)
                return True
        except PermissionError as exc:
            logger.error(exc)
        return False

    def load(self, name):
        # type: (str) -> typing.Optional[typing.Dict]
        fname = self.get_entry_path(name)
        try:
            with open(fname) as fp:
                return json.load(fp)
        except PermissionError as exc:
            logger.error(exc)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError as exc:
            logger.warning('Unable to load config: file=%s; error=%s', fname, exc)
        return None

    def delete(self, name):
        # type: (str) -> bool
        try:
            os.unlink(self.get_entry_path(name))
            return True
        except FileNotFoundError:
            return True
        except Exception as exc:
            logger.warning('%s', exc)
        return False

    def _iter_entries(self):
        # type: () -> typing.Generator[typing.Dict]
        try:
            for root, _, files in os.walk(self._path):
                for fname in files:
                    try:
                        fname = os.path.realpath(os.path.join(os.path.curdir, root, fname))
                        with open(fname) as fp:
                            yield json.load(fp)
                    except json.JSONDecodeError:
                        pass
                    except FileNotFoundError:
                        pass
        except FileNotFoundError:
            pass

    def list(self):
        # type: () -> typing.List[typing.Dict]
        return [entry for entry in self._iter_entries()]

    def search(self, criteria):
        # type: (typing.Dict) -> typing.List[typing.Dict]
        return [entry for entry in self._iter_entries() if is_entry_match(entry, criteria)]
