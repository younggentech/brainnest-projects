# -*- coding: utf-8 -*-
from countdown.model import get_time


def test_validate_form():
    f_rps_dict = {"hours": "", "minutes": "", "seconds": ""}
    test = get_time(f_rps_dict)
    assert list(test) == []
