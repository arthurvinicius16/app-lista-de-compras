import tkinter as tk
import json
from tkinter import messagebox

# Variáveis globais
lista_compras = [] # Inicializa uma lista de compras vazia
entrada_item = None
entrada_quantidade = None
entrada_valor = None
caixa_lista = None


# Função de Exibir/Atualizar a Lista
def exibir_lista():
    global caixa_lista
    caixa_lista.delete(0, tk.END)
    for item in lista_compras:
        if item['comprado']==True:
            status="✅"
        else:
            status="❌"
        texto= f"{status} {item['nome']} | {item['quantidade']} un | R${item['valor']:.2f}"
        caixa_lista.insert(tk.END, texto)

# Função para Acrescentar Itens

def adicionar_item():
    global entrada_item, entrada_quantidade, entrada_valor
    nome_digitado=entrada_item.get().strip() #ele recebe a string da caixa de texto (.get) e remove espaços desnecessários, como no fim e início (.strip)
    quantidade=entrada_quantidade.get()
    valor=entrada_valor.get()
    if nome_digitado and quantidade and valor:
        try:
            quantidade=int(quantidade)
            valor=float(valor)
            novo_item={'nome':nome_digitado,'quantidade':quantidade,'valor':valor, 'comprado':False}
            lista_compras.append(novo_item)
            exibir_lista()
            calcular_total()
            entrada_item.delete(0, tk.END)
            entrada_quantidade.delete(0, tk.END)
            entrada_valor.delete(0, tk.END)
            messagebox.showinfo("Sucesso",f"O item {nome_digitado} foi adicionado com sucesso.")
        except ValueError:
            messagebox.showerror("Erro","Insira caracteres válidos nos campos Quantidade e Preço (somente números)")
    else:
        messagebox.showerror("Erro","Por favor, preencha todos os campos (Item, Quantidade e Preço)")

# Função de Remover Item

def remover_item():
    selecao = caixa_lista.curselection()
    if selecao:
       indice=selecao[0]
       item_removido=lista_compras.pop(indice)
       exibir_lista()
       calcular_total()
       messagebox.showinfo("Sucesso", f"{item_removido['nome']} foi removido da lista")

    else:
        messagebox.showerror("Erro", "Selecione um item para removê-lo")


# Função para Calcular a Quantidade de Itens e o Preço Total
def calcular_total():
    soma_valor=0.0
    soma_itens=0
    for item in lista_compras:
        soma_valor+=item['quantidade']*item['valor']
        soma_itens+=item['quantidade']
    texto_total.set(f"Itens: {soma_itens}un | Preço Total: R${soma_valor:.2f}")


# Função principal que constrói a interface
def main():
    global entrada_item, entrada_quantidade, caixa_lista, entrada_valor, texto_total
    janela = tk.Tk()
    janela.title("Lista de Compras")
    texto_total = tk.StringVar()
    texto_total.set("Itens: 0 un | Preço Total: R$0.00")

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

    #Campo: Preço
    label_valor = tk.Label(frame_conteudo, text="Preço")
    label_valor.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_valor = tk.Entry(frame_conteudo)
    entrada_valor.grid(row=2, column=1, padx=5, pady=5)

    # Botão: Adicionar
    botao_adicionar = tk.Button(
        frame_conteudo, text="Adicionar Item", command=adicionar_item
    )
    botao_adicionar.grid(
        row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we"
    )

    # Botão: Remover
    botao_remover = tk.Button(
        frame_conteudo, text="Remover Item", command=remover_item
    )
    botao_remover.grid(
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

    #Rodapé da Quantidade e Preço Total
    label_rodape = tk.Label(frame_conteudo, textvariable=texto_total, font=("Helvetica", 10, "bold"))
    label_rodape.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    janela.mainloop()


# Executa o programa
if __name__ == "__main__":
    main()