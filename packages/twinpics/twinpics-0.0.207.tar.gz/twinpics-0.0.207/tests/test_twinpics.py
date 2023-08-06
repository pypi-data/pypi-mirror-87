# Copyright 2020 Alberto Martín Mateos and Niloufar Shoeibi
# See LICENSE for details.

import pytest

import twinpics


def sample_tests():
    params = [
        {
            'value': True
        },
        {
            'value': False
        }
    ]

    for param in params:
        assert twinpics.sample_function(value=param['value'])


if __name__ == "__main__":
    sample_tests()
