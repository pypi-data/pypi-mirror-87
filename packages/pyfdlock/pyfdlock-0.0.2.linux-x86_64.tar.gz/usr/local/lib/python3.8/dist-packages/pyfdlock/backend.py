import os
import fcntl


class AIOBackend(object):
    def lockf(self, fd, pos, length):
        raise NotImplementedError

    def unlockf(self, fd, pos, length):
        raise NotImplementedError


class VirtualBackend(AIOBackend):
    def lockf(self, fd, pos, length):
        pass

    def unlockf(self, fd, pos, length):
        pass


class fnctlBackend(AIOBackend):
    def lockf(self, fd, pos, length):
        return fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, length, pos, os.SEEK_SET)

    def unlockf(self, fd, pos, length):
        return fcntl.lockf(fd, fcntl.LOCK_UN, length, pos, os.SEEK_SET)
