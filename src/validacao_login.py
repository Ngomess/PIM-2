import tkinter as tk 
from tkinter import ttk

# tela 
login = tk.Tk()
login.title("Sistema Academico")
login.geometry('600x400')
    
# Define um estilo (tema moderno)
style = ttk.Style()
style.theme_use("clam")  # você pode testar: 'clam', 'alt', 'default', 'vista', 'xpnative'

#botoes tela login 

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

def fazer_login():
    email = entrada_email.get()
    senha = entrada_senha.get()

    try: 
        with open("teste_login.txt", "r") as arquivo: 
            for linha in arquivo: 
                usuario, entrada_senha = linha.strip().split(",") 
                # strip() só limpa as extremidades, espaços em branco/ split() um separador, parte o texto em pedaços
                
                if email == usuario and senha == entrada_senha:
                    resultado_label.config(text="Login realizado com sucesso!")
                    login.destroy()
                    return
                
    except ValueError:
        resultado_label.config(text="Perfil de usuário não encontrado.", foreground="red") #ttk nao usa fg e sim foreground para cor das letras! 
        login.destroy()

#botao de enter - login
#bt_entrar = tk.Button(login, text="Entrar", command= fazer_login, font=('Arial', 16))
#bt_entrar.pack(pady=5)

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
