### DUMP textos para Riviera: The Promised Land
### PSP
### v.0.1
### www.lucjedi.com
### Python 3.11


import csv
import binascii
import os
import tkinter as tk
from tkinter import filedialog

# 1.0 posicao do primeiro texto
posicaoTextoInicialHex = '015A8C'  # valor hex
print("Primeiro Texto Hex (First Hex Text): " + str(posicaoTextoInicialHex))
posicaoTextoInicialDec = int(posicaoTextoInicialHex, 16)  # numero inteiro

# 1.1 Posicao do primeiro Ponteiro
posicaoPrimeiroPonteiro = '08'  # valor hex
print("Primeiro Ponteiro Hex (First Hex Pointer): " + str(posicaoPrimeiroPonteiro))
posicaoPrimeiroPonteiro = int(posicaoPrimeiroPonteiro, 16)  # numero inteiro

# Posicao do ultimo ponteiro
posicaoUltimoPonteiro = '015A88'  # valor hex
print("Ultimo Ponteiro Hex (Last Hex Pointer): " + str(posicaoUltimoPonteiro))
posicaoUltimoPonteiro = int(posicaoUltimoPonteiro, 16)  # numero inteiro

# Função para abrir o explorador de arquivos
def abrir_arquivo():
    root = tk.Tk()
    root.withdraw()
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo usCstring.bin (Select usCstring.bin file):",
        initialfile="usCstring.bin",
        filetypes=[("Arquivos binários", "*.bin")]
    )
    if arquivo:
        print(f"Arquivo selecionado (Selected file): {arquivo}")
        return arquivo
    else:
        print("Nenhum arquivo foi selecionado (No file was selected).")
        exit()

# Chamar a função e armazenar o caminho do arquivo em uma variável
arquivo = abrir_arquivo()

# Obter o diretório do arquivo selecionado
diretorio_arquivo = os.path.dirname(arquivo)

# Obter o nome do arquivo sem o caminho
nome_arquivo = os.path.basename(arquivo)

# Usar o nome do arquivo selecionado como nome do Dump
dump_txt_nome = nome_arquivo.replace('.bin', '_Dump.txt')

# Caminho completo para o arquivo Dump
dump_txt_path = os.path.join(diretorio_arquivo, dump_txt_nome)
print(f"Arquivo Dump selecionado (Dump file selected): {dump_txt_path}")

# Criando dicionario do arquivo (usando o diretorio do arquivo)
dicionario_txt_path = os.path.join(diretorio_arquivo, 'Dicionario.txt')
print(f"Arquivo dicionario selecionado (Dictionary file selected): {dicionario_txt_path}")
leituraDicinarioTxt = csv.reader(open(dicionario_txt_path, 'r'), delimiter=';')
dicinarioCaracter = {}  # Criando um dicionario vazio

# Criando dicionario do arquivo Dicionario.txt
for __LinhaLida in leituraDicinarioTxt:
    valorHex, valorCaracter = __LinhaLida
    dicinarioCaracter[valorHex] = valorCaracter

# Abrindo arquivo de gravacao (usando o diretório do arquivo) com codificação ANSI
gravandoArquivoDump = open(dump_txt_path, 'w', encoding='latin-1')
gravandoArquivoDump.truncate()

# Abrir o arquivo binário sem 'with open'
cstringAberto = open(arquivo, 'rb')

# Criando dicionario para os ponteiros
dicinarioPonteiros = {}

cstringAberto.seek(posicaoPrimeiroPonteiro)
while True:
    hexCapturadoTamanho4 = cstringAberto.read(4)
    hexCapturadoTamanho4 = binascii.hexlify(hexCapturadoTamanho4).decode('utf-8')
    hexCapturadoTamanho4 = hexCapturadoTamanho4[6:8] + hexCapturadoTamanho4[4:6] + hexCapturadoTamanho4[2:4] + hexCapturadoTamanho4[0:2]

    if hexCapturadoTamanho4 in dicinarioPonteiros:
        dicinarioPonteiros[hexCapturadoTamanho4] = f"{dicinarioPonteiros[hexCapturadoTamanho4]},{cstringAberto.tell()-4}"
    else:
        dicinarioPonteiros[hexCapturadoTamanho4] = cstringAberto.tell()-4

    if cstringAberto.tell() == posicaoUltimoPonteiro + 4:
        break

# Gravar a saída no arquivo gravandoArquivoDump
for indice_hex in dicinarioPonteiros:
    indice_decimal = int(indice_hex, 16)
    posicaoTextoDec = indice_decimal + posicaoTextoInicialDec
    ##gravandoArquivoDump.write(indice_hex + '/' + str(indice_decimal) + '/' + str(posicaoTextoDec) + ':' + str(dicinarioPonteiros[indice_hex]) + '\n')
    gravandoArquivoDump.write(str(dicinarioPonteiros[indice_hex]) + '\n')
    cstringAberto.seek(posicaoTextoDec)

    textosConcatenados = ''
    while True:
       hexCapturadoTexto = cstringAberto.read(1)
       hexCapturadoTexto = str(binascii.hexlify(hexCapturadoTexto))
       hexCapturadoTexto = hexCapturadoTexto[2:4]
       if hexCapturadoTexto == 'ff':
          gravandoArquivoDump.write(str(textosConcatenados))
          gravandoArquivoDump.write(str('\n'))
          break
       else:
          cstringAberto.seek(cstringAberto.tell()-1)
          hexCapturadoTexto = cstringAberto.read(2)
          hexCapturadoTexto = str(binascii.hexlify(hexCapturadoTexto))
          hexCapturadoTexto = hexCapturadoTexto[2:6]
          try:
             textosConcatenados += dicinarioCaracter[hexCapturadoTexto]
          except:
             cstringAberto.seek(cstringAberto.tell()-2)
             hexCapturadoTexto = cstringAberto.read(1)
             hexCapturadoTexto = str(binascii.hexlify(hexCapturadoTexto))
             hexCapturadoTexto = hexCapturadoTexto[2:4]
             try:
                textosConcatenados += dicinarioCaracter[hexCapturadoTexto]
             except:
                textosConcatenados += '<' + hexCapturadoTexto + '>'
    gravandoArquivoDump.write(str('\n'))

# Fechar arquivos manualmente
cstringAberto.close()
gravandoArquivoDump.close()

print('FIM')
