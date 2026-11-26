# -*- coding: utf-8 -*-
"""E6, exemplo: reducer que suma os valores de cada clave.

Hadoop entrega as liñas ORDENADAS por clave: todas as dunha barra chegan
seguidas. Usa Decimal para sumar sen erros de redondeo: vale para contar
(valores 1) e para sumar importes (valores con decimais).

Entrada:  clave<TAB>valor    (ordenado por clave)
Saída:    clave<TAB>suma
"""
from __future__ import print_function
import sys
from decimal import Decimal

clave_actual, suma = None, Decimal(0)
for linha in sys.stdin:
    clave, valor = linha.rstrip("\n").split("\t", 1)
    if clave != clave_actual:
        if clave_actual is not None:
            print("%s\t%s" % (clave_actual, suma))
        clave_actual, suma = clave, Decimal(0)
    suma += Decimal(valor)
if clave_actual is not None:
    print("%s\t%s" % (clave_actual, suma))
