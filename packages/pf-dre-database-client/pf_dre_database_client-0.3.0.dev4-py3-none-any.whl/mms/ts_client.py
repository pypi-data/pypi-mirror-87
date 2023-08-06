#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The following client is used to read data to and write data from the postgres
Meter Management System which includes TimescaleDB for meter metric data.
"""

# Built-in Modules
import logging
import csv
import json
from abc import ABC
from datetime import datetime, timedelta
from io import StringIO

# Third Party Modules
import pandas as pd
import psycopg2
from psycopg2 import sql, extras

# Project Specific Modules
from mms import helpers as h

# Logging
logger = logging.getLogger('timescale')


class TimescaleClient:
    """
    Standardized Format
        MultiIndex: (device_id <int64>,
                     device_metric_type_id <str>,
                     measurement_date/received_date <datetime64[ns])
        Columns: value <float64>
    """
    def __init__(self, tbl_name, pk, standardized=True, db_type='reference',
                 **kwargs):
        self.tbl_name = tbl_name
        self.standardized = standardized
        if kwargs.get('dbname') is None:
            kwargs = h.get_db_client_kwargs(db_type)
        self.conn = psycopg2.connect(**kwargs)
        if kwargs.get('port') == "5000":
            read_only = False
        else:
            read_only = True
        self.conn.set_session(isolation_level="read uncommitted",
                              readonly=read_only,
                              autocommit=False)
        self.pk = pk
        self.allowed_aggs = ['first', 'last', 'avg']

    @staticmethod
    def standardize_df(db, **kwargs):
        raise NotImplementedError

    def rollback(self):
        self.conn.rollback()
        self.conn.close()

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def allowed_agg(self, agg):
        if agg not in self.allowed_aggs:
            raise ValueError("agg must be one of: {0}"
                             .format(self.allowed_aggs))
        return

    def query_to_df(self, query, qry_params, **standardize_args):
        try:
            df = pd.read_sql(query,
                             con=self.conn,
                             params=qry_params)
            df.rename(columns = {'time': 'measurement_date'}, inplace = True)

            if self.standardized:
                df = self.standardize_df(df, **standardize_args)
            return df

        except psycopg2.Error as error:
            print("Error: %s".format(error))
            self.rollback()
            return None

    def df_to_schema(self, df):
        return df

    def get_all_metrics(self, *args):
        raise NotImplementedError

    def get_aggregated_metrics(self, *args):
        raise NotImplementedError

    def df_from_data_model(self, data_model, res, ts_start, ts_end):
        """
        Using the standardized data_model object format:

        "features": <-- Forms the columns of the Dataframe
            "feature_name>: <-- DataFrame Column Name
                <timeseries_name>: <Arithmetic operation>
                ...Dict of Timeseries (From MMS Queries)...
                <timeseries_name>: <Arithmetic operation>
            ...Dict of Features...
            "uncontrollable_demand":
                net_demand: '+'
                pv_generation: '-'
                controllable_generation: '-'
        "timeseries":
            <timeseries_name>:
                "device_ids":
                    - <device_id> INT
                "metrics":
                    - <device_metric_type_id>
                "agg": <aggregate method>
                "fill": <fill method>
            ...Dict of Timeseries, definitions for MMS Queries...
            "net_demand":
                "device_ids":
                    - 281
                    - 282
                    - 283
                "metrics":
                    - 'P'
                "agg": 'avg'
                "fill": 'interpolate'
        :param data_model:
        :param res:
        :param ts_end:
        :param ts_start:
        :return: A compiled dataframe in accordance with the Data Model
        """
        stats = {'timeseries': {}, 'features': {}}
        features_df = None
        timeseries_dfs = {}
        timeseries = data_model.get('timeseries')
        features = data_model.get('features')
        for name, ts in timeseries.items():
            logger.debug('Querying data for timeseries {0}'.format(name))
            timeseries_dfs[name] = self.get_aggregated_metrics(
                res,
                ts.get('device_ids'),
                ts.get('metrics'),
                ts_start, ts_end,
                ts.get('agg'), ts.get('fill'))
            stats['timeseries'].update({
                name: dict(zip(
                    timeseries_dfs[name].groupby(
                        ['device_id']).count().index.values,
                    ["{} rows".format(count)
                     for count in timeseries_dfs[name].groupby(
                        ['device_id']).count().values[:, 0]]
                ))
            })

        for feature, components in features.items():
            # Dictionary of features for model
            feature_df = None
            logger.debug('Preparing feature {0}'.format(feature))
            for component, operation in components.items():
                # Dictionary of feature components.
                logger.debug('Using component {0}'.format(component))
                # Does not need to be only a sum operation.
                component_df = timeseries_dfs[component] \
                    .groupby(['measurement_date']) \
                    .sum(min_count=1)
                if feature_df is None:
                    feature_df = component_df.copy()
                else:
                    if operation == '+':
                        feature_df = feature_df.add(component_df)
                    if operation == '-':
                        feature_df = feature_df.subtract(component_df)
            feature_df.rename(columns={'value': feature}, inplace=True)
            stats['features'].update({
                feature: "{} rows".format(
                    feature_df.count().values[0])
            })
            if features_df is None:
                features_df = feature_df.copy()
            else:
                features_df = features_df.join(feature_df)
        return features_df, stats

    def execute_values(self, df, method='fail', parse_df=False):
        """
        Using psycopg2.extras.execute_values() to insert the Data Frame
        :param df: Data frame matching the schema of 'table' in the MMS.
        :param method: Action to perform when a duplicate row is
        :param parse_df: Boolean indicating whether the dataframe should first
        passed through the df_to_schema method to form the correct format.
        encountered in the DB.
            - fail: Do not insert any rows in the transaction
            - update: Update the duplicate rows
            - ignore: Ignore the duplicate rows
        """
        if parse_df:
            df = self.df_to_schema(df)
        # Comma-separated Data Frame columns, excluding index
        upsert_col_names = list(set(df.columns) - set(self.pk))
        upsert_setters = ', '.join(["{} = EXCLUDED.{}".format(a, a)
                                    for a in upsert_col_names])
        # Comma-separated Data Frame columns, including index
        cols = ','.join(list(df.columns))
        # Create a list of tuples from the Data Frame values
        tuples = [tuple(x) for x in df.to_numpy()]

        if method == 'fail':
            query = "INSERT INTO %s(%s) " \
                    "VALUES %%s " \
                    "RETURNING %s " % (self.tbl_name, cols, ','.join(self.pk))
        elif method == 'ignore':
            query = "INSERT INTO %s(%s) " \
                    "VALUES %%s " \
                    "ON CONFLICT (%s)" \
                    "DO NOTHING " \
                    "RETURNING %s " % (self.tbl_name, cols,
                                       ','.join(self.pk), ','.join(self.pk))
        elif method == 'update':
            query = "INSERT INTO %s(%s) " \
                    "VALUES %%s " \
                    "ON CONFLICT (%s)" \
                    "DO UPDATE SET %s " \
                    "RETURNING %s" % (self.tbl_name, cols,
                                      ','.join(self.pk), upsert_setters,
                                      ','.join(self.pk))
        else:
            raise ValueError("Param method must be one of 'fail', "
                             "'update', 'ignore'.")

        # SQL query to execute
        try:
            with self.conn.cursor() as cursor:
                extras.execute_values(cursor, query, tuples, page_size=1000)
                return cursor.fetchall()
        except psycopg2.IntegrityError as e:
            if e.pgcode == '23505':
                raise psycopg2.IntegrityError(
                    "Cannot overwrite existing data in the MMS using 'fail' "
                    "method")
            else:
                raise e

        except psycopg2.DatabaseError as error:
            print("Unexpected Error: %s" % error)
            self.rollback()
            raise error

    def copy_df_from_stringio(self, df, parse_df=False):
        """
        Save the Data Frame in memory and use copy_from() to copy it to
        the table
        :param df: Data frame matching the schema of 'table' in the MMS.
        The index of the data frame will always be measurement_date
        :param parse_df: Boolean indicating whether the dataframe should first
        passed through the df_to_schema method to form the correct format.
        :return: True if successful
        """
        if parse_df:
            df = self.df_to_schema(df)
        s_buf = StringIO()
        cols = list(df.columns)
        # df_idx = df.set_index('measurement_date', inplace=False)
        df.to_csv(s_buf, sep='\t', quoting=csv.QUOTE_NONE,
                  header=False, index = False)
        s_buf.seek(0)
        try:
            with self.conn.cursor() as cursor:
                cursor.copy_from(s_buf, self.tbl_name, columns=cols,
                                 sep='\t', size=8192)
                return cursor.rowcount
        except psycopg2.IntegrityError as e:
            if e.pgcode == '23505':
                print("Will not copy over existing data in the MMS, ignoring")
            return 0
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.rollback()
            raise error


class TimescaleClientNarrow(TimescaleClient):
    def __init__(self, tbl_name, standardized=True, **kwargs):
        pk = ['measurement_date', 'device_id', 'device_metric_type_id']
        TimescaleClient.__init__(self, tbl_name, pk, standardized, **kwargs)

    @staticmethod
    def get_agg_str(agg):
        if agg == 'avg':
            return "{0}(value)".format(agg)
        else:
            return "{0}(value, measurement_date)".format(agg)

    @staticmethod
    def standardize_df(df, **kwargs):
        """
        Convert narrow Data Frame format into the standard pandas DF
        result format by creating a multiIndex on
        device_id, device_metric_type_id, measurement_date.
        :param df: Raw query Data Frame with generic pandas index and the
        following columns:
        'device_id' (int), 'measurement_date' (string), '
        :return: Data frame in the format:
            - Index = ('measurement_date', 'device_id', 'device_metric_type_id')
            - Columns = ['value']
        """
        h.apply_standard_index(df, dropna = kwargs.get('dropna', False))
        return df

    def df_to_schema(self, df):
        """
        :param df: Dataframe to be updated
        This dataframe must have all the key metrics required for the schema in
        order to generate a valid dataframe.
        """
        if type(df.index) != pd.RangeIndex:
            df.reset_index(inplace = True)
        return df

    def get_all_metrics(self, device_ids, metrics, ts_start, ts_end):
        query = sql.SQL(
            "SELECT * "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND device_metric_type_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s ") \
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
        df = self.query_to_df(query,
                              device_ids +
                              metrics +
                              [h.validate_timestamp(ts_start),
                               h.validate_timestamp(ts_end)])

        return df

    def get_aggregated_metrics(self, res, device_ids, metrics,
                               ts_start, ts_end, agg='avg', fill=None):
        self.allowed_agg(agg)

        if fill == 'locf':
            # Linear interpolation between points
            value_str = "locf({0}) AS value".format(self.get_agg_str(agg))
        elif fill == 'interpolate':
            # Last Observation Carried Forward
            value_str = "interpolate({0}) AS value"\
                .format(self.get_agg_str(agg))
        elif fill == 'zero':
            # Last Observation Carried Forward
            value_str = "COALESCE({0}, 0) AS value" \
                .format(self.get_agg_str(agg))
        else:
            value_str = "{0} AS value".format(self.get_agg_str(agg))
        query = sql.SQL(
            "SELECT "
            "time_bucket_gapfill({}, measurement_date) as time, "
            "device_id, device_metric_type_id, {} "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND device_metric_type_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s "
            "GROUP BY device_id, device_metric_type_id, time") \
            .format(sql.Literal(res),
                    sql.SQL(value_str),
                    sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
        df = self.query_to_df(query,
                              device_ids + metrics +
                              [h.validate_timestamp(ts_start),
                               h.validate_timestamp(ts_end)])
        return df

    def get_num_readings(self, device_ids, ts_start, ts_end, simulation=None):
        """
        :param device_ids: A list of device_ids to be queried
        :param simulation: Set a simulation name to lookup in the DB
        :param ts_start: Start time for the measurement_date index to be
        scanned (inclusive) [Datetime]
        :param ts_end: End time for the measurement_date index to be
        scanned (exclusive) [Datetime]
        :return: Data Frame in raw or standardized format:
        """
        cond = ""
        cond_vals = device_ids + [h.validate_timestamp(ts_start),
                                  h.validate_timestamp(ts_end)]
        if simulation is not None:
            cond = "AND simulation = %s "
            cond_vals.append(simulation)
        query = sql.SQL(
            "SELECT DISTINCT(device_id) as device_id, "
            "COUNT(device_id) as count "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s "
            "{}"
            "GROUP BY measurement_date, device_id") \
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(cond))
        old_state = self.standardized
        self.standardized = False
        df = self.query_to_df(query, cond_vals, dropna = True)
        self.standardized = old_state
        df.set_index('device_id', inplace = True)
        return df

    def get_latest_metrics(self, device_ids, metrics,
                           reference_time=None, window=None):
        """
        :param device_ids: A list of device_ids to be queried
        :param metrics: A list of metrics (Strings) to be queried for
        each device_id
        :param reference_time: Set a reference time for when the latest values
        are to be queried for. If this is not set the latest values for now will
        be queried. [Datetime]
        :param window: [Optional] The number of minutes prior to now that the
        latest values
        should be queried from.
        :return: Data Frame in raw or standardized format:
        """

        query = sql.SQL(
            "SELECT device_id, "
            "device_metric_type_id, "
            "last(measurement_date, measurement_date) AS measurement_date, "
            "last(value, measurement_date) AS value "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND device_metric_type_id IN ({}) "
            "AND measurement_date >= %s "
            "AND measurement_date < %s "
            "GROUP BY device_id, device_metric_type_id") \
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
        df = self.query_to_df(query,
                              device_ids + metrics +
                              h.get_ts_conditional_vals(reference_time, window),
                              dropna = True)
        return df


class TimescaleClientJSON(TimescaleClient):
    """
    Inheriting from the TimescaleClient base class, this class is used for
    accessing, and modifying instantaneous device metric data in the MMS.
    """
    def __init__(self, tbl_name, standardized=True, **kwargs):
        pk = ['measurement_date', 'device_id']
        TimescaleClient.__init__(self, tbl_name, pk, standardized, **kwargs)

    @staticmethod
    def get_agg_str(agg, m):
        if agg == 'avg':
            return "{0}((metrics->>'{1}')::numeric)".format(agg, m)
        else:
            return "{0}((metrics->>'{1}')::numeric, measurement_date)"\
                .format(agg, m)

    def df_to_schema(self, df):
        """
        :param df: Dataframe to be updated
        This dataframe must have all the key metrics required for the schema in
        order to generate a valid dataframe.
        """
        if type(df.index) != pd.RangeIndex:
            df.reset_index(inplace = True)
        if {'value', 'device_metric_type_id'}.issubset(df.columns.tolist()):
            if 'simulation' in df.columns.tolist():
                idx = ['simulation'] + self.pk
            else:
                idx = self.pk
            df = df.pivot(index=idx,
                          columns='device_metric_type_id',
                          values='value').rename_axis(None, axis=1)
            columns = df.columns.tolist()
            df['metrics'] = [
                {k: v for k, v in m.items()
                 if pd.notnull(v)}
                for m in df[columns].to_dict(orient='records')
            ]
            df['metrics'] = df['metrics'].apply(json.dumps)
            df = df.drop(columns=columns)
            df.reset_index(inplace = True)
            return df
        else:
            raise ValueError("Unable to parse dataframe")

    def standardize_df(self, df, **kwargs):
        """
        Convert JSON blob 'metrics' from query into the standard
        pandas DF
        result format.
        :param df:
        :key metrics: List fo metrics to be returned in the
        function
        :return: Data frame in the format:
            - Index = ('measurement_date', 'device_id', 'device_metric_type_id')
            - Columns = ['value']
        """

        # If the query returned raw rows (i.e. the metrics column), the JSON
        # data must be processed.
        if 'metrics' in list(df.columns):
            # Convert the JSON column to a pandas Series,
            # this creates columns for each key in the JSON
            df = pd.concat([df.drop(['metrics'], axis=1),
                            df['metrics'].apply(pd.Series)], axis=1)
            # Filter the columns so only the requested metrics are stored
            df = df[[c for c in df.columns
                     if c in self.pk + kwargs.get('metrics')]]
        # Unpivot the DataFrame so the metric columns are compiled into
        # a single key value column pairing (number of DF rows increase)
        df = df.melt(
            id_vars=self.pk,
            var_name='device_metric_type_id',
            value_name='value'
        )
        h.apply_standard_index(df, dropna = kwargs.get('dropna', False))
        return df

    def get_all_metrics(self, device_ids, metrics, ts_start, ts_end):
        query = sql.SQL(
            "SELECT * "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s") \
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)))
        df = self.query_to_df(query,
                              device_ids +
                              [h.validate_timestamp(ts_start),
                               h.validate_timestamp(ts_end)],
                              metrics = metrics)
        return df

    def get_aggregated_metrics(self, res, device_ids, metrics,
                               ts_start, ts_end, agg='avg', fill=None):
        self.allowed_agg(agg)

        if fill == 'locf':
            # Last Observation Carried Forward
            values = ", ".join(["locf({0}) AS \"{1}\""
                               .format(self.get_agg_str(agg, m), m)
                                for m in metrics])
        elif fill == 'interpolate':
            # Linear interpolation between points
            values = ", ".join(["interpolate({0}) AS \"{1}\""
                               .format(self.get_agg_str(agg, m), m)
                                for m in metrics])
        elif fill == 'zero':
            values = ", ".join(["COALESCE({0}, 0) AS \"{1}\""
                               .format(self.get_agg_str(agg, m), m)
                                for m in metrics])
        else:
            values = ", ".join(["{0} AS \"{1}\""
                               .format(self.get_agg_str(agg, m), m)
                                for m in metrics])

        query = sql.SQL(
            "SELECT "
            "time_bucket_gapfill({}, measurement_date) AS time, "
            "device_id, {} "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s "
            "GROUP BY device_id, time")\
            .format(sql.Literal(res),
                    sql.SQL(values),
                    sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)))
        df = self.query_to_df(query,
                              device_ids +
                              [h.validate_timestamp(ts_start),
                               h.validate_timestamp(ts_end)],
                              metrics = metrics)
        return df

    def get_num_readings(self, device_ids, ts_start, ts_end):
        """
        :param device_ids: A list of device_ids to be queried
        :param ts_start: Start time for the measurement_date index to be
        scanned (inclusive) [Datetime]
        :param ts_end: End time for the measurement_date index to be
        scanned (exclusive) [Datetime]
        :return: Data Frame in raw or standardized format:
        """
        cond = ''
        cond_vals = device_ids + [h.validate_timestamp(ts_start),
                                  h.validate_timestamp(ts_end)]
        query = sql.SQL(
            "SELECT device_id, "
            "COUNT(*) as count "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s "
            "{}"
            "GROUP BY device_id") \
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(cond))
        old_state = self.standardized
        self.standardized = False
        df = self.query_to_df(query,
                              cond_vals,
                              dropna = True)
        self.standardized = old_state
        df.set_index('device_id', inplace = True)
        return df

    def get_latest_metrics(self, device_ids, metrics,
                           reference_time=None, window=None):
        """
        :param device_ids: A list of device_ids to be queried
        :param metrics: A list of metrics (Strings) to be queried for
        each device_id
        :param reference_time: Set a reference time for when the latest values
        are to be queried for. If this is not set the latest values for now will
        be queried. [Datetime]
        :param window: [Optional] The number of minutes prior to now that the
        latest values
        should be queried from.
        :return: Data Frame in raw or standardized format:
        """

        query = sql.SQL(
            "SELECT device_id, "
            "last(measurement_date, measurement_date) AS measurement_date, "
            "last(metrics, measurement_date) AS metrics "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND measurement_date >= %s "
            "AND measurement_date < %s "
            "GROUP BY device_id") \
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)))
        df = self.query_to_df(query,
                              device_ids +
                              h.get_ts_conditional_vals(reference_time, window),
                              metrics = metrics,
                              dropna = True)
        return df


class ForecastJSONClient(TimescaleClient, ABC):
    """
    Inheriting from the TimescaleClient base class, this class is used for
    accessing, and modifying forecast metrics in the MMS.
    """

    def __init__(self, tbl_name, **kwargs):
        pk = ['received_date', 'device_id']
        TimescaleClient.__init__(self, tbl_name, pk,
                                 standardized=True, **kwargs)

    @staticmethod
    def standardize_df(df, **kwargs):
        """
        Convert Forecast Data Frame format into the standard pandas DF
        result format by creating a multiIndex on
        received_date, device_id, device_metric_type_id, measurement_date.
        :param **kwargs: Not Used
        :param df: Raw query Data Frame with generic pandas index and the
        following columns:
        'received_date' (int), 'device_id' (int), 'measurement_date' (string), '
        :return: Data frame in the format:
            - Index = ('received_date', 'device_id', 'device_metric_type_id', 'measurement_date')
            - Columns = ['value']
        """
        h.apply_forecast_index(df, dropna = kwargs.get('dropna', False))
        return df

    def get_latest_forecasts(self, device_ids, metrics,
                             reference_time=None, window=None):
        """
        :param device_ids: A list of device_ids to be queried
        :param metrics: A list of metrics (Strings) to be queried for
        each device_id
        :param reference_time: Set a reference time for when the
        latest values
        are to be queried for. If this is not set the latest values
        for now will
        be queried. [Datetime]
        :param window: [Optional] The number of minutes prior to now
        that the
        latest values
        should be queried from.
        :return: Data Frame in raw or standardized format:
        """
        query = sql.SQL(
            "WITH latest_forecast AS ("
            "SELECT "
            "device_id, "
            "last(received_date, received_date) AS r, "
            "last(metrics, received_date) AS metrics "
            "FROM {} "
            "WHERE received_date >= %s AND received_date < %s "
            "AND device_id IN ({}) "
            "GROUP BY device_id) "
            "SELECT latest_forecast.r AS received_date, "
            "latest_forecast.device_id AS device_id, "
            "j.key::timestamptz AS measurement_date, "
            "device_metrics.device_metrics AS device_metric_type_id, "
            "AVG(j.value::numeric) AS value "
            "FROM latest_forecast, "
            "jsonb_object_keys(latest_forecast.metrics) device_metrics, "
            "jsonb_each(latest_forecast.metrics->>device_metrics) j "
            "WHERE device_metrics.device_metrics IN ({}) "
            "GROUP BY 1, 2, 3, 4"
            "ORDER BY 1") \
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
        df = self.query_to_df(query,
                              h.get_ts_conditional_vals(
                                  reference_time, window) +
                              device_ids +
                              metrics,
                              dropna = True)
        return df

    def get_missing_forecasts(self, device_ids, expected_resolution,
                              ts_start, ts_end):
        query = sql.SQL(
            "WITH counts AS ("
            "SELECT time_bucket_gapfill(%s, received_date) AS time, "
            "device_id, COUNT(metrics) "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND received_date >= %s AND received_date < %s "
            "GROUP BY time, device_id) "
            "SELECT time AS received_date, device_id "
            "FROM counts "
            "WHERE count IS NULL")\
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)))
        cond_vals = [expected_resolution] + device_ids + \
                    [h.validate_timestamp(ts_start), h.validate_timestamp(ts_end)]
        old_state = self.standardized
        self.standardized = False
        df = self.query_to_df(query,
                              cond_vals)
        self.standardized = old_state
        df.set_index(['device_id', 'received_date'], inplace = True)
        df.index = df.index.set_levels(
            [df.index.levels[0].astype('int64'),
             pd.to_datetime(df.index.levels[1], utc = True)])
        return df

    def get_all_forecasts(self, device_ids, metrics, ts_start, ts_end):
        query = sql.SQL(
            "WITH forecasts AS ("
            "SELECT received_date, metrics "
            "FROM {} "
            "WHERE received_date >= %s AND received_date < %s "
            "AND device_id IN ({}) "
            "GROUP BY device_id, received_date) "
            "SELECT forecasts.received_date AS received_date, "
            "j.key::timestamptz AS measurement_date, "
            "device_metrics.device_metrics AS device_metric_type_id, "
            "AVG(j.value::numeric) AS value, "
            "FROM latest_forecast, "
            "jsonb_object_keys(latest_forecast.metrics) device_metrics, "
            "jsonb_each(latest_forecast.metrics->>device_metrics) j "
            "WHERE device_metrics.device_metrics IN ({}) "
            "GROUP BY 1, 2, 3"
            "ORDER BY 1") \
            .format(sql.Identifier(self.tbl_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
        df = self.query_to_df(query,
                              device_ids + metrics +
                              [h.validate_timestamp(ts_start),
                               h.validate_timestamp(ts_end)],
                              metrics = metrics,
                              dropna = True)
        return df


class SimulationJSONClient(TimescaleClient, ABC):
    """
        Inheriting from the ForecastJSONClient class, this class is used for
        accessing, and modifying simulation results in the MMS.
        """

    def __init__(self, tbl_name, **kwargs):
        pk = ['simulation_name', 'received_date', 'device_id']
        TimescaleClient.__init__(self, tbl_name, pk=pk,
                                 standardized=True, **kwargs)

    @staticmethod
    def standardize_df(df, **kwargs):
        """
        Convert narrow Data Frame format into the standard pandas DF
        result format by creating a multiIndex on
        device_id, device_metric_type_id, measurement_date.
        :param **kwargs: Not Used
        :param df: Raw query Data Frame with generic pandas index and the
        following columns:
        'device_id' (int), 'measurement_date' (string), '
        :return: Data frame in the format:
            - Index = ('measurement_date', 'device_id', 'device_metric_type_id')
            - Columns = ['value']
        """
        h.apply_simulation_index(df, dropna = kwargs.get('dropna', False))
        return df

    def simulation_exists(self, sim):
        """
        :param sim: The name of the simulation
        :return:
        """
        query = sql.SQL(
            "SELECT COUNT(*) as count "
            "FROM {} " 
            "WHERE simulation_name = %s "
            "LIMIT 1").format(sql.Identifier(self.tbl_name))

        with self.conn.cursor() as cur:
            cur.execute(query, (sim,))
            if cur.fetchone:
                return True
            else:
                return False
