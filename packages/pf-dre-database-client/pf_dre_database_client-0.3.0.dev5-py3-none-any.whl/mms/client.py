#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The following client is used to read data to and write data from the postgres
Meter Management System which includes TimescaleDB for meter metric data.
"""

# Built-in Modules

# Third Party Modules
import pandas as pd
import psycopg2
from psycopg2 import sql
from mms.helpers import get_db_client_kwargs


class MMSClient:
    def __init__(self, **kwargs):
        if kwargs.get('dbname') is None:
            self.kwargs = get_db_client_kwargs('reference')
        else:
            self.kwargs = kwargs

    def get_device_codes_for_service(self, service):
        """
        :param service: A device_service from the MMS (string).
        :return: A list of (device code) of type 'service'
        """
        query = sql.SQL(
            " SELECT code FROM devices "
            "JOIN device_models dm on devices.device_model_id = dm.id "
            "JOIN device_services ds on dm.device_service_id = ds.id "
            "WHERE device_service_id = %s") \
            .format(sql.SQL(', ').join(sql.Placeholder() * len(service)))
        with psycopg2.connect(**self.kwargs) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (service,))
                if cur.fetchone:
                    return [r[0] for r in cur.fetchall()]
                else:
                    # No codes matching device service
                    raise LookupError("No devices found with service {0}"
                                      .format(service))

    def get_device_ids_for_codes(self, codes):
        """
        :param codes: A list of device codes (strings) to return the
        device id's for.
        :return: A 1 to 1 dictionary with key (device code)
        and value (device id) (All strings)
        """
        query = sql.SQL("SELECT code, id FROM devices WHERE code IN ({})")\
            .format(sql.SQL(', ').join(sql.Placeholder() * len(codes)))
        with psycopg2.connect(**self.kwargs) as conn:
            df = pd.read_sql(query,
                             con=conn,
                             index_col='code',
                             params=codes)
        df['id'] = df['id'].apply(str)
        return dict(zip(list(df.index.values), list(df['id'].values)))

    def device_inverted(self, device_id):
        """
            :param device_id: A device codes (string) to return the
            device id for.
            :return: A single integer (device id)
            """
        if device_id is None:
            return 0

        query = "SELECT is_inverted " \
                "FROM meters " \
                "WHERE device_id = %s"
        with psycopg2.connect(**self.kwargs) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (device_id,))
                if cur.fetchone:
                    return int(cur.fetchone()[0])
                else:
                    # No device record returned
                    raise LookupError("No meter found for device {0}"
                                      .format(device_id))
