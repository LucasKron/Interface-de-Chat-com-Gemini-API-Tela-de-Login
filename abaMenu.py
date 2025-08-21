import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog
import google.generativeai as genai
import base64

genai.configure(api_key="")  

modelo = genai.GenerativeModel('gemini-1.5-flash')

def responder_ia(dados):
    try:
        if isinstance(dados, tuple):
            mensagem, imagem_b64 = dados
            
            resposta = modelo.generate_content([mensagem, {"mime_type": "image/png", "data": imagem_b64}])
        else:
            resposta = modelo.generate_content(dados)
        return resposta.text
    except Exception as e:
        return f"IA: Erro: {str(e)}"

def criar_menu(app):
    label = ctk.CTkLabel(app, text='Bem-vindo ao Chat!')
    label.pack(pady=10)

    texto_inteligente = ctk.CTkLabel(app, text='Chat com IA Gemini')
    texto_inteligente.pack(pady=5)

    caixa_chat = ctk.CTkTextbox(app, width=600, height=400)
    caixa_chat.pack(pady=(10, 10))

    texto_usuario = ctk.CTkEntry(app, placeholder_text='Digite sua mensagem aqui')
    texto_usuario.place(relx=0.05, rely=1.0, anchor='sw', relwidth=0.75, y=-10)

    def fechar_imagem():
        label_imagem.configure(image=None, text="")
        label_imagem.image = None
        label_imagem.caminho = None
        botao_fechar.place_forget() 

    botao_fechar = ctk.CTkButton(app, text="✖", width=15, height=15, command=fechar_imagem)
    botao_fechar.configure(fg_color="transparent", bg_color="transparent")

    def anexar_arquivo():
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if file_path:
            imagem = Image.open(file_path)
            imagem = imagem.resize((50, 50))
            imagem_tk = ImageTk.PhotoImage(imagem)

            label_imagem.configure(image=imagem_tk)
            label_imagem.place(x=60, y=510)
            label_imagem.image = imagem_tk  
            label_imagem.caminho = file_path   
            botao_fechar.place(x=100, y=505)

    label_imagem = ctk.CTkLabel(app, text="")
    label_imagem.pack(pady=10)

    def enviar_mensagem():
        mensagem = texto_usuario.get()
        if mensagem.strip() == "" and not getattr(label_imagem, "caminho", None):
            return
        caixa_chat.insert("end", f"Você: {mensagem}\n")
        app.update()
        if getattr(label_imagem, "caminho", None):
            with open(label_imagem.caminho, "rb") as img_file:
                imagem_bytes = img_file.read()
                imagem_b64 = base64.b64encode(imagem_bytes).decode('utf-8')
            resposta = responder_ia((mensagem, imagem_b64))
            caixa_chat.insert("end", f"IA: {resposta}\n\n")
            fechar_imagem()
        else:
            resposta = responder_ia(mensagem)
            caixa_chat.insert("end", f"IA: {resposta}\n\n")
        texto_usuario.delete(0, 'end')

    botao_enviar = ctk.CTkButton(app, text="Enviar", command=enviar_mensagem)
    botao_enviar.place(relx=0.83, rely=1.0, anchor='sw', relwidth=0.12,x=8, y=-10)

    icone_anexar = Image.open("paperclip-solid-full.png")
    icone_anexar = icone_anexar.resize((20, 20))
    foto = ImageTk.PhotoImage(icone_anexar)

    botao_anexar = ctk.CTkButton(app, text="", image=foto, command=anexar_arquivo)
    botao_anexar.place(relx=0.83, rely=1.0, anchor='sw', relwidth=0.03,x = -20, y=-10)

    texto_usuario.bind("<Return>", lambda event: enviar_mensagem())

