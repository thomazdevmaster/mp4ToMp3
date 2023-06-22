import io
import os
from fastapi import FastAPI, UploadFile, File
import logging
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

from os import environ as env

import requests

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env


app = FastAPI()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World dfgdfg"}

@app.get("/convert/{file}")
async def convert_mp4ToMp3(file: str):
    logger.info(f"Iniciando conversão do arquivo {file}")
    file_name = "/tmp/downloads/" + file
    file_name_converted = file_name.removesuffix("mp4") + "mp3"

    endpoint = "minio:9000"

    client = Minio(endpoint=endpoint, 
                   access_key = env.get("MINIO_ROOT_USER"), 
                   secret_key = env.get("MINIO_ROOT_PASSWORD"), 
                   secure=False
                   )
    
    try:
        client.fget_object(env.get("BUCKET_NAME"), file, file_name)
        video_to_audio(file_name, file_name_converted)

        logger.info(f"Arquivo {file_name_converted} gerado com {os.path.getsize(file_name_converted)} bytes")

        # Upload the converted file to MinIO
        logger.info("Enviando arquivo para o bucket " + env.get("BUCKET_NAME"))
        with open(file_name_converted, "rb") as f:
            file_data = f.read()
        
        stream = io.BytesIO(file_data)  # Cria um objeto BytesIO com os dados do arquivo
        
        client.put_object(
            bucket_name=env.get("BUCKET_NAME"),
            object_name="convertidos/" + file_name_converted.split("/")[-1],
            data=stream,
            length=len(file_data),
            content_type="audio/mpeg"
        )

        logger.info("Successo no envio")

        logger.info("Apagando arquivos temporários . . .")

        try:
            folder_path = "/tmp/downloads"
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            logger.info("Todos os arquivos foram removidos com sucesso.")
        except OSError as e:
            logger.error(f"Erro ao remover os arquivos: {e}")


        return {"message": "Conversão finalizada e arquivo salvo no MinIO"}
    except Exception as e:
        logger.error(f"Erro durante a conversão e salvamento no MinIO: {str(e)}")
        return {"message": "Ocorreu um erro durante a conversão e salvamento no MinIO"}

def video_to_audio(video_file, audio_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_file)
    audio_clip.close()
    video_clip.close()
    logger.info("Finalizando mp4 para mp3")
