import os, sys

def rename(base_path, start_index=1):
    """
    Renames files in subdirectories of a given base path.

    This function iterates through subdirectories, renames the first file to 'CAPA',
    and subsequent files sequentially. It is a generator that yields status
    messages for each operation.

    Args:
        base_path (str): The path to the main folder containing album subfolders.
        start_index (int): The starting number for the album prefixes.

    Yields:
        str: Status messages indicating the progress of the renaming operations.
    """
    pastas = sorted([p for p in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, p))])

    for indice_pasta, pasta in enumerate(pastas, start=start_index):
        yield f"\nProcessando pasta: '{pasta}'..."
        caminho_pasta = os.path.join(base_path, pasta)
        arquivos = sorted(os.listdir(caminho_pasta))

        if len(arquivos) < 1:
            yield f"⚠️  A pasta '{pasta}' está vazia. Pulando..."
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
            try:
                os.rename(antigo_caminho, novo_caminho)
                yield f"✅ Renomeado: {arquivo} → {novo_nome}"
            except OSError as e:
                yield f"❌ ERRO ao renomear {arquivo}: {e}"

        yield "----------------------------------------------------------"

if __name__ == "__main__":
    # This block runs only when the script is executed directly
    print("Renomeador para Envio de Álbuns (Modo Console)")
    print("----------------------------------------------------------")

    try:
        caminho_base = input("Digite o caminho da Pasta: ")
        caminho_base = caminho_base.replace("\\", "/") + '/'

        i = 0
        print()
        print("Caso seja o PRIMEIRO Álbum digite \033[1;37m0\033[0m.")
        i = int(input("Se está continuando um envio digite o NÚMERO do \033[1;37mULTIMO Álbum Renomeado\033[0m: "))
        i = i + 1
        print("----------------------------------------------------------")

        # The rename function is a generator, so we iterate over it to get status messages
        for status_message in rename(caminho_base, i):
            print(status_message)

        print()
        print("Todos os álbuns foram processados!")

    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

    finally:
        input("Pressione ENTER para sair.")
