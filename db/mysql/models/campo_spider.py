from tortoise import fields
from tortoise.models import Model


class CampoSpider(Model):
    id = fields.IntField(pk=True)
    id_spider = fields.IntField()
    id_campo = fields.IntField()
    valor = fields.CharField(max_length=64)
    caminho = fields.CharField(max_length=128)

    class Meta:
        table = "campo_spider"

    campo = fields.ForeignKeyField(
        "models.Campo", source_field="id_campo", related_name="campo"
    )

    @classmethod
    async def get_by_spider(cls, spider_id: int):
        """
        Monta a busca pelo id da spider
        """
        query = cls.filter(id_spider=spider_id)
        campos = await query.all()

        for campo in campos:
            await campo.fetch_related("campo")

        return campos
