from datetime import datetime
 
 
class Relatorios:
 
    @staticmethod
    def _formatar_data_hora(data_hora_str):
        dt = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d/%m/%Y %H:%M:%S")
 
    @staticmethod
    def _formatar_data(data):
        """Formata um objeto datetime para 'DD/MM/YYYY'."""
        return data.strftime("%d/%m/%Y")
 
    @staticmethod
    def relatorio_vendas(pilha_pagamentos):
        print("\n========== RELATÓRIO DE VENDAS ==========")
        atual = pilha_pagamentos.ver_topo()
        if atual is None:
            print("Nenhuma venda registrada.")
            print("=========================================\n")
            return
 
        total_geral = 0.0
        total_vendas = 0
 
        while atual is not None:
            info = atual.get_info()
            data_formatada = Relatorios._formatar_data_hora(info['data_hora'])
            print(f"\nCliente: {info['nome']}")
            print(f"  Categoria: {info['categoria']} | Curso: {info['curso']}")
            print(f"  Data/Hora: {data_formatada}")
            print(f"  Valor pago: R${info['valor']:.2f}")
            total_geral += info['valor']
            total_vendas += 1
            atual = atual.proximo
 
        print(f"\nTotal de vendas: {total_vendas}")
        print(f"Receita total:  R${total_geral:.2f}")
        print("=========================================\n")
 
    @staticmethod
    def relatorio_consumo(pilha_pagamentos):
        print("\n========== RELATÓRIO DE CONSUMO ==========")
        atual = pilha_pagamentos.ver_topo()
        if atual is None:
            print("Nenhum consumo registrado.")
            print("==========================================\n")
            return
 
        consumo_total = {}  
        while atual is not None:
            for produto, qtd in atual.get_itens().items():
                if produto in consumo_total:
                    consumo_total[produto] += qtd
                else:
                    consumo_total[produto] = qtd
            atual = atual.proximo
 
        print("\nProduto                  | Qtd vendida")
        print("-" * 40)
        for produto, qtd in consumo_total.items():
            print(f"{produto:<25}| {qtd}")
        print("==========================================\n")
 
    @staticmethod
    def relatorio_estoque(fila_estoque):
        print("\n========== RELATÓRIO DE ESTOQUE ==========")
        atual = fila_estoque._inicio
        if atual is None:
            print("Estoque vazio.")
            print("==========================================\n")
            return

        
        normais = []
        vencidos = []
        while atual is not None:
            if atual.esta_vencido():
                vencidos.append(atual)
            elif atual.get_quantidade() > 0:
                normais.append(atual)
            atual = atual.proximo

        
        grupos = {}
        for lote in normais:
            nome = lote.get_nome()
            if nome not in grupos:
                grupos[nome] = []
            grupos[nome].append(lote)
        for nome in grupos:
            grupos[nome].sort(key=lambda l: l.get_validade())

        
        if grupos:
            for nome in sorted(grupos.keys()):
                print(f"\n{nome}")
                print(f"  {'Qtd':<5} | Validade")
                print("  " + "-" * 20)
                for lote in grupos[nome]:
                    validade = Relatorios._formatar_data(lote.get_validade())
                    print(f"  {lote.get_quantidade():<5} | {validade}")
        else:
            print("\nNenhum produto disponível no estoque.")

        #vencidos
        if vencidos:
            vencidos.sort(key=lambda l: (l.get_nome(), l.get_validade()))
            print(f"\n--- VENCIDOS ---")
            print(f"{'Produto':<20} | {'Qtd':<5} | Venceu em")
            print("-" * 42)
            for lote in vencidos:
                validade = Relatorios._formatar_data(lote.get_validade())
                print(f"{lote.get_nome():<20} | {lote.get_quantidade():<5} | {validade}")

        print("\n==========================================\n")