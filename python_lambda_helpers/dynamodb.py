import logging

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class TableNameNotDefined(Exception):
    pass


class MissingRequiredParameter(Exception):
    pass


class ClientErrorException(Exception):
    pass


def get_connection():
    return boto3.resource('dynamodb')


def get_table(table_name=None, dynamodb=None):
    if not dynamodb:
        dynamodb = get_connection()

    if table_name is None:
        raise TableNameNotDefined()

    return dynamodb, dynamodb.Table(table_name)


def update(table_name=None, dynamodb=None, **kwargs):
    _, table = get_table(table_name=table_name, dynamodb=dynamodb)

    try:
        primary_key = kwargs['primary']
        primary_value = kwargs['primary_value']
        sort_key = kwargs['sort']
        sort_value = kwargs['sort_value']
        field = kwargs['field']
        value = kwargs['value']
    except KeyError as exp:
        raise MissingRequiredParameter(str(exp))

    response = table.update_item(
        Key={
            primary_key: primary_value,
            sort_key: sort_value,
        },
        UpdateExpression=f'SET #firstField=:c',
        ExpressionAttributeValues={
            ':c': value,
        },
        ExpressionAttributeNames={
            '#firstField': f'{field}',
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def query(value, table_name=None, field=None, dynamodb=None):
    dynamodb, table = get_table(table_name=table_name, dynamodb=dynamodb)

    if field is None:
        field = 'email'

    try:
        response = table.query(
            KeyConditionExpression=Key(field).eq(value)
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise ClientErrorException(str(e.response['Error']['Message']))
    else:
        return response['Items'], dynamodb


def insert(table_name=None, dynamodb=None, **kwargs):
    dynamodb, table = get_table(table_name=table_name, dynamodb=dynamodb)

    try:
        primary_key = kwargs['primary']
        primary_value = kwargs['primary_value']
        sort_key = kwargs['sort']
        sort_value = kwargs['sort_value']
        field = kwargs['field']
        value = kwargs['value']
    except KeyError as exp:
        raise MissingRequiredParameter(str(exp))

    response = table.put_item(
        Item={
            primary_key: primary_value,
            sort_key: sort_value,
            field: value,
        }
    )
    return response
