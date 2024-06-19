import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def save_file(url, folder):
    try:
        print(f"Downloading {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        file_name = os.path.basename(urlparse(url).path)
        file_path = os.path.join(folder, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Saved {file_name} to {folder}")
        return file_name
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None

def download_background_images(css_content, css_url, css_folder):
    url_pattern = re.compile(r'url\((.*?)\)')
    for match in url_pattern.findall(css_content):
        img_url = match.strip('\'"')
        if not img_url.startswith('http'):
            img_url = urljoin(css_url, img_url)
        save_file(img_url, css_folder)

def download_site(url, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        print(f"Downloading main page: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the main page: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    # Save index.html
    index_path = os.path.join(output_folder, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    print(f"Saved main page to {index_path}")

    # Create folders for CSS, JS, and images
    css_folder = os.path.join(output_folder, 'css')
    js_folder = os.path.join(output_folder, 'js')
    img_folder = os.path.join(output_folder, 'images')
    os.makedirs(css_folder, exist_ok=True)
    os.makedirs(js_folder, exist_ok=True)
    os.makedirs(img_folder, exist_ok=True)

    # Download CSS files and find background images
    for link in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, link['href'])
        file_name = save_file(css_url, css_folder)
        if file_name:
            link['href'] = os.path.join('css', file_name)
            with open(os.path.join(css_folder, file_name), 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()
                download_background_images(css_content, css_url, img_folder)

    # Download JS files
    for script in soup.find_all('script', src=True):
        js_url = urljoin(url, script['src'])
        file_name = save_file(js_url, js_folder)
        if file_name:
            script['src'] = os.path.join('js', file_name)

    # Download images in <img> tags
    for img in soup.find_all('img'):
        img_url = urljoin(url, img['src'])
        file_name = save_file(img_url, img_folder)
        if file_name:
            img['src'] = os.path.join('images', file_name)

    # Save the updated index.html with local paths
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    print(f"Updated main page with local paths: {index_path}")

if __name__ == "__main__":
    website_url = input("Ingresa el enlace del sitio web que quieres descargar: ")  # Reemplaza esto con la URL del sitio web que quieres descargar
    output_directory = input("Ingresa el nombre de la carpeta donde guardar el sitio web")
    download_site(website_url, output_directory)
