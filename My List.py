import tkinter as tk
from tkinter import ttk
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

#Funções Auxiliares de Adicionar
def ir_quantidade(event):
    entrada_quantidade.focus_set()
def ir_valor(event):
    entrada_valor.focus_set()

#Auxiliar para finalizar funções
def finalizar():
    exibir_lista()
    salvar_lista()
    calcular_total()
    entrada_item.delete(0, tk.END)
    entrada_quantidade.delete(0, tk.END)
    entrada_valor.delete(0, tk.END)

# Função de Exibir/Atualizar a Lista
def exibir_lista():
    global caixa_lista
    for item in caixa_lista.get_children():
        caixa_lista.delete(item)
    for item in lista_compras:
        if item['comprado']==True:
            status="✅"
        else:
            status="❌"
        caixa_lista.insert("", tk.END, values=(status, item['nome'], item['quantidade'], f"R${item['valor']:.2f}"))

# Função para Acrescentar Itens

def adicionar_item(event=None):
    global entrada_item, entrada_quantidade, entrada_valor
    nome_digitado=entrada_item.get().strip() #ele recebe a string da caixa de texto (.get)
    quantidade=entrada_quantidade.get().strip()
    valor = entrada_valor.get().strip().replace(",", ".")
    if not nome_digitado:
        messagebox.showerror("Erro", "Insira o nome do Item.")
        return
    if quantidade == "":
        quantidade=1
    else:
        try:
            quantidade=int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro")
            return
    if quantidade<=0:
        messagebox.showerror("Erro", "Insira uma quantidade válida (maior que zero)")
        return
    valor_foi_digitado = False
    if valor:
        try:
            valor=float(valor)
            if valor<0:
                messagebox.showerror("Erro", "Somente números positivos em 'Valor'")
                return
            valor_foi_digitado=True
        except ValueError:
            messagebox.showerror("Erro", "Insira somente números em 'Valor'")
            return
    else:
        valor=0.0
    item_busca = normalizar(nome_digitado)
    for item in lista_compras:
        item_existe = normalizar(item['nome'])
        if item_existe == item_busca:
            item['quantidade'] += quantidade
            if valor_foi_digitado:
                item['valor'] = valor
            finalizar()
            entrada_item.focus_set()
            return
    novo_item = {'nome': nome_digitado, 'quantidade': quantidade, 'valor': valor, 'comprado': False}
    lista_compras.append(novo_item)
    finalizar()
    entrada_item.focus_set()

# Função de Remover Item

def remover_item(event=None):
    selecao = caixa_lista.selection()
    if selecao:
       ID=selecao[0]
       indice=caixa_lista.index(ID)
       prox_id=caixa_lista.next(ID)
       anterior_id=caixa_lista.prev(ID)
       if prox_id:
           subs=prox_id
       else:
           subs=anterior_id
       item_removido=lista_compras.pop(indice)
       finalizar()
       linhas=caixa_lista.get_children()
       if linhas:
           if indice>=len(linhas):
               indice=len(linhas)-1
           id_foco=linhas[indice]
           caixa_lista.selection_set(id_foco)
           caixa_lista.focus(id_foco)
           caixa_lista.focus_set()
    else:
        messagebox.showerror("Erro", "Selecione um item para removê-lo")


# Função para Limpar a Lista
def limpar_lista():
    #Verifica se a lista já está vazia antes de perguntar
    if len(lista_compras) == 0:
        messagebox.showerror("Erro", "A lista já está vazia")
        return

   #Se a lista tiver itens, faz a pergunta ao usuário
    escolha = messagebox.askyesno("Escolha", "Deseja limpar toda a lista?")
    if escolha:
        lista_compras.clear()
        finalizar()

#Função para mudar o emoji de não comprado para comprado e vice-versa
def alternar_status():
    selecao = caixa_lista.selection()
    if selecao:
        ID=selecao[0]
        indice=caixa_lista.index(ID)
        lista_compras[indice]['comprado']=not lista_compras[indice]['comprado']
        finalizar()
        linhas=caixa_lista.get_children()
        id_foco=linhas[indice]
        caixa_lista.selection_set(id_foco)
        caixa_lista.focus(id_foco)
        caixa_lista.focus_set()
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
    texto_total.set(f"Itens: {soma_itens} un. | Total: R${soma_valor:.2f} | No Carrinho: R${soma_carrinho:.2f} ")


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
    label_titulo = tk.Label(frame_titulo, text="LISTA DE COMPRAS", font=("Helvetica", 24, "bold"))
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
    botao_adicionar = tk.Button(frame_conteudo, text="Adicionar Item", command=adicionar_item)
    botao_adicionar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Botão: Remover
    botao_remover = tk.Button(frame_conteudo, text="Remover Item", command=remover_item)
    botao_remover.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    #Botão: Limpar
    botao_limpar = tk.Button(frame_conteudo, text="Limpar Lista", command=limpar_lista)
    botao_limpar.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Botão: Alternar Status
    botao_status = tk.Button(frame_conteudo, text="Marcar | Desmarcar", command=alternar_status)
    botao_status.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Listbox: Onde a lista aparece na tela
    caixa_lista = ttk.Treeview(frame_conteudo, columns=("status","nome", "quantidade", "valor"), show="headings")
    caixa_lista.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    caixa_lista.heading("status", text="Status", anchor='center')
    caixa_lista.heading("nome", text="Nome", anchor='w')
    caixa_lista.heading("quantidade", text="Qtd", anchor='center')
    caixa_lista.heading("valor", text="Valor", anchor='center')
    caixa_lista.column("status", width=50, anchor='center')
    caixa_lista.column("nome", width=200, anchor='w')
    caixa_lista.column("quantidade", width=60, anchor='center')
    caixa_lista.column("valor", width=100, anchor='center')
    caixa_lista.bind("<Delete>", remover_item)
    entrada_item.bind("<Return>", ir_quantidade)
    entrada_quantidade.bind("<Return>", ir_valor)
    entrada_valor.bind("<Return>", adicionar_item)


    #Rodapé da Quantidade e Preço Total
    label_rodape = tk.Label(frame_conteudo, textvariable=texto_total, font=("Helvetica", 10, "bold"))
    label_rodape.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    carregar_lista()
    janela.mainloop()


# Executa o programa
if __name__ == "__main__":
    main()