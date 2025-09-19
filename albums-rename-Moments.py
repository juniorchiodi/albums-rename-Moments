import os, sys

def rename(base_path):
    pastas = sorted([p for p in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, p))]) # processando pastas em ordem alfabética
    
    for indice_pasta, pasta in enumerate(pastas, start=i):
        caminho_pasta = os.path.join(base_path, pasta)
        arquivos = sorted(os.listdir(caminho_pasta))  # ordenando os arquivos para manter a sequência

        arquivo_qr = None
        for arquivo in arquivos:
            if "qr" in arquivo.lower():
                arquivo_qr = arquivo
                break

        if arquivo_qr:
            arquivos.remove(arquivo_qr)
        else:
            print(f"⚠️  A pasta '{pasta}' não contém um arquivo de QR Code. Pulando...")
            print("----------------------------------------------------------")
            continue

        if not arquivos:
            print(f"⚠️  A pasta '{pasta}' está vazia (além do QR Code). Pulando...")
            print("----------------------------------------------------------")
            continue
            
        # Renomeando o primeiro arquivo como "CAPA.jpg"
        primeiro_arquivo = arquivos[0]
        extensao = os.path.splitext(primeiro_arquivo)[1]  # mantém a extensão original
        caminho_antigo = os.path.join(caminho_pasta, primeiro_arquivo)
        caminho_novo = os.path.join(caminho_pasta, f"CAPA{extensao}")
        os.rename(caminho_antigo, caminho_novo)
        print(f"✅ Renomeado: {primeiro_arquivo} → CAPA{extensao}")
        
        prefixo = f"{indice_pasta:02d}"  # definindo o prefixo (01, 02, 03...)
        
        # Renomeando as páginas
        page_counter = 0
        for index_arquivo, arquivo in enumerate(arquivos[1:], start=1):
            extensao = os.path.splitext(arquivo)[1]  # mantém a extensão original
            novo_nome = f"{prefixo}-{index_arquivo:03d}{extensao}"  # Ex: 01-001.jpg
            
            antigo_caminho = os.path.join(caminho_pasta, arquivo)
            novo_caminho = os.path.join(caminho_pasta, novo_nome)

            os.rename(antigo_caminho, novo_caminho)
            print(f"✅ Renomeado: {arquivo} → {novo_nome}")
            page_counter = index_arquivo

        # Renomeando o QR Code por último
        if arquivo_qr:
            extensao_qr = os.path.splitext(arquivo_qr)[1]
            novo_nome_qr = f"{prefixo}-{page_counter + 1:03d}{extensao_qr}"
            antigo_caminho_qr = os.path.join(caminho_pasta, arquivo_qr)
            novo_caminho_qr = os.path.join(caminho_pasta, novo_nome_qr)
            os.rename(antigo_caminho_qr, novo_caminho_qr)
            print(f"✅ Renomeado: {arquivo_qr} → {novo_nome_qr}")
        
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
