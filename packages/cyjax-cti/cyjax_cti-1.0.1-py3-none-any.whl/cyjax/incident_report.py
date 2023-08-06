from .helpers import DateHelper
from .resource import Resource


class IncidentReport(Resource):

    def __init__(self, api_key=None):
        """
        :param api_key: The API key.
        """
        super(IncidentReport, self).__init__(api_key=api_key)

    def list(self, query=None, since=None, until=None):
        """
        Returns incident reports.
        :param query: The search query.
        :type query: str, optional
        :param since: The start date time.
        :type since: (datetime, timedelta, str), optional
        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional
        :return: The list of incident reports.
        :rtype list
        """

        params = DateHelper.build_date_params(since=since, until=until)
        if query:
            params.update({'query': query})

        return self.paginate(endpoint='report/incident', params=params)
