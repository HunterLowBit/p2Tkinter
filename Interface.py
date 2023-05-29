import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox
from tkinter import simpledialog

# Função para validar as credenciais do usuário
def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (usuario, senha))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        frame_login.pack_forget()
        if user[3] == 1:  # Usuário administrador
            frame_administrativo.pack()
            listar_produtos_admin()
        else:
            frame_usuario.pack()

        listar_produtos()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")
        entry_usuario.delete(0, tk.END)
        entry_senha.delete(0, tk.END)

    conn.close()

# Função para exibir a tela de login
def mostrar_login():
    frame_administrativo.pack_forget()
    frame_usuario.pack_forget()
    frame_login.pack()

    entry_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT, admin INTEGER)")

    conn.commit()
    conn.close()

def cadastrar_produto():
    nome_produto = entry_nome.get()
    quantidade = entry_quantidade.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome_produto, quantidade))

    conn.commit()
    conn.close()

    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)

    listar_produtos()  # Atualiza a lista de produtos

    if frame_administrativo.winfo_ismapped():
        listar_produtos_admin()

# Função para listar os produtos cadastrados
def listar_produtos():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()

    # Exibe os produtos na lista
    listbox_itens.delete(0, tk.END)
    for row in rows:
        listbox_itens.insert(tk.END, f"{row[1]} - Quantidade: {row[2]}")

    conn.close()

# Função para listar os produtos cadastrados (tela de administração)
def listar_produtos_admin():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()

    # Exibe os produtos na lista
    listbox_itens.delete(0, tk.END)
    for row in rows:
        listbox_itens.insert(tk.END, f"{row[0]} - {row[1]} - Quantidade: {row[2]}")

    conn.close()

# Função para remover produtos existentes
def remover_produto():
    selected_product = listbox_itens.curselection()
    if selected_product:
        product = listbox_itens.get(selected_product)
        product_name = product.split(" - ")[0]

        conn = sqlite3.connect("almoxarifado.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM produtos WHERE nome=?", (product_name,))
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
        
        conn.commit()
        conn.close()

        listar_produtos()
        if frame_administrativo.winfo_ismapped():
            listar_produtos_admin()


# Função para listar os produtos cadastrados (tela de administração)
def listar_produtos_admin():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()

    # Exibe os produtos na lista
    listbox_itens.delete(0, tk.END)
    for row in rows:
        listbox_itens.insert(tk.END, f"{row[0]} - {row[1]} - Quantidade: {row[2]}")

    conn.close()


# Função para fazer logout
def fazer_logout():
    frame_usuario.pack_forget()
    frame_administrativo.pack_forget()
    mostrar_login()
    messagebox.showinfo("Sucesso", "Logout realizado com sucesso!")

# Função para adicionar um novo usuário (admin)
def cadastrar_usuario():
    nome_usuario = entry_nome_usuario.get()
    senha = entry_senha_usuario.get()
    admin = int(var_admin.get())

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO usuarios (nome, senha, admin) VALUES (?, ?, ?)", (nome_usuario, senha, admin))

    conn.commit()
    conn.close()

    entry_nome_usuario.delete(0, tk.END)
    entry_senha_usuario.delete(0, tk.END)
    var_admin.set(0)

    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

# Função para remover um usuário (admin)
def remover_usuario():
    selected_user = listbox_usuarios.curselection()
    if selected_user:
        user_id = listbox_usuarios.get(selected_user).split(" - ")[0]

        conn = sqlite3.connect("almoxarifado.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id=?", (user_id,))

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
        listar_usuarios()

# Função para listar os usuários cadastrados (admin)
def listar_usuarios():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()

    # Exibe os usuários na lista
    listbox_usuarios.delete(0, tk.END)
    for row in rows:
        user_info = f"{row[0]} - {row[1]}"
        if row[3] == 1:
            user_info += " (Admin)"
        listbox_usuarios.insert(tk.END, user_info)

    conn.close()

