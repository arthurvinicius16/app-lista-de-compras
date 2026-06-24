import tkinter as tk
import json
from tkinter import messagebox
import unicodedata

# Variáveis globais
lista_compras = [] # Inicializa uma lista de compras vazia
entrada_item = None
entrada_quantidade = None
entrada_valor = None
caixa_lista = None

#Função para Salvar a Lista em Json
def salvar_lista():
    with open('lista.json', 'w') as file:
        json.dump(lista_compras, file, indent=4)

#Função para Carregar a Lista Json
def carregar_lista():
    global lista_compras
    try:
        with open('lista.json', 'r') as file:
            lista_compras = json.load(file)
        exibir_lista()
        calcular_total()
    except FileNotFoundError:
        pass
#Função para tornar a palavra inserida uma string sem espaços desnecessários, sem acento e totalmente minúscula
def normalizar(texto):
    texto=texto.strip().lower().replace(" ", "")
    texto=unicodedata.normalize("NFKD", texto)
    texto=texto.encode("ascii", "ignore").decode("utf-8")
    return texto

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
    nome_digitado=entrada_item.get() #ele recebe a string da caixa de texto (.get)
    quantidade=entrada_quantidade.get()
    if nome_digitado and quantidade>0:
        try:
            quantidade=int(quantidade)
            item_busca=normalizar(nome_digitado)
            valor = entrada_valor.get().replace(",", ".")
            if valor:
                valor=float(valor)
            else:
                valor=0.0
            for item in lista_compras:
                item_existe=normalizar(item['nome'])
                if item_existe == item_busca:
                    item['quantidade']+=quantidade
                    item['valor']=valor
                    exibir_lista()
                    salvar_lista()
                    calcular_total()
                    entrada_item.delete(0, tk.END)
                    entrada_quantidade.delete(0, tk.END)
                    entrada_valor.delete(0, tk.END)
                    messagebox.showinfo("Sucesso", f"A quantidade e o preço de {item['nome']} foram atualizados")
                    return
            novo_item = {'nome': nome_digitado, 'quantidade': quantidade, 'valor': valor, 'comprado': False}
            lista_compras.append(novo_item)
            exibir_lista()
            salvar_lista()
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
       salvar_lista()
       calcular_total()
       messagebox.showinfo("Sucesso", f"{item_removido['nome']} foi removido da lista")

    else:
        messagebox.showerror("Erro", "Selecione um item para removê-lo")

#Função para mudar o emoji de não comprado para comprado e vice-versa
def alternar_status():
    selecao = caixa_lista.curselection()
    if selecao:
        indice=selecao[0]
        lista_compras[indice]['comprado']=not lista_compras[indice]['comprado']
        exibir_lista()
        salvar_lista()
        calcular_total()
        messagebox.showinfo("Sucesso!", f"Status de {lista_compras[indice]['nome']} foi alterado.")
    else:
        messagebox.showerror("Erro", "Selecione um item para alterar o status")

# Função para Calcular a Quantidade de Itens e o Preço Total
def calcular_total():
    soma_valor=0.0
    soma_itens=0
    soma_carrinho=0.0
    for item in lista_compras:
        soma_valor+=item['quantidade']*item['valor']
        soma_itens+=item['quantidade']
        if item['comprado']:
            soma_carrinho+=item['quantidade']*item['valor']
    texto_total.set(f"Itens: {soma_itens}un | Total: R${soma_valor:.2f} | No Carrinho: R${soma_carrinho:.2f} ")


# Função principal que constrói a interface
def main():
    global entrada_item, entrada_quantidade, caixa_lista, entrada_valor, texto_total
    janela = tk.Tk()
    janela.title("Lista de Compras")
    texto_total = tk.StringVar()
    texto_total.set("Itens: 0 un | Total: R$0.00 | No Carrinho: R$0.00")

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

    # Botão: Alternar Status
    botao_status = tk.Button(
        frame_conteudo, text="Marcar | Desmarcar", command=alternar_status
    )
    botao_status.grid(
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
    carregar_lista()
    janela.mainloop()


# Executa o programa
if __name__ == "__main__":
    main()