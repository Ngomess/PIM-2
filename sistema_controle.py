import tkinter as tk 
from tkinter import ttk, messagebox
import os

# ======================================================================================================
# FUNÇÕES DE MANIPULAÇÃO DE DADOS (teste_login.txt)

ARQUIVO_LOGIN = "teste_login.txt"

def ler_usuarios(): #Lê todos os usuários do arquivo de login.
    """Lê todos os usuários do arquivo de login."""
    usuarios = []
    if not os.path.exists(ARQUIVO_LOGIN): #Cria o arquivo com um usuário padrão se não existir
        with open(ARQUIVO_LOGIN, "w") as f: #a variável f é o objeto arquivo
            f.write("administrador@escola.com,123,admin\n")
            f.write("professor@escola.com,123,professor\n")
            f.write("aluno@escola.com,123,aluno\n")

    try:
        with open(ARQUIVO_LOGIN, "r") as f:
            for linha in f:
                if linha.strip(): #strip() remove espaços em branco e o \n
                    try:
                        email, senha, tipo = linha.strip().split(",")
                        usuarios.append({"email": email, "senha": senha, "tipo": tipo})
                    except ValueError:
                        # Ignora linhas mal formatadas

                        '''se em cada linha de email, senha e tipo nao tiver exatamente as 3 partes, 
                                        isso gera ValueError e cai no except'''
                        
                        continue
    except Exception as e:
        messagebox.showerror("Erro de Arquivo", f"Não foi possível ler o arquivo de login: {e}")
    return usuarios

help(ler_usuarios)

def salvar_usuarios(usuarios): #Salva a lista completa de usuários de volta no arquivo.
    try:
        with open(ARQUIVO_LOGIN, "w") as f:
            for user in usuarios:
                f.write(f"{user['email']},{user['senha']},{user['tipo']}\n")
    except Exception as e:
        messagebox.showerror("Erro de Arquivo", f"Não foi possível salvar o arquivo de login: {e}")
# ======================================================================================================
# FUNÇÕES DE MANIPULAÇÃO DE DADOS (dados.txt)
ARQUIVO_DADOS = "dados.txt"

def salvar_dado(tipo, aluno, disciplina, info):
    """Salva qualquer tipo de dado (nota, presença, tarefa) no mesmo arquivo"""
    try:
        with open(ARQUIVO_DADOS, "a") as f:
            f.write(f"{tipo},{aluno},{disciplina},{info}\n")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar o dado: {e}")

def ler_dados(aluno, tipo=None):
    """Lê os dados de um aluno, filtrando por tipo se desejado"""
    dados = []
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as f:
            for linha in f:
                if linha.strip():
                    try:
                        t, a, disciplina, info = linha.strip().split(",", 3)
                        if a == aluno and (tipo is None or t == tipo):
                            dados.append({"tipo": t, "disciplina": disciplina, "info": info})
                    except ValueError:
                        continue
    return dados

# ======================================================================================================

def lista_materias():
    materias = ["Python", "Engenharia de Software", "Programação em C"]
    return materias #quando a função for chamada, ela devolva a lista

# ======================================================================================================
# FUNÇÕES DO administrador: GERENCIAMENTO DE USUÁRIOS

def confirmar_saida(janela):
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
        janela.destroy()

def logica_adicionar_usuario(janela, email_entry, senha_entry, tipo_var):
    """Lógica para adicionar um novo usuário ao arquivo."""
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

    usuarios.append({"email": email, "senha": senha, "tipo": tipo})
    salvar_usuarios(usuarios)
    
    messagebox.showinfo("Sucesso", f"Usuário {email} ({tipo}) adicionado com sucesso!")
    janela.destroy()


