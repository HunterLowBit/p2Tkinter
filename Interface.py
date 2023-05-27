
from db import *
import tkinter as tk

# Função para cadastrar um novo item
def cadastrar_item():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO itens (nome, quantidade) VALUES (?, ?)", (nome, quantidade))

    conn.commit()
    conn.close()

    # Limpar os campos de entrada após o cadastro
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)

# Função para listar os itens cadastrados
def listar_itens():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM itens")
    rows = cursor.fetchall()

    # Exibir os itens na janela
    listbox_itens.delete(0, tk.END)
    for row in rows:
        listbox_itens.insert(tk.END, f"Nome: {row[1]} - Quantidade: {row[2]}")

    conn.close()

# Função para fazer login
def fazer_login():
    nome_usuario = entry_usuario.get()
    senha = entry_senha.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome_usuario, senha))
    user = cursor.fetchone()

    if user:
        # Verifica se é um usuário administrativo
        if user[3] == 1:
            # Exibe a área administrativa
            frame_administrativo.pack()
        else:
            # Exibe a área de usuário comum
            frame_usuario.pack()
    else:
        # Exibe uma mensagem de erro se o login falhar
        label_login_error.pack()

    conn.close()

# Função para cadastrar um novo usuário
def cadastrar_usuario():
    nome = entry_novo_usuario.get()
    senha = entry_nova_senha.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))

    conn.commit()
    conn.close()

    # Limpar os campos de entrada após o cadastro
    entry_novo_usuario.delete(0, tk.END)
    entry_nova_senha.delete(0, tk.END)

# Função para excluir um usuário
def excluir_usuario():
    nome = entry_excluir_usuario.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE nome = ?", (nome,))

    conn.commit()
    conn.close()

    # Limpar o campo de entrada após a exclusão
    entry_excluir_usuario.delete(0, tk.END)

# Função para alterar a senha de um usuário
def alterar_senha():
    nome = entry_alterar_usuario.get()
    nova_senha = entry_nova_senha_admin.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE usuarios SET senha = ? WHERE nome = ?", (nova_senha, nome))

    conn.commit()
    conn.close()

    # Limpar os campos de entrada após a alteração
    entry_alterar_usuario.delete(0, tk.END)
    entry_nova_senha_admin.delete(0, tk.END)

# Criação da janela principal
janela = tk.Tk()
janela.title("Almoxarifado")
janela.geometry("400x300")

# Componentes da janela de login
label_usuario = tk.Label(janela, text="Usuário:")
label_usuario.pack()

entry_usuario = tk.Entry(janela)
entry_usuario.pack()

label_senha = tk.Label(janela, text="Senha:")
label_senha.pack()

entry_senha = tk.Entry(janela, show="*")
entry_senha.pack()

button_login = tk.Button(janela, text="Login", command=fazer_login)
button_login.pack()

label_login_error = tk.Label(janela, text="Usuário ou senha inválidos.", fg="red")

# Componentes da área de usuário comum
frame_usuario = tk.Frame(janela)

label_nome = tk.Label(frame_usuario, text="Nome:")
label_nome.pack()

entry_nome = tk.Entry(frame_usuario)
entry_nome.pack()

label_quantidade = tk.Label(frame_usuario, text="Quantidade:")
label_quantidade.pack()

entry_quantidade = tk.Entry(frame_usuario)
entry_quantidade.pack()

button_cadastrar = tk.Button(frame_usuario, text="Cadastrar", command=cadastrar_item)
button_cadastrar.pack()

listbox_itens = tk.Listbox(frame_usuario)
listbox_itens.pack()

button_listar = tk.Button(frame_usuario, text="Listar Itens", command=listar_itens)
button_listar.pack()

# Componentes da área administrativa
frame_administrativo = tk.Frame(janela)

label_novo_usuario = tk.Label(frame_administrativo, text="Novo usuário:")
label_novo_usuario.pack()

entry_novo_usuario = tk.Entry(frame_administrativo)
entry_novo_usuario.pack()

label_nova_senha = tk.Label(frame_administrativo, text="Nova senha:")
label_nova_senha.pack()

entry_nova_senha = tk.Entry(frame_administrativo, show="*")
entry_nova_senha.pack()

button_cadastrar_usuario = tk.Button(frame_administrativo, text="Cadastrar Usuário", command=cadastrar_usuario)
button_cadastrar_usuario.pack()

label_excluir_usuario = tk.Label(frame_administrativo, text="Usuário a excluir:")
label_excluir_usuario.pack()

entry_excluir_usuario = tk.Entry(frame_administrativo)
entry_excluir_usuario.pack()

button_excluir_usuario = tk.Button(frame_administrativo, text="Excluir Usuário", command=excluir_usuario)
button_excluir_usuario.pack()

label_alterar_usuario = tk.Label(frame_administrativo, text="Usuário a alterar senha:")
label_alterar_usuario.pack()

entry_alterar_usuario = tk.Entry(frame_administrativo)
entry_alterar_usuario.pack()

label_nova_senha_admin = tk.Label(frame_administrativo, text="Nova senha:")
label_nova_senha_admin.pack()

entry_nova_senha_admin = tk.Entry(frame_administrativo, show="*")
entry_nova_senha_admin.pack()

button_alterar_senha = tk.Button(frame_administrativo, text="Alterar Senha", command=alterar_senha)
button_alterar_senha.pack()

# Cria as tabelas no banco de dados
criar_tabelas()

# Inicialmente, as áreas de usuário comum e administrativa estão ocultas
frame_usuario.pack_forget()
frame_administrativo.pack_forget()

# Inicia o loop principal da janela
janela.mainloop()