from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class Proprietarios(Model):

    id = fields.IntField(pk=True)
    id_client = fields.IntField()
    nome = fields.CharField(max_length=255)
    documento = fields.CharField(max_length=40)
    email = fields.CharField(max_length=255, null=True)
    fl_manual = fields.BooleanField(default=False)
    id_responsavel = fields.IntField()
    updated_at = fields.DatetimeField(default=datetime.today())
    created_at = fields.DatetimeField(default=datetime.today())

    class Meta:
        table = "proprietarios"

    @classmethod
    async def get_by_client_nome(cls, client_id: int, nome: str):
        """
        Monta a busca pelo id do cliente e seu nome
        """

        return await cls.filter(id_client=client_id, nome=nome).first()

    @classmethod
    async def get_by_id(cls, proprietario_id: int, client_id: int):
        """
        Monta a busca pelo id do cliente e seu id
        """

        return await cls.filter(id=proprietario_id, id_client=client_id).get()
