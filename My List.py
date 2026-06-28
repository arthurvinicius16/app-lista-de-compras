import tkinter as tk
from tkinter import ttk, messagebox
import json
import unicodedata
import customtkinter as ctk  # Importa o CustomTkinter

# -------------------------------------------------------------------------
# FONTES DE INSPIRAÇÃO E RECURSOS UTILIZADOS:
# Código Base de Interface: Adaptado de repositórios públicos do GitHub.
# Créditos: https://github.com/Mehnaz2004/Tkinter-ShoppingList.git
# Co-pilotagem e Mentoria de Desenvolvimento: Utilização de IA (Gemini e ChatGPT)
# para validação de dados, tratamento de exceções, testes de usabilidade e interface moderna.
# -------------------------------------------------------------------------

# Configurações visuais globais do CustomTkinter
ctk.set_appearance_mode("System")  # Detecta automaticamente Modo Escuro/Claro do PC
ctk.set_default_color_theme("blue")  # Tema de cor dos botões (pode ser "blue", "green" ou "dark-blue")

# Variáveis globais
lista_compras = []  # Inicializa uma lista de compras vazia
entrada_item = None
entrada_quantidade = None
entrada_valor = None
caixa_lista = None
texto_total = None


# Função para Salvar a Lista em Json
def salvar_lista():
    with open('lista.json', 'w') as file:
        json.dump(lista_compras, file, indent=4)


# Função para Carregar a Lista Json
def carregar_lista():
    global lista_compras
    try:
        with open('lista.json', 'r') as file:
            lista_compras = json.load(file)
        exibir_lista()
        calcular_total()
    except FileNotFoundError:
        pass


# Função para tornar a palavra inserida uma string sem espaços desnecessários, sem acento e totalmente minúscula
def normalizar(texto):
    texto = texto.strip().lower().replace(" ", "")
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto


# Funções Auxiliares de Adicionar
def ir_quantidade(event):
    entrada_quantidade.focus_set()


def ir_valor(event):
    entrada_valor.focus_set()


# Auxiliar para finalizar funções
def finalizar():
    exibir_lista()
    salvar_lista()
    calcular_total()
    entrada_item.delete(0, "end")
    entrada_quantidade.delete(0, "end")
    entrada_valor.delete(0, "end")


# Função de Exibir/Atualizar a Lista
def exibir_lista():
    global caixa_lista
    for item in caixa_lista.get_children():
        caixa_lista.delete(item)
    for item in lista_compras:
        if item['comprado']:
            status = "✅"
        else:
            status = "❌"
        id_item = normalizar(item['nome'])
        caixa_lista.insert("", tk.END, iid=id_item,
                           values=(status, item['nome'], item['quantidade'], f"R${item['valor']:.2f}"))


# Função para Acrescentar Itens
def adicionar_item(event=None):
    global entrada_item, entrada_quantidade, entrada_valor
    nome_digitado = entrada_item.get().strip()
    quantidade = entrada_quantidade.get().strip()
    valor = entrada_valor.get().strip().replace(",", ".")

    if not nome_digitado:
        messagebox.showerror("Erro", "Insira o nome do Item.")
        entrada_item.focus_set()
        return
    if quantidade == "":
        quantidade = 1
    else:
        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro")
            entrada_quantidade.focus_set()
            return
    if quantidade <= 0:
        messagebox.showerror("Erro", "Insira uma quantidade válida (maior que zero)")
        entrada_quantidade.focus_set()
        return

    valor_foi_digitado = False
    if valor:
        try:
            valor = float(valor)
            if valor < 0:
                messagebox.showerror("Erro", "Somente números positivos em 'Valor'")
                entrada_valor.focus_set()
                return
            valor_foi_digitado = True
        except ValueError:
            messagebox.showerror("Erro", "Insira somente números em 'Valor'")
            entrada_valor.focus_set()
            return
    else:
        valor = 0.0

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
    global lista_compras
    selecao = caixa_lista.selection()
    if selecao:
        ID = selecao[0]
        lista_aux = []
        prox_id = caixa_lista.next(ID)
        anterior_id = caixa_lista.prev(ID)
        if prox_id:
            subs = prox_id
        else:
            subs = anterior_id
        for item in lista_compras:
            if ID != normalizar(item['nome']):
                lista_aux.append(item)
        lista_compras = lista_aux
        finalizar()
        if not subs:
            return
        caixa_lista.selection_set(subs)
        caixa_lista.focus(subs)
        caixa_lista.focus_set()
    else:
        messagebox.showerror("Erro", "Selecione um item para removê-lo")


# Função para Limpar a Lista
def limpar_lista():
    if len(lista_compras) == 0:
        messagebox.showerror("Erro", "A lista já está vazia")
        return
    escolha = messagebox.askyesno("Escolha", "Deseja limpar toda a lista?")
    if escolha:
        lista_compras.clear()
        finalizar()


# Função para mudar o emoji de comprado/não comprado
def alternar_status(event=None):
    selecao = caixa_lista.selection()
    if selecao:
        ID = selecao[0]
        indice = caixa_lista.index(ID)
        lista_compras[indice]['comprado'] = not lista_compras[indice]['comprado']
        finalizar()
        linhas = caixa_lista.get_children()
        id_foco = linhas[indice]
        caixa_lista.selection_set(id_foco)
        caixa_lista.focus(id_foco)
        caixa_lista.focus_set()
    else:
        messagebox.showerror("Erro", "Selecione um item para alterar o status")


