import tkinter as tk 
from tkinter import ttk

    # tela 
login = tk.Tk()
login.title("Sistema Academico")
login.geometry('500x400')
    

#botoes tela login 

#email
campo_email = tk.Label(login,text='Email', font=('Arial', 12))
campo_email.pack(pady = 20)
entrada_email = tk.Entry(login, width=30)
entrada_email.pack(pady = 10) #pady espaço na vertical 

#senha
campo_senha = tk.Label(login, text='Senha', font=('Arial', 12))
campo_senha.pack(pady = 20)
entrada_senha = tk.Entry(login, width=30, show= "*") # show='*' oculta a senha
entrada_senha.pack(pady = 10)

# para exibir o resultado login
resultado_label = tk.Label(login, text="") 
resultado_label.pack(pady=25)

def fazer_login():
    email = entrada_email.get()
    senha = entrada_senha.get()

    try: 
        with open("teste_pim.txt", "w") as arquivo: 
            for linha in arquivo: 
                usuario, entrada_senha, senha = linha.strip().split(",") 
                # strip() só limpa as extremidades, espaços em branco/ split() um separador, parte o texto em pedaços
                if email == usuario and senha == entrada_senha:
                    resultado_label.config(text="Login realizado com sucesso!")
                    return
    except ValueError:
        resultado_label.config(text="Perfil de usuário não encontrado.", fg="red")

#botao de enter - login

#bt_entrar = tk.Button(login, text="Entrar", command= fazer_login, font=('Arial', 16))
#bt_entrar.pack(pady=5)


bt_entrar = tk.Button(
    login, 
    text="Entrar", 
    command= fazer_login, 
    font=('Arial', 16),
    pady=15,
    padx=10,
)
bt_entrar.pack(pady=5)

login.mainloop()