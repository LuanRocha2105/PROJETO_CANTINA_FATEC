import pickle
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("pt_BR")

PRODUTOS_PRECOS = {
    "Coca-Cola":       (2.50, 4.00),
    "Pepsi":           (2.00, 3.50),
    "Fanta":           (2.00, 3.50),
    "Guaraná":         (2.00, 3.50),
    "Água":            (0.80, 2.00),
    "Suco de Laranja": (3.00, 5.00),
    "Café":            (1.00, 2.50),
    "Achocolatado":    (2.50, 4.00),
    "Biscoito":        (1.50, 3.00),
    "Salgadinho":      (1.80, 3.50),
}


def listar_menu_produtos():
    nomes = list(PRODUTOS_PRECOS.keys())
    print("\nProdutos disponíveis: \n")
    for i, nome in enumerate(nomes, 1):
        print(f"{i}. {nome}")
    escolha = input("Escolha o número do produto: ")
    if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
        return nomes[int(escolha) - 1]
    print("Opção inválida.")
    return None


def gerar_produtos(fila_estoque, quantidade=10):
    from Modelos.Produto import Produto

    for _ in range(quantidade):
        nome = random.choice(list(PRODUTOS_PRECOS.keys()))
        quantidade_estoque = random.randint(5, 50)
        preco_compra, preco_venda = PRODUTOS_PRECOS[nome]

        data_compra = datetime.now() - timedelta(days=random.randint(1, 60))
        data_vencimento = datetime.now() + timedelta(days=random.randint(10, 365))

        produto = Produto(nome, quantidade_estoque, preco_compra, preco_venda, data_compra, data_vencimento)
        fila_estoque.adicionar_produto(produto)

    print(f"{quantidade} produtos gerados com sucesso!")


def gerar_pessoas(quantidade=5):
    from Modelos.Pessoa import Pessoa

    categorias = ["Aluno", "Funcionário", "Professor"]
    cursos = ["IA", "ESG", "Não se aplica"]
    pessoas = []

    for _ in range(quantidade):
        nome = fake.name()
        categoria = random.choice(categorias)
        curso = random.choice(cursos)
        pessoas.append(Pessoa(nome, categoria, curso))

    return pessoas

def gerar_vendas(fila_estoque, pilha_pagamentos, quantidade=5):
    from Estruturas.PilhaPagamentos import Pagamento

    vendas_geradas = 0

    for _ in range(quantidade):
        cliente = gerar_pessoas(1)[0]
        nome_cliente, categoria, curso = cliente.get_info()

        # Coleta lotes disponíveis no estoque
        lotes_disponiveis = []
        atual = fila_estoque._inicio
        while atual is not None:
            if not atual.esta_vencido() and atual.get_quantidade() > 0:
                lotes_disponiveis.append(atual)
            atual = atual.proximo

        if not lotes_disponiveis:
            print("\nEstoque insuficiente para gerar mais vendas.")
            break

        # Escolhe entre 1 e 3 produtos diferentes para a venda
        qtd_itens = random.randint(1, min(3, len(lotes_disponiveis)))
        lotes_escolhidos = random.sample(lotes_disponiveis, qtd_itens)

        itens_dict = {}
        total = 0.0

        for lote in lotes_escolhidos:
            quantidade_venda = random.randint(1, min(3, lote.get_quantidade()))
            lote.set_quantidade(lote.get_quantidade() - quantidade_venda)
            itens_dict[lote.get_nome()] = itens_dict.get(lote.get_nome(), 0) + quantidade_venda
            total += lote.get_preco_venda() * quantidade_venda

        pagamento = Pagamento(nome_cliente, categoria, curso, total, itens_dict)
        pilha_pagamentos.empilhar(pagamento)
        vendas_geradas += 1

    

    
 
def salvar_dados(fila_estoque, pilha_pagamentos, caminho="dados_cantina.pkl"):
    dados = {
        "fila_estoque": fila_estoque,
        "pilha_pagamentos": pilha_pagamentos
    }
    with open(caminho, "wb") as f:
        pickle.dump(dados, f)
    print(f"Dados salvos em '{caminho}'.")


def salvar_dados(fila_estoque, pilha_pagamentos, caminho="dados_cantina.pkl"):
    dados = {
        "fila_estoque": fila_estoque,
        "pilha_pagamentos": pilha_pagamentos
    }
    with open(caminho, "wb") as f:
        pickle.dump(dados, f)


def carregar_dados(caminho="dados_cantina.pkl"):
    try:
        with open(caminho, "rb") as f:
            dados = pickle.load(f)
        print(f"Dados carregados de '{caminho}'.")
        return dados["fila_estoque"], dados["pilha_pagamentos"]
    except FileNotFoundError:
        print("Nenhum dado salvo encontrado. Iniciando do zero.")
        return None, None