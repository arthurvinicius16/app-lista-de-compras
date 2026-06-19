import tkinter as tk
import json
from tkinter import messagebox

# Variáveis globais
lista_compras = [] # Inicializa uma lista de compras vazia
entrada_item = None
entrada_quantidade = None
caixa_lista = None


# Função para exibir a lista de compras na tela
def exibir_lista():
    caixa_lista.delete(0, tk.END)
    for item, quantidade in lista_compras.items():
        caixa_lista.insert(
            tk.END, f"- {item} (Quantidade: {str(quantidade)})"
        )


# Função para adicionar un item à lista de compras
def adicionar_item():
    global entrada_item, entrada_quantidade
    item = entrada_item.get()
    quantidade = entrada_quantidade.get()

    if item and quantidade:
        try:
            quantidade = int(quantidade)
            if item in lista_compras:
                lista_compras[item] += quantidade
            else:
                lista_compras[item] = quantidade

            entrada_item.delete(0, tk.END)
            entrada_quantidade.delete(0, tk.END)
            exibir_lista()
            messagebox.showinfo(
                "Sucesso",
                f"{str(quantidade)}x '{item}' adicionado(s) com sucesso à sua lista.",
            )
        except ValueError:
            messagebox.showerror(
                "Erro", "Por favor, insira um número válido para a quantidade."
            )
    else:
        messagebox.showerror(
            "Erro", "Por favor, preencha tanto o item quanto a quantidade."
        )


# Função para remover um item da lista de compras

    else:def remover_item():
    global entrada_item
    item_para_remover = None

    #1.Primeiro,verifica se o usuário seleciounou  item clicando na listbox
    selecao = caixa_lista.curselection()
    if selecao:
        texto_linha = caixa_lista.get(selecao[0])
        #Extrai o nome do item limpando o formato "- Item (Quantidade: X)"
        item_para_remover = texto_linha.split("(")[0].replace("-","").strip()
    else:
        # 2. Se não clicou na lista,pega o que foi digitado no campo de texto
        item_para_remover = entrada_item.get().strip()

    # Execulta a remoção se o item for válido e existir
    if item_para_remover in lista_compras:
        del lista_compras[item_para_remover]
        entrada_item.delete(0, tk.END)
        exibir_lista()
        messagebox.showinfo(
            "Sucesso",f"'{item_para_remover}' foi removido da sua lista de compras."
        )
        messagebox.showerror(
            "Error",
            "Selecione um item na lista visual ou digite o nome exato para remover."
        )



# Função para calcular o total de todos os itens somados
def calcular_total():
    total = sum(lista_compras.values())
    messagebox.showinfo(
        "Total de Itens", f"Quantidade total de itens na lista: {str(total)}"
    )


# Função principal que constrói a interface
def main():
    global entrada_item, entrada_quantidade, caixa_lista
    janela = tk.Tk()
    janela.title("Lista de Compras")

    # Título principal da interface
    frame_titulo = tk.Frame(janela)
    frame_titulo.pack(padx=10, pady=10)
    label_titulo = tk.Label(
        frame_titulo, text="LISTA DE COMPRAS", font=("Helvetica", 24, "bold")
    )
    label_titulo.pack()

    # Área dos campos de entrada e botões
    frame_conteudo = tk.Frame(janela)
    frame_conteudo.pack(padx=10, pady=10)

    # Campo: Item
    label_item = tk.Label(frame_conteudo, text="Item:")
    label_item.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entrada_item = tk.Entry(frame_conteudo)
    entrada_item.grid(row=0, column=1, padx=5, pady=5)

    # Campo: Quantidade
    label_quantidade = tk.Label(frame_conteudo, text="Quantidade:")
    label_quantidade.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_quantidade = tk.Entry(frame_conteudo)
    entrada_quantidade.grid(row=1, column=1, padx=5, pady=5)

    # Botão: Adicionar
    botao_adicionar = tk.Button(
        frame_conteudo, text="Adicionar Item", command=adicionar_item
    )
    botao_adicionar.grid(
        row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we"
    )

    # Botão: Remover
    botao_remover = tk.Button(
        frame_conteudo, text="Remover Item", command=remover_item
    )
    botao_remover.grid(
        row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we"
    )

    # Botão: Atualizar/Exibir
    botao_exibir = tk.Button(
        frame_conteudo, text="Atualizar Lista", command=exibir_lista
    )
    botao_exibir.grid(
        row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we"
    )

    # Botão: Calcular Total
    botao_calcular = tk.Button(
        frame_conteudo, text="Calcular Total Geral", command=calcular_total
    )
    botao_calcular.grid(
        row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we"
    )

    # Listbox: Onde a lista aparece na tela
    caixa_lista = tk.Listbox(frame_conteudo)
    caixa_lista.grid(
        row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
    )

    janela.mainloop()


# Executa o programa
if __name__ == "__main__":
    main()