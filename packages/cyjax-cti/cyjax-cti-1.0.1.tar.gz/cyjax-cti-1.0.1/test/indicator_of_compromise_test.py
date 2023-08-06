#  CYjAX Limited

import datetime
import logging
from datetime import timedelta
from unittest.mock import patch, Mock

import pytest
import pytz

from cyjax import IndicatorOfCompromise, InvalidDateFormatException


class TestIndicatorOfCompromise:

    fake_date = Mock(wraps=datetime.datetime)
    fake_date.now.return_value.astimezone.return_value = datetime.datetime(2020, 5, 2, 12, 0, 0, tzinfo=pytz.UTC)

    def test_get_indicator_of_compromise_without_parameters(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list()
        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params={})

    def test_get_indicator_of_compromise_with_parameters(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since='2020-05-02T07:31:11+00:00', until='2020-07-02T00:00:00+00:00')

        expected_params = {'since': '2020-05-02T07:31:11+00:00', 'until': '2020-07-02T00:00:00+00:00'}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    @patch('cyjax.helpers.datetime', fake_date)
    def test_get_indicator_of_compromise_with_date_as_timedelta(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since=timedelta(hours=2), until=timedelta(hours=1))

        since = '2020-05-02T10:00:00+00:00'
        until = '2020-05-02T11:00:00+00:00'
        expected_params = {'since': since, 'until': until}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicator_of_compromise_with_date_as_datetime_without_timezone(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0),
                                     until=datetime.datetime(2020, 5, 2, 11, 0, 0))

        since = datetime.datetime(2020, 5, 2, 10, 0, 0).astimezone().isoformat()
        until = datetime.datetime(2020, 5, 2, 11, 0, 0).astimezone().isoformat()
        expected_params = {'since': since, 'until': until}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicator_of_compromise_with_date_as_datetime_with_timezone(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0, tzinfo=pytz.UTC),
                                     until=datetime.datetime(2020, 5, 2, 11, 0, 0, tzinfo=pytz.UTC))

        expected_params = {'since': '2020-05-02T10:00:00+00:00', 'until': '2020-05-02T11:00:00+00:00'}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicator_of_compromise_with_date_as_string(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since='2020-05-02T10:00:00+00:00', until='2020-05-02T11:00:00+00:00')

        expected_params = {'since': '2020-05-02T10:00:00+00:00', 'until': '2020-05-02T11:00:00+00:00'}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicator_of_compromise_with_wrong_date(self):
        indicator_of_compromise = IndicatorOfCompromise()
        with pytest.raises(InvalidDateFormatException):
            indicator_of_compromise.list(since='2020-05', until='2020-05-02T11:00:00+00:00')

        with pytest.raises(InvalidDateFormatException):
            indicator_of_compromise.list(since='2020-05-02T11:00:00+00:00', until='2020-05')
