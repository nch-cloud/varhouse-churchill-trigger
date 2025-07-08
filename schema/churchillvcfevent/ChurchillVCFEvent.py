# coding: utf-8
import pprint
import re  # noqa: F401

import six
from schema.churchillvcfevent.ChurchillVCFEventItem import ChurchillVCFEventItem  # noqa: F401,E501


class ChurchillVCFEvent(object):

    def __init__(self, case_name:str=None, genome_ver:str=None, merged_vcf:str=None, mutect2_somatic_vcf:str=None,
                 strelka2_somatic_vcf:str=None, mode:str=None, project:str=None, run_id:str=None, samples:list[ChurchillVCFEventItem]=None,
                 sequencer_id:str=None):  # noqa: E501
        self.case_name = case_name
        self.genome_ver = genome_ver
        self.merged_vcf = merged_vcf
        self.mutect2_somatic_vcf = mutect2_somatic_vcf
        self.strelka2_somatic_vcf = strelka2_somatic_vcf
        self.mode = mode
        self.project = project
        self.run_id = run_id
        self.samples = samples
        self.sequencer_id = sequencer_id

    @property
    def case_name(self):

        return self._case_name

    @case_name.setter
    def case_name(self, case_name):

        self._case_name = case_name

    @property
    def genome_ver(self):

        return self._genome_ver

    @genome_ver.setter
    def genome_ver(self, genome_ver):

        self._genome_ver = genome_ver

    @property
    def merged_vcf(self):

        return self._merged_vcf

    @merged_vcf.setter
    def merged_vcf(self, merged_vcf):

        self._merged_vcf = merged_vcf

    @property
    def mutect2_somatic_vcf(self):

        return self._mutect2_somatic_vcf

    @mutect2_somatic_vcf.setter
    def mutect2_somatic_vcf(self, mutect2_somatic_vcf):

        self._mutect2_somatic_vcf = mutect2_somatic_vcf

    @property
    def strelka2_somatic_vcf(self):

        return self._strelka2_somatic_vcf

    @strelka2_somatic_vcf.setter
    def strelka2_somatic_vcf(self, strelka2_somatic_vcf):

        self._strelka2_somatic_vcf = strelka2_somatic_vcf

    @property
    def mode(self):

        return self._mode

    @mode.setter
    def mode(self, mode):

        self._mode = mode

    @property
    def project(self):

        return self._project

    @project.setter
    def project(self, project):

        self._project = project

    @property
    def run_id(self):

        return self._run_id

    @run_id.setter
    def run_id(self, run_id):

        self._run_id = run_id

    @property
    def samples(self):

        return self._samples

    @samples.setter
    def samples(self, samples):

        self._samples = samples

    @property
    def sequencer_id(self):

        return self._sequencer_id

    @sequencer_id.setter
    def sequencer_id(self, sequencer_id):

        self._sequencer_id = sequencer_id

    @classmethod
    def from_dict(cls, data):
        return cls(
            case_name=data.get("caseName") if "caseName" in data else data.get("case_name"),
            genome_ver=data.get("genome_ver"),
            merged_vcf=data.get("merged_vcf"),
            mutect2_somatic_vcf=data.get("mutect2_somatic_vcf"),
            strelka2_somatic_vcf=data.get("strelka2_somatic_vcf"),
            mode=data.get("mode"),
            project=data.get("project"),
            run_id=data.get("run_id"),
            samples=[ChurchillVCFEventItem.from_dict(s) for s in data.get("samples")] if data.get("samples") else None,
            sequencer_id=data.get("sequencer_id")
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
        if issubclass(ChurchillVCFEvent, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __eq__(self, other):
        if not isinstance(other, ChurchillVCFEvent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
