# -*- coding: utf-8 -*-

from ..dbal.platforms import PostgresPlatform
from .connector import Connector
import aurora_data_api_orator


class RdsPostgresConnector(Connector):
    def get_api(self):
        return aurora_data_api_orator

    def get_dbal_platform(self):
        return PostgresPlatform()

    def cursor(self):
        return aurora_data_api_orator.AuroraDataAPICursor(**self.get_params())
