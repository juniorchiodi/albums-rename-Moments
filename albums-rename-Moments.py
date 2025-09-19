import os, sys

def rename(base_path):
    pastas = sorted([p for p in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, p))])
    
    for indice_pasta, pasta in enumerate(pastas, start=i):
        caminho_pasta = os.path.join(base_path, pasta)
        arquivos = sorted(os.listdir(caminho_pasta))

        if len(arquivos) < 1: # Changed to < 1 as even a single file can be a CAPA
            print(f"⚠️  A pasta '{pasta}' está vazia. Pulando...")
            print("----------------------------------------------------------")
            continue
            
        prefixo = f"{indice_pasta:02d}"

        # Loop through all files and rename based on position
        for index, arquivo in enumerate(arquivos):
            antigo_caminho = os.path.join(caminho_pasta, arquivo)
            extensao = os.path.splitext(arquivo)[1]

            if index == 0:
                # First file is always CAPA
                novo_nome = f"CAPA{extensao}"
            else:
                # Other files are numbered sequentially, starting from 1
                # The page number is the index in the list (e.g. index 1 is page 1)
                novo_nome = f"{prefixo}-{index:03d}{extensao}"

            novo_caminho = os.path.join(caminho_pasta, novo_nome)
            os.rename(antigo_caminho, novo_caminho)
            print(f"✅ Renomeado: {arquivo} → {novo_nome}")

        print("----------------------------------------------------------")

    print()
    print("Todos Arquivos foram renomeados com sucesso!")
    input("Pressione ENTER para continuar: ")
    ##os.startfile(caminho_base) # Abrindo pasta que está as pastas onde os arquivos foram renomeados
    os.system("exit")
    sys.exit()

# pedindo pasta de caminho
print("Renomeador para Envio de Álbuns")
print("----------------------------------------------------------")
caminho_base = input("Digite o caminho da Pasta: ")
caminho_base = caminho_base.replace("\\", "/") + '/'

# enumerando o indice
i = 0
print()
print("Caso seja o PRIMEIRO Álbum digite \033[1;37m0\033[0m.")
i = int(input("Se está continuando um envio digite o NÚMERO do \033[1;37mULTIMO Álbum Renomeado\033[0m: "))
i = i + 1
print("----------------------------------------------------------")
rename(caminho_base)
