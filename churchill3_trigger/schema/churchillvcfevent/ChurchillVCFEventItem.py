# coding: utf-8
import pprint
import re  # noqa: F401

import six


class ChurchillVCFEventItem(object):

    def __init__(self, name:str=None, relation:str=None, sample_type:str=None, umi:bool=None, unaligned_files:list[str]=None):  # noqa: E501
        self.name = name
        self.relation = relation
        self.type = sample_type
        self.umi = umi
        self.unaligned_files = unaligned_files

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, name):

        self._name = name

    @property
    def relation(self):

        return self._relation

    @relation.setter
    def relation(self, relation):

        self._relation = relation

    @property
    def type(self):

        return self._type

    @type.setter
    def type(self, sample_type):

        self._type = sample_type

    @property
    def umi(self):

        return self._umi

    @umi.setter
    def umi(self, umi):

        self._umi = umi

    @property
    def unaligned_files(self):

        return self._unaligned_files

    @unaligned_files.setter
    def unaligned_files(self, unaligned_files):

        self._unaligned_files = unaligned_files

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            relation=data.get("relation"),
            sample_type=data.get("type"),
            umi=data.get("umi"),
            unaligned_files=[s for s in data.get("unaligned_files")] if data.get("unaligned_files") else None
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
        if issubclass(ChurchillVCFEventItem, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __eq__(self, other):
        if not isinstance(other, ChurchillVCFEventItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
