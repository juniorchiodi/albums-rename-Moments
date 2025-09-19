import tkinter as tk
from tkinter import filedialog, messagebox
import os
from album_renamer_logic import rename

class RenamerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Renomear Albuns - Moments Eventos")
        self.geometry("800x600")
        self.configure(bg="#FFFFFF") # White background

        # Define colors
        self.RED_COLOR = "#E60023" # A common 'YouTube' red, good for contrast
        self.WHITE_COLOR = "#FFFFFF"
        self.BLACK_COLOR = "#282828"

        # Path variable
        self.folder_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # --- Main container ---
        main_frame = tk.Frame(self, bg=self.WHITE_COLOR, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Top bar for Logo ---
        top_frame = tk.Frame(main_frame, bg=self.WHITE_COLOR)
        top_frame.pack(fill=tk.X)

        try:
            # Note: User requested 'logo preto.png', but it was not found. Using 'logo.png'.
            self.logo_image = tk.PhotoImage(file="assets/logo.png")
            logo_label = tk.Label(top_frame, image=self.logo_image, bg=self.WHITE_COLOR)
            logo_label.pack(side=tk.RIGHT)
        except tk.TclError:
            # Fallback if image fails to load
            logo_label = tk.Label(top_frame, text="Moments Eventos", bg=self.WHITE_COLOR, fg=self.RED_COLOR, font=("Helvetica", 16, "bold"))
            logo_label.pack(side=tk.RIGHT, padx=10)

        title_label = tk.Label(top_frame, text="Renomeador de Álbuns", bg=self.WHITE_COLOR, fg=self.BLACK_COLOR, font=("Helvetica", 24, "bold"))
        title_label.pack(side=tk.LEFT)

        # --- Controls Frame ---
        controls_frame = tk.Frame(main_frame, bg=self.WHITE_COLOR, pady=10)
        controls_frame.pack(fill=tk.X)

        # Folder Selection
        select_button = tk.Button(controls_frame, text="Selecionar Pasta dos Álbuns", command=self.select_folder, bg=self.RED_COLOR, fg=self.WHITE_COLOR, font=("Helvetica", 12, "bold"), relief=tk.FLAT, padx=10, pady=5)
        select_button.grid(row=0, column=0, padx=(0, 10))

        self.folder_label = tk.Label(controls_frame, text="Nenhuma pasta selecionada", bg=self.WHITE_COLOR, fg=self.BLACK_COLOR, font=("Helvetica", 10))
        self.folder_label.grid(row=0, column=1, sticky="w")

        # Starting Number
        start_num_label = tk.Label(controls_frame, text="Nº do Último Álbum (se continuar):", bg=self.WHITE_COLOR, fg=self.BLACK_COLOR, font=("Helvetica", 10))
        start_num_label.grid(row=1, column=0, pady=(10,0), sticky="e")

        self.start_num_entry = tk.Entry(controls_frame, font=("Helvetica", 10), width=10)
        self.start_num_entry.insert(0, "0")
        self.start_num_entry.grid(row=1, column=1, pady=(10,0), sticky="w")

        # --- Log display ---
        log_frame = tk.Frame(main_frame, bg=self.BLACK_COLOR, bd=1, relief=tk.SOLID)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_text = tk.Text(log_frame, bg="#3C3C3C", fg=self.WHITE_COLOR, font=("Consolas", 10), relief=tk.FLAT, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # --- Action Button ---
        rename_button = tk.Button(main_frame, text="RENOMEAR ÁLBUNS", command=self.start_renaming, bg=self.RED_COLOR, fg=self.WHITE_COLOR, font=("Helvetica", 14, "bold"), relief=tk.FLAT, padx=20, pady=10)
        rename_button.pack()

    def select_folder(self):
        path = filedialog.askdirectory(title="Selecione a pasta que contém os álbuns")
        if not path:
            return

        self.folder_path.set(path)
        self.folder_label.config(text=f".../{os.path.basename(path)}")

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Pastas encontradas para renomear:\n\n", "title")

        try:
            subfolders = sorted([p for p in os.listdir(path) if os.path.isdir(os.path.join(path, p))])
            if not subfolders:
                self.log_text.insert(tk.END, "Nenhuma subpasta encontrada no diretório selecionado.")
            else:
                for folder in subfolders:
                    self.log_text.insert(tk.END, f"- {folder}\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler as pastas do diretório:\n{e}")

    def start_renaming(self):
        path = self.folder_path.get()
        if not path:
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")
            return

        try:
            start_num = int(self.start_num_entry.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Por favor, insira um número válido para o 'Nº do Último Álbum'.")
            return

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Iniciando processo de renomeação...\n\n", "title")
        self.update_idletasks()

        try:
            # The rename function is a generator, so we loop through it
            for message in rename(path, start_num + 1):
                self.log_text.insert(tk.END, f"{message}\n")
                self.log_text.see(tk.END) # Scroll to the end
                self.update_idletasks() # Update the GUI to prevent freezing

            self.log_text.insert(tk.END, "\nPROCESSO CONCLUÍDO!", "title")
            messagebox.showinfo("Sucesso", "Todos os álbuns foram renomeados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro durante a renomeação:\n{e}")

if __name__ == "__main__":
    app = RenamerApp()
    app.mainloop()
