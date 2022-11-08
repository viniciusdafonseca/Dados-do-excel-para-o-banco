from tortoise import fields
from tortoise.exceptions import DoesNotExist
from tortoise.models import Model
from loguru import logger


class Imovel(Model):

    id = fields.IntField(pk=True)
    inscricao = fields.CharField(max_length=64)
    document = fields.CharField(max_length=25)
    parametro_adicional = fields.CharField(max_length=256)
    usuario = fields.CharField(max_length=100)
    senha = fields.CharField(max_length=32)
    rip = fields.CharField(max_length=255)
    fl_ativo = fields.IntField(default=1)
    id_cidade = fields.IntField()
    client_id = fields.IntField()
    department_id = fields.IntField()
    updated_at = fields.DateField()
    city = fields.CharField(max_length=32)
    state = fields.CharField(max_length=2)

    spider = fields.ManyToManyField(
        "models.Spider",
        through="property_spider",
        forward_key="id_spider",
        backward_key="id_property",
    )

    class Meta:
        table = "properties"

    @classmethod
    async def buscar_imovel(cls, imovel_inscricao: int, imovel_city: str, imovel_state: str):
        """
        Busca imovel no banco.

        :param imovel_inscricao: inscricao do imovel.
        :param imovel_city: nome da cidade do imovel.
        :param imovel_state: estado do imovel.
        :return: O imovel.
        """

        logger.info(f"{imovel_inscricao}  {imovel_city}  {imovel_state}")
        imovel = await cls.filter(inscricao=imovel_inscricao, city=imovel_city, state=imovel_state).first()
        if not imovel:
            logger.warning(imovel_inscricao)
            imovel = await cls.filter(inscricao=str(imovel_inscricao).lstrip("0"), city=imovel_city, state=imovel_state).first()

        return imovel

    @classmethod
    async def buscar_imovel_armacao(cls):

        imovel = await cls.filter(inscricao="01060260196001".lstrip("0"), city="ARMAÇÃO DOS BÚZIOS", state="RJ").first()

        return imovel



