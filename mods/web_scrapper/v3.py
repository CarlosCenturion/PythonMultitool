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

def download_background_resources(css_content, css_url, resource_folder):
    url_pattern = re.compile(r'url\((.*?)\)')
    for match in url_pattern.findall(css_content):
        resource_url = match.strip('\'"')
        if not resource_url.startswith('http'):
            resource_url = urljoin(css_url, resource_url)
        save_file(resource_url, resource_folder)

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

    # Create folders for various types of resources
    css_folder = os.path.join(output_folder, 'css')
    js_folder = os.path.join(output_folder, 'js')
    php_folder = os.path.join(output_folder, 'php')
    asp_folder = os.path.join(output_folder, 'asp')
    img_folder = os.path.join(output_folder, 'images')
    video_folder = os.path.join(output_folder, 'videos')
    font_folder = os.path.join(output_folder, 'fonts')
    doc_folder = os.path.join(output_folder, 'docs')
    audio_folder = os.path.join(output_folder, 'audio')
    os.makedirs(css_folder, exist_ok=True)
    os.makedirs(js_folder, exist_ok=True)
    os.makedirs(php_folder, exist_ok=True)
    os.makedirs(asp_folder, exist_ok=True)
    os.makedirs(img_folder, exist_ok=True)
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(font_folder, exist_ok=True)
    os.makedirs(doc_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)

    # Download CSS files and find background resources
    for link in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, link['href'])
        file_name = save_file(css_url, css_folder)
        if file_name:
            link['href'] = os.path.join('css', file_name)
            with open(os.path.join(css_folder, file_name), 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()
                download_background_resources(css_content, css_url, img_folder)

    # Download JS files
    for script in soup.find_all('script', src=True):
        js_url = urljoin(url, script['src'])
        file_name = save_file(js_url, js_folder)
        if file_name:
            script['src'] = os.path.join('js', file_name)

    # Download PHP files
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.php'):
            php_url = urljoin(url, href)
            file_name = save_file(php_url, php_folder)
            if file_name:
                link['href'] = os.path.join('php', file_name)

    # Download ASP files
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.asp'):
            asp_url = urljoin(url, href)
            file_name = save_file(asp_url, asp_folder)
            if file_name:
                link['href'] = os.path.join('asp', file_name)

    # Download images in <img> tags
    for img in soup.find_all('img'):
        img_url = urljoin(url, img['src'])
        file_name = save_file(img_url, img_folder)
        if file_name:
            img['src'] = os.path.join('images', file_name)

    # Download video sources
    for video in soup.find_all('video'):
        for source in video.find_all('source'):
            video_url = urljoin(url, source['src'])
            file_name = save_file(video_url, video_folder)
            if file_name:
                source['src'] = os.path.join('videos', file_name)

    # Download fonts
    for link in soup.find_all('link', href=True):
        href = link['href']
        if href.endswith(('.woff', '.woff2', '.ttf', '.otf')):
            font_url = urljoin(url, href)
            file_name = save_file(font_url, font_folder)
            if file_name:
                link['href'] = os.path.join('fonts', file_name)

    # Download documents
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith(('.pdf', '.doc', '.docx')):
            doc_url = urljoin(url, href)
            file_name = save_file(doc_url, doc_folder)
            if file_name:
                link['href'] = os.path.join('docs', file_name)

    # Download audio files
    for audio in soup.find_all('audio'):
        for source in audio.find_all('source'):
            audio_url = urljoin(url, source['src'])
            file_name = save_file(audio_url, audio_folder)
            if file_name:
                source['src'] = os.path.join('audio', file_name)

    # Save the updated index.html with local paths
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    print(f"Updated main page with local paths: {index_path}")

if __name__ == "__main__":
    website_url = input("Ingresa el enlace del sitio web que quieres descargar: ")  # Reemplaza esto con la URL del sitio web que quieres descargar
    output_directory = input("Nombre de la carpeta donde descargar el sitio: ")
    download_site(website_url, output_directory)
