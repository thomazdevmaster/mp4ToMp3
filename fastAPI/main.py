from fastapi import FastAPI
import logging
from minio import Minio
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

from os import environ as env

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env


app = FastAPI()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World dfgdfg"}

@app.get("/convert")
async def convert_mp4ToMp3():
    logger.info("Iniciando conversão do arquivo mp4")
    file_name = "/tmp/downloads/teste.mp4"
    file_name_converted = "/tmp/downloads/teste.mp3"


    client = Minio(endpoint="minio:9000", 
                   access_key = env.get("MINIO_ROOT_USER"), 
                   secret_key = env.get("MINIO_ROOT_PASSWORD"), 
                   secure=False
                   )
    
    client.fget_object(env.get("BUCKET_NAME"), "ledzepellin.mp4" ,file_name)
    video_to_audio(file_name, file_name_converted)

    logger.info("Success")
    
    return{"message": "Conversão finalizada"}

def video_to_audio(video_file, audio_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_file)
    audio_clip.close()
    video_clip.close()
    logger.info("Finalizando mp4 para mp3")