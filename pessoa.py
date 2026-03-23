class Pessoa:
    def __init__(self, nome, categoria, curso):
        self._nome = nome
        self._categoria = categoria
        self._curso = curso


    def get_info(self):
        return self._nome, self._categoria, self._curso
        