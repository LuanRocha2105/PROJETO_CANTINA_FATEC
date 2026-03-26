from Modelos.Produto import Produto


class FilaEstoque:

    def __init__(self):
        self._inicio = None
        self.fim = None

    def adicionar_produto(self, produto: Produto):
        if self._inicio is None:
            self._inicio = produto
            self.fim = produto
        else:
            self.fim.proximo = produto
            self.fim = produto

    def remover_produto(self, nome_produto):
        atual = self._inicio
        anterior = None
        while atual is not None:
            if atual.get_nome() == nome_produto:
                if anterior is None:
                    self._inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                if atual == self.fim:
                    self.fim = anterior
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def listar_produtos(self):
        atual = self._inicio
        while atual is not None:
            print(f"{atual.get_nome()} - Quantidade: {atual.get_quantidade()} - Vence em: {atual.get_validade()}")
            atual = atual.proximo

    def listar_nomes_disponiveis(self):
        nomes = []
        atual = self._inicio
        while atual is not None:
            if not atual.esta_vencido() and atual.get_quantidade() > 0:
                if atual.get_nome() not in nomes:
                    nomes.append(atual.get_nome())
            atual = atual.proximo
        return nomes

    def buscar_lotes_disponiveis(self, nome):
        lotes = []
        atual = self._inicio
        while atual is not None:
            if atual.get_nome() == nome and not atual.esta_vencido() and atual.get_quantidade() > 0:
                lotes.append(atual)
            atual = atual.proximo
        lotes.sort(key=lambda l: l.get_validade())
        return lotes

    def limpar(self):
        self._inicio = None
        self.fim = None