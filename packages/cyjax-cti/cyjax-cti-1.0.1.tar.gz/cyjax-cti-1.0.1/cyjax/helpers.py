from datetime import datetime, timedelta

from .exceptions import InvalidDateFormatException

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


class DateHelper(object):

    @staticmethod
    def parse_date(date):
        """
        Parse the date to string based on the parameter type.
        :param date: The date.
        :type date: datetime, timedelta, str
        :return: The date as string in ISO8601 format.
        :rtype: str
        :raises InvalidDateFormatException: Whether the date cannot be parsed.
        """
        if isinstance(date, timedelta):
            date = datetime.now().astimezone() - date
            date = date.replace(microsecond=0).isoformat()
        elif isinstance(date, datetime):
            if not date.tzinfo:
                date = date.astimezone()

            date = date.replace(microsecond=0).isoformat()

        elif isinstance(date, str):
            try:
                datetime.fromisoformat(date)
            except:
                raise InvalidDateFormatException("Incorrect date format, should be %s" % DATE_FORMAT)
        else:
            raise InvalidDateFormatException("Please provide a datetime, timedelta or str object")

        return date

    @staticmethod
    def build_date_params(since=None, until=None):
        date_params = {}

        if since:
            try:
                date_params.update({'since': DateHelper.parse_date(since)})
            except InvalidDateFormatException as e:
                raise InvalidDateFormatException("since: %s" % e)

        if until:
            try:
                date_params.update({'until': DateHelper.parse_date(until)})
            except InvalidDateFormatException as e:
                raise InvalidDateFormatException("until: %s" % e)

        return date_params

