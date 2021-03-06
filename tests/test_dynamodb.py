from contextlib import suppress
from unittest.mock import patch

import boto3

from python_lambda_helpers import dynamodb as ddb_helpers


def test_get_connection():
    conn = ddb_helpers.get_connection()
    assert conn.__class__.__name__ == 'dynamodb.ServiceResource'


def test_no_table_exception():
    with suppress(ddb_helpers.TableNameNotDefined):
        conn, _ = ddb_helpers.get_table()


@patch('python_lambda_helpers.dynamodb.get_table')
def test_get_table_called(get_table):
    table_name = 'TableName'
    ddb_helpers.get_table(table_name)

    get_table.assert_called_once()
    get_table.assert_called_with(table_name)


def test_get_table_response():
    table_name = 'TableName'
    conn, table = ddb_helpers.get_table(table_name)
    assert conn.__class__.__name__ == 'dynamodb.ServiceResource'

    assert table.__class__.__name__ == 'dynamodb.Table'


def test_update_required_params():
    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.update('TestTable')

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.update('TestTable', primary='email')

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.update(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
        )
    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.update(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
            sort='verified',
        )

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.update(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
            sort='verified',
            sort_value=True,
        )

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.update(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
            sort='verified',
            sort_value=True,
            field='my_custom_field'
        )

    client = boto3.client('dynamodb')
    with suppress(client.exceptions.ResourceNotFoundException):
        ddb_helpers.update(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
            sort='verified',
            sort_value=True,
            field='my_custom_field',
            value='my_custom_value'
        )


@patch('botocore.client.BaseClient._make_api_call')
def test_update_response(make_api_call):
    make_api_call.return_value = True
    response = ddb_helpers.update(
        table_name='TestTable',
        primary='email',
        primary_value='faker@example.com',
        sort='verified',
        sort_value=True,
        field='my_custom_field',
        value='my_custom_value'
    )

    assert response is True


def test_query_required_params():
    sql_stmt = 'SELECT * FROM table'

    with suppress(ddb_helpers.TableNameNotDefined):
        ddb_helpers.query(sql_stmt)

    with suppress(ddb_helpers.ClientErrorException):
        ddb_helpers.query(
            value=sql_stmt,
            table_name='TestTable',
        )


@patch('botocore.client.BaseClient._make_api_call')
def test_query_response(make_api_call):
    make_api_call.return_value = {
        'Items': []
    }

    sql_stmt = 'SELECT * FROM table'

    results, _ = ddb_helpers.query(
        value=sql_stmt,
        table_name='TestTable',
    )

    assert results == []


def test_insert_required_params():
    with suppress(ddb_helpers.TableNameNotDefined):
        ddb_helpers.insert()

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.insert(table_name='TestTable')

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.insert(
            table_name='TestTable',
            primary='email',
        )

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.insert(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
        )

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.insert(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
            sort='verified',
        )

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.insert(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
            sort='verified',
            sort_value=False,
        )

    with suppress(ddb_helpers.MissingRequiredParameter):
        ddb_helpers.insert(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
            sort='verified',
            sort_value=False,
            field='custom_field'
        )

    client = boto3.client('dynamodb')
    with suppress(client.exceptions.ResourceNotFoundException):
        ddb_helpers.insert(
            table_name='TestTable',
            primary='email',
            primary_value='faker@example.com',
            sort='verified',
            sort_value=False,
            field='custom_field',
            value='custom_value'
        )


@patch('botocore.client.BaseClient._make_api_call')
def test_insert_response(make_api_call):
    make_api_call.return_value = True

    response = ddb_helpers.insert(
        table_name='TestTable',
        primary='email',
        primary_value='faker@example.com',
        sort='verified',
        sort_value=False,
        field='custom_field',
        value='custom_value'
    )

    assert response is True