def alterar_senha_usuario():
    selected_user = listbox_usuarios.curselection()
    if selected_user:
        user_id = listbox_usuarios.get(selected_user).split(" - ")[0]

        # Exibir uma nova janela ou caixa de diálogo para solicitar a nova senha
        nova_senha = tk.simpledialog.askstring("Alterar Senha", "Digite a nova senha para o usuário:")

        if nova_senha:
            conn = sqlite3.connect("almoxarifado.db")
            cursor = conn.cursor()

            cursor.execute("UPDATE usuarios SET senha=? WHERE id=?", (nova_senha, user_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Senha do usuário alterada com sucesso!")
            listar_usuarios()
            

# Função para alterar as informações de um produto existente
def alterar_produto():
    selected_product = listbox_itens.curselection()
    if selected_product:
        product = listbox_itens.get(selected_product)
        product_id = product.split(" - ")[0]

        # Criar uma nova janela para solicitar as novas informações do produto
        nova_janela = tk.Toplevel(root)
        nova_janela.title("Alterar Produto")

        label_nova_quantidade = tk.Label(nova_janela, text="Digite a nova quantidade para o produto:")
        label_nova_quantidade.pack()

        entry_nova_quantidade = tk.Entry(nova_janela)
        entry_nova_quantidade.pack()

        button_confirmar = tk.Button(nova_janela, text="Confirmar", command=lambda: atualizar_quantidade(entry_nova_quantidade.get(), product_id, nova_janela))
        button_confirmar.pack()

        nova_janela.focus_set()

# Função para atualizar a quantidade do produto no banco de dados
def atualizar_quantidade(nova_quantidade, product_id, janela):
    if nova_quantidade:
        conn = sqlite3.connect("almoxarifado.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE produtos SET quantidade=? WHERE id=?", (nova_quantidade, product_id))

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
        listar_produtos()

        janela.destroy()



# Criar a janela principal
root = tk.Tk()
root.title("Almoxarifado")
root.geometry("400x400")

# Criar os frames
frame_login = tk.Frame(root)
frame_administrativo = tk.Frame(root)
frame_usuario = tk.Frame(root)

# Label de hora
label_hora = tk.Label(frame_usuario, text="")
label_hora.pack()

# Widgets para a tela de login
label_usuario = tk.Label(frame_login, text="Usuário:")
label_usuario.pack()

entry_usuario = tk.Entry(frame_login)
entry_usuario.pack()

label_senha = tk.Label(frame_login, text="Senha:")
label_senha.pack()

entry_senha = tk.Entry(frame_login, show="*")
entry_senha.pack()

button_login = tk.Button(frame_login, text="Login", command=fazer_login)
button_login.pack()

# Widgets para cadastro de produto
label_nome = tk.Label(frame_usuario, text="Nome do Produto:")
label_nome.pack()

entry_nome = tk.Entry(frame_usuario)
entry_nome.pack()

label_quantidade = tk.Label(frame_usuario, text="Quantidade:")
label_quantidade.pack()

entry_quantidade = tk.Entry(frame_usuario)
entry_quantidade.pack()

button_cadastrar_produto = tk.Button(frame_usuario, text="Cadastrar Produto", command=cadastrar_produto)
button_cadastrar_produto.pack()

button_fazer_logout = tk.Button(frame_usuario, text="Logout", command=fazer_logout)
button_fazer_logout.pack()

# Lista de produtos
listbox_itens = tk.Listbox(frame_usuario, width=50)
listbox_itens.pack()

# Botão para remover produto
button_remover_produto = tk.Button(frame_usuario, text="Remover Produto", command=remover_produto)
button_remover_produto.pack()

# Widgets para a tela de administração
button_fazer_logout = tk.Button(frame_administrativo, text="Logout", command=fazer_logout)
button_fazer_logout.pack()

# Widgets para cadastro de usuário (admin)
label_nome_usuario = tk.Label(frame_administrativo, text="Nome do Usuário:")
label_nome_usuario.pack()

entry_nome_usuario = tk.Entry(frame_administrativo)
entry_nome_usuario.pack()

label_senha_usuario = tk.Label(frame_administrativo, text="Senha:")
label_senha_usuario.pack()

entry_senha_usuario = tk.Entry(frame_administrativo, show="*")
entry_senha_usuario.pack()

label_admin = tk.Label(frame_administrativo, text="Admin:")
label_admin.pack()

var_admin = tk.IntVar()
check_admin = tk.Checkbutton(frame_administrativo, text="Administrador", variable=var_admin)
check_admin.pack()

button_cadastrar_usuario = tk.Button(frame_administrativo, text="Cadastrar Usuário", command=cadastrar_usuario)
button_cadastrar_usuario.pack()

# Lista de usuários (admin)
listbox_usuarios = tk.Listbox(frame_administrativo, width=40)
listbox_usuarios.pack()

button_remover_usuario = tk.Button(frame_administrativo, text="Remover Usuário", command=remover_usuario)
button_remover_usuario.pack()

button_alterar_senha_usuario = tk.Button(frame_administrativo, text="Alterar Senha do Usuário", command=alterar_senha_usuario)
button_alterar_senha_usuario.pack()

button_alterar_quantidade = tk.Button(frame_usuario, text="Alterar Produto", command=alterar_produto)
button_alterar_quantidade.pack()

# Inicializar o banco de dados e criar as tabelas se não existirem
criar_tabelas()

# Exibir a tela de login no início
mostrar_login()


# Atualiza o horário dinamicamente
def atualizar_hora():
    hora_atual = datetime.now().strftime("%H:%M:%S")
    label_hora.config(text="Hora atual: " + hora_atual)
    label_hora.after(1000, atualizar_hora)

atualizar_hora()

# Atualiza a janela a cada 10 segundos
def atualizar_janela():
    listar_produtos()
    if frame_administrativo.winfo_ismapped():
        listar_produtos_admin()
        listar_usuarios()

    root.after(10000, atualizar_janela)


root.mainloop()
