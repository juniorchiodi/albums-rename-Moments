import tkinter as tk
from tkinter import filedialog, messagebox
import os
from album_renamer_logic import rename

import time

class RenamerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Renomear Albuns - Moments Eventos")
        try:
            # For Windows
            self.state('zoomed')
        except tk.TclError:
            # Fallback for other OSes if 'zoomed' state is not available
            self.attributes('-zoomed', True)

        # Define colors
        self.RED_COLOR = "#E60023"
        self.WHITE_COLOR = "#FFFFFF"
        self.BLACK_COLOR = "#282828"
        self.SUCCESS_GREEN = "#4CAF50"
        self.ERROR_RED = "#F44336"
        self.WARNING_YELLOW = "#FFC107"

        # Path variable
        self.folder_path = tk.StringVar()

        self.create_widgets()
        self.configure_tags()

    def configure_tags(self):
        """Configure tags for colored text in the log."""
        self.log_text.tag_config("success", foreground=self.SUCCESS_GREEN)
        self.log_text.tag_config("error", foreground=self.ERROR_RED)
        self.log_text.tag_config("warning", foreground=self.WARNING_YELLOW)
        self.log_text.tag_config("info", foreground=self.BLACK_COLOR, font=("Helvetica", 11, "bold"))
        self.log_text.tag_config("summary", foreground=self.WHITE_COLOR, font=("Helvetica", 12, "bold"))
        self.log_text.tag_config("folder", foreground="#00BCD4", font=("Helvetica", 11, "bold")) # Cyan for folder names

    def create_widgets(self):
        """Creates and arranges all the widgets in the window."""
        self.configure(bg=self.WHITE_COLOR)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Top bar for Logo & Title ---
        top_frame = tk.Frame(self, bg=self.WHITE_COLOR, padx=10, pady=10)
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(top_frame, text="Renomeador de Álbuns", bg=self.WHITE_COLOR, fg=self.BLACK_COLOR, font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, sticky="w")

        try:
            unresized_logo = tk.PhotoImage(file="assets/logo.png")
            # Resize the image by a factor of 10 to make it smaller
            self.logo_image = unresized_logo.subsample(10, 10)
            logo_label = tk.Label(top_frame, image=self.logo_image, bg=self.WHITE_COLOR)
            logo_label.grid(row=0, column=1, sticky="e")
        except tk.TclError:
            logo_label = tk.Label(top_frame, text="Moments Eventos", bg=self.WHITE_COLOR, fg=self.RED_COLOR, font=("Helvetica", 16, "bold"))
            logo_label.grid(row=0, column=1, sticky="e")

        # --- Controls Frame ---
        controls_frame = tk.Frame(self, bg=self.WHITE_COLOR, padx=20, pady=10)
        controls_frame.grid(row=1, column=0, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)

        select_button = tk.Button(controls_frame, text="Selecionar Pasta", command=self.select_folder, bg=self.RED_COLOR, fg=self.WHITE_COLOR, font=("Helvetica", 12, "bold"), relief=tk.FLAT, padx=10, pady=5)
        select_button.grid(row=0, column=0, sticky="w")

        self.folder_label = tk.Label(controls_frame, text="Nenhuma pasta selecionada", bg=self.WHITE_COLOR, fg=self.BLACK_COLOR, font=("Helvetica", 12))
        self.folder_label.grid(row=0, column=1, sticky="w", padx=(10, 0))

        start_num_label = tk.Label(controls_frame, text="Nº do Último Álbum:", bg=self.WHITE_COLOR, fg=self.BLACK_COLOR, font=("Helvetica", 12))
        start_num_label.grid(row=0, column=2, padx=(20, 5))

        self.start_num_entry = tk.Entry(controls_frame, font=("Helvetica", 12), width=10)
        self.start_num_entry.insert(0, "0")
        self.start_num_entry.grid(row=0, column=3, sticky="e")

        # --- Log display ---
        log_frame = tk.Frame(self, bg=self.WHITE_COLOR)
        log_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 10))
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, bg=self.BLACK_COLOR, fg=self.WHITE_COLOR, font=("Consolas", 10), relief=tk.SOLID, wrap=tk.WORD, bd=1)
        self.log_text.grid(row=0, column=0, sticky="nsew")

        # --- Action Button Frame ---
        bottom_frame = tk.Frame(self, bg=self.WHITE_COLOR, padx=20, pady=10)
        bottom_frame.grid(row=3, column=0, sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.rename_button = tk.Button(bottom_frame, text="RENOMEAR ÁLBUNS", command=self.start_renaming, bg=self.RED_COLOR, fg=self.WHITE_COLOR, font=("Helvetica", 14, "bold"), relief=tk.FLAT, padx=20, pady=10)
        self.rename_button.grid(row=0, column=0, sticky="ew")

    def select_folder(self):
        path = filedialog.askdirectory(title="Selecione a pasta que contém os álbuns")
        if not path: return

        self.folder_path.set(path)
        self.folder_label.config(text=f".../{os.path.basename(path)}")

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Pastas encontradas para renomear:\n\n", "info")

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
        self.rename_button.config(state=tk.DISABLED)
        path = self.folder_path.get()
        if not path:
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")
            self.rename_button.config(state=tk.NORMAL)
            return

        try:
            start_num = int(self.start_num_entry.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Por favor, insira um número válido para o 'Nº do Último Álbum'.")
            self.rename_button.config(state=tk.NORMAL)
            return

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Iniciando processo de renomeação...\n\n", "info")
        self.update_idletasks()

        start_time = time.time()
        try:
            for message in rename(path, start_num + 1):
                tag = None
                if message.startswith("✅"):
                    tag = "success"
                elif message.startswith("❌"):
                    tag = "error"
                elif message.startswith("⚠️"):
                    tag = "warning"
                elif "Processando pasta:" in message:
                    tag = "folder"
                elif "Total de arquivos na pasta" in message:
                    tag = "info"

                self.log_text.insert(tk.END, f"{message}\n", tag)
                self.log_text.see(tk.END)
                self.update_idletasks()

            end_time = time.time()
            duration = end_time - start_time
            summary_message = f"\nPROCESSO CONCLUÍDO em {duration:.2f} segundos."
            self.log_text.insert(tk.END, summary_message, "summary")
            messagebox.showinfo("Sucesso", "Todos os álbuns foram renomeados com sucesso!")
            self.rename_button.config(text="Renomear outra pasta", command=self.reset_app, state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro durante a renomeação:\n{e}")
            self.rename_button.config(state=tk.NORMAL)

    def reset_app(self):
        """Resets the application state for a new operation."""
        self.folder_path.set("")
        self.folder_label.config(text="Nenhuma pasta selecionada")

        self.start_num_entry.delete(0, tk.END)
        self.start_num_entry.insert(0, "0")

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Interface resetada. Selecione uma nova pasta para começar.", "info")

        self.rename_button.config(text="RENOMEAR ÁLBUNS", command=self.start_renaming)

if __name__ == "__main__":
    app = RenamerApp()
    app.mainloop()
