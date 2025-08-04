import customtkinter as ctk 
import abaMenu

ctk.set_appearance_mode('dark')

def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    if usuario == 'admin' and senha == '1234':
        app.destroy()
        nova_janela = ctk.CTk()
        nova_janela.title('Conversa com ia')
        nova_janela.geometry('800x600')
        abaMenu.criar_menu(nova_janela)
        nova_janela.mainloop()
    else:
        resultado_login.configure(text='Login incorreto!', text_color='red')

app = ctk.CTk()

app.title('Sistema de login')
app.geometry('400x300')

label_usuario = ctk.CTkLabel(app, text='Usuario:')
label_usuario.pack(pady=10)

campo_usuario = ctk.CTkEntry(app,placeholder_text='Digite seu usuario')
campo_usuario.pack(pady=10)

label_senha = ctk.CTkLabel(app, text='Senha:')
label_senha.pack(pady=10)

campo_senha = ctk.CTkEntry(app,placeholder_text='Digite sua senha',show='*')
campo_senha.pack(pady=10)

botao_login = ctk.CTkButton(app,text='Login',command=validar_login)
botao_login.pack(pady=10)

resultado_login = ctk.CTkLabel(app,text='')
resultado_login.pack(pady=10)

app.mainloop()