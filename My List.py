import tkinter as tk
from tkinter import ttk, messagebox
import json  # Importa a biblioteca de persistência de arquivos do programa, num tipo de arquivo .json nativo do python
import unicodedata  # Importa a biblioteca que retira qualquer acentuação ou símbolos de strings
import customtkinter as ctk  # Importa o CustomTkinter para criar uma interface visual moderna

# -------------------------------------------------------------------------
# FONTES DE INSPIRAÇÃO E RECURSOS UTILIZADOS:
# Código Base de Interface: Adaptado de repositórios públicos do GitHub.
# Créditos: https://github.com/Mehnaz2004/Tkinter-ShoppingList.git
# Mentoria de Desenvolvimento: Utilização de IA (Gemini e ChatGPT)
# para validação de dados, tratamento de exceções, testes de usabilidade e interface moderna.
# -------------------------------------------------------------------------

# Configurações visuais globais do CustomTkinter
ctk.set_appearance_mode("System")  # Detecta automaticamente Modo Escuro/Claro do PC
ctk.set_default_color_theme("blue")  # Tema de cor dos botões (pode ser "blue", "green" ou "dark-blue")

# Variáveis globais que guardam o estado da aplicação e os componentes da interface
lista_compras = []  # Inicializa uma lista de compras vazia na memória
entrada_item = None  # Guardará o campo de texto onde o usuário digita o nome do item
entrada_quantidade = None  # Guardará o campo de texto da quantidade do item
entrada_valor = None  # Guardará o campo de texto do preço/valor do item
caixa_lista = None  # Guardará o componente visual da tabela (Treeview) onde os itens aparecem
texto_total = None  # Guardará a variável de texto que atualiza o rodapé de valores acumulados
item_editar = None  # Guarda temporariamente a chave do item que está sendo editado no momento
botao_adicionar = None  # Guardará o botão principal para podermos alternar o texto dele (Adicionar / Salvar)


# Função para Salvar a Lista em um arquivo JSON
def salvar_lista():
    # Abre o arquivo 'lista.json' para escrita ('w'), garantindo a codificação UTF-8 para aceitar caracteres especiais
    with open('lista.json', 'w', encoding='utf-8') as file:
        # Converte a lista de compras em formato JSON grava no arquivo
        json.dump(lista_compras, file, indent=4)


# Função para Carregar a Lista do arquivo JSON quando o programa inicia
def carregar_lista():
    global lista_compras
    try:
        # Tenta abrir o arquivo 'lista.json' em modo de leitura ('r')
        with open('lista.json', 'r', encoding='utf-8') as file:
            lista_compras = json.load(file)  # Converte o conteúdo do arquivo JSON de volta para a lista do Python
        exibir_lista()  # Atualiza a tabela na tela com os dados carregados
        calcular_total()  # Recalcula os valores totais da lista
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver corrompido, inicia com uma lista vazia sem quebrar o programa
        lista_compras = []


# Função para tornar a palavra inserida uma string sem espaços desnecessários, sem acento e totalmente minúscula.
# Isso serve para evitar que o usuário adicione o mesmo item duas vezes por digitar de formas diferentes (ex: "Cimento" e "cimento").
def normalizar(texto):
    texto = texto.strip().lower().replace(" ", "")  # Remove espaços nas pontas, deixa em minúsculo e tira espaços internos
    texto = unicodedata.normalize("NFKD", texto)  # Separa caracteres de seus acentos (ex: "á" vira "a" + "´")
    texto = texto.encode("ascii", "ignore").decode("utf-8")  # Remove os caracteres de acento que foram separados
    return texto


# Funções Auxiliares de Navegação no Teclado
def ir_quantidade(event):
    entrada_quantidade.focus_set()  # Move o cursor de digitação para o campo de Quantidade ao apertar Enter no campo de Item


def ir_valor(event):
    entrada_valor.focus_set()  # Move o cursor de digitação para o campo de Valor ao apertar Enter no campo de Quantidade


# Auxiliar para finalizar operações comuns (como adicionar ou editar)
def finalizar():
    exibir_lista()  # Atualiza a exibição da tabela visual
    salvar_lista()  # Salva as alterações no arquivo JSON local
    calcular_total()  # Atualiza as somas de valores no rodapé
    # Limpa todos os campos de entrada de texto para as próximas digitações
    entrada_item.delete(0, tk.END)
    entrada_quantidade.delete(0, tk.END)
    entrada_valor.delete(0, tk.END)


