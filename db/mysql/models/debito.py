from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class PropertyDebito(Model):
    id = fields.IntField(pk=True)
    id_property = fields.IntField()
    id_spider = fields.IntField()
    id_tipo_property_debito = fields.IntField()
    ano = fields.CharField(max_length=32)
    parcela = fields.CharField(max_length=64)
    descricao = fields.CharField(max_length=128)
    vencimento = fields.DateField()
    valor_inicial = fields.FloatField()
    valor_final = fields.FloatField()
    acrescimos = fields.FloatField()
    descontos = fields.FloatField(null=True)
    campo_adicional = fields.CharField(max_length=64, null=True)
    linha_digitavel = fields.CharField(max_length=128, null=True)
    caminho_boleto = fields.CharField(max_length=128, null=True)
    fl_unica = fields.BooleanField(default=False)
    fl_ativo = fields.BooleanField(default=True)
    fl_manual = fields.BooleanField(default=False)
    id_responsavel = fields.IntField()
    updated_at = fields.DatetimeField(default=datetime.today())
    created_at = fields.DatetimeField(default=datetime.today())

    class Meta:
        table = "property_debito"

    @classmethod
    async def get_by_property(
        cls,
        imovel_id: int,
        tipo_debito_id: int,
    ):
        """
        Monta a busca pelo id da propriedade e seu tipo
        """

        debitos = await cls.filter(
            fl_ativo=True,
            id_property=imovel_id,
            id_tipo_property_debito=tipo_debito_id,
        ).all()
        return debitos

    @classmethod
    async def get_debitos_inativos(
        cls,
        imovel_id: int,
        tipo_debito_id: int,
        debitos_id: list,
    ):
        """
        Monta a busca dos debitos que nao estao na lista passada
        """

        debitos = await cls.filter(
            fl_ativo=True,
            id_property=imovel_id,
            id_tipo_property_debito=tipo_debito_id,
            id__not_in=debitos_id,
        ).all()

        return debitos

    @staticmethod
    async def set_debito(result, debito):
        """
        Atuliza os valores
        """

        result.id_property = debito.id_property
        result.id_spider = debito.id_spider
        result.id_tipo_property_debito = debito.id_tipo_property_debito
        result.ano = debito.ano
        result.parcela = debito.parcela
        result.descricao = debito.descricao
        result.vencimento = debito.vencimento
        result.valor_inicial = debito.valor_inicial
        result.valor_final = debito.valor_final
        result.acrescimos = debito.acrescimos
        result.descontos = debito.descontos
        result.campo_adicional = debito.campo_adicional
        result.linha_digitavel = debito.linha_digitavel
        result.caminho_boleto = debito.caminho_boleto
        result.fl_unica = debito.fl_unica
        result.fl_ativo = True
        result.fl_manual = False
        result.id_responsavel = None
        result.updated_at = datetime.today()

        return result
