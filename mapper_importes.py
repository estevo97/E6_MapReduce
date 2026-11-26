# -*- coding: utf-8 -*-
"""Mapper que emite (barra, importe) por cada compra."""
from __future__ import print_function
import sys

for linha in sys.stdin:
    campos = linha.strip().split(",")
    if len(campos) != 7 or campos[0] == "compra_id":
        continue
    barra = campos[2]
    importe = campos[6]
    print("%s\t%s" % (barra, importe))