def janela_adicionar_usuario(): #Cria a janela para adicionar um novo usuário
    janela = tk.Toplevel()
    janela.title("Adicionar Novo Usuário")
    janela.geometry("600x400")
    
    frame = ttk.Frame(janela, padding="10")
    frame.pack(fill="both", expand=True)

    # Email
    ttk.Label(frame, text="E-mail:").pack(pady=(10, 0))
    email_entry = ttk.Entry(frame, width=40)
    email_entry.pack(pady=5)

    # Senha
    ttk.Label(frame, text="Senha:").pack(pady=(10, 0))
    senha_entry = ttk.Entry(frame, width=40, show="*")
    senha_entry.pack(pady=5)

    # Tipo de Usuário
    ttk.Label(frame, text="Tipo:").pack(pady=(10, 0))
    tipo_var = tk.StringVar(value="Selecione o Tipo")
    tipos = ["professor", "aluno"]
    tipo_menu = ttk.OptionMenu(frame, tipo_var, tipo_var.get(), *tipos)
    tipo_menu.config(width=37)
    tipo_menu.pack(pady=5)

    # Botão de Adicionar
    ttk.Button(frame, text="Adicionar",width=25, command=lambda: logica_adicionar_usuario(janela, email_entry, senha_entry, tipo_var)).pack(pady=20)
    ttk.Button(frame, text="Sair", width=25, command=lambda: confirmar_saida(janela)).pack(pady=10)


def logica_editar_usuario(janela, email_original, nova_senha_entry, novo_tipo_var): #Lógica para editar um usuário existente no arquivo.
    nova_senha = nova_senha_entry.get().strip()
    novo_tipo = novo_tipo_var.get()

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


def janela_editar_usuario(): #Cria a janela para buscar e editar um usuário.
    janela = tk.Toplevel()
    janela.title("Editar Usuário")
    janela.geometry("600x400")
    
    frame = ttk.Frame(janela, padding="10")
    frame.pack(fill="both", expand=True)

    # --- Busca de Usuário ---
    ttk.Label(frame, text="Buscar Usuário por E-mail:").pack(pady=(10, 0))
    busca_email_entry = ttk.Entry(frame, width=40)
    busca_email_entry.pack(pady=5)

    # Frame para os campos de edição (escondido inicialmente)
    edicao_frame = ttk.Frame(frame, padding="10")
    
    # Variáveis para os campos de edição
    email_var = tk.StringVar()
    senha_entry = tk.Entry(edicao_frame, width=40, show="*")
    tipo_var = tk.StringVar(value="Selecione o Tipo")
    

    # Função para carregar os dados do usuário
    def carregar_usuario():
        email_busca = busca_email_entry.get().strip()
        if not email_busca:
            messagebox.showerror("Erro", "Digite o e-mail do usuário para buscar.")
            return

        usuarios = ler_usuarios()
        usuario_encontrado = next((user for user in usuarios if user['email'] == email_busca), None)
        
        if usuario_encontrado:
            # Preenche os campos de edição
            email_var.set(usuario_encontrado['email'])
            senha_entry.delete(0, tk.END)
            senha_entry.insert(0, usuario_encontrado['senha'])
            tipo_var.set(usuario_encontrado['tipo'])
            
            # Exibe os campos de edição
            edicao_frame.pack(fill="x", pady=10)
            messagebox.showinfo("Sucesso", f"Usuário {email_busca} carregado para edição.")
        else:
            messagebox.showerror("Erro", f"Usuário {email_busca} não encontrado.")
            edicao_frame.pack_forget()

    ttk.Button(frame, text="Buscar", width=25, command=carregar_usuario).pack(pady=10)
    ttk.Button(frame, text="Sair", width=25, command=lambda: confirmar_saida(janela)).pack(pady=10)

    # --- Campos de Edição ---
    
    # Email (somente leitura)
    ttk.Label(edicao_frame, text="E-mail (Não Editável):").pack(pady=(10, 0))
    ttk.Label(edicao_frame, textvariable=email_var, font=('Arial', 10, 'bold')).pack(pady=5)
    
    # Senha
    ttk.Label(edicao_frame, text="Nova Senha:").pack(pady=(10, 0))
    senha_entry.pack(pady=5)

    # Tipo de Usuário
    ttk.Label(edicao_frame, text="Novo Tipo:").pack(pady=(10, 0))
    tipos = ["professor", "aluno"]
    tipo_menu = ttk.OptionMenu(edicao_frame, tipo_var, tipo_var.get(), *tipos)
    tipo_menu.config(width=37)
    tipo_menu.pack(pady=5)

    # Botão de Salvar Edição
    ttk.Button(edicao_frame, text="Salvar Edição", 
               command=lambda: logica_editar_usuario(janela, email_var.get(), senha_entry, tipo_var)).pack(pady=20)


