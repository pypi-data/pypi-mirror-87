# -*- coding: utf-8 -*-


from ..dbal.platforms import PostgresPlatform
from .connector import Connector


class EmptyAPI:
    @staticmethod
    def connect(dsn=None, connection_factory=None, cursor_factory=None, **kwargs):
        pass


class EmptyConnector(Connector):
    def get_api(self):
        return EmptyAPI

    def get_dbal_platform(self):
        return PostgresPlatform()
