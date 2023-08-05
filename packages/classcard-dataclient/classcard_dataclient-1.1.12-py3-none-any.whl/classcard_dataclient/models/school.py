from ..models.base import BaseModel


class School(BaseModel):
    def __init__(self, *args, **kwargs):
        self.uid = None
        self.name = None
        self.description = None
        self.phone = None
        self.number = None
        self.province = None
        self.area = None
        self.city = None
        self.address = None
        self.motto = None
        self.principal_name = None
        self.principal_email = None
        self.principal_phone = None
        super(School, self).__init__(*args, **kwargs)
        self.required_filed = ['name', 'phone', "number", "province", "area", "city", "address",
                               "principal_name", "principal_email", "principal_phone"]

    @property
    def sso_data(self):
        data = {"name": self.name,
                "description": self.description,
                "phone": self.phone,
                "code": self.number,
                "province": self.province,
                "area": self.area,
                "city": self.city,
                "address": self.address,
                "motto": self.motto,
                "principal_name": self.principal_name,
                "principal_email": self.principal_email,
                "principal_phone": self.principal_phone}
        return data
