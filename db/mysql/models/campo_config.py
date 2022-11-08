from tortoise import fields
from tortoise.models import Model


class CampoSpiderConfig(Model):
    id = fields.IntField(pk=True)
    id_spider = fields.IntField()
    campo = fields.CharField(max_length=64)
    valor = fields.CharField(max_length=128)
    id_tipo_campo_spider_config = fields.IntField()

    class Meta:
        table = "campo_spider_config"

    @classmethod
    async def buscar_campo_spider_config(cls, spider_id: int):
        """
        Monta a busca pelo id da spider
        """
        query = cls.filter(id_spider=spider_id)
        cotas_unicas = await query.all()

        return cotas_unicas
