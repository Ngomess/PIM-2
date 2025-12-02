import tkinter as tk 
from tkinter import ttk


def janela_coordenador():
    coordenador = tk.Toplevel()
    coordenador.title("Painel do Coordenador")
    coordenador.geometry("600x400")
    ttk.Label(coordenador, text="Bem-vindo, Coordenador!", font=('Arial', 16)).pack(pady=40)


    ttk.Button(coordenador, text="Sair", command=coordenador.destroy).pack()

    # INFORMAÇÃO NO CANTO SUPERIOR DIREITO - NOME/EMAIL
    info_user = ttk.Label(
        coordenador, 
        text= "Usuário: Coordenador\nEmail: Coordenador@escola.com", 
        font=('Arial', 10),
        foreground='black'
    )
    info_user.place(
        relx=1.0,    # 100% da largura da janela (canto direito)
        rely=0.0,    # 0% da altura da janela (canto superior)
        anchor='ne', # O ponto 'ne' (canto superior direito) do widget é ancorado em (relx, rely)
        x=-10,       # Um pequeno deslocamento de 10 pixels para a esquerda (margem)
        y=10         # Um pequeno deslocamento de 10 pixels para baixo (margem)
    )

def janela_professor():
    prof = tk.Toplevel()
    prof.title("Painel do Professor")
    prof.geometry("600x400")
    ttk.Label(prof, text="Bem-vindo, Professor!", font=('Arial', 16)).pack(pady=40)
    #ttk.Button(prof, text="Sair", command=prof.destroy).pack()

#BOTOES ABA (opçoes) PROFESSOR
    ttk.Button(prof, text="Area de Presença", font=('Arial', 14 ), command=lancar_presenca).pack(pady=15)
    ttk.Button(prof, text="Notas", font=('Arial', 14 ), command=lancar_notas).pack(pady=15)
    ttk.Button(prof, text="Disciplina",font= ('Arial', 14), command= lancar_tarefas).pack(pady=15)
    ttk.Button(prof, text="Sair", command=prof.destroy).pack() #botao sair aba opçoes

    # INFORMAÇÃO NO CANTO SUPERIOR DIREITO - NOME/EMAIL
    info_user = ttk.Label(
        prof, 
        text= "Usuário: Professor\nEmail: Professor@escola.com", 
        font=('Arial', 10),
        foreground='black'
    )
    info_user.place(
        relx=1.0,    # 100% da largura da janela (canto direito)
        rely=0.0,    # 0% da altura da janela (canto superior)
        anchor='ne', # O ponto 'ne' (canto superior direito) do widget é ancorado em (relx, rely)
        x=-10,       # Um pequeno deslocamento de 10 pixels para a esquerda (margem)
        y=10         # Um pequeno deslocamento de 10 pixels para baixo (margem)
    )


def lancar_presenca(): 
    janela_presenca= tk.Toplevel() #Cria uma nova janela
    janela_presenca.title("Lançamento de Presença")
    janela_presenca.geometry("800x600")
    
    ttk.Label(janela_presenca, text="Área de Lançamento de Presença", font=('Arial', 18)).pack(pady=50)
    ttk.Button(janela_presenca, text="Fechar", command=janela_presenca.destroy).pack()

def lancar_notas():
    
    janela_notas = tk.Toplevel()
    janela_notas.title("Lançamento de Notas")
    janela_notas.geometry("800x600")

    ttk.Label(janela_notas, text="Área de Lançamento de Notas", font=('Arial', 18)).pack(pady=50)
    ttk.Button(janela_notas, text="Fechar", command=janela_notas.destroy).pack()

def lancar_tarefas():
    janela_tarefas = tk.Toplevel()#Cria uma nova janela
    janela_tarefas.title("Gestão de Disciplinas/Tarefas")
    janela_tarefas.geometry("800x600")    

    ttk.Label(janela_tarefas, text="Área de Gestão de Disciplinas e Tarefas", font=('Arial', 18)).pack(pady=50)

#ttk.Button(janela_tarefas, text="Fechar", command=janela_tarefas.destroy).pack()

def janela_aluno():
    aluno = tk.Toplevel()
    aluno.title("Painel do Aluno")
    aluno.geometry("600x400")
    ttk.Label(aluno, text="Bem-vindo, Aluno!", font=('Arial', 16)).pack(pady=40)
    ttk.Button(aluno, text="Sair", command=aluno.destroy).pack()
   
# INFORMAÇÃO NO CANTO SUPERIOR DIREITO - NOME/EMAIL
    info_user = ttk.Label(
        aluno, 
        text= "Usuário: Aluno\nEmail: Aluno@escola.com", 
        font=('Arial', 10),
        foreground='black'
    )
    info_user.place(
        relx=1.0,    # 100% da largura da janela (canto direito)
        rely=0.0,    # 0% da altura da janela (canto superior)
        anchor='ne', # O ponto 'ne' (canto superior direito) do widget é ancorado em (relx, rely)
        x=-10,       # Um pequeno deslocamento de 10 pixels para a esquerda (margem)
        y=10         # Um pequeno deslocamento de 10 pixels para baixo (margem)
    )

# tela 
login = tk.Tk()
login.title("Sistema Academico")
login.geometry('600x400')
    
# Define um estilo (tema moderno)
style = ttk.Style()
style.theme_use("clam")  # você pode testar: 'clam', 'alt', 'default', 'vista', 'xpnative'

#CAMPOS DA TELA LOGIN ----------------------------------------
#email
campo_email = ttk.Label(login,text='Email', font=('Arial', 12))
campo_email.pack(pady = 20)
entrada_email = ttk.Entry(login, width=30)
entrada_email.pack(pady = 10) #pady espaço na vertical 

#senha
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

    try: 
        with open("teste_login.txt", "r") as arquivo: 
            for linha in arquivo: 
                usuario, senha_arquivo, tipo = linha.strip().split(",") 
                # strip() só limpa as extremidades, espaços em branco/ split() um separador, parte o texto em pedaços
                
                if email == usuario and senha == senha_arquivo:
                    resultado_label.config(text="Login realizado com sucesso!")
                    
                    login.withdraw()  # esconde as abas sem "destruir"

                    if tipo == "Coordenador":
                        janela_coordenador()

                    elif tipo == "professor":
                        janela_professor()

                    elif tipo == "aluno":
                        janela_aluno()
                        
                    return  #vai sair da função após o login der certo
        
        resultado_label.config(text="Email ou senha incorretos.", foreground="red")  #caso for digitado erro em algum dos campos no login aparecera a mensagem

    except FileNotFoundError:
        resultado_label.config(text="Perfil de usuário não encontrado.", foreground="red") #ttk nao usa fg e sim foreground para cor das letras! 


#BOTÃO - estilo personalizado

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
    #active -> quando o botão é pressionado é tal cor
    #!disabled -> quando está ativo é tal cor
)

# botao de login
bt_entrar = ttk.Button(
    login,
    text="Entrar",
    command=fazer_login,
    style="Custom.TButton" #aplica o estilo que criamos
)
bt_entrar.pack(pady=25)

login.mainloop()
a
