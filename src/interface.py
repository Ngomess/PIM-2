# -*- coding: utf-8 -*-

import tkinter as tk 
from tkinter import ttk, messagebox
import os
import csv 

"""bibliotecas e extensoes 

messagebox: mostrar pop-ups de alerta, erro, confirmação
os: verificar se arquivo existe
csv: ler/escrever arquivos CSV """

# ======================================================================================================
# FUNÇÕES DE MANIPULAÇÃO DE DADOS (usuario_dados.csv)

ARQUIVO_LOGIN = "usuario_dados.csv"

def ler_usuarios():
    """Lê todos os usuários do arquivo de login."""
    usuarios = []
    if not os.path.exists(ARQUIVO_LOGIN): 
        """Cria o arquivo com um usuário padrão se não existir"""
        with open(ARQUIVO_LOGIN, "w", encoding="utf-8") as f: 
            writer = csv.writer(f)
            writer.writerow(["administrador@escola.com", "123", "Administrador"])

    try:
        with open(ARQUIVO_LOGIN, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                """Lê linha por linha e transforma em: email, senha e tipo"""
                
                if len(row) == 3:
                    email, senha, tipo = [c.strip().strip('"') for c in row]
                    usuarios.append({"email": email, "senha": senha, "tipo": tipo})
                """Retorna uma lista de usuários""" 

    except Exception as e:
        messagebox.showerror("Erro de Arquivo", f"Não foi possível ler o arquivo de login: {e}")
    return usuarios

def salvar_usuarios(usuarios): 
    """Recebe todos os usuários e salva novamente no arquivo CSV"""
    try:
        with open(ARQUIVO_LOGIN, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            for user in usuarios:
                writer.writerow([user['email'], user['senha'], user['tipo']])

    except Exception as e:
        messagebox.showerror("Erro de Arquivo", f"Não foi possível salvar o arquivo de login: {e}")
# ======================================================================================================
# FUNÇÕES DE MANIPULAÇÃO DE DADOS (dados_academicos.csv)

ARQUIVO_DADOS = "dados_academicos.csv"

def normalize_simple(s):
    """Normaliza nomes de alunos:
    tudo minúsculo, remove acentos, remove símbolos, usa só letras, números, ponto e underline, se vier email → pega antes do @
    """
    if s is None:
        return ""
    s = s.strip().lower()
    if '@' in s:
        s = s.split('@')[0]

    mapa = {
        'á':'a','à':'a','ã':'a','â':'a','ä':'a',
        'é':'e','è':'e','ê':'e','ë':'e',
        'í':'i','ì':'i','î':'i','ï':'i',
        'ó':'o','ò':'o','õ':'o','ô':'o','ö':'o',
        'ú':'u','ù':'u','û':'u','ü':'u',
        'ç':'c'
    }
    """aplica o mapa removendo acentos e deixar as letras “limpas” """

    s2 = []
    for ch in s:
        s2.append(mapa.get(ch, ch))
    s = ''.join(s2)

    """mantém apenas a-z, 0-9, '.' e '_' """
    resultado = []
    for ch in s:
        if ('a' <= ch <= 'z') or ('0' <= ch <= '9') or ch in '._':
            resultado.append(ch)

        """ ignora todo o resto (espaços, sinais, etc.)"""
    return ''.join(resultado)

def salvar_dado(tipo, aluno, disciplina, info):
    try:
        aluno = aluno.strip().lower()

        """Agora o cabeçalho será criado se:
        - o arquivo NÃO existir
        - OU existir mas estiver VAZIO (como quando o C cria ele)"""
        criar_cabecalho = (not os.path.exists(ARQUIVO_DADOS)) or os.path.getsize(ARQUIVO_DADOS) == 0

        with open(ARQUIVO_DADOS, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            if criar_cabecalho:
                writer.writerow(["tipo", "aluno", "disciplina", "info"])
            writer.writerow([tipo, aluno, disciplina, info])
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar o dado: {e}")

def ler_dados(aluno, tipo=None):
    aluno_id = normalize_simple(aluno)  
    """normaliza o identificador do aluno (prefixo do e-mail)"""

    dados = []
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if {"tipo", "aluno", "disciplina", "info"}.issubset(row.keys()):
                        aluno_csv = normalize_simple(row["aluno"])
                        tipo_csv = row["tipo"].strip().lower()

                        if tipo is not None and tipo_csv != tipo.lower():
                            continue

                        """Permite busca flexível, aceitando:
                        igualdade, começa igual e parte dentro do nome
                        
                        Ajuda a tolerar variações como: (mike@aluno.com) 
                        o professor consegue dar notas como "mike", "mi", "mike.alves"""

                        if (aluno_csv == aluno_id
                            or aluno_csv.startswith(aluno_id)
                            or aluno_id.startswith(aluno_csv)
                            or (aluno_id in aluno_csv)
                            or (aluno_csv in aluno_id)):
                            dados.append({
                                "tipo": row["tipo"],
                                "disciplina": row["disciplina"],
                                "info": row["info"]
                            })
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler os dados: {e}")
    return dados


# ======================================================================================================

def lista_materias():
    materias = [ "Python", "Engenharia de Software", "Programação em C", "Analise e Projetos de Sistemas"]
    return materias 
"""quando a função for chamada, ela devolve a lista combobox"""

# ======================================================================================================
# FUNÇÕES DO administrador: GERENCIAMENTO DE USUÁRIOS

"""FUNÇÃO DE EXCLUSÃO DE USUÁRIOS"""
def logica_excluir_usuario(janela, email_entry):
    email = email_entry.get().strip()
    """obtém e-mail do campo Entry"""

    if not email:
        messagebox.showerror("Erro", "Digite o e-mail do usuário para excluir.")
        return

    usuarios = ler_usuarios()
    usuario_encontrado = next((user for user in usuarios if user['email'] == email), None)

    if usuario_encontrado:
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o usuário {email}?"):
            usuarios.remove(usuario_encontrado)
            salvar_usuarios(usuarios)
            messagebox.showinfo("Sucesso", f"Usuário {email} excluído com sucesso!")

    else:
        messagebox.showerror("Erro", f"Usuário {email} não encontrado.")

def confirmar_saida(janela):
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
        janela.destroy()

def janela_excluir_usuario():
    """cria a janela de exclusão de usuario"""

    janela = tk.Toplevel()
    janela.title("Excluir Usuário")
    janela.geometry("500x500")

    frame = ttk.Frame(janela, padding="10")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Digite o e-mail do usuário a ser excluído:").pack(pady=(20, 5))
    email_entry = ttk.Entry(frame, width=40)
    email_entry.pack(pady=5)

    ttk.Button(frame, text="Excluir", width=25, command=lambda: logica_excluir_usuario(janela, email_entry)).pack(pady=10)
    ttk.Button(frame, text="Sair", width=25, command=lambda: confirmar_saida(janela)).pack(pady=10)

def confirmar_saida(janela):
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
        janela.destroy()
        """fecha a janela"""
        
def logica_adicionar_usuario(janela, email_entry, senha_entry, tipo_var):
    """Lógica para adicionar um novo usuário ao arquivo"""

    email = email_entry.get().strip()
    senha = senha_entry.get().strip()
    tipo = tipo_var.get()

    if not email or not senha or tipo == "Selecione o Tipo":
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    usuarios = ler_usuarios()
    if any(user['email'] == email for user in usuarios):
        messagebox.showerror("Erro", f"O e-mail {email} já está cadastrado.")
        return
    """Validação: se algum campo vazio ou email igual, da erro"""

    usuarios.append({"email": email, "senha": senha, "tipo": tipo})
    salvar_usuarios(usuarios)
    
    messagebox.showinfo("Sucesso", f"Usuário {email} ({tipo}) adicionado com sucesso!")
    janela.destroy()
    """fecha a janela"""

def janela_adicionar_usuario(): 
    """Cria a janela para adicionar um novo usuário"""

    janela = tk.Toplevel()
    janela.title("Adicionar Novo Usuário")
    janela.geometry("600x500")
    
    frame = ttk.Frame(janela, padding="10")
    frame.pack(fill="both", expand=True)

    """Email"""
    ttk.Label(frame, text="E-mail:").pack(pady=(10, 0))
    email_entry = ttk.Entry(frame, width=40)
    email_entry.pack(pady=5)

    """Senha"""
    ttk.Label(frame, text="Senha:").pack(pady=(10, 0))
    senha_entry = ttk.Entry(frame, width=40, show="*")
    senha_entry.pack(pady=5)

    """Tipo de Usuário"""
    ttk.Label(frame, text="Tipo:").pack(pady=(10, 0))
    tipo_var = tk.StringVar(value="Selecione o Tipo")
    tipos = ["professor", "aluno"]
    tipo_menu = ttk.OptionMenu(frame, tipo_var, tipo_var.get(), *tipos)
    tipo_menu.config(width=37)
    tipo_menu.pack(pady=5)

    """Botoes"""
    ttk.Button(frame, text="Adicionar",width=25, command=lambda: logica_adicionar_usuario(janela, email_entry, senha_entry, tipo_var)).pack(pady=20)
    ttk.Button(frame, text="Sair", width=25, command=lambda: confirmar_saida(janela)).pack(pady=10)


def logica_editar_usuario(janela, email_original, nova_senha_entry, novo_tipo_var):    
    """Lógica para editar um usuário existente no arquivo."""

    nova_senha = nova_senha_entry.get().strip()
    novo_tipo = novo_tipo_var.get()
    """Edita usuário identificado no email_original"""

    if not nova_senha or novo_tipo == "Selecione o Tipo":
        messagebox.showerror("Erro", "A senha e o tipo devem ser preenchidos.")
        return

    usuarios = ler_usuarios()
    usuario_encontrado = False
    
    for user in usuarios:
        if user['email'] == email_original:
            user['senha'] = nova_senha
            user['tipo'] = novo_tipo
            usuario_encontrado = True
            break

    if usuario_encontrado:
        salvar_usuarios(usuarios)
        messagebox.showinfo("Sucesso", f"Usuário {email_original} editado com sucesso!")
        janela.destroy()
    else:
        messagebox.showerror("Erro", f"Usuário {email_original} não encontrado para edição.")


def janela_editar_usuario(): 
    """Cria a janela para buscar e editar um usuário"""

    janela = tk.Toplevel()
    janela.title("Editar Usuário")
    janela.geometry("500x500")
    
    frame = ttk.Frame(janela, padding="10")
    frame.pack(fill="both", expand=True)

    """Busca de Usuário"""
    ttk.Label(frame, text="Buscar Usuário por E-mail:").pack(pady=(10, 0))
    busca_email_entry = ttk.Entry(frame, width=40)
    busca_email_entry.pack(pady=5)

    """Frame para os campos de edição (escondido inicialmente)"""
    edicao_frame = ttk.Frame(frame, padding="10")
    
    """Variáveis para os campos de edição"""
    email_var = tk.StringVar()
    senha_entry = tk.Entry(edicao_frame, width=40, show="*")
    tipo_var = tk.StringVar(value="Selecione o Tipo")
    

    """Função para carregar os dados do usuário"""
    def carregar_usuario():
        email_busca = busca_email_entry.get().strip()
        if not email_busca:
            messagebox.showerror("Erro", "Digite o e-mail do usuário para buscar.")
            return

        usuarios = ler_usuarios()
        usuario_encontrado = next((user for user in usuarios if user['email'] == email_busca), None)
        
        if usuario_encontrado:
            """Preenche os campos de edição"""

            email_var.set(usuario_encontrado['email'])
            senha_entry.delete(0, tk.END)
            senha_entry.insert(0, usuario_encontrado['senha'])
            tipo_var.set(usuario_encontrado['tipo'])
            
            """Exibe os campos de edição"""
            edicao_frame.pack(fill="x", pady=10)
            messagebox.showinfo("Sucesso", f"Usuário {email_busca} carregado para edição.")
        else:
            messagebox.showerror("Erro", f"Usuário {email_busca} não encontrado.")
            edicao_frame.pack_forget()

    ttk.Button(frame, text="Buscar", width=25, command=carregar_usuario).pack(pady=10)
    ttk.Button(frame, text="Sair", width=25, command=lambda: confirmar_saida(janela)).pack(pady=10)


    """CAMPOS DE EDIÇÃO
    Email (somente leitura)"""
    ttk.Label(edicao_frame, text="E-mail (Não Editável):").pack(pady=(10, 0))
    ttk.Label(edicao_frame, textvariable=email_var, font=('Arial', 10, 'bold')).pack(pady=5)
    
    """Senha"""
    ttk.Label(edicao_frame, text="Nova Senha:").pack(pady=(10, 0))
    senha_entry.pack(pady=5)

    """Tipo de Usuário"""
    ttk.Label(edicao_frame, text="Novo Tipo:").pack(pady=(10, 0))
    tipos = ["professor", "aluno"]
    tipo_menu = ttk.OptionMenu(edicao_frame, tipo_var, tipo_var.get(), *tipos)
    tipo_menu.config(width=37)
    tipo_menu.pack(pady=5)

    """Botão de Salvar Edição"""
    ttk.Button(edicao_frame, text="Salvar Edição", 
               command=lambda: logica_editar_usuario(janela, email_var.get(), senha_entry, tipo_var)).pack(pady=20)


# ADMINISTRADOR ============================================================================================================================== 

def janela_administrador(login_window, usuario_logado): 
    """Cria janela do administrador
    .withdraw() esconde a janela de login e abre a outra nova
    usuario_logado (dados do usuário atual) """

    administrador = tk.Toplevel()
    administrador.title("Painel do Administrador")
    administrador.geometry("600x400")

    def confirmar_saida(administrador):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
            administrador.destroy()
            login_window.deiconify()   
            """.destroy()- fecha a janela Painel do Administrador (destrói completamente)
            login_window.deiconify() - Reexibe a janela de login"""

    """ FRAME DO TOPO (título + info usuário)"""

    frame_topo = ttk.Frame(administrador) 
    """frame com o título e a informação do Administrador """

    frame_topo.pack(fill="x", pady=10) 
    """fill="x" - o frame ocupa toda a largura da janela e pady define a distancia na vertical """

    ttk.Label(frame_topo, text="Bem-vindo, Administrador!", font=('Arial', 16)).pack(side="left", padx=10)

    info_user = ttk.Label(frame_topo, text="Usuário: Administrador\nEmail: Administrador@escola.com",font=('Arial', 10), justify='right')
    info_user.pack(side="right", padx=10)

    """Frame para o conteúdo central"""
    frame_conteudo = ttk.Frame(administrador)
    frame_conteudo.pack(expand=True, padx=20, pady=20)
    
    ttk.Label(frame_conteudo, text="Bem-vindo, administrador!", font=('Arial', 16)).pack(pady=20)

    """Botões de gerenciamento"""
    ttk.Button(frame_conteudo, text="Adicionar Usuário", width=30, command=janela_adicionar_usuario).pack(pady=10)
    ttk.Button(frame_conteudo, text="Editar Usuário", width=30, command=janela_editar_usuario).pack(pady=10)
    ttk.Button(frame_conteudo, text="Excluir Usuário", width=30, command=janela_excluir_usuario).pack(pady=10)

    ttk.Button(frame_conteudo, text="Sair", width=25, command=lambda: confirmar_saida(administrador)).pack(pady=20)


# PROFESSOR ============================================================================================================================== 

def lancar_presenca(): 
    """cria janela para lançar presença"""

    janela_presenca= tk.Toplevel()
    janela_presenca.title("Lançamento de Presença")
    janela_presenca.geometry("500x400")

    def confirmar_saida(janela):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
            janela.destroy()

    ttk.Label(janela_presenca, text="Nome do Aluno:").pack(pady=10)
    entrada_aluno = ttk.Entry(janela_presenca, width=30)
    entrada_aluno.pack(pady=5)

    ttk.Label(janela_presenca, text="Disciplina:").pack(pady=10)
    materias = lista_materias()
    disciplina_opcoes = tk.StringVar()
    combo_disciplina = ttk.Combobox(janela_presenca, textvariable=disciplina_opcoes, values=materias, width=27)
    """pega a função lista_materias() e faz um combobox"""
    combo_disciplina.pack(pady=5)

    ttk.Label(janela_presenca, text="Presente? (Sim/Não)").pack(pady=10)
    entrada_presenca = ttk.Entry(janela_presenca, width=15)
    entrada_presenca.pack(pady=5)

    def salvar():
        aluno = entrada_aluno.get()
        disciplina = disciplina_opcoes.get()
        presenca = entrada_presenca.get()

        if aluno and disciplina and presenca:
            salvar_dado("presenca", aluno.lower(), disciplina, presenca)

            messagebox.showinfo("Sucesso!", f"Presença lançada:\nAluno: {aluno}\nDisciplina: {disciplina}\nPresença: {presenca}")
            janela_presenca.destroy()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        
        """mostra messagebox.showinfo e fecha janela; ou mostra erro"""

    """botoes de sair e salvar"""
    ttk.Button(janela_presenca, text="Salvar", command=salvar).pack(pady=20)
    ttk.Button(janela_presenca, text="Sair", command=lambda: confirmar_saida(janela_presenca)).pack()


def lancar_notas():
    """cria uma janela para lançar notas"""

    janela_notas = tk.Toplevel()
    janela_notas.title("Lançamento de Notas")
    janela_notas.geometry("500x400")

    def confirmar_saida(janela):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
            janela.destroy()

    ttk.Label(janela_notas, text="Nome do Aluno:").pack(pady=10)
    entrada_aluno = ttk.Entry(janela_notas, width=30)
    entrada_aluno.pack(pady=5)

    ttk.Label(janela_notas, text="Disciplina:").pack(pady=10)
    materias = lista_materias()
    disciplina_opcoes = tk.StringVar()
    combo_disciplina = ttk.Combobox(janela_notas, textvariable=disciplina_opcoes, values=materias, width=27)
    """pega a função lista_materias() e faz um combobox"""
    combo_disciplina.pack(pady=5)

    ttk.Label(janela_notas, text="Nota:").pack(pady=10)
    entrada_nota = ttk.Entry(janela_notas, width=20)
    entrada_nota.pack(pady=5)

    def salvar():
        aluno = entrada_aluno.get()
        disciplina = disciplina_opcoes.get()
        nota = entrada_nota.get()

        if aluno and disciplina and nota:
            salvar_dado("nota", aluno.lower(), disciplina, nota)

            messagebox.showinfo("Sucesso!", f"Nota lançada:\nAluno: {aluno}\nDisciplina: {disciplina}\nNota: {nota}")
            janela_notas.destroy()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

            """mostra messagebox.showinfo e fecha janela; ou mostra erro"""
    
    """botoes de sair e salvar"""
    ttk.Button(janela_notas, text="Salvar", command=salvar).pack(pady=20)
    ttk.Button(janela_notas, text="Sair", command=lambda: confirmar_saida(janela_notas)).pack()


def lancar_tarefas():
    """cria uma janela para lançar tarefas"""

    janela_tarefas = tk.Toplevel()
    janela_tarefas.title("Gestão de Disciplinas e Tarefas")
    janela_tarefas.geometry("500x400")    

    def confirmar_saida(janela):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
            janela.destroy()

    ttk.Label(janela_tarefas, text="Nome do Aluno:").pack(pady=10)
    entrada_aluno = ttk.Entry(janela_tarefas, width=30)
    entrada_aluno.pack(pady=5)

    ttk.Label(janela_tarefas, text="Disciplina:").pack(pady=10)
    materias = lista_materias()
    disciplina_opcoes = tk.StringVar()
    combo_disciplina = ttk.Combobox(janela_tarefas, textvariable=disciplina_opcoes, values=materias, width=27)
    """pega a função lista_materias() e faz um combobox"""
    combo_disciplina.pack(pady=5)

    ttk.Label(janela_tarefas, text="Tarefa (com data):").pack(pady=10)
    entrada_tarefa = ttk.Entry(janela_tarefas, width=50)
    entrada_tarefa.pack(pady=5)

    def salvar():
        aluno = entrada_aluno.get()
        disciplina = disciplina_opcoes.get()
        tarefa = entrada_tarefa.get()
        
        if aluno and disciplina and tarefa:
            salvar_dado("tarefa", aluno.lower(), disciplina, tarefa)

            messagebox.showinfo("Sucesso!", f"Tarefa lançada para {aluno}")
            janela_tarefas.destroy()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

            """mostra messagebox.showinfo e fecha janela; ou mostra erro"""

    """botoes de salvar e sair"""
    ttk.Button(janela_tarefas, text="Salvar", command=salvar).pack(pady=20)
    ttk.Button(janela_tarefas, text="Sair", command=lambda: confirmar_saida(janela_tarefas)).pack()

        
def janela_professor(login_window, usuario_logado): 
    """Cria a janela do professor
    .withdraw() esconde a janela de login e abre a outra nova
    usuario_logado (dados do usuário atual)"""

    prof = tk.Toplevel()
    prof.title("Painel do Professor")
    prof.geometry("600x400")

    def confirmar_saida(prof):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
            prof.destroy()
            login_window.deiconify()
        """.destroy()- fecha a janela Painel do professor (destrói completamente)
            login_window.deiconify() - Reexibe a janela de login"""


    """Depois de fazer o login e ter usuario_logado"""
    email = usuario_logado ['email']
    tipo = usuario_logado ['tipo']

    """Extrai o nome do email"""
    nome_usuario = email.split("@")[0].capitalize() 

    """email.split("@") Divide a string do email em uma lista usando @ como separador
    Pegamos o primeiro item da lista, que é o "nome", antes do @
    .capitalize() - Colocamos a primeira letra em maiúscula e o resto em minúscula"""

    """Frame do topo"""
    frame_topo = ttk.Frame(prof) 
    frame_topo.pack(fill="x", pady=10, padx=10)

    """Título"""
    ttk.Label(frame_topo, text=f"Bem-vindo(a), {nome_usuario}!", font=('Arial', 16)).pack(side="left", padx=10)

    """Info do usuário"""
    tipo_formatado = tipo.capitalize()
    info_user = ttk.Label(frame_topo, text=f"{tipo_formatado}(a): {nome_usuario}\nEmail: {email}", 
                      font=('Arial', 10), justify='right')
    info_user.pack(side="right", padx=10)


    """Frame central (botões)"""
    frame_conteudo = ttk.Frame(prof)
    frame_conteudo.pack(expand=True)

    ttk.Button(frame_conteudo, text="Área de Presença", width=25, command=lancar_presenca).pack(pady=10)
    ttk.Button(frame_conteudo, text="Notas", width=25, command=lancar_notas).pack(pady=10)
    ttk.Button(frame_conteudo, text="Disciplinas", width=25, command=lancar_tarefas).pack(pady=10)
    ttk.Button(frame_conteudo, text="Sair", width=25, command=lambda: confirmar_saida(prof)).pack (pady=20)

# ALUNO  ============================================================================================================================== 
def janela_aluno(login_window, usuario_logado):
    """cria painel do aluno"""

    aluno = tk.Toplevel()
    aluno.title("Painel do Aluno")
    aluno.geometry("600x400")

    def confirmar_saida(aluno):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
            aluno.destroy()
            login_window.deiconify()
            """.destroy()- fecha a janela Painel do aluno (destrói completamente)
            login_window.deiconify() - Reexibe a janela de login"""


    email = usuario_logado['email']
    tipo = usuario_logado['tipo']
    nome_usuario = email.split("@")[0].capitalize()  
    """.capitalize() deixa a primeira letra maiúscula"""

    """Frame do topo"""
    frame_topo = ttk.Frame(aluno)
    frame_topo.pack(fill="x", pady=10, padx=10)

    ttk.Label(frame_topo, text=f"Bem-vindo(a), {nome_usuario}!", font=('Arial', 16)).pack(side="left", padx=10)
    tipo_formatado = tipo.capitalize()
    ttk.Label(frame_topo, text=f"{tipo_formatado}(a): {nome_usuario}\nEmail: {email}", font=('Arial', 10)).pack(side="right")

    """Frame de botões"""
    frame_botoes = ttk.Frame(aluno)
    frame_botoes.pack(side="left", padx=20, pady=20)

    """Frame de conteúdo"""
    frame_conteudo = ttk.Frame(aluno, relief="solid", width=350, height=300)
    frame_conteudo.pack(side="right", padx=20, pady=20)

    frame_conteudo.pack_propagate(False)
    """para ter tamanho fixo"""


    """Função para atualizar conteúdo"""
    def atualizar_conteudo(dados, titulo):
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

        ttk.Label(frame_conteudo, text=titulo, font=("Arial", 14)).pack(pady=10)

        if dados:
            for item in dados:
                disciplina = item['disciplina'].capitalize() 

                info = item['info']
                ttk.Label(frame_conteudo, text=f"{disciplina}: {info}").pack(anchor="w", pady=3, padx=10)
        else:
            ttk.Label(frame_conteudo, text="Nenhum registro encontrado.").pack(pady=20)

    """Botões para mostrar Notas, Presenças e Tarefas"""
    ttk.Button(frame_botoes, text="Notas", width=20,
               command=lambda: atualizar_conteudo(
                   ler_dados(nome_usuario.lower(), "nota"), "Minhas Notas")).pack(pady=5)

    ttk.Button(frame_botoes, text="Presença", width=20,
               command=lambda: atualizar_conteudo(
                   ler_dados(nome_usuario.lower(), "presenca"), "Minhas Presenças")).pack(pady=5)

    ttk.Button(frame_botoes, text="Tarefas", width=20,
               command=lambda: atualizar_conteudo(
                   ler_dados(nome_usuario.lower(), "tarefa"), "Minhas Tarefas")).pack(pady=5)

    ttk.Button(frame_botoes, text="Sair", command=lambda: confirmar_saida(aluno)).pack()

# ======================================================================================================
# TELA DE LOGIN (INÍCIO DA APLICAÇÃO)

"""primeira tela - login"""
login = tk.Tk()
login.title("Sistema Academico")
login.geometry('600x400')
    
"""Define um estilo (tema moderno)"""
style = ttk.Style()
style.theme_use("clam")
"""define tema visual dos widgets"""

# CAMPOS DA TELA LOGIN ----------------------------------------

"""email"""
campo_email = ttk.Label(login,text='Email', font=('Arial', 12))
campo_email.pack(pady = 20)
entrada_email = ttk.Entry(login, width=30)
entrada_email.pack(pady = 10) 
"""pady espaço na vertical """


"""senha"""
campo_senha = ttk.Label(login, text='Senha', font=('Arial', 12))
campo_senha.pack(pady = 20)
entrada_senha = ttk.Entry(login, width=30, show= "*") 
"""show='*' oculta a senha"""
entrada_senha.pack(pady = 10)

"""para exibir o resultado login"""
resultado_label = ttk.Label(login, text="") 
resultado_label.pack(pady=25)


def fazer_login(event=None):  
    """event=None permite ser chamada pelo botão e pela tecla Enter"""

    email = entrada_email.get().strip()
    senha = entrada_senha.get().strip()

    usuarios = ler_usuarios()
    usuario_logado = next((user for user in usuarios if user['email'].strip().lower() == email.lower() and user['senha'].strip() == senha), None)

    if usuario_logado:
        resultado_label.config(text="Login realizado com sucesso!", foreground="green")

        """esconde a janela de login sem destruir"""
        login.withdraw()

        """normaliza o tipo para evitar problemas de caixa, espaços, aspas, etc"""
        tipo = usuario_logado.get('tipo', '')
        tipo_normalizado = tipo.strip().strip('"').lower()

        try:
            if tipo_normalizado == "administrador":
                janela_administrador(login, usuario_logado)
            elif tipo_normalizado == "professor":
                janela_professor(login, usuario_logado)
            elif tipo_normalizado == "aluno":
                janela_aluno(login, usuario_logado)
            else:
                login.deiconify()
                messagebox.showerror("Tipo inválido", f"Tipo de usuário não reconhecido: '{tipo}'. Verifique o arquivo de usuários.")
                """(reexibe login) e messagebox.showerror("Tipo inválido", ...) (tipo desconhecido no CSV)."""

        except Exception as e:
            """se deu erro ao abrir a nova janela, reexibe login e mostra erro (útil para debugging)"""

            login.deiconify()
            messagebox.showerror("Erro ao abrir painel", f"Ocorreu um erro ao abrir a janela de {tipo_normalizado}: {e}")

    else:
        resultado_label.config(text="Email ou senha incorretos.", foreground="red")
        """mensagem de erro"""


"""BOTÃO - estilo personalizado"""
style.configure(
    "Custom.TButton",
    font=("Arial", 16, "bold"),
    padding=(20, 15),  # (horizontal, vertical)
    background="#007ACC",
    foreground="white"
)

"""Corrige a cor de fundo no tema "clam" """
style.map(
    "Custom.TButton",
    background=[("active", "#005B99"), ("!disabled", "#007ACC")], 
    foreground=[("active", "white")]
)

"""botao de login"""
bt_entrar = ttk.Button(
    login,
    text="Entrar",
    command=fazer_login,
    style="Custom.TButton" 
)
bt_entrar.pack(pady=25)
"""aplica o estilo que criamos"""


"""Adiciona a funcionalidade de login ao pressionar Enter"""
login.bind('<Return>', fazer_login)

"""Inicia a aplicação"""
login.mainloop()