from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel
from datetime import datetime


class ShortUrl(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    short_url = fields.CharField(max_length=255)
    created_date = fields.DatetimeField(auto_now_add=True)
    redirect_count = fields.IntField(default=0)
    last_redirected_date = fields.DatetimeField(default=datetime.now())
    last_client_ip = fields.CharField(default='None', max_length=15)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.short_url
