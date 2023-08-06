# -*- coding: utf-8 -*-

from .connection import Connection


class EmptyConnection(Connection):
    name = "empty"
