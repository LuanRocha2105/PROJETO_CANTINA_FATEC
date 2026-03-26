from datetime import datetime


class Pagamento:
    def __init__(self, nome_cliente, categoria, curso, valor, itens_comprados):
        self._nome_cliente = nome_cliente
        self._categoria = categoria
        self._curso = curso
        self._valor = valor
        self._data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._itens_comprados = itens_comprados
        self.proximo = None

    def get_info(self):
        return {
            "nome": self._nome_cliente,
            "categoria": self._categoria,
            "curso": self._curso,
            "valor": self._valor,
            "data_hora": self._data_hora,
            "itens": self._itens_comprados
        }

    def get_valor(self):
        return self._valor

    def get_nome_cliente(self):
        return self._nome_cliente

    def get_data_hora(self):
        return self._data_hora

    def get_itens(self):
        return self._itens_comprados


class PilhaPagamentos:

    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def empilhar(self, pagamento: Pagamento):
        pagamento.proximo = self._topo
        self._topo = pagamento
        self._tamanho += 1

    def desempilhar(self):
        if self._topo is None:
            print("Pilha vazia.")
            return None
        pagamento = self._topo
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return pagamento

    def ver_topo(self):
        return self._topo

    def esta_vazia(self):
        return self._topo is None

    def listar_pagamentos(self):
        atual = self._topo
        if atual is None:
            print("Nenhum pagamento registrado.")
            return
        while atual is not None:
            info = atual.get_info()
            print(f"Cliente: {info['nome']} | Categoria: {info['categoria']} | Curso: {info['curso']} | Valor: R${info['valor']:.2f} | Data/Hora: {info['data_hora']}")
            atual = atual.proximo

    def tamanho(self):
        return self._tamanho

    def limpar(self):
        self._topo = None
        self._tamanho = 0