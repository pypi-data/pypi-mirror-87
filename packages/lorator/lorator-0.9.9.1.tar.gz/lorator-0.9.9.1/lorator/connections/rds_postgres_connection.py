# -*- coding: utf-8 -*-

from .connection import Connection


class RdsPostgresConnection(Connection):
    name = "rds_postgres"
