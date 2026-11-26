# -*- coding: utf-8 -*-
"""Xera as compras nas barras do festival Son do Mar (ficticio) para o E6.

Cada liña:  compra_id,data_hora,barra,pulseira,produto,unidades,importe

Funciona con Python 2.7 (o do clúster) e con Python 3, e xera o mesmo
ficheiro nas dúas versións (usa o seu propio xerador pseudoaleatorio).

Uso:  python xera_compras.py --dias 3 --compras-por-hora 3000 --saida compras.csv
"""
from __future__ import print_function, division
import argparse
import io
from datetime import datetime, timedelta


class Aleatorio(object):
    def __init__(self, semente):
        self.estado = semente

    def enteiro(self, minimo, maximo):
        self.estado = (self.estado * 6364136223846793005 + 1442695040888963407) % (2 ** 64)
        return minimo + (self.estado >> 33) % (maximo - minimo + 1)

    def escoller(self, lista, pesos=None):
        if pesos is None:
            return lista[self.enteiro(0, len(lista) - 1)]
        x = self.enteiro(1, sum(pesos))
        for elemento, peso in zip(lista, pesos):
            x -= peso
            if x <= 0:
                return elemento


BARRAS = [u"Praia", u"Norte", u"Escenario", u"VIP"]
PESOS_BARRAS = [35, 25, 30, 10]
CATALOGO = [(u"auga", 150), (u"refresco", 250), (u"cervexa", 300), (u"viño", 350), (u"bocadillo", 500)]
PESOS_PRODUTOS = [30, 15, 35, 10, 10]

p = argparse.ArgumentParser()
p.add_argument("--dias", type=int, default=3)
p.add_argument("--compras-por-hora", type=int, default=3000)
p.add_argument("--semente", type=int, default=26)
p.add_argument("--saida", default="compras.csv")
a = p.parse_args()

r = Aleatorio(a.semente)
n = 0
with io.open(a.saida, "w", encoding="utf-8", newline="\n") as f:
    f.write(u"compra_id,data_hora,barra,pulseira,produto,unidades,importe\n")
    for d in range(a.dias):
        apertura = datetime(2027, 7, 16, 18) + timedelta(days=d)        # 18:00 a 04:00
        segundos = sorted(r.enteiro(0, 10 * 3600 - 1) for _ in range(10 * a.compras_por_hora))
        for s in segundos:
            n += 1
            produto, centimos = r.escoller(CATALOGO, PESOS_PRODUTOS)
            unidades = r.enteiro(1, 4)
            total = centimos * unidades
            f.write(u"%d,%s,%s,P-%04d,%s,%d,%d.%02d\n" % (
                n, (apertura + timedelta(seconds=s)).strftime("%Y-%m-%d %H:%M:%S"),
                r.escoller(BARRAS, PESOS_BARRAS), r.enteiro(1, 5000), produto, unidades,
                total // 100, total % 100))
print("%s: %d compras" % (a.saida, n))
