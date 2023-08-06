import boto3
from boto3.dynamodb.conditions import Key, Attr
from uuid import uuid4
from boto3.dynamodb.types import Decimal, Binary
from datetime import datetime
import time
from revcore.ddb import exceptions


class Model:
    abstract = False
    TABLE_NAME = None
    AWS_REGION = 'ap-northeast-1'
    partition_key = None
    partition_type = 'S'
    sort_key = None
    sort_type = 'S'
    s_indexes = {}

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def init_table(cls):
        client = boto3.client('dynamodb', region_name=cls.AWS_REGION)
        try:
            response = client.describe_table(
                TableName=cls.TABLE_NAME
            )
        except:
            key_schema = [{'AttributeName': cls.partition_key, 'KeyType': 'HASH'}]
            attrs = [{'AttributeName': cls.partition_key, 'AttributeType': cls.partition_type}]
            indexes = []

            kwargs = {'TableName': cls.TABLE_NAME, 'KeySchema': key_schema, 'AttributeDefinitions': attrs, 'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }}
            for key, value in cls.s_indexes:
                schemas = [{'AttributeName': value['pkey'], 'KeyType': 'HASH'}]
                attrs.append({'AttributeName': value['pkey'], 'AttributeType': value.get('ptype', 'S')})
                if value.get('skey'):
                    schemas.append({'AttributeName': value['skey'], 'KeyType': 'RANGE'})
                    attrs.append({'AttributeName': value['skey'], 'AttributeType': value.get('stype', 'S')})
                indexes.append({'IndexName': key, 'KeySchemas': shemas})
            if cls.sort_key:
                key_schema.append({'AttributeName': cls.sort_key, 'KeyType': 'RANGE'})
                attrs.append({'AttributeName': cls.sort_key, 'AttributeType': cls.sort_type})

            if indexes:
                kwargs['LocaleSecondaryIndexes'] = indexes
            response = client.create_table(
                **kwargs
            )

    def build_condition(is_key=True, **kwargs):
        method = Key if is_key else Attr
        condition = None
        for k, v in kwargs.items():
            key = k
            try:
                if k[-5:] == '__lte':
                    op = 'lte'
                    key = k[:-5]
                elif k[-5:] == '__gte':
                    op = 'gte'
                    key = k[:-5]
                else:
                    op = 'eq'
            except:
                op = 'eq'

            if not condition:
                condition = getattr(method(key), op)(v)
            else:
                condition = condition & getattr(method(key), op)(v)
        return condition

    @ classmethod
    def _get_client(cls):
        dynamo = boto3.resource('dynamodb', region_name=cls.AWS_REGION)
        return dynamo.Table(cls.TABLE_NAME)

    @ classmethod
    def get(cls, **kwargs):
        client = cls._get_client()
        key = {
            cls.partition_key: kwargs[cls.partition_key],
        }
        if cls.sort_key:
            key[cls.sort_key] = kwargs[cls.sort_key]
        resp = client.get_item(Key=key)
        try:
            return cls._format_input(**resp['Item'])
        except KeyError:
            raise exceptions.InstanceNotFound

    @ classmethod
    def put(cls, **kwargs):
        client = cls._get_client()
        kwargs = cls._format_input(**kwargs)
        if cls.sort_key:
            key = {
                cls.partition_key: kwargs.pop(cls.partition_key),
                cls.sort_key: kwargs.pop(cls.sort_key, uuid4().hex)
            }
        else:
            key = {
                cls.partition_key: kwargs.pop(cls.partition_key, uuid4().hex),
            }
        items = {
            'timestamp': {
                'Value': kwargs.pop('timestamp', int(datetime.now().timestamp())),
                'Action': 'PUT'
            },
            'updated': {
                'Value': int(datetime.now().timestamp()),
                'Action': 'PUT'
            }
        }
        for k, v in kwargs.items():
            items[k] = {
                'Value': v,
                'Action': 'PUT'
            }
        resp = client.update_item(Key=key,
                                  AttributeUpdates=items,
                                  ReturnValues='ALL_NEW')
        resp_item = cls._format_input(**resp['Attributes'])
        return resp_item

    @ classmethod
    def delete(cls, **kwargs):
        client = cls._get_client()
        key = {
            cls.partition_key: kwargs[cls.partition_key],
        }
        if cls.sort_key:
            key[cls.sort_key] = kwargs[cls.sort_key]
        resp = client.delete_item(Key=key)

    @ classmethod
    def query(cls, index_name=None, **kwargs):
        client = cls._get_client()
        condition = cls.build_condition(**kwargs)
        extra = {
            'KeyConditionExpression': condition
        }
        if index_name:
            extra['IndexName'] = index_name
        resp = client.query(**extra)
        return cls._format_input(result=resp['Items'])['result']

    @ classmethod
    def filter_query(cls, key_condition, index_name=None, **kwargs):
        client = cls._get_client()
        condition = cls.build_condition(is_key=False, **kwargs)
        k_condition = cls.build_condition(**key_condition)
        extra = {
            'KeyConditionExpression': k_condition,
            'FilterExpression': condition
        }
        if index_name:
            extra['IndexName'] = index_name
        resp = client.query(**extra)
        return resp['Items']

    @ classmethod
    def batch_write(cls, items: list):
        client = cls._get_client()
        result = []
        with client.batch_writer() as batch:
            for item in items:
                _item = {
                    cls.partition_key: uuid4().hex,
                }
                if cls.sort_key:
                    _item[cls.sort_key] = uuid4().hex
                _item = {
                    **_item,
                    **item
                }
                _item = cls._format_input(**_item)
                batch.put_item(Item=_item)
                result.append(_item)
        return result

    @ staticmethod
    def _format_value(value):
        value_type = type(value)
        if value_type is float:
            return int(value)
        if value_type is Binary:
            return value.value
        elif value_type in [dict, object]:
            return Model._format_input(**value)
        elif value_type is list:
            return list(map(lambda _item: Model._format_value(_item), value))
        elif value_type is Decimal:
            return value.__int__()
        else:
            return value

    @ staticmethod
    def _format_input(**kwargs):
        after_formatting = {**kwargs}
        for k, v in after_formatting.items():
            after_formatting[k] = Model._format_value(v)
        return after_formatting

    @ classmethod
    def scan(cls, **kwargs):
        client = cls._get_client()
        resp = client.scan(**kwargs)
        return cls._format_input(result=resp['Items'])['result']

    @ classmethod
    def clean_up(cls, **kwargs):
        if not DEBUG:
            raise Exception
        client = cls._get_client()
        scan = cls.scan()
        with client.batch_writer() as batch:
            for each in scan:
                key = {
                    cls.partition_key: each[cls.partition_key]
                }
                if cls.sort_key:
                    key[cls.sort_key] = each[cls.sort_key]

                batch.delete_item(
                    Key=key
                )


class BigModel(Model):
    model = None
    partition_key = 'model'
    sort_key = 'id'
    TABLE_NAME = None
    abstract = True

    @ classmethod
    def get(cls, **kwargs):
        kwargs['model'] = cls.model
        return super(BigModel, cls).get(**kwargs)

    @ classmethod
    def delete(cls, **kwargs):
        kwargs['model'] = cls.model
        return super(BigModel, cls).delete(**kwargs)

    @ classmethod
    def put(cls, **kwargs):
        kwargs['model'] = cls.model
        return super(BigModel, cls).put(**kwargs)

    @ classmethod
    def query(cls, index_name=None, **kwargs):
        kwargs['model'] = cls.model
        return super(BigModel, cls).query(**kwargs, index_name=index_name)

    @ classmethod
    def filter_query(cls, key_condition, index_name=None, **kwargs):
        key_condition['model'] = cls.model
        return super(BigModel, cls).filter_query(**kwargs, index_name=index_name, key_condition=key_condition)

    @ classmethod
    def batch_write(cls, items: list):
        items = list(map(lambda _item: {**_item, 'model': cls.model}, items))
        return super(BigModel, cls).batch_write(items)


class BaseInstance:
    def __init__(self, model_class=None, **kwargs):
        self.model_class = model_class
        for k, v in kwargs.items():
            if not k.startswith('__'):
                setattr(self, k, v)

    def save(self):
        attr_dict = self.to_dict()
        return self.model_class.put(**attr_dict)

    def to_dict(self):
        attr_dict = {**self.__dict__}
        attr_dict.pop('model_class', None)
        return attr_dict


class InstanceModel(Model):
    instance_class = BaseInstance
    abstract = True

    @ classmethod
    def _build_instance(cls, **kwargs):
        return cls.instance_class(model_class=cls, **kwargs)

    @ classmethod
    def get(cls, **kwargs):
        result = super(InstanceModel, cls).get(**kwargs)
        return cls._build_instance(**result)

    @ classmethod
    def put(cls, **kwargs):
        result = super(InstanceModel, cls).put(**kwargs)
        return cls._build_instance(**result)

    @ classmethod
    def query(cls, index_name=None, **kwargs):
        result = super(InstanceModel, cls).query(index_name=index_name, **kwargs)
        return list(map(lambda _item: cls._build_instance(**_item), result))

    @ classmethod
    def batch_write(cls, items: list):
        result = super(InstanceModel, cls).batch_write(items)
        return list(map(lambda _item: cls._build_instance(**_item), result))

    @ classmethod
    def scan(cls, **kwargs):
        result = super(InstanceModel, cls).scan()
        return list(map(lambda _item: cls._build_instance(**_item), result))
