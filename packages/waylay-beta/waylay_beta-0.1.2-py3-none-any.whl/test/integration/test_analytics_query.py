"""integration tests for waylay.service.analytics module"""
import csv
import pytest
from waylay import (
    WaylayClient
)


def test_analytics_query_json(waylay_test_client: WaylayClient):
    "execute query with json response"
    data_resp = waylay_test_client.analytics.query.data('151CF-temperature', raw=True).body
    assert data_resp is not None
    assert 'data' in data_resp
    assert len(data_resp['data']) == 1
    assert 'columns' in data_resp['data'][0]


def test_analytics_query_df(waylay_test_client: WaylayClient):
    "execute query with dataframe response"
    data_df = waylay_test_client.analytics.query.data('151CF-temperature')
    assert data_df is not None
    assert data_df.columns.names == ['resource', 'metric', 'aggregation']
    assert data_df.size > 0


def test_analytics_query_df_no_data(waylay_test_client: WaylayClient):
    data_df = waylay_test_client.analytics.query.data('151CF-temperature', params={
        'from': '2010-10-10',
        'window': 'P1D',
    })
    assert data_df is not None


def test_analytics_execute_query_df_no_aggr_no_data(waylay_test_client: WaylayClient):
    data_df = waylay_test_client.analytics.query.execute(body={
        "resource": "doesnotexist",
        "from": "2010-10-10",
        "until": "2010-10-11",
        "data": [
            {"metric": "colourfullness"},
            {"metric": "playfullness"}
        ]
    })
    assert data_df is not None
    assert data_df.size == 0


def test_analytics_query_csv(waylay_test_client: WaylayClient):
    "execute query with json response"
    query = waylay_test_client.analytics.query.get('151CF-temperature', raw=True).body['query']
    data_resp = waylay_test_client.analytics.query.data(
        '151CF-temperature', raw=True, params={'render.mode': 'RENDER_MODE_CSV'}).body
    assert isinstance(data_resp, str)
    reader = csv.reader(data_resp.splitlines(), delimiter=',')
    header = next(reader)
    assert isinstance(header, list)
    potential_column_names = ['timestamp'] + [
        series.get(
            'name',
            series.get(
                'resource', query.get('resource')
            ) + '/' + series.get(
                'metric',  query.get('metric')
            )
        ) for series in query['data']
    ]
    for col in header:
        assert col in potential_column_names
