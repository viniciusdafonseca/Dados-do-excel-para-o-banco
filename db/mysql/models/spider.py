from tortoise import fields
from tortoise.exceptions import DoesNotExist
from tortoise.models import Model


class Spider(Model):

    id = fields.IntField(pk=True)
    id_cidade = fields.IntField(unique=True)
    id_tipo_spider = fields.IntField(unique=True)
    nome = fields.CharField(max_length=128)
    url = fields.CharField(max_length=128)
    url_boleto = fields.CharField(max_length=128)
    extensao_boleto = fields.CharField(max_length=10)

    imoveis = fields.ManyToManyField(
        "models.Imovel",
        through="property_spider",
        forward_key="id_property",
    )

    @classmethod
    async def buscar_spider(cls, id_cidade: int):
        """
        Busca spider.
        :param id_cidade: ID da cidade da spider.
        :return: A spider.
        """

        try:
            spider = await cls.filter(id_cidade=id_cidade, id_tipo_spider=-1).first()
        except DoesNotExist as err:
            msg = f"[MySQL] Não foi encontrado nenhuma spider!"
            raise Exception(msg) from err

        return spider
