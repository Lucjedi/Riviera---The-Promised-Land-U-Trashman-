import csv
import os
import sys
import tkinter as tk
from tkinter import filedialog

csv.field_size_limit(10**7)

def abrir_arquivo(titulo, arquivo_inicial, tipo):
    root = tk.Tk()
    root.withdraw()
    arquivo = filedialog.askopenfilename(
        title=titulo,
        initialfile=arquivo_inicial,
        filetypes=[tipo]
    )
    if not arquivo:
        print("Nenhum arquivo foi selecionado. Encerrando.")
        sys.exit(1)
    print(f"Arquivo selecionado: {arquivo}")
    return arquivo

arquivo_tradu = abrir_arquivo("Selecione o arquivo Tradu.tsv", "Tradu.tsv", ("Arquivos TSV", "*.tsv"))
arquivo_uscstring = abrir_arquivo("Selecione o arquivo ORIGINAL usCstring.bin", "usCstring.bin", ("Arquivos BIN", "*.bin"))

diretorio_arquivo = os.path.dirname(arquivo_tradu)

dicionario_txt_path = os.path.join(diretorio_arquivo, 'Dicionario.txt')
print(f"Arquivo dicionário selecionado: {dicionario_txt_path}")

with open(dicionario_txt_path, 'r', encoding='latin1') as dict_file:
    leitor = csv.reader(dict_file, delimiter=';', quotechar=None, quoting=csv.QUOTE_NONE)
    dicionario = {caractere: hexstr.lower() for hexstr, caractere in leitor}

chaves_ordenadas = sorted(dicionario.keys(), key=lambda x: -len(x))

###nome_base = os.path.splitext(os.path.basename(arquivo_tradu))[0]
###insert_bin_path = os.path.join(diretorio_arquivo, f"{nome_base}_insert.bin")
###print(f"Arquivo Insert será criado em: {insert_bin_path}")

def salvar_como(titulo, nome_sugerido, tipo):
    root = tk.Tk()
    root.withdraw()
    caminho = filedialog.asksaveasfilename(
        title=titulo,
        initialfile=nome_sugerido,
        defaultextension=".bin",
        filetypes=[tipo]
    )
    if not caminho:
        print("Nenhum arquivo de saída foi selecionado. Encerrando.")
        sys.exit(1)
    print(f"Arquivo de saída selecionado: {caminho}")
    return caminho

insert_bin_path = salvar_como("Salvar arquivo Traduzido Insert.bin como...", "Insert.bin", ("Arquivos BIN", "*.bin"))


byte_offset = 0
dict_posicoes = {}
posicoes_atuais = []

with open(insert_bin_path, 'wb') as destino:
    with open(arquivo_uscstring, 'rb') as origem:
        conteudo_inicial = origem.read(0x15A8C)
        destino.write(conteudo_inicial)
        print(f"Copiados os primeiros {len(conteudo_inicial)} bytes de usCstring.bin")

    with open(arquivo_tradu, encoding="utf-8") as tsv_file:
        linhas = tsv_file.readlines()
        for i, linha in enumerate(linhas, start=1):
            linha = linha.replace('\t', '').strip()

            if i % 2 != 0 and linha:
                posicoes_atuais = [int(x) for x in linha.split(',') if x.isdigit()]
                continue

            if i % 2 == 0 and linha:
                offset_bytes = byte_offset.to_bytes(4, 'little')
                for pos in posicoes_atuais:
                    dict_posicoes[pos] = offset_bytes

                texto = linha
                idx = 0
                tamanho_em_bytes_do_texto = 0

                while idx < len(texto):
                    encontrou = False

                    if texto[idx] == '<':
                        final = texto.find('>', idx)
                        if final == -1:
                            print(f"[ERRO] Símbolo '<' sem fechamento na linha {i}")
                            sys.exit(1)

                        conteudo = texto[idx+1:final]
                        if all(c in '0123456789abcdefABCDEF' for c in conteudo) and len(conteudo) in [2, 4]:
                            try:
                                bytes_hex = bytes.fromhex(conteudo)
                                destino.write(bytes_hex)
                                tamanho_em_bytes_do_texto += len(bytes_hex)
                                idx = final + 1
                                continue
                            except ValueError:
                                print(f"[ERRO] Valor hex inválido em <{conteudo}> na linha {i}")
                                sys.exit(1)
                        else:
                            print(f"[ERRO] Comando inválido entre <>: <{conteudo}> na linha {i}")
                            sys.exit(1)

                    for chave in chaves_ordenadas:
                        if texto.startswith(chave, idx):
                            valor_hex = dicionario[chave]
                            try:
                                bytes_hex = bytes.fromhex(valor_hex)
                                destino.write(bytes_hex)
                                tamanho_em_bytes_do_texto += len(bytes_hex)
                                idx += len(chave)
                                encontrou = True
                                break
                            except ValueError:
                                print(f"[ERRO] Hex inválido para '{chave}': {valor_hex}")
                                sys.exit(1)

                    if not encontrou:
                        trecho_problema = texto[idx:idx+4]
                        print(f"\n[ERRO] Sequência não encontrada no dicionário: '{trecho_problema}' na linha {i}")
                        print(f"Texto da linha: {texto}")
                        sys.exit(1)

                destino.write(bytes.fromhex("FF"))
                tamanho_em_bytes_do_texto += 1

                byte_offset += tamanho_em_bytes_do_texto

#print("\nDicionário posições -> offset (hex little-endian):")
#for pos in sorted(dict_posicoes.keys()):
#    offset_hex_str = dict_posicoes[pos].hex()
#    print(f"{pos}: {offset_hex_str}")

# Salvar dicionário em arquivo temporário para conferência
validar_path = os.path.join(diretorio_arquivo, 'validar_offset.txt')

###with open(validar_path, 'w', encoding='utf-8') as f:
###    for pos in sorted(dict_posicoes.keys()):
###        offset_hex_str = dict_posicoes[pos].hex()
###        f.write(f"{pos}: {offset_hex_str}\n")
###
###print(f"\nDicionário de offsets salvo em: {validar_path}")

with open(insert_bin_path, 'r+b') as f:
    for posicao, offset_bytes in dict_posicoes.items():
        f.seek(posicao)
        f.write(offset_bytes)
print(f"Arquivo {insert_bin_path} atualizado com os offsets nas posições indicadas.")



# Inserir o total de bytes dos textos na posição 4 do arquivo insert
total_texto_bytes = byte_offset
total_texto_bytes_le = total_texto_bytes.to_bytes(4, 'little')

with open(insert_bin_path, 'r+b') as f:
    f.seek(4)
    f.write(total_texto_bytes_le)

print(f"Total de {total_texto_bytes} bytes de texto inseridos. Valor gravado na posição 4 de {insert_bin_path}.")

print("FIM DO PROCESSO")
