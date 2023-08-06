import pytest


class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        self.id = None


def test_salvar_usuario(conexao, sessao):
    usuario = Usuario(nome='Jonh', email='jonhdoe@gmail.com')
    sessao.salvar(usuario)
    assert isinstance(usuario.id, int)


@pytest.mark.parametrize(
    'usuarios',
    [
        [
            Usuario(nome='jonh', email='jonh@gmail.com'),
            Usuario(nome='example', email='example@gmail.com')
        ],
    ]
)
def test_lista_usuario(conexao, sessao, usuarios):
    for usuario in usuarios:
        sessao.salvar(usuario)
    assert usuarios == sessao.listar()
