from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class PropertyDebitoCamposBoleto(Model):
    id = fields.IntField(pk=True)
    id_property_debito = fields.IntField()
    nome = fields.CharField(max_length=255)
    valor = fields.CharField(max_length=1000)
    updated_at = fields.DatetimeField(default=datetime.today())
    created_at = fields.DatetimeField(default=datetime.today())

    class Meta:
        table = "property_debito_campos_boleto"

    @classmethod
    async def get_by_debitos(cls, debitos_banco: list):
        """
        Monta a busca pelos debitos passados
        """
        return await cls.filter(
            id_property_debito__in=[d.id for d in debitos_banco]
        ).all()
