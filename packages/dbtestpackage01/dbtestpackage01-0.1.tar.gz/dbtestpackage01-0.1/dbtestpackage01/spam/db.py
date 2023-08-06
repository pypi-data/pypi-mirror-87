class Sessao:
    contador = 0
    usuarios = []

    def salvar(self, usuario):
        Sessao.contador += 1
        usuario.id = Sessao.contador
        self.usuarios.append(usuario)

    def roll_back(self):
        return self.usuarios.clear()

    def listar(self):
        return self.usuarios

    def fechar(self):
        pass


class Conexao:
    def gerar_sessao(self):
        return Sessao()

    def fechar(self):
        pass