# ADMINISTRADOR ============================================================================================================================== 
def confirmar_saida(administrador):
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
        administrador.destroy()


def janela_administrador(login_window, usuario_logado): #.withdraw() esconde a janela de login e abre a outra nova 
    administrador = tk.Toplevel()
    administrador.title("Painel do Administrador")
    administrador.geometry("600x400")
    
    # === Frame do topo (título + info usuário) ===
    frame_topo = ttk.Frame(administrador) #frame com o título e a informação do Administrador 
    frame_topo.pack(fill="x", pady=10) #fill="x" - o frame ocupa toda a largura da janela e pady define a distancia na vertical 

    ttk.Label(frame_topo, text="Bem-vindo, Administrador!", font=('Arial', 16)).pack(side="left", padx=10)

    info_user = ttk.Label(frame_topo, text="Usuário: Administrador\nEmail: Administrador@escola.com",font=('Arial', 10), justify='right')
    info_user.pack(side="right", padx=10)

    # Frame para o conteúdo central
    frame_conteudo = ttk.Frame(administrador)
    frame_conteudo.pack(expand=True, padx=20, pady=20)
    
    ttk.Label(frame_conteudo, text="Bem-vindo, administrador!", font=('Arial', 16)).pack(pady=20)

    # Botões de gerenciamento
    ttk.Button(frame_conteudo, text="Adicionar Usuário", width=30, command=janela_adicionar_usuario).pack(pady=10)
    ttk.Button(frame_conteudo, text="Editar Usuário", width=30, command=janela_editar_usuario).pack(pady=10)

    ttk.Button(frame_conteudo, text="Sair", width=25,
           command=lambda: confirmar_saida(administrador)).pack(pady=20)


# PROFESSOR ============================================================================================================================== 

def lancar_presenca(): 
    janela_presenca= tk.Toplevel()
    janela_presenca.title("Lançamento de Presença")
    janela_presenca.geometry("500x400")

    ttk.Label(janela_presenca, text="Nome do Aluno:").pack(pady=10)
    entrada_aluno = ttk.Entry(janela_presenca, width=30)
    entrada_aluno.pack(pady=5)

    ttk.Label(janela_presenca, text="Disciplina:").pack(pady=10)
    materias = lista_materias()
    disciplina_opcoes = tk.StringVar()
    combo_disciplina = ttk.Combobox(janela_presenca, textvariable=disciplina_opcoes, values=materias, width=27)
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

    ttk.Button(janela_presenca, text="Salvar", command=salvar).pack(pady=20)
    ttk.Button(janela_presenca, text="Sair", command=janela_presenca.destroy).pack()


def lancar_notas():
    janela_notas = tk.Toplevel()
    janela_notas.title("Lançamento de Notas")
    janela_notas.geometry("500x400")

    ttk.Label(janela_notas, text="Nome do Aluno:").pack(pady=10)
    entrada_aluno = ttk.Entry(janela_notas, width=30)
    entrada_aluno.pack(pady=5)

    ttk.Label(janela_notas, text="Disciplina:").pack(pady=10)
    entrada_disciplina = ttk.Entry(janela_notas, width=30)
    entrada_disciplina.pack(pady=5)

    ttk.Label(janela_notas, text="Nota:").pack(pady=10)
    entrada_nota = ttk.Entry(janela_notas, width=20)
    entrada_nota.pack(pady=5)

    def salvar():
        aluno = entrada_aluno.get()
        disciplina = entrada_disciplina.get()
        nota = entrada_nota.get()
        if aluno and disciplina and nota:
            salvar_dado("nota", aluno.lower(), disciplina, nota)
            messagebox.showinfo("Sucesso!", f"Nota lançada:\nAluno: {aluno}\nDisciplina: {disciplina}\nNota: {nota}")
            janela_notas.destroy()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    ttk.Button(janela_notas, text="Salvar", command=salvar).pack(pady=20)
    ttk.Button(janela_notas, text="Sair", command=janela_notas.destroy).pack()


