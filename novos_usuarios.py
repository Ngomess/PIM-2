import tkinter as tk 
from tkinter import ttk


def janela_admin():
    admin = tk.Toplevel()
    admin.title("Painel do Administrador")
    admin.geometry("600x400")
    ttk.Label(admin, text="Bem-vindo, Administrador!", font=('Arial', 16)).pack(pady=40)
    ttk.Button(admin, text="Sair", command=admin.destroy).pack()


def janela_professor():
    prof = tk.Toplevel()
    prof.title("Painel do Professor")
    prof.geometry("600x400")
    ttk.Label(prof, text="Bem-vindo, Professor!", font=('Arial', 16)).pack(pady=40)
    ttk.Button(prof, text="Sair", command=prof.destroy).pack()


def janela_aluno():
    aluno = tk.Toplevel()
    aluno.title("Painel do Aluno")
    aluno.geometry("600x400")
    ttk.Label(aluno, text="Bem-vindo, Aluno!", font=('Arial', 16)).pack(pady=40)
    ttk.Button(aluno, text="Sair", command=aluno.destroy).pack()
   

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

                    if tipo == "admin":
                        janela_admin()

                    elif tipo == "professor":
                        janela_professor()

                    elif tipo == "aluno":
                        janela_aluno()
                        
                    return
                
    except ValueError:
        resultado_label.config(text="Perfil de usuário não encontrado.", foreground="red") #ttk nao usa fg e sim foreground para cor das letras! 
        login.destroy()


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