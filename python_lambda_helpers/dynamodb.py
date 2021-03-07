import boto3


class TableNameNotDefined(Exception):
    pass


class MissingRequiredParameter(Exception):
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
