#!/usr/bin/python
import os


class FilterModule(object):
    def filters(self):
        return {
            'path_join': self.path_join,
        }

    def path_join(self, paths):
        return os.path.join(*paths)
