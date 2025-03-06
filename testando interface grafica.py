import os
import tkinter as tk
from tkinter import filedialog, messagebox

def renomear_pastas(base_path, i):
    pastas = sorted([p for p in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, p))])
    
    for indice_pasta, pasta in enumerate(pastas, start=i):
        caminho_pasta = os.path.join(base_path, pasta)
        arquivos = sorted(os.listdir(caminho_pasta))

        if len(arquivos) != 17:
            messagebox.showwarning("Erro", f"O Álbum '{pasta}' não tem 17 arquivos (Lâminas). Parando...")
            return
        
        prefixo = f"{indice_pasta:02d}"
        
        for index_arquivo, arquivo in enumerate(arquivos[:-1], start=1):
            extensao = os.path.splitext(arquivo)[1]
            novo_nome = f"{prefixo}-{index_arquivo:03d}{extensao}"
            os.rename(os.path.join(caminho_pasta, arquivo), os.path.join(caminho_pasta, novo_nome))
        
        ultimo_arquivo = arquivos[-1]
        extensao = os.path.splitext(ultimo_arquivo)[1]
        os.rename(os.path.join(caminho_pasta, ultimo_arquivo), os.path.join(caminho_pasta, f"CAPA{extensao}"))
    
    messagebox.showinfo("Sucesso", "Arquivos renomeados com sucesso!")
    root.quit()

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)

def iniciar_renomeacao():
    pasta = entry_pasta.get()
    if checkbox_0.get():
        i = 0
    elif checkbox_custom.get():
        try:
            i = int(entry_numero.get())
        except ValueError:
            messagebox.showwarning("Erro", "Digite um número inteiro válido para o álbum!")
            return
    else:
        messagebox.showwarning("Atenção", "Selecione uma opção de álbum!")
        return
    
    if not pasta:
        messagebox.showwarning("Atenção", "Selecione um diretório válido!")
        return
    
    i = i + 1
    renomear_pastas(pasta, i)

# Função para garantir que apenas um checkbox seja selecionado
def desmarcar_outro(checkbox_marco, checkbox_oposto):
    if checkbox_marco.get():
        checkbox_oposto.set(False)

# Criando a interface gráfica
root = tk.Tk()
root.title("Renomeador de Pastas")
root.geometry("500x250")
root.resizable(False, False)  # Bloqueia a alteração de tamanho da janela

# Centralizar a janela na tela
root.update_idletasks()
width = 500
height = 250
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=20)

label_pasta = tk.Label(frame, text="Selecione a pasta base:")
label_pasta.grid(row=0, column=0, sticky="w")

entry_pasta = tk.Entry(frame, width=40)
entry_pasta.grid(row=1, column=0)

btn_pasta = tk.Button(frame, text="Procurar", command=selecionar_pasta)
btn_pasta.grid(row=1, column=1)

label_opcao = tk.Label(frame, text="Selecione a opção para o álbum:")
label_opcao.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

checkbox_0 = tk.BooleanVar()
cb_0 = tk.Checkbutton(frame, text="Selecione para Primeiro Álbum.", variable=checkbox_0, command=lambda: desmarcar_outro(checkbox_0, checkbox_custom))
cb_0.grid(row=3, column=0, sticky="w")

checkbox_custom = tk.BooleanVar()
cb_custom = tk.Checkbutton(frame, text="Continuar Renomeando (Digite o NÚMERO do último Álbum Renomeado.)", variable=checkbox_custom, command=lambda: desmarcar_outro(checkbox_custom, checkbox_0))
cb_custom.grid(row=4, column=0, sticky="w")

entry_numero = tk.Entry(frame, width=10)
entry_numero.grid(row=4, column=1, sticky="w")
entry_numero.config(state="disabled")  # Inicialmente desabilitado

# Habilitar/desabilitar o campo de número conforme o checkbox
def atualizar_entrada():
    if checkbox_custom.get():
        entry_numero.config(state="normal")
    else:
        entry_numero.config(state="disabled")
        entry_numero.delete(0, tk.END)

cb_custom.config(command=atualizar_entrada)  # Usando o config para o Checkbutton

btn_iniciar = tk.Button(frame, text="Iniciar Renomeação", command=iniciar_renomeacao)
btn_iniciar.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
