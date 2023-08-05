from functools import partial

import pandas as pd

from bmll._rest import DEFAULT_SESSION
from bmll._utils import to_list_of_str, paginate, ID_COL_TYPE

__all__ = ('query', 'available_markets', 'ReferenceDataClient')


class ReferenceDataClient:
    """
    The ReferenceDataClient provides a convenient interface to interact with the BMLL Reference Data API.

    Parameters
    ----------
    session: :class:`bmll.Session`, optional
        if provided use this session object to communicate with the API, else use the default session.
    """

    def __init__(self, session=None):
        self._session = session or DEFAULT_SESSION

    def query(self,
              start_date=None,
              end_date=None,
              object_ids=None,
              object_type=None,
              **constraint):
        """
        Find reference data for Listings relating to a set of constraints, optionally over a date
        range and including sibling Listings on multilateral trading facilities or primary exchange.

        Parameters
        ----------
        start_date: str or datetime.date, optional
            First date to get data for.  iso-formatted date
            Default, previous business day.
        end_date: str or datetime.date, optional
            Last date to get data for. iso-formatted date
            Defaults to same date as start_date.
        object_ids: list(int), optional
            List of bmll ids to get reference data for.
        object_type: str, optional
            Must be either:
                - Listing
                - Instrument
                - Market
        **constraint:
            Keyword arguments for constraints to search for reference data.

            For example:

            .. code-block:: python

                MIC='XLON' or MIC=['XLON', 'XPAR']

            Allowed constraints include:
                - MIC
                - Ticker
                - FIGI
                - FIGIShareClass
                - ISIN
                - OPOL
                - DisplayName
                - Description.

            .. note:: constraints look for exact matches.

        Returns
        -------
        :class:`pandas.DataFrame`
            DataFrame of reference data matching the given criteria.

        """
        constraint = {identifier_name: to_list_of_str(identifiers)
                      for identifier_name, identifiers in constraint.items()}

        start_date = str(start_date) if start_date else None
        end_date = str(end_date) if end_date else None

        req = partial(self._get_page,
                      start_date=start_date,
                      end_date=end_date,
                      object_ids=object_ids,
                      object_type=object_type,
                      **constraint)

        result = paginate(req)
        result.pop('token')

        bmll_index_columns = [col for col in ('ListingId', 'InstrumentId', 'MarketId')
                              if col in result['columns']]
        bool_column_map = {col: 'bool' for col in ('IsUpdate', 'IsPrimary', 'IsAlive')
                           if col in result['columns']}

        df = pd.DataFrame(**result).set_index(['Date'] + bmll_index_columns).sort_index()

        df = (
            df[sorted(df)]
            .reset_index()
            .replace({"True": True, "False": False})
            .astype({'Date': 'datetime64[ns]'})
            .astype({index_col: ID_COL_TYPE for index_col in bmll_index_columns})
            .astype(bool_column_map)  # Must be after string to bool conversion.
        )

        return df

    def available_markets(self, start_date=None, end_date=None):
        """
        Get the available markets

        Parameters
        ----------
        start_date: str or datetime.date, optional
            First date to get data for.  iso-formatted date
            Default, previous business day.
        end_date: str or datetime.date, optional
            Last date to get data for. iso-formatted date
            Defaults to same date as start_date.

        Returns
        -------
        :class:`pandas.DataFrame`
            DataFrame of reference data matching the given criteria.

        """
        return self.query(start_date=start_date, end_date=end_date, object_type='Market')

    def _get_page(self, start_date, end_date, object_ids, object_type, token=None, **constraint):
        """Get reference data for a given constraint and date range, and handle the
        paginated response.

        Parameters
        ----------
        start_date: str
            isoformat date
        end_date: str
            isoformat date
        object_ids: list(int)
            Look up reference data for these ids
        object_type: str
            Must be either "Listing", "Instrument", or "Market"
        **constraint: list(str)
            Field name to list of values

        Returns
        -------
        dict:
            Dictionary of {'date': {'id': {'field': 'value'}}}
        """

        params = {
            'objectType': object_type,
            'startDate': start_date,
            'endDate': end_date,
            'token': token
        }

        if object_ids:
            params['objectIds'] = object_ids

        params.update(constraint)

        return self._session.execute('post', 'reference', '/query', json=params)


# we setup a default client and session so that users can still call
# bmll.reference.query() etc.
_DEFAULT_CLIENT = ReferenceDataClient()
query = _DEFAULT_CLIENT.query
available_markets = _DEFAULT_CLIENT.available_markets
