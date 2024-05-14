import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if is_admin():
        # Se já estiver rodando como administrador, execute o script normalmente
        excluir_usuario_e_pasta("bem-vindo")
    else:
        # Caso contrário, execute novamente como administrador
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )


def excluir_usuario_e_pasta(username):
    # Verificar se o usuário existe
    try:
        subprocess.check_output(["net", "user", username], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", f"O usuário '{username}' não existe.")
        return

    # Excluir o usuário
    try:
        subprocess.check_output(
            ["net", "user", username, "/delete"], stderr=subprocess.STDOUT
        )
        messagebox.showinfo("Sucesso", f"Usuário '{username}' excluído com sucesso.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror(
            "Erro",
            f"Erro ao excluir o usuário '{username}': {e.output.decode('utf-8')}",
        )
        return

    # Excluir a pasta do usuário
    try:
        user_folder = os.path.join("C:\\Users", username)
        subprocess.check_output(
            ["rd", "/s", "/q", user_folder], stderr=subprocess.STDOUT
        )
        messagebox.showinfo(
            "Sucesso", f"Pasta do usuário '{username}' excluída com sucesso."
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror(
            "Erro",
            f"Erro ao excluir a pasta do usuário '{username}': {e.output.decode('utf-8')}",
        )


if __name__ == "__main__":
    # Verificar se está rodando como administrador
    if not is_admin():
        run_as_admin()
    else:
        # Criar uma janela Tkinter
        root = tk.Tk()
        root.withdraw()  # Ocultar a janela principal

        # Chamar a função para excluir o usuário "Bem-vindo" e sua pasta
        excluir_usuario_e_pasta("bem-vindo")
