class Pessoa:
    def __init__(self, nome, categoria, curso):
        self._nome = nome
        self._categoria = categoria
        self._curso = curso

    def get_info(self):
        return self._nome, self._categoria, self._curso

    def get_nome(self):
        return self._nome
    


    @classmethod
    def criar_com_menu(cls):
        
        print("\n--- Cliente ---")
        nome = input("Nome do cliente: ")
       
        categorias = ["Aluno", "Professor", "Funcionário"]
        print("\n--- Categoria ---")
        for i, cat in enumerate(categorias, 1):
            print(f"{i}. {cat}")
        escolha_cat = input("Escolha o número da categoria: ")
        if not escolha_cat.isdigit() or not (1 <= int(escolha_cat) <= len(categorias)):
            print("Opção inválida.")
            return None
        categoria = categorias[int(escolha_cat) - 1]
        
        cursos = ["IA", "ESG", "Não se aplica"]
        print("\n--- Curso ---")
        for i, cur in enumerate(cursos, 1):
            print(f"{i}. {cur}")
        escolha_cur = input("Escolha o número do curso: ")
        if not escolha_cur.isdigit() or not (1 <= int(escolha_cur) <= len(cursos)):
            print("Opção inválida.")
            return None
        curso = cursos[int(escolha_cur) - 1]

        return cls(nome, categoria, curso)
        