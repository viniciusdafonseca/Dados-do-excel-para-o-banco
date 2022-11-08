from pydantic import BaseModel


class InfoDebitoDto(BaseModel):
    """
    Estrutura que representa os dados mais importantes para coleta dos débitos
    """

    # DADOS OBRIGATORIOS DE DÉBITOS
    valor_inicial: float
    valor_final: float
    vencimento: str
    exercicio: int = 2022
    parcela: str = "UNICA"
    descricao: str = "IPTU"
    linha_digitavel: str
    unica: bool = True

