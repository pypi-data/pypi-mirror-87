# -*- coding: utf-8 -*-

from enum import Enum


class Channel(Enum):
    PROD = "PROD"
    RECETTE = "RECETTE"
    TEST = "TEST"

    def __str__(self):
        return self._name_
