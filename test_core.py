"""Testes do núcleo. Uso:  python test_core.py <pasta com xxCstring.bin e Dicionario.txt>"""
import glob
import os
import sys
import tempfile

from riviera_core import BuildError, EncodeError, Project, Table

here = os.path.dirname(os.path.abspath(__file__))
folder = sys.argv[1] if len(sys.argv) > 1 else here
table = Table.load(os.path.join(folder, 'Dicionario.txt'))
bins = sorted(glob.glob(os.path.join(folder, '*Cstring.bin')))
ok_all = True


def check(name, cond):
    global ok_all
    ok_all &= bool(cond)
    print(('  OK   ' if cond else '  FALHA'), name)


for path in bins:
    data = open(path, 'rb').read()
    if data[:4] == b'<!DO':
        print(os.path.basename(path), '-> é uma página HTML, ignorando')
        continue
    print(os.path.basename(path))
    pj = Project.from_bin(data, table, os.path.basename(path))
    check(f'round-trip idêntico ({len(pj.entries)} entradas)', pj.build(table) == data)

    # --- salvar/abrir projeto mantém tudo ---
    with tempfile.TemporaryDirectory() as tmp:
        pp = os.path.join(tmp, 'p.json')
        pj.save(pp)
        check('projeto salvo/aberto gera o mesmo .bin', Project.load(pp).build(table) == data)

    # --- traduzir algumas entradas (maiores e menores) e reler ---
    cands = [e for e in pj.entries if e.has_text][:50]
    for k, e in enumerate(cands):
        e.tr = ('Teste ação ç ' * (k % 5 + 1)).strip() + ' <fe><02>' if k % 2 else 'Oi!'
    out = pj.build(table)
    again = Project.from_bin(out, table)
    check('texto traduzido relido igual', all(
        a.current == b.orig for a, b in zip(pj.entries, again.entries)))
    check('ponteiros compartilhados preservados',
          [e.ptrs for e in pj.entries] == [e.ptrs for e in again.entries])
    check('header: count e total corretos',
          int.from_bytes(out[:4], 'little') == pj.count and
          int.from_bytes(out[4:8], 'little') == len(out) - 8 - 4 * pj.count - len(pj.trailer))

    # --- caractere fora da tabela é recusado ---
    pj.entries[0].tr = 'texto com € inválido'
    try:
        pj.build(table)
        check('caractere inválido gera erro', False)
    except BuildError as be:
        check('caractere inválido gera erro', be.errors[0][0] == 0)

    # --- importar Tradu.tsv no formato antigo (com ';' e ü) ---
    pj2 = Project.from_bin(data, table)
    with tempfile.TemporaryDirectory() as tmp:
        tsv = os.path.join(tmp, 'Tradu.tsv')
        sample = [e for e in pj2.entries if e.has_text][:3]
        with open(tsv, 'w', encoding='utf-8') as f:
            for e in pj2.entries[:6]:
                f.write(','.join(str(8 + 4 * k) for k in e.ptrs) + '\n')
                if e in sample:
                    f.write('Pi\u00fc;<fe>;ola\n')      # como o DUMP antigo escrevia
                else:
                    f.write(e.orig + '\n')
        n, skipped = pj2.import_dump(tsv)
        check(f'importação do formato antigo ({n} traduzidas)',
              n == len([e for e in sample if e.has_text]) and
              all(e.tr == 'Pi\u00f9<fe>ola' for e in sample))

print('\nRESULTADO:', 'TUDO OK' if ok_all else 'HÁ FALHAS')
sys.exit(0 if ok_all else 1)
