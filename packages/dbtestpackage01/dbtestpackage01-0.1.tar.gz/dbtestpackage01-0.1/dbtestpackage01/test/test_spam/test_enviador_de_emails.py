import pytest

from dbtestpackage01.spam.enviador_de_email import Enviador, EmailInvalido


def test_criar_enviador():
    enviador = Enviador()
    assert enviador is not None


@pytest.mark.parametrize(
    'remetente',
    ['example@gmail.com', 'anotherexample@gmail.com']
)
def test_remetente(remetente):
    enviador = Enviador()
    resultado = enviador.enviar(
        remetente,
        'johndoe@gmail.com',
        'Pytest',
        'Tests on Pytest',
    )
    assert remetente in resultado


@pytest.mark.parametrize(
    'remetente',
    ['', 'example']
)
def test_remetente_invalido(remetente):
    enviador = Enviador()
    with pytest.raises(EmailInvalido):
        enviador.enviar(
            remetente,
            'johndoe@gmail.com',
            'Pytest',
            'Tests on pytest'
        )
