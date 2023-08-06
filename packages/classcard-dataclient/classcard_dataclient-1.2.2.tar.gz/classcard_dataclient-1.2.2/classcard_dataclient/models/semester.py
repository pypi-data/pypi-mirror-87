from ..models.base import BaseModel


class SemesterV2(BaseModel):
    class_version = "v2"

    def __init__(self, *args, **kwargs):
        self.uid = None
        self.name = None  # 必填*,学期名称
        self.number = None
        self.term = None  # 第一学期，第二学期
        self.academic_year = None  # 学年, 2018-2019
        self.begin_date = None
        self.end_date = None
        super(SemesterV2, self).__init__(*args, **kwargs)
        self.required_filed = ["name", "begin_date", "end_date"]

    @property
    def nirvana_data(self):
        data = {"name": self.name,
                "number": self.number,
                "term": self.term,
                "begin_date": self.begin_date,
                "end_date": self.end_date}
        if self.academic_year:
            data["academic_year"] = self.academic_year
        return data
