from datetime import datetime

from dtos.iptu import InfoDebitoDto
from tortoise import Tortoise

from .models import (
    Imovel,
    PropertyDebito,
    ProprietariosProperty,
    Spider,
    PropertyDebitoCamposBoleto
)
from .models.proprietario import Proprietarios


class MysqlConnection:
    def __init__(
        self,
        db_url: str = "",
    ):
        self.db_url = db_url

    async def init(self):
        """Inicia a conexão com o banco."""
        await Tortoise.init(
            db_url=self.db_url,
            modules={"models": ["db.mysql.models"]},
        )

    @staticmethod
    async def close():
        """Fecha a conexão com o banco."""
        await Tortoise.close_connections()

    async def buscar_imovel(self, imovel_inscricao: int, imovel_city: str, imovel_state: str) -> Imovel:
        """
        Busca imovel no banco.

        :param imovel_inscricao: inscricao do imovel.
        :param imovel_city: nome da cidade do imovel.
        :param imovel_state: estado do imovel.
        :return: O imovel.
        """
        await self.init()
        imovel = await Imovel.buscar_imovel(imovel_inscricao, imovel_city, imovel_state)
        await self.close()

        return imovel

    async def buscar_imovel_armacao(self):
        await self.init()
        imovel = await Imovel.buscar_imovel_armacao()
        await self.close()

        return imovel

    async def update_debitos(
        self,
        imovel: Imovel,
        spider: Spider,
        debito: InfoDebitoDto,
    ):
        """
        Acessa o banco e adiciona o debito.

        :param imovel: objeto Imovel
        :param spider: objeto Spider
        :param debito: debito do imovel
        """
        await self.init()

        assert imovel.id is not None, "id do imovel é None"
        assert spider.id is not None

        property_debito = PropertyDebito(
            id_property=imovel.id,
            id_spider=spider.id,
            id_tipo_property_debito=-1,
            ano=debito.exercicio,
            parcela=debito.parcela,
            descricao=debito.descricao,
            vencimento=debito.vencimento,
            valor_inicial=debito.valor_inicial,
            valor_final=debito.valor_final,
            linha_digitavel=debito.linha_digitavel,
        )

        debito = await PropertyDebito.filter(
            id_property=imovel.id,
            id_spider=spider.id,
            ano=debito.exercicio,
            parcela=debito.parcela,
            descricao=debito.descricao).first()
        if not debito:
            await PropertyDebito.save(property_debito)

        await self.close()

    async def update_proprietario(
        self, imovel: Imovel, id_tipo_debito: int, nome: str, documento: str
    ):
        """
        Acessa o banco e atualiza o proprietario de um imovel

        :param imovel: objeto Imovel
        :param id_tipo_debito: tipo do debito
        :param nome: nome do proprietario
        :param documento: documento do proprietario
        """
        await self.init()

        # Busca o proprietario
        proprietario = await Proprietarios.get_by_client_nome(
            imovel.client_id, nome
        )

        # Se não encontrar cria um novo
        if not proprietario:
            proprietario = await Proprietarios(
                id_client=imovel.client_id, nome=nome, documento=documento
            )
            await Proprietarios.save(proprietario)
        else:
            # se ja existir o proprietario, apenas atualiza seu documento
            proprietario.documento = documento
            await Proprietarios.save(proprietario)

        assert (
            proprietario and imovel.id and proprietario.id is not None
        ), "proprietario nao encontrado"

        # Busca todos os proprietarios desse imovel e desse tipo de debito
        proprietarios_antigos = await ProprietariosProperty.get_inativos(
            imovel.id, id_tipo_debito, proprietario.id
        )

        # Inativa esses proprietarios
        for prop in proprietarios_antigos:
            prop.fl_atual = False
            prop.fl_manual = False
            prop.id_responsavel = None
            prop.updated_at = datetime.today()
            await ProprietariosProperty.save(prop)

        # Busca o proprietarios_property
        proprietarios_property = await ProprietariosProperty.get_by_ids(
            imovel.id, proprietario.id, id_tipo_debito
        )

        if proprietarios_property:
            proprietarios_property.fl_atual = True
            proprietarios_property.fl_manual = False
            proprietarios_property.id_responsavel = None
            await ProprietariosProperty.save(proprietarios_property)
        # Se não encontrar cria um novo
        else:
            proprietarios_property = await ProprietariosProperty(
                id_property=imovel.id,
                id_proprietarios=proprietario.id,
                id_tipo_property_debito=id_tipo_debito,
                fl_atual=True,
            )
            await ProprietariosProperty.save(proprietarios_property)

        await self.close()

    async def buscar_spider(self, id_cidade: int):
        """Busca os parâmetros do imóvel a partir do seu ID."""

        await self.init()
        spider = await Spider.buscar_spider(id_cidade)
        await self.close()

        return spider
