import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import init, Fore

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

init(autoreset=True)

def save_file(url, folder):
    try:
        print(f"{Fore.YELLOW}Downloading {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        parsed_url = urlparse(url)
        if not parsed_url.path or parsed_url.path.endswith('/'):
            file_name = "index.html"
            file_path = os.path.join(folder, file_name)
        else:
            file_name = os.path.basename(parsed_url.path)
            file_path = os.path.join(folder, parsed_url.path.lstrip("/"))

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"{Fore.GREEN}Saved {file_path}")
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Failed to download {url}: {e}")
        return None
    except PermissionError as e:
        print(f"{Fore.RED}Permission error when trying to write {file_path}: {e}")
        return None

def download_resources(soup, base_url, output_folder):
    resource_tags = {
        'link': 'href',
        'script': 'src',
        'img': 'src',
        'video': 'src',
        'audio': 'src',
        'source': 'src'
    }

    for tag, attribute in resource_tags.items():
        for element in soup.find_all(tag):
            resource_url = element.get(attribute)
            if resource_url:
                resource_url = urljoin(base_url, resource_url)
                if not urlparse(resource_url).scheme.startswith('http'):
                    continue
                file_path = save_file(resource_url, output_folder)
                if file_path:
                    element[attribute] = os.path.relpath(file_path, output_folder)

def download_site(url, output_folder):
    output_folder = os.path.join('Descargas', 'Webs', output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        print(f"{Fore.YELLOW}Downloading main page: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Failed to download the main page: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    # Save index.html
    index_path = os.path.join(output_folder, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    print(f"{Fore.GREEN}Saved main page to {index_path}")

    # Download all resources
    download_resources(soup, url, output_folder)

    # Save the updated index.html with local paths
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    print(f"{Fore.GREEN}Updated main page with local paths: {index_path}")

def ejecutar():
    website_url = input(f"{Fore.YELLOW}Ingresa el enlace del sitio web que quieres descargar: ")
    output_directory = input(f"{Fore.YELLOW}Nombre de la carpeta donde descargar el sitio: ")
    download_site(website_url, output_directory)
    
if __name__ == "__main__":
    ejecutar()
