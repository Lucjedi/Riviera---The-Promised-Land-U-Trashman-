#!/usr/bin/python
import sys
import binascii
from DicionarioInsert import Dic
print ('---------------------------------\nInsert tool for Riviera: The Promised Land\n---------------------------------\nby: http://www.lucjedi.com/\n---------------------------------')

somaOffset = int('16980608')

f1 = open("dumpBR.txt", "rbU")
f2 = open("dumpRP.txt", 'w')
contents = f1.read()

def trocar(x,y):
    global contents
    global replaced_contents
    replaced_contents = contents.replace(x,y)
    contents = replaced_contents
    
trocar('!?', '$a2$47')
trocar('...', '$fc$19')
trocar('!!', '$a2$48')
trocar('| ', '|')
trocar(' |', '|')
trocar('$ ', '$')
trocar('= ', '=')
trocar('# ', '#')
trocar(' =', '=')
trocar(' #', '#')
trocar('|\n|', '|\n \n|')


f2.write(replaced_contents)
f1.close()
f2.close()

## Verifica arquivo de entrada
try:
    #arquivo = open(raw_input("Filename Riviera's dump: "), "rb")
    arquivo = open("dumpRP.txt", "rbU")
except:
    print ('Error: File not found!')
    raw_input('Press ENTER to exit...')
    sys.exit(0)


print ('Wait...')

gravando = open('NovoInsert.txt', 'w')
gravando.truncate

gravandoErro = open('NovoInsertErro.txt', 'w')
gravandoErro.truncate

OffsHex ={}

def Tentar():
    try:
        gravando.write(Dic[hexCapturado])
    except:
        gravandoErro.write(hexCapturado)
def Ponteiros():
    hexCapturado = arquivo.read(8)
    VerhexCapturado = hexCapturado[0]+hexCapturado[1]
    if VerhexCapturado == '00':
        VerhexCapturado = '08'
    else:
        VerhexCapturado = '09'
        
    OffAntigo = hexCapturado[6]+hexCapturado[7]+hexCapturado[4]+hexCapturado[5]+hexCapturado[2]+hexCapturado[3]+VerhexCapturado
    trimnewoff = hex(somaOffset)
    OffNovo = trimnewoff[7]+trimnewoff[8]+trimnewoff[5]+trimnewoff[6]+trimnewoff[3]+trimnewoff[4]+'09'

    OffsHex[OffAntigo] = OffNovo
    
    hexCapturado = arquivo.read(1).encode("hex")
    hexCapturado = arquivo.read(1).encode("hex")
    
def HexsDireto():
    hexCapturado = arquivo.read(2)
    gravando.write(hexCapturado)

def Somar():
    global somaOffset
    try:
        somaOffset += int(len(Dic[hexCapturado])/2)
    except:
        print arquivo.tell()
        print ('Erro 45. :%s') % (hexCapturado)
        raw_input('Press ENTER to exit...')
        sys.exit(0)
    

hexCapturado = arquivo.read(1).encode("hex")
Ponteiros()

while True:
    hexCapturado = arquivo.read(1).encode("hex")
    hexCapturadoSeg = arquivo.read(1).encode("hex")

    if hexCapturado == 'c1' or hexCapturado == 'c2' or hexCapturado == 'c0' or hexCapturado == 'c3' or hexCapturado == 'c9' or hexCapturado == 'ca' or hexCapturado == 'cd' or hexCapturado == 'd3' or hexCapturado == 'd4' or hexCapturado == 'd5' or hexCapturado == 'da' or hexCapturado == 'c7':
        hexCapturado += hexCapturadoSeg
    elif hexCapturadoSeg == 'e1' or hexCapturadoSeg == 'e2' or hexCapturadoSeg == 'e0' or hexCapturadoSeg == 'e3' or hexCapturadoSeg == 'e9' or hexCapturadoSeg == 'ea' or hexCapturadoSeg == 'ed' or hexCapturadoSeg == 'f3' or hexCapturadoSeg == 'f4' or hexCapturadoSeg == 'f5' or hexCapturadoSeg == 'fa':
        hexCapturado += hexCapturadoSeg
    elif hexCapturadoSeg == 'e7':
        hexCapturadoSegDois = arquivo.read(1).encode("hex")
        if hexCapturadoSegDois == 'e1' or hexCapturadoSegDois == 'e2' or hexCapturadoSegDois == 'e0' or hexCapturadoSegDois == 'e3' or hexCapturadoSegDois == 'e9' or hexCapturadoSegDois == 'ea' or hexCapturadoSegDois == 'ed' or hexCapturadoSegDois == 'f3' or hexCapturadoSegDois == 'f4' or hexCapturadoSegDois == 'f5' or hexCapturadoSegDois == 'fa':
            arquivo.seek(arquivo.tell()-2)
        else:
            arquivo.seek(arquivo.tell()-1)
            hexCapturado += hexCapturadoSeg
            
    elif hexCapturadoSeg == '':
        linha = 'ignorada'
    else:
        arquivo.seek(arquivo.tell()-1)
    
    if hexCapturado == '': break
    elif hexCapturado == '7c':
        Tentar()
        Somar()
        Ponteiros()
    elif hexCapturado == '20' or hexCapturado == '23':
        Somar()
        Tentar()
    elif hexCapturado == '24':
        somaOffset += 1
        HexsDireto()
    elif hexCapturado == '0a' or hexCapturado == '09':
        linha = 'ignorada'
    else:
        Somar()
        Tentar()

arquivo.close()

## Verifica arquivo de entrada
try:
    #arquivo = open(raw_input("Filename Riviera's rom: "), "rb")
    arquivo = open("Riviera.gba", "rb")
except:
    print ('Error: File not found!')
    raw_input('Press ENTER to exit...')
    sys.exit(0)


gravando.close()
gravandoErro.close()

Newgravando = open('New_Riviera.gba', 'wb')
Newgravando.truncate

positionInsert = int('0')

while True:
    positionInsert = positionInsert + 4
    HexCapturadoNew = arquivo.read(4).encode("hex")
    if HexCapturadoNew == '': break
    elif positionInsert == 16980612:
        try:
            arquivoNovoInsert = open("NovoInsert.txt", "rbU")
        except:
            print ('Error: File NovoInsert.txt not found!')
            raw_input('Press ENTER to exit...')
            sys.exit(0)
        while True:
            HexCapturadoNew = arquivoNovoInsert.read(2)
            if HexCapturadoNew == '': break
            else:
                try:
                    positionInsert = positionInsert + 1
                    Newgravando.write(binascii.a2b_hex(''.join(HexCapturadoNew)))
                except:
                    print arquivo.tell()
                    print ('Erro 33. :%s') % (HexCapturadoNew)
                    raw_input('Press ENTER to exit...')
                    sys.exit(0)
        arquivo.seek(positionInsert - 4)
    else:
        
        try:
            Newgravando.write(binascii.a2b_hex(''.join(OffsHex[HexCapturadoNew])))
        except:
            Newgravando.write(binascii.a2b_hex(''.join(HexCapturadoNew)))
arquivo.close()
Newgravando.close()
#raw_input('Press ENTER to exit...')