def lancar_tarefas():
    janela_tarefas = tk.Toplevel()
    janela_tarefas.title("Gestão de Disciplinas e Tarefas")
    janela_tarefas.geometry("500x400")    

    ttk.Label(janela_tarefas, text="Nome do Aluno:").pack(pady=10)
    entrada_aluno = ttk.Entry(janela_tarefas, width=30)
    entrada_aluno.pack(pady=5)

    ttk.Label(janela_tarefas, text="Disciplina:").pack(pady=10)
    entrada_disciplina = ttk.Entry(janela_tarefas, width=30)
    entrada_disciplina.pack(pady=5)

    ttk.Label(janela_tarefas, text="Tarefa (com data):").pack(pady=10)
    entrada_tarefa = ttk.Entry(janela_tarefas, width=50)
    entrada_tarefa.pack(pady=5)

    def salvar():
        aluno = entrada_aluno.get()
        disciplina = entrada_disciplina.get()
        tarefa = entrada_tarefa.get()
        if aluno and disciplina and tarefa:
            salvar_dado("tarefa", aluno.lower(), disciplina, tarefa)
            messagebox.showinfo("Sucesso!", f"Tarefa lançada para {aluno}")
            janela_tarefas.destroy()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    ttk.Button(janela_tarefas, text="Salvar", command=salvar).pack(pady=20)
    ttk.Button(janela_tarefas, text="Sair", command=janela_tarefas.destroy).pack()


def confirmar_saida(prof):
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
        prof.destroy()

def janela_professor(login_window, usuario_logado): #.withdraw() esconde a janela de login e abre a outra nova 
    prof = tk.Toplevel()
    prof.title("Painel do Professor")
    prof.geometry("600x400")

    # Depois de fazer o login e ter usuario_logado
    email = usuario_logado ['email']
    tipo = usuario_logado ['tipo']

    # Extrai o nome do email
    nome_usuario = email.split("@")[0].capitalize() 
    #email.split("@") Divide a string do email em uma lista usando @ como separador
    #Pegamos o primeiro item da lista, que é o "nome", antes do @
    #.capitalize() - Colocamos a primeira letra em maiúscula e o resto em minúscula

    # === Frame do topo ===
    frame_topo = ttk.Frame(prof) 
    frame_topo.pack(fill="x", pady=10, padx=10)

    # Título
    ttk.Label(frame_topo, text=f"Bem-vindo(a), {nome_usuario}!", font=('Arial', 16)).pack(side="left", padx=10)

    # Info do usuário
    tipo_formatado = tipo.capitalize()
    info_user = ttk.Label(frame_topo, text=f"{tipo_formatado}(a): {nome_usuario}\nEmail: {email}", 
                      font=('Arial', 10), justify='right')
    info_user.pack(side="right", padx=10)


    # === Frame central (botões) ===
    frame_conteudo = ttk.Frame(prof)
    frame_conteudo.pack(expand=True)

    ttk.Button(frame_conteudo, text="Área de Presença", width=25, command=lancar_presenca).pack(pady=10)
    ttk.Button(frame_conteudo, text="Notas", width=25, command=lancar_notas).pack(pady=10)
    ttk.Button(frame_conteudo, text="Disciplinas", width=25, command=lancar_tarefas).pack(pady=10)
    ttk.Button(frame_conteudo, text="Sair", width=25,
           command=lambda: confirmar_saida(prof)).pack (pady=20)

