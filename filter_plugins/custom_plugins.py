#!/usr/bin/python
import os


class FilterModule(object):
    def filters(self):
        return {
            'path_join': self.path_join,
            'not': self._not,
        }

    def path_join(self, paths):
        return os.path.join(*paths)

    def _not(self, x): return not x