# Função de Exibir/Atualizar a Tabela de Itens na Interface
def exibir_lista():
    global caixa_lista
    # Limpa todos os itens que estão atualmente sendo mostrados na tabela para reconstruí-la sem repetir
    for item in caixa_lista.get_children():
        caixa_lista.delete(item)
    # Percorre cada dicionário de item contido na lista de compras
    for item in lista_compras:
        # Define o emoji indicador se o item já foi comprado ou não
        if item['comprado']:
            status = "✅"
        else:
            status = "❌"
        id_item = normalizar(
            item['nome'])  # Gera um identificador único textual para a linha da tabela baseado no nome normalizado (ex: IID=feijao)
        # Insere a linha com os respectivos valores de status, nome, quantidade e valor na tabela visual
        caixa_lista.insert("", tk.END, iid=id_item,
                           values=(status, item['nome'], item['quantidade'], f"R${item['valor']:.2f}"))


# Função para Acrescentar ou Atualizar Itens
def adicionar_item(event=None):
    global entrada_item, entrada_quantidade, entrada_valor, item_editar, botao_adicionar
    # Obtém e limpa os valores digitados nos campos de entrada
    nome_digitado = entrada_item.get().strip()
    quantidade = entrada_quantidade.get().strip()
    valor = entrada_valor.get().strip().replace(",", ".")  # Substitui vírgulas por pontos para o Python aceitar como float
    # Validação: O nome do item é obrigatório
    if not nome_digitado:
        messagebox.showerror("Erro", "Insira o nome do Item.")
        entrada_item.focus_set()
        return
    # Validação da quantidade
    if quantidade == "":
        quantidade = 1  # Se o campo quantidade estiver vazio, define o padrão de 1 unidade
    else:
        try:
            quantidade = int(quantidade)  # Tenta converter o texto para número inteiro
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro")
            entrada_quantidade.focus_set()
            return
    # Validação de quantidade negativa ou zero
    if quantidade <= 0:
        messagebox.showerror("Erro", "Insira uma quantidade válida (maior que zero)")
        entrada_quantidade.focus_set()
        return
    # Validação do valor do item
    valor_foi_digitado = False
    if valor:
        try:
            valor = float(valor)  # Tenta converter o texto para número decimal (float)
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
        valor = 0.0  # Se não digitar valor, assume R$0.00 como padrão
    # Caso de Edição: Se estivermos editando um item existente na lista
    if item_editar is not None:
        for item in lista_compras:
            # Verifica se o novo nome digitado já pertence a outro item diferente da lista para evitar duplicidade
            if normalizar(nome_digitado) == normalizar(item['nome']) and normalizar(item['nome']) != item_editar:
                messagebox.showerror("Erro", f"{item['nome']} já está na lista")
                return
            # Localiza o item que está sendo editado na lista original e atualiza seus dados
            if normalizar(item['nome']) == item_editar:
                item['nome'] = nome_digitado
                item['quantidade'] = quantidade
                item['valor'] = valor
                break
        # Retorna o botão visual ao seu estado padrão verde "Adicionar Item"
        botao_adicionar.configure(text="Adicionar Item", fg_color="#2ecc71", hover_color="#27ae60")
        item_editar = None  # Reseta a variável de controle de edição
        finalizar()
        entrada_item.focus_set()
        return
    # Caso de Adição: Verifica se o item digitado já existe na lista para acumular quantidades
    item_busca = normalizar(nome_digitado)
    for item in lista_compras:
        item_existe = normalizar(item['nome'])
        if item_existe == item_busca:
            item['quantidade'] += quantidade  # Soma a nova quantidade à quantidade existente
            if valor_foi_digitado:
                item['valor'] = valor  # Atualiza o valor caso um novo valor tenha sido digitado expressamente
            finalizar()
            entrada_item.focus_set()
            return
    # Caso de Item Totalmente Novo: Adiciona um novo dicionário à lista de compras
    novo_item = {'nome': nome_digitado, 'quantidade': quantidade, 'valor': valor, 'comprado': False}
    lista_compras.append(novo_item)
    finalizar()
    entrada_item.focus_set()


