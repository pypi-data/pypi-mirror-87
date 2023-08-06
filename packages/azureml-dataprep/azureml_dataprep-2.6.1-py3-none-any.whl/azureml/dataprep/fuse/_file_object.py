from typing import Optional

from azureml.dataprep.api._loggerfactory import _LoggerFactory

from ._handle_object import HandleObject
from ._local_driver import LocalDriver


log = _LoggerFactory.get_logger('dprep.writable_fuse')


class FileObject(HandleObject):
    def __init__(self, handle: int, path: str, flags: int, driver: LocalDriver):
        super().__init__(path, handle)
        self.flags = flags
        self._driver = driver
        self._last_flush_modified_time = None

    def read(self, size, offset, buffer):
        return self._driver.read(self.path, size, offset, self.handle, buffer)

    def write(self, size, offset, buffer):
        result = self._driver.write(self.path, size, offset, self.handle, buffer)
        return result

    def release(self):
        pass

    def reset_last_flush_modified_time(self):
        self._last_flush_modified_time = self._get_local_last_modified()

    @property
    def is_dirty(self):
        return self._get_local_last_modified() != self._last_flush_modified_time

    @property
    def last_flush_modified_time(self) -> Optional[float]:
        return self._last_flush_modified_time

    @last_flush_modified_time.setter
    def last_flush_modified_time(self, value: Optional[float]):
        self._last_flush_modified_time = value

    def _get_local_last_modified(self) -> float:
        try:
            stat = self._driver.get_attributes(self.path)
            return stat.st_mtime
        except Exception as e:
            log.debug('Unable to get last modified of {} because of {}.'.format(self.path, e))
            return None
