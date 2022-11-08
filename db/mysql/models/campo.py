from tortoise import fields
from tortoise.models import Model


class Campo(Model):

    id = fields.IntField(pk=True)
    nome = fields.CharField(max_length=32)
    identificador = fields.CharField(max_length=32)

    class Meta:
        table = "campo"