# Função de Remover o Item Selecionado da Lista
def remover_item(event=None):
    global lista_compras, item_editar, botao_adicionar
    selecao = caixa_lista.selection()  # Obtém a linha que o usuário clicou na tabela visual
    if selecao:
        ID = selecao[0]  # Identifica o ID correspondente ao item selecionado
        lista_aux = []  # Lista temporária para reconstruir a lista original sem o item removido
        # Lógica para manter a seleção visual da tabela em um item vizinho após a exclusão
        prox_id = caixa_lista.next(ID)
        anterior_id = caixa_lista.prev(ID)
        if prox_id:
            subs = prox_id
        else:
            subs = anterior_id
        # Filtra a lista mantendo apenas os itens cujo ID normalizado seja diferente do selecionado
        for item in lista_compras:
            if ID != normalizar(item['nome']):
                lista_aux.append(item)
        lista_compras = lista_aux  # Substitui a lista de compras oficial pela filtrada
        item_editar = None  # Cancela qualquer edição em andamento se o item for deletado
        botao_adicionar.configure(text="Adicionar Item", fg_color="#2ecc71", hover_color="#27ae60")
        finalizar()
        if not subs:
            return
        # Restabelece o foco visual na linha vizinha da tabela que sobrou
        caixa_lista.selection_set(subs)
        caixa_lista.focus(subs)
        caixa_lista.focus_set()
    else:
        messagebox.showerror("Erro", "Selecione um item para removê-lo")

# Função para Limpar Toda a Lista de Compras
def limpar_lista(event=None):
    global item_editar, botao_adicionar
    if len(lista_compras) == 0:
        messagebox.showerror("Erro", "A lista já está vazia")
        return
    # Exibe uma caixa de diálogo para confirmação do usuário (Sim/Não)
    escolha = messagebox.askyesno("Escolha", "Deseja limpar toda a lista?")
    if escolha:
        item_editar = None  # Reseta o estado de edição
        botao_adicionar.configure(text="Adicionar Item", fg_color="#2ecc71", hover_color="#27ae60")
        lista_compras.clear()  # Limpa todos os elementos do vetor na memória
        finalizar()

# Função para Editar Itens Existentes
def editar_item(event=None):
    global item_editar, botao_adicionar
    selecao = caixa_lista.selection()  # Obtém a linha selecionada na tabela
    if not selecao:
        messagebox.showerror("Erro", "Selecione um item para editar")
        return
    item_editar = selecao[0]  # Identifica o ID do item selecionado para edição
    # Procura o item correspondente dentro da nossa lista de compras
    for item in lista_compras:
        if item_editar == normalizar(item['nome']):
            # Limpa os campos de entrada e preenche-os com os dados atuais do item selecionado
            entrada_item.delete(0, tk.END)
            entrada_quantidade.delete(0, tk.END)
            entrada_valor.delete(0, tk.END)
            entrada_item.insert(0, item['nome'])
            entrada_quantidade.insert(0, str(item['quantidade']))
            entrada_valor.insert(0, f"{item['valor']:.2f}")
            # Modifica visualmente o botão principal para indicar o modo de edição (azul "Salvar Alterações")
            botao_adicionar.configure(text="Salvar Alterações", fg_color="#3498db", hover_color="#2980b9")
            entrada_item.focus_set()  # Coloca o cursor no primeiro campo de texto
            return

# Função para alternar o status do item entre Comprado (✅) e Não Comprado (❌)
def alternar_status(event=None):
    selecao = caixa_lista.selection()  # Obtém o item selecionado
    if selecao:
        ID = selecao[0]
        for item in lista_compras:
            if ID == normalizar(item['nome']):
                item['comprado'] = not item['comprado']  # Inverte o valor booleano (True vira False e vice-versa)
                finalizar()
                # Mantém o cursor visual e a seleção na mesma linha após a mudança de status
                caixa_lista.selection_set(ID)
                caixa_lista.focus(ID)
                caixa_lista.focus_set()
                return
    else:
        messagebox.showerror("Erro", "Selecione um item para alterar o status")

