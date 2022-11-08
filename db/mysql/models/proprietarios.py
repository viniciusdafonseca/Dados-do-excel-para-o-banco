from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class ProprietariosProperty(Model):
    id = fields.IntField(pk=True)
    id_property = fields.IntField()
    id_proprietarios = fields.IntField()
    id_tipo_property_debito = fields.IntField()
    fl_atual = fields.BooleanField()
    fl_manual = fields.BooleanField(default=False)
    id_responsavel = fields.IntField()
    updated_at = fields.DatetimeField(default=datetime.today())
    created_at = fields.DatetimeField(default=datetime.today())

    class Meta:
        table = "proprietarios_property"

    @classmethod
    async def get_inativos(
        cls, imovel_id: int, tipo_debito_id: int, proprietario_id: int
    ):
        """
        Monta a busca de todos os proprietarios_property do imovel menos o atual
        """
        proprietarios = await cls.filter(
            fl_atual=True,
            id_property=imovel_id,
            id_tipo_property_debito=tipo_debito_id,
            id_proprietarios__not=proprietario_id,
        ).all()

        return proprietarios

    @classmethod
    async def get_by_ids(
        cls, imovel_id: int, proprietario_id: int, tipo_debito_id: int
    ):
        """
        Monta a busca pelo id da propriedade, id do proprieario e seu tipo
        """
        return await cls.filter(
            fl_atual=True,
            id_property=imovel_id,
            id_proprietarios=proprietario_id,
            id_tipo_property_debito=tipo_debito_id,
        ).first()
