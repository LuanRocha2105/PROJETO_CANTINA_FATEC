class Pagamento:
    def __init__(self, pessoa, valor, data_pagamento):
        self._pessoa = pessoa
        self._valor = valor
        self._data_pagamento = data_pagamento
        self.proximo = None  

    def get_resumo(self):
        nome, categoria, curso = self._pessoa.get_info()
        return f"Pagamento de {self._valor} por {nome} ({categoria} - {curso}) em {self._data_pagamento}"