from unittest.mock import Mock

import pytest

from dbtestpackage01.spam.main import EnviadorDeSpam
from dbtestpackage01.test.test_spam.test_usuario import Usuario


@pytest.mark.parametrize(
    'usuarios',
    [
        [
            Usuario(nome='jonh', email='jonhdoe@gmail.com'),
            Usuario(nome='july', email='july@gmail.com')
        ]
    ]

)
def test_qtd_spam(sessao, usuarios):
    for usuario in usuarios:
        sessao.salvar(usuario)

    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'john@doe',
        'Pytest',
        'Tests on Pytest'
    )
    assert len(usuarios) == enviador.enviar.call_count


def test_parametros_spam(sessao):
    usuario = Usuario(nome='Jonh', email='johndoe@gmail.com')
    sessao.salvar(usuario)
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'july@gmail.com',
        'Pytest',
        'Tests on pytest'
    )
    enviador.enviar_assert_once_called_with(
        'july@gmail.com',
        'jonhdoe@gmail.com',
        'Pytest',
        'Tests on pytest'
    )
