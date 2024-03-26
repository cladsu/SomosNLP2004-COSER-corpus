formulas_provincia = [
    "Los informadores de la entrevista son de {provincia}, según su estilo lingüístico.",
    "{provincia} es la procedencia de los informadores en esta entrevista.",
    "En esta entrevista, los informadores provienen de {provincia}.",
    "Los rasgos lingüísticos de los informadores sugieren que son de {provincia} en España.",
    "Se puede inferir que los informadores son de {provincia} basándose en su lenguaje durante la entrevista.",
    "Según su habla, los informadores son originarios de {provincia}.",
    "Los informadores entrevistados muestran características lingüísticas propias de {provincia}.",
    "La provincia de {provincia} es el lugar de origen de los informadores que participan en esta entrevista.",
    "El origen geográfico de los informadores en esta entrevista se encuentra en {provincia}.",
    "Los informadores presentan patrones lingüísticos asociados con {provincia}, según se desprende de la entrevista.",
    "De acuerdo con su manera de hablar, los informadores son de {provincia}.",
    "{provincia} es la región de la que provienen los informadores de esta entrevista.",
    "Los informadores entrevistados tienen el acento característico de {provincia}.",
    "Los informadores parecen ser nativos de {provincia}, según su dialecto.",
    "La provincia de origen de los informadores en esta entrevista es {provincia}.",
    "Los informadores tienen rasgos lingüísticos típicos de {provincia}.",
    "Se puede identificar la provincia de los informadores por su manera de hablar, que corresponde a {provincia}.",
    "La procedencia de los informadores, según su modo de expresarse, es {provincia}.",
    "{provincia} es la localidad de la que proceden los informadores de esta entrevista.",
    "Los informadores utilizan expresiones propias de {provincia}, indicando su procedencia.",
    "Los informadores muestran un léxico y acento que sugieren su origen en {provincia}.",
    "Según su acento y vocabulario, los informadores son oriundos de {provincia}.",
    "Los informadores de la entrevista son característicos de la provincia de {provincia}.",
    "La procedencia geográfica de los informadores se evidencia por su dialecto, propio de {provincia}.",
    "Los informadores en esta entrevista tienen un habla que los sitúa en {provincia}.",
    "Se puede deducir que los informadores son de {provincia}, basándose en su forma de expresarse.",
    "La provincia de {provincia} es la región de la que proceden los informadores entrevistados.",
    "Los informadores exhiben patrones lingüísticos asociados con {provincia}.",
    "Su manera de hablar indica que los informadores son de {provincia}.",
    "Los informadores tienen un acento que sugiere que son de {provincia}.",
]

import os
import coser
import pandas as pd
from random import randint

model = "formulas"

output_folder = 'outputs/'+model

####################################

os.makedirs(output_folder, exist_ok=True)

df = coser.csv2Df('CLEAN_df_hack_full.csv')
df = coser.elegirRegionalismos(df, regionalismos = True)
df = coser.agregar_columna_topics(df)

####################################

file_list = list(df.filename.unique())

####################################


for i,file in enumerate(file_list):
    print(f'Processing File {file} [{i+1}/{len(file_list)}]')
    provincia = coser.obtenerProvincia(df, file)

    n =  randint(0, len(formulas_provincia)-1)

    r = formulas_provincia[n].format(provincia=provincia)

    filename = 'provincia_'+file+'.txt'

    with open(os.path.join(output_folder, filename), 'w') as f:
        f.write(r)