# Função para Calcular Totais e Atualizar as Métricas da Lista
def calcular_total():
    soma_valor = 0.0  # Soma o valor total estimado da lista inteira
    soma_itens = 0  # Soma a quantidade de unidades físicas totais de itens
    soma_carrinho = 0.0  # Soma o valor gasto apenas com os itens marcados como comprados (✅)
    for item in lista_compras:
        soma_valor += item['quantidade'] * item['valor']
        soma_itens += item['quantidade']
        if item['comprado']:
            soma_carrinho += item['quantidade'] * item['valor']
    # Atualiza dinamicamente o texto exibido no rodapé da aplicação
    texto_total.set(f"Itens: {soma_itens} un. | Total: R${soma_valor:.2f} | No Carrinho: R${soma_carrinho:.2f}")

# Função principal de construção e inicialização da interface visual
def main():
    global entrada_item, entrada_quantidade, caixa_lista, entrada_valor, texto_total, botao_adicionar

    # Cria a janela principal usando a biblioteca CustomTkinter
    janela = ctk.CTk()
    janela.geometry("550x650")  # Define o tamanho padrão inicial da janela (largura x altura)
    janela.minsize(480, 580)  # Define as dimensões mínimas para que o layout não quebre ao ser redimensionado
    janela.title("Minha Lista de Compras")  # Título exibido na barra superior do programa

    # Inicializa a variável de controle de texto que se auto-atualiza na interface
    texto_total = tk.StringVar()
    texto_total.set("Itens: 0 un | Total: R$0.00 | No Carrinho: R$0.00")

    # Frame (quadro) para o título principal da interface
    frame_titulo = ctk.CTkFrame(janela, fg_color="transparent")
    frame_titulo.pack(padx=10, pady=10)
    label_titulo = ctk.CTkLabel(frame_titulo, text="Minha Lista de Compras", font=("Segoe UI", 28, "bold"))
    label_titulo.pack()

    # Frame principal que conterá os campos de entrada de dados, os botões e a tabela de exibição
    frame_conteudo = ctk.CTkFrame(janela)
    frame_conteudo.pack(padx=15, pady=15, fill="both", expand=True)
    frame_conteudo.grid_columnconfigure(1, weight=1)  # Faz a coluna de inputs se esticar para preencher o espaço lateral
    frame_conteudo.grid_rowconfigure(7, weight=1)  # Faz a linha da tabela (row 7) se esticar verticalmente

    # Configuração visual do Campo de Entrada: Item
    label_item = ctk.CTkLabel(frame_conteudo, text="Item:", font=("Segoe UI", 14, "bold"))
    label_item.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Alinhado à esquerda ('w' - west)
    entrada_item = ctk.CTkEntry(frame_conteudo, width=200, placeholder_text="Ex: Argamassa", font=("Segoe UI", 14))
    entrada_item.grid(row=0, column=1, padx=10, pady=5, sticky="ew")  # Preenche o espaço disponível na horizontal ('ew')

    # Configuração visual do Campo de Entrada: Quantidade
    label_quantidade = ctk.CTkLabel(frame_conteudo, text="Quantidade:", font=("Segoe UI", 14, "bold"))
    label_quantidade.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entrada_quantidade = ctk.CTkEntry(frame_conteudo, width=200, placeholder_text="(Opcional)", font=("Segoe UI", 14))
    entrada_quantidade.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Configuração visual do Campo de Entrada: Preço
    label_valor = ctk.CTkLabel(frame_conteudo, text="Preço (R$):", font=("Segoe UI", 14, "bold"))
    label_valor.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entrada_valor = ctk.CTkEntry(frame_conteudo, width=200, placeholder_text="(Opcional)", font=("Segoe UI", 14))
    entrada_valor.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Configuração visual do Botão: Adicionar Item (inicialmente estilizado em cor verde)
    botao_adicionar = ctk.CTkButton(frame_conteudo, text="Adicionar Item", command=adicionar_item, fg_color="#2ecc71", hover_color="#27ae60", font=("Segoe UI", 15, "bold"), height=38)
    botao_adicionar.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # Configuração visual do Botão: Remover Item (estilizado em vermelho)
    botao_remover = ctk.CTkButton(frame_conteudo, text="Remover Item", command=remover_item, fg_color="#e74c3c", hover_color="#c0392b", font=("Segoe UI", 15, "bold"), height=38)
    botao_remover.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # Configuração visual do Botão: Limpar Lista (estilizado em laranja)
    botao_limpar = ctk.CTkButton(frame_conteudo, text="Limpar Lista", command=limpar_lista, fg_color="#f39c12", hover_color="#d35400", font=("Segoe UI", 15, "bold"), height=38)
    botao_limpar.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # Configuração visual do Botão: Alternar Status (Marca/Desmarca)
    botao_status = ctk.CTkButton(frame_conteudo, text="Marcar | Desmarcar", command=alternar_status, font=("Segoe UI", 15, "bold"), height=38)
    botao_status.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # Configuração de estilo para o Treeview se adaptar melhor visualmente ao tema escuro/claro
    estilo_tabela = ttk.Style()
    estilo_tabela.theme_use("clam")  # Estilo básico do Tkinter que permite customização de bordas e fontes
    estilo_tabela.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
    estilo_tabela.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # Configuração da Listbox/Treeview (Utilizamos ttk.Treeview pois o customtkinter não possui tabela nativa)
    caixa_lista = ttk.Treeview(frame_conteudo, columns=("status", "nome", "quantidade", "valor"), show="headings")
    caixa_lista.grid(row=7, column=0, columnspan=2, padx=(10, 0), pady=10, sticky="nsew")  # Ocupa toda a área útil disponível ('nsew')

    # Define os títulos das colunas visíveis e seu alinhamento de texto
    caixa_lista.heading("status", text="Status", anchor='center')
    caixa_lista.heading("nome", text="Nome", anchor='w')
    caixa_lista.heading("quantidade", text="Qtd", anchor='center')
    caixa_lista.heading("valor", text="Valor", anchor='center')

    # Define as larguras padrão e comportamentos de redimensionamento para cada uma das colunas da tabela
    caixa_lista.column("status", width=60, anchor='center', stretch=False)  # Status não se estica ao aumentar o tamanho da janela
    caixa_lista.column("nome", width=190, anchor='w')  # Nome do item se estica para preencher espaço
    caixa_lista.column("quantidade", width=60, anchor='center')
    caixa_lista.column("valor", width=90, anchor='center')

    # Configuração da Barra de Rolagem vertical integrada à tabela de itens
    barra_rolagem = ttk.Scrollbar(frame_conteudo, orient=tk.VERTICAL, command=caixa_lista.yview)
    barra_rolagem.grid(row=7, column=2, padx=(0, 10), pady=10, sticky="ns")
    caixa_lista.configure(yscrollcommand=barra_rolagem.set)

    # Associação de Atalhos do Teclado e Eventos do Mouse
    caixa_lista.bind("<Delete>", remover_item)  # Remove o item selecionado ao pressionar a tecla 'Delete'
    caixa_lista.bind("<Double-1>", alternar_status)  # Alterna o emoji de comprado/não comprado com clique duplo do mouse
    entrada_item.bind("<Return>", ir_quantidade)  # Vai para o campo de quantidade ao apertar 'Enter' no campo Item
    entrada_quantidade.bind("<Return>", ir_valor)  # Vai para o campo de preço ao apertar 'Enter' no campo Quantidade
    entrada_valor.bind("<Return>", adicionar_item)  # Adiciona ou salva o item na lista ao apertar 'Enter' no campo de Preço
    janela.bind("<Shift-Delete>", limpar_lista)  # Abre caixa para limpar toda a lista ao apertar 'Shift + Delete'
    caixa_lista.bind("<Return>", editar_item)  # Entra no modo de edição do item selecionado ao apertar 'Enter' na tabela

    # Exibição do Rodapé de Informações Consolidadas
    label_rodape = ctk.CTkLabel(frame_conteudo, textvariable=texto_total, font=("Helvetica", 17, "bold"))
    label_rodape.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    carregar_lista()  # Executa a busca inicial no arquivo local antes de renderizar a janela
    janela.mainloop()  # Inicia o loop infinito da interface gráfica para responder às ações do usuário

# Condicional para garantir que o programa só execute a função main se for iniciado diretamente
if __name__ == "__main__":
    main()