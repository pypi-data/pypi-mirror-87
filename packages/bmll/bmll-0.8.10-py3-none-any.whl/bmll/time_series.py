from functools import partial

import pandas as pd

from bmll import reference
from bmll._utils import to_pandas, paginate
from bmll._rest import DEFAULT_SESSION

__all__ = ('query', 'available', 'TimeSeriesClient')


class TimeSeriesClient:
    """
    The TimeSeriesClient provides a convenient interface to interact with the BMLL Time-Series API.

    Parameters
    ----------
    session: :class:`bmll.Session`, optional
        if provided use this session object to communicate with the API, else use the default session.
    reference_client: :class:`bmll.reference.ReferenceDataClient`, optional
        if provided use this client to query the Reference Data API, else use `bmll.reference.query`.

    """
    def __init__(self, session=None, reference_client=None):
        self._session = session if session is not None else DEFAULT_SESSION
        self._reference_client = reference_client if reference_client is not None else reference

    def query(self,
              *,
              start_date,
              end_date,
              metric,
              frequency='D',
              object_ids=None,
              object_type='Listing',
              **constraint):
        """
        Query the Time-Series Service.

        Parameters
        ----------
        **constraint:
            Keyword arguments for constraints to search for reference data.

            For example:

            .. code-block:: python

                MIC='XLON' or MIC=['XLON', 'XPAR']

            Allowed constraints include:
                - MIC
                - Ticker
                - Index
                - FIGI
                - FIGIShareClass
                - ISIN
                - OPOL
                - DisplayName
                - Description.

            .. note:: constraints look for exact matches.

        start_date: as compatible with :func:`pandas.to_datetime`, required
            The start date (inclusive) for the query.

        end_date: as compatible with :func:`pandas.to_datetime`, required
            The end date (inclusive) for the query.

        metric: str or list of str or dict, required
            The metric names as provided by :func:`bmll.time_series.available`

            or

            A mongo query, see the `Mongo Documentation
            <https://docs.mongodb.com/manual/reference/method/db.collection.find/>`_ for more details.

        frequency: str, optional
            A frequency string as specified in :func:`bmll.time_series.available`
            The default is 'D'

        object_ids: list of int, optional
            The set of bmll ids for the query.
            This is required if no `constraints` are specified.

        object_type: str, optional
            One of:
                - Listing (default)
                - Instrument
                - Market

            ..note::only used if a `constraint` is provided.

        Examples
        --------
        >>> query(Ticker='VOD',
        ...       MIC='XLON',
        ...       metric='TradeCount',
        ...       frequency='D',
        ...       start_date='2019-06-24',
        ...       end_date='2019-12-31')

        >>> query(Ticker=['VOD', 'RDSA'],
        ...       MIC='XLON',
        ...       metric={
        ...           'metric': {'$in': ['TradeCount', 'TradeVolume']},
        ...           'tags.Classification':'LitAddressable'
        ...       },
        ...       frequency='D',
        ...       start_date='2019-06-24',
        ...       end_date='2019-12-31')

        Returns
        -------
        :class:`pandas.DataFrame`
            Time-Series DataFrame.

        """
        if isinstance(metric, str):
            metric = [metric]
        elif isinstance(metric, pd.DataFrame):
            metric = _dataframe_to_query(metric)

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        object_column = object_type + 'Id'

        if constraint:
            if object_ids:
                raise ValueError("Cannot provide 'object_ids' and 'constraint'")

            ref_data = self._reference_client.query(object_ids=object_ids,
                                                    object_type=object_type,
                                                    **constraint)
            if object_type == 'Instrument':
                # Only use reference data from the primary exchange for Instrument metrics.
                ref_data = ref_data.query('IsPrimary')

            identifiers = (
                ref_data[[object_column] + list(constraint)]
                .drop_duplicates()  # no dupes
                .dropna(subset=[object_column])  # no Nans in ListingId/InstrumentId
            )
            object_ids = list(identifiers[object_column].unique())

            if not object_ids:
                raise ValueError(f"No Object Ids found for given constraint. {constraint}")

        req = partial(self._get_page, object_ids, metric, frequency, start_date, end_date)

        table = paginate(req)
        df = to_pandas(table)

        if constraint:
            df = pd.merge(identifiers, df, left_on=[object_column], right_on=['ObjectId'])
            del df['ObjectId']

        return df

    def available(self, object_id=None, explode_tags=False):
        """
        Return the metrics available.

        Parameters
        ----------
        object_id: int, optional
            if provided, only return the metrics which exist for this object.

        Returns
        -------
        :class:`pandas.DataFrame`
            The available metrics.
        """
        url = '/available'

        if object_id:
            url += f'/{object_id}'

        table = self._session.execute('get', 'time-series', url)
        df = to_pandas(table)

        if explode_tags:
            df = df.join(df.tags.apply(pd.Series))
            del df['tags']

        return df

    def _get_page(self, object_ids, metrics, freq, start_date, end_date, token=None):
        payload = {
            'objectId': [int(o) for o in object_ids],
            'metric': metrics,
            'frequency': freq,
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
        }

        if token:
            payload['token'] = token

        return self._session.execute('post', 'time-series', '/query', json=payload)


def _dataframe_to_query(df):
    assert 'metric' in df.columns
    assert 'suffix' in df.columns

    _or = df.loc[:, ['metric', 'suffix']].to_dict(orient='records')

    return {
        '$or': _or
    }


# we setup a default client and session so that users can still call
# bmll.time_series.query() etc.
_DEFAULT_CLIENT = TimeSeriesClient()
query = _DEFAULT_CLIENT.query
available = _DEFAULT_CLIENT.available
