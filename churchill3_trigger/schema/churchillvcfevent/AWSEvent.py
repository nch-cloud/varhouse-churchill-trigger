# coding: utf-8
import pprint
import re  # noqa: F401

import six
import datetime
from dateutil.parser import parse as parse_datetime
from churchill3_trigger.schema.churchillvcfevent.ChurchillVCFEvent import ChurchillVCFEvent  # noqa: F401,E501


class AWSEvent(object):

    def __init__(self, detail:ChurchillVCFEvent=None, account:str=None, detail_type:str=None, event_id:str=None, region:str=None,
                 resources:list[str]=None, source:str=None, time:datetime.datetime=None, version:str=None):  # noqa: E501
        self.detail = detail
        self.account = account
        self.detail_type = detail_type
        self.id = event_id
        self.region = region
        self.resources = resources
        self.source = source
        self.time = time
        self.version = version

    @property
    def detail(self):

        return self._detail

    @detail.setter
    def detail(self, detail):

        self._detail = detail

    @property
    def account(self):

        return self._account

    @account.setter
    def account(self, account):

        self._account = account

    @property
    def detail_type(self):

        return self._detail_type

    @detail_type.setter
    def detail_type(self, detail_type):

        self._detail_type = detail_type

    @property
    def id(self):

        return self._id

    @id.setter
    def id(self, event_id):

        self._id = event_id

    @property
    def region(self):

        return self._region

    @region.setter
    def region(self, region):

        self._region = region

    @property
    def resources(self):

        return self._resources

    @resources.setter
    def resources(self, resources):

        self._resources = resources

    @property
    def source(self):

        return self._source

    @source.setter
    def source(self, source):

        self._source = source

    @property
    def time(self):

        return self._time

    @time.setter
    def time(self, time):

        self._time = time

    @property
    def version(self):

        return self._version

    @version.setter
    def version(self, version):

        self._version = version

    @classmethod
    def from_dict(cls, data):
        return cls(
            detail=ChurchillVCFEvent.from_dict(data.get("detail")),
            account=data.get("account"),
            detail_type=data.get("detail-type"),
            event_id=data.get("id"),
            region=data.get("region"),
            resources=data.get("resources"),
            source=data.get("source"),
            time=parse_datetime(data.get("time")),
            version=data.get("version")
        )

    def to_dict(self):
        result = {}

        for attr, _ in six.iteritems(self._types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(AWSEvent, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __eq__(self, other):
        if not isinstance(other, AWSEvent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