# Função para Calcular Totais
def calcular_total():
    soma_valor = 0.0
    soma_itens = 0
    soma_carrinho = 0.0
    for item in lista_compras:
        soma_valor += item['quantidade'] * item['valor']
        soma_itens += item['quantidade']
        if item['comprado']:
            soma_carrinho += item['quantidade'] * item['valor']
    texto_total.set(f"Itens: {soma_itens} un. | Total: R${soma_valor:.2f} | No Carrinho: R${soma_carrinho:.2f}")


# Função principal da interface
def main():
    global entrada_item, entrada_quantidade, caixa_lista, entrada_valor, texto_total

    # Janela principal usando CTk
    janela = ctk.CTk()
    janela.geometry("550x650")
    janela.minsize(480, 580)
    janela.title("Lista de Compras")

    texto_total = tk.StringVar()
    texto_total.set("Itens: 0 un | Total: R$0.00 | No Carrinho: R$0.00")

    # Título principal da interface
    frame_titulo = ctk.CTkFrame(janela, fg_color="transparent")
    frame_titulo.pack(padx=10, pady=10)
    label_titulo = ctk.CTkLabel(frame_titulo, text="LISTA DE COMPRAS", font=("Helvetica", 24, "bold"))
    label_titulo.pack()

    # Área dos campos de entrada e botões
    frame_conteudo = ctk.CTkFrame(janela)
    frame_conteudo.pack(padx=15, pady=15, fill="both", expand=True)
    frame_conteudo.grid_columnconfigure(1, weight=1)
    frame_conteudo.grid_rowconfigure(7, weight=1)

    # Campo: Item
    label_item = ctk.CTkLabel(frame_conteudo, text="Item:")
    label_item.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entrada_item = ctk.CTkEntry(frame_conteudo, width=200, placeholder_text="Ex:Argamassa")
    entrada_item.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    # Campo: Quantidade
    label_quantidade = ctk.CTkLabel(frame_conteudo, text="Quantidade:")
    label_quantidade.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entrada_quantidade = ctk.CTkEntry(frame_conteudo, width=200, placeholder_text="(Opcional)")
    entrada_quantidade.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Campo: Preço
    label_valor = ctk.CTkLabel(frame_conteudo, text="Preço (R$):")
    label_valor.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entrada_valor = ctk.CTkEntry(frame_conteudo, width=200, placeholder_text="(Opcional)")
    entrada_valor.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Botão: Adicionar (Adicionado cantos arredondados padrão e cor diferenciada)
    botao_adicionar = ctk.CTkButton(frame_conteudo, text="Adicionar Item", command=adicionar_item, fg_color="#2ecc71",
                                    hover_color="#27ae60")
    botao_adicionar.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # Botão: Remover
    botao_remover = ctk.CTkButton(frame_conteudo, text="Remover Item", command=remover_item, fg_color="#e74c3c",
                                  hover_color="#c0392b")
    botao_remover.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # Botão: Limpar
    botao_limpar = ctk.CTkButton(frame_conteudo, text="Limpar Lista", command=limpar_lista, fg_color="#f39c12",
                                 hover_color="#d35400")
    botao_limpar.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # Botão: Alternar Status
    botao_status = ctk.CTkButton(frame_conteudo, text="Marcar | Desmarcar", command=alternar_status)
    botao_status.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # Configuração de estilo para o Treeview se adaptar melhor visualmente
    estilo_tabela = ttk.Style()
    estilo_tabela.theme_use("clam")
    estilo_tabela.configure("Treeview", rowheight=25)

    # Listbox/Treeview (Mantido ttk.Treeview pois o ctk não possui tabela nativa)
    caixa_lista = ttk.Treeview(frame_conteudo, columns=("status", "nome", "quantidade", "valor"), show="headings")
    caixa_lista.grid(row=7, column=0, columnspan=2, padx=(10, 0), pady=10, sticky="nsew")

    caixa_lista.heading("status", text="Status", anchor='center')
    caixa_lista.heading("nome", text="Nome", anchor='w')
    caixa_lista.heading("quantidade", text="Qtd", anchor='center')
    caixa_lista.heading("valor", text="Valor", anchor='center')

    caixa_lista.column("status", width=60, anchor='center', stretch=False)
    caixa_lista.column("nome", width=190, anchor='w')
    caixa_lista.column("quantidade", width=60, anchor='center')
    caixa_lista.column("valor", width=90, anchor='center')

    # Scrollbar
    barra_rolagem = ttk.Scrollbar(frame_conteudo, orient=tk.VERTICAL, command=caixa_lista.yview)
    barra_rolagem.grid(row=7, column=2, padx=(0, 10), pady=10, sticky="ns")
    caixa_lista.configure(yscrollcommand=barra_rolagem.set)

    # Atalhos e Eventos
    caixa_lista.bind("<Delete>", remover_item)
    caixa_lista.bind("<Double-1>", alternar_status)
    entrada_item.bind("<Return>", ir_quantidade)
    entrada_quantidade.bind("<Return>", ir_valor)
    entrada_valor.bind("<Return>", adicionar_item)
    janela.bind("<Shift-Delete>", limpar_lista)

    # Rodapé da Quantidade e Preço Total
    label_rodape = ctk.CTkLabel(frame_conteudo, textvariable=texto_total, font=("Helvetica", 17, "bold"))
    label_rodape.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    carregar_lista()
    janela.mainloop()


# Executa o programa
if __name__ == "__main__":
    main()