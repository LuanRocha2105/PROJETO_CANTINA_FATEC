import Produto

class FilaEstoque:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def adicionar_produto(self, produto: Produto):
        if self.inicio is None:
            self.inicio = produto
            self.fim = produto
        else:
            self.fim.proximo = produto
            self.fim = produto

    def remover_produto(self):
        if self.inicio is not None:
            produto_removido = self.inicio
            self.inicio = self.inicio.proximo
            if self.inicio is None:
                self.fim = None
            return produto_removido
        return None