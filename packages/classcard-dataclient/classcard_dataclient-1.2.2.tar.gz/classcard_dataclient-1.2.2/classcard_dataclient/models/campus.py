# -*- coding: utf-8 -*-
from ..models.base import BaseModel


class Campus(BaseModel):
    def __init__(self, *args, **kwargs):
        self.uid = None
        self.name = None  # 必填*
        self.code = None
        self.external_id = None
        self.description = None
        self.school = None
        super(Campus, self).__init__(*args, **kwargs)
        self.required_filed = ['name']

    @property
    def nirvana_data(self):
        data = {
            "name": self.name,
            "code": self.code,
            "external_id": self.external_id,
            "school": self.school
        }
        return data
