#!/usr/bin/python
import sys
from DicionarioDump import Dic
print ('---------------------------------\nDump tool for Riviera: The Promised Land\n---------------------------------\nby: http://www.lucjedi.com/\n---------------------------------')

## Verifica arquivo de entrada
try:
    arquivo = open('Riviera.gba', "rb")
except:
    print ('Error: File not found!')
    raw_input('Press ENTER to exit...')
    sys.exit(0)

print ('Wait...')

## Ggrava e apaga arquivo dump
gravando = open('dump.txt', 'w')
gravando.truncate

def Executa(x,y):
    OffInicial = int(x, 16)
    OffFinal = int(y, 16)
    
    def GravandoPointer(y):
         gravando.write('|')
         gravando.write(("%x" % y).zfill(8))
         gravando.write('|')
    
    GravandoPointer(OffInicial)
    gravando.write('\n')
    
    while True:
        def GravandohexCapturado():
            gravando.write('$')
            hexEscrita = hexCapturado[:2] + '$' + hexCapturado[2:]
            gravando.write(hexEscrita)
    
        if OffInicial == OffFinal:
            gravando.write('\n')
            break
        arquivo.seek(OffInicial)
        hexCapturado = arquivo.read(1).encode("hex")
        try:
            gravando.write(Dic[hexCapturado])
        except:
            if hexCapturado == 'ff':
                gravando.write('\n')
                OffInicialSeg = OffInicial + 1
                GravandoPointer(OffInicialSeg)
                gravando.write('\n')
            elif hexCapturado == '8a':
                 gravando.write(' ')
            elif hexCapturado == 'a9':
                 gravando.write(' ')
            elif hexCapturado == 'a2':
                OffInicial = OffInicial + 1
                hexCapturado = hexCapturado + arquivo.read(1).encode("hex")
                try:
                    gravando.write(Dic[hexCapturado])
                except:
                    GravandohexCapturado()
            elif hexCapturado == 'fe':
                OffInicial = OffInicial + 1
                hexCapturado = hexCapturado + arquivo.read(1).encode("hex")
                try:
                    gravando.write(Dic[hexCapturado])
                except:
                     GravandohexCapturado()
            elif hexCapturado == 'fc':
                OffInicial = OffInicial + 1
                hexCapturado = hexCapturado + arquivo.read(1).encode("hex")
                try:
                    gravando.write(Dic[hexCapturado])
                except:
                     GravandohexCapturado()
            else:
                gravando.write('$')
                gravando.write(hexCapturado)
        OffInicial = OffInicial + 1

Executa('CE329C','CE7757')
Executa('CE9914','CEDC6A')
Executa('CEE780','CF0E9B')
Executa('CF1184','CF8AC4')
Executa('CF910C','CF92B4')
Executa('CF9350','CFB0F2')
Executa('CFB134','CFB1CC')
Executa('CFB1F0','CFD8F4')
Executa('CFDBD4','CFF4F1')
Executa('CFF570','D004C4')
Executa('D006D4','D06796')
Executa('D09380','D0F4DF')
Executa('D0F6EC','D0FF73')
Executa('D105F0','D23F18')
Executa('D250C4','D2560A')
Executa('D25630','D25E83')
Executa('D2610C','D327FA')
Executa('D33524','D33B33')
Executa('D33B5C','D34B94')
Executa('D3506C','D4824B')
Executa('D49F48','D4A603')
Executa('D4A630','D4C2B8')
Executa('D4C968','D60307')
Executa('D6202C','D625C7')
Executa('D625EC','D63388')
Executa('D638A8','D73A26')
Executa('D753B8','D75BE5')
Executa('D75C18','D77117')
Executa('D77780','D85BAA')
Executa('D87398','D88740')
Executa('D887AC','D89126')
Executa('D8945C','D95E79')
Executa('D96F5C','D9754B')
Executa('D97570','D97A4E')
Executa('D97CD8','DA31F7')
Executa('DA4224','DA485C')
Executa('DA4884','DA493F')
Executa('DA4964','DA4E77')
Executa('DA4ED4','DA4F9E')
Executa('DA4FA8','DA57D5')
Executa('0100D96A','0100D993')
Executa('0100DB50','0100DB5C')
Executa('0100DEFC','0100DF24')
Executa('0100E248','0100E297')
Executa('0100E794','0100E845')
Executa('010113AC','01012366')

raw_input('Press ENTER to exit...')