# ALUNO  ============================================================================================================================== 
def janela_aluno(login_window, usuario_logado):
    aluno = tk.Toplevel()
    aluno.title("Painel do Aluno")
    aluno.geometry("600x400")

    def sair():
        aluno.destroy()
        login_window.deiconify()

    email = usuario_logado['email']
    tipo = usuario_logado['tipo']
    nome_usuario = email.split("@")[0].capitalize()

    # Frame do topo
    frame_topo = ttk.Frame(aluno)
    frame_topo.pack(fill="x", pady=10)

    ttk.Label(frame_topo, text=f"Bem-vindo(a), {nome_usuario}!", font=('Arial', 16)).pack(side="left", padx=10)
    tipo_formatado = tipo.capitalize()
    ttk.Label(frame_topo, text=f"{tipo_formatado}(a): {nome_usuario}\nEmail: {email}", font=('Arial', 10)).pack(side="right")

    # Frame de botões
    frame_botoes = ttk.Frame(aluno)
    frame_botoes.pack(side="left", padx=20, pady=20)

    # Frame de conteúdo
    frame_conteudo = ttk.Frame(aluno, relief="solid", width=350, height=300)
    frame_conteudo.pack(side="right", padx=20, pady=20)
    frame_conteudo.pack_propagate(False)  # Impede encolhimento automático

    # Função para atualizar conteúdo
    def atualizar_conteudo(dados, titulo):
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

        ttk.Label(frame_conteudo, text=titulo, font=("Arial", 14)).pack(pady=10)

        if dados:
            for item in dados:
                ttk.Label(frame_conteudo, text=f"{item['disciplina']}: {item['info']}").pack(anchor="w", pady=3)
        else:
            ttk.Label(frame_conteudo, text="Nenhum registro encontrado.").pack(pady=20)

    # Botões
    ttk.Button(frame_botoes, text="Notas", width=20,
               command=lambda: atualizar_conteudo(
                   ler_dados(nome_usuario.lower().capitalize(), "nota"), "Minhas Notas")).pack(pady=5)

    ttk.Button(frame_botoes, text="Presença", width=20,
               command=lambda: atualizar_conteudo(
                   ler_dados(nome_usuario.lower().capitalize(), "presenca"), "Minhas Presenças")).pack(pady=5)

    ttk.Button(frame_botoes, text="Tarefas", width=20,
               command=lambda: atualizar_conteudo(
                   ler_dados(nome_usuario.lower().capitalize(), "tarefa"), "Minhas Tarefas")).pack(pady=5)

    ttk.Button(frame_botoes, text="Sair", width=20, command=sair).pack(pady=30)

# ======================================================================================================
# TELA DE LOGIN (INÍCIO DA APLICAÇÃO)
# ======================================================================================================

# primeira tela - login
login = tk.Tk()
login.title("Sistema Academico")
login.geometry('600x400')
    
# Define um estilo (tema moderno)
style = ttk.Style()
style.theme_use("clam")  # você pode testar: 'clam', 'alt', 'default', 'vista', 'xpnative'

# CAMPOS DA TELA LOGIN ----------------------------------------
# email
campo_email = ttk.Label(login,text='Email', font=('Arial', 12))
campo_email.pack(pady = 20)
entrada_email = ttk.Entry(login, width=30)
entrada_email.pack(pady = 10) #pady espaço na vertical 

# senha
campo_senha = ttk.Label(login, text='Senha', font=('Arial', 12))
campo_senha.pack(pady = 20)
entrada_senha = ttk.Entry(login, width=30, show= "*") # show='*' oculta a senha
entrada_senha.pack(pady = 10)

# para exibir o resultado login
resultado_label = ttk.Label(login, text="") 
resultado_label.pack(pady=25)


def fazer_login(event=None):  # event=None permite ser chamada pelo botão e pela tecla Enter
    email = entrada_email.get()
    senha = entrada_senha.get()

    usuarios = ler_usuarios()
    usuario_logado = next((user for user in usuarios if user['email'] == email and user['senha'] == senha), None)

    if usuario_logado:
        resultado_label.config(text="Login realizado com sucesso!", foreground="green")
        
        login.withdraw()  # esconde as abas sem "destruir"

        if usuario_logado['tipo'] == "administrador":
            janela_administrador(login, usuario_logado)

        elif usuario_logado['tipo'] == "professor":
            janela_professor(login, usuario_logado)

        elif usuario_logado['tipo'] == "aluno":
            janela_aluno(login, usuario_logado)
            
    else:
        resultado_label.config(text="Email ou senha incorretos.", foreground="red")

# BOTÃO - estilo personalizado
style.configure(
    "Custom.TButton",
    font=("Arial", 16, "bold"),
    padding=(20, 15),  # (horizontal, vertical)
    background="#007ACC",
    foreground="white"
)

# Corrigir a cor de fundo no tema "clam"
style.map(
    "Custom.TButton",
    background=[("active", "#005B99"), ("!disabled", "#007ACC")], 
    foreground=[("active", "white")]
)

# botao de login
bt_entrar = ttk.Button(
    login,
    text="Cadastrar",
    command=fazer_login,
    style="Custom.TButton" #aplica o estilo que criamos
)
bt_entrar.pack(pady=25)

# Adiciona a funcionalidade de login ao pressionar Enter
login.bind('<Return>', fazer_login)

# Inicia a aplicação
login.mainloop()