import os
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import coser
import pandas as pd

# first run "ollama pull <model>"

model = "llama2:13b-chat-q4_0" #"gemma:7b-instruct"

output_folder = 'outputs/resumenes/'+model

####################################

os.makedirs(output_folder, exist_ok=True)

df = coser.csv2Df('CLEAN_df_hack_full.csv')
df = coser.elegirRegionalismos(df, regionalismos = True)
df = coser.agregar_columna_topics(df)

####################################

llm = Ollama(model=model, temperature=0.1)
print(f"--- Modelo: {model} ---\n")

prompt = PromptTemplate(
    template="""A continuación vas a recibir una entrevista en la que pueden participar varios entrevistadores (E), indicados como E1, E2, ..., y varios informadores (I), indicados como I1, I2, sucesivamente. Ten en cuenta que los detalles personales sobre algunas personas han sido anonimizados. 
    
    Texto de la entrevista: {text}

    Resume en uno o dos párrafos el contenido de la entrevista, prestando atención a los detalles más relevantes.
    """,
    input_variables=["text"],
)

chain = prompt | llm 

####################################

file_list = list(df.filename.unique())

####################################

turn_ini = 0
turn_fin = 50

for i,file in enumerate(file_list):
    print(f'Processing File {file} [{i+1}/{len(file_list)}]')
    text = coser.obtenerFragmentoEntrevista(df, file, turn_ini, turn_fin)

    r = chain.invoke(
        {
        'text': text,
        }
    )

    filename = 'resumen_'+file+'.txt'

    with open(os.path.join(output_folder, filename), 'w') as f:
        f.write(r)