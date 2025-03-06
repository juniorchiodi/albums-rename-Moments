import os,sys

def renomear_pastas(base_path):
    pastas = sorted([p for p in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, p))]) # processando pastas em ordem alfabética
    
    for indice_pasta, pasta in enumerate(pastas, start=i):
        caminho_pasta = os.path.join(base_path, pasta)
        arquivos = sorted(os.listdir(caminho_pasta))  # ordenando os arquivos para manter a sequência

        if len(arquivos) != 17:
            print(f"⚠️ O Álbum '{pasta}' não tem 17 arquivos(Lâminas). Parando...")
            print("⚠️ Para Continuar todas as Pastas devem ter 17 arquivos(Lâminas em JPG).")
            print("----------------------------------------------------------")
            break
            
        
        prefixo = f"{indice_pasta:02d}"  # definindo o prefixo (01, 02, 03...)
        
        # Renomeando os 16 primeiros arquivos
        for index_arquivo, arquivo in enumerate(arquivos[:-1], start=1):
            extensao = os.path.splitext(arquivo)[1]  # mantém a extensão original
            novo_nome = f"{prefixo}-{index_arquivo:03d}{extensao}"  # Ex: 01-001.jpg
            
            antigo_caminho = os.path.join(caminho_pasta, arquivo)
            novo_caminho = os.path.join(caminho_pasta, novo_nome)

            os.rename(antigo_caminho, novo_caminho)
            print(f"✅ Renomeado: {arquivo} → {novo_nome}")

        # Renomeando o último arquivo como "CAPA.jpg"
        ultimo_arquivo = arquivos[-1]
        extensao = os.path.splitext(ultimo_arquivo)[1]  # mantém a extensão original
        caminho_antigo = os.path.join(caminho_pasta, ultimo_arquivo)
        caminho_novo = os.path.join(caminho_pasta, f"CAPA{extensao}")

        os.rename(caminho_antigo, caminho_novo)
        print(f"✅ Renomeado: {ultimo_arquivo} → CAPA{extensao}")
        print("----------------------------------------------------------")

    print()
    print("Todos Arquivos foram renomeados com sucesso!")
    input("Pressione ENTER para continuar: ")
    ##os.startfile(caminho_base) # Abrindo pasta que está as pastas onde os arquivos foram renomeados
    os.system("exit")
    sys.exit()
    

    
        

# pedindo pasta de caminho
print("Renomeador de Pastas para Envio de Álbuns")
print("----------------------------------------------------------")
caminho_base = input("Digite o caminho da pasta: ")
caminho_base = caminho_base.replace("\\", "/") + '/'

# enumerando o indice
i = 0
print()
print("Caso for o PRIMEIRO Álbum digite \033[1;37m0\033[0m.")
i = int(input("Se está continuando um envio digite o NÚMERO do \033[1;37mULTIMO Álbum Renomeado\033[0m: "))
i = i + 1
print("----------------------------------------------------------")
renomear_pastas(caminho_base)

