from colorama import Fore
import os
from openai import AsyncOpenAI, OpenAI
import asyncio
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API Key de las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No se encontró la API Key de OpenAI en las variables de entorno")

client = AsyncOpenAI(
    api_key=api_key,
)

async def main() -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(chat_completion)

def ejecutar():
    print(Fore.GREEN + "Bienvenido al Modulo de OpenIA")
    asyncio.run(main())

if __name__ == "__main__":
    ejecutar()
