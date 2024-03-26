from coser.common.services.CoserService import CoserService
from coser.common.configuration.config import load_config
from tqdm import tqdm

service=CoserService(load_config().get("coser_service"))

df=service.get_dataset_from_local()
turn_ini = 0
turn_fin = 50


for filename in tqdm(df.iloc[:, 0].unique()):
    text = service.obtenerFragmentoEntrevista(df, filename, turn_ini, turn_fin)

    out_prompt=service.obtener_prompts(filename)
    if out_prompt:
        print(text,out_prompt)