import logging
import os
import platform
import random
import re
import shutil
from time import sleep
from tqdm import tqdm
import instaloader
from colorama import Fore

logging.basicConfig(level=logging.CRITICAL)

CONFIG_FILE = os.path.expanduser("~/.insta-hive")


def show_banner():
    banners = [
        f"""{Fore.MAGENTA}
╔══════════════════════════════════════════════╗
║     📸 InstaHive - Instagram Downloader     ║
╠══════════════════════════════════════════════╣
║ GitHub: https://github.com/imraj569          ║
╚══════════════════════════════════════════════╝
""",
        f"""{Fore.CYAN}
╔══════════════════════════════════════════════╗
║     📲 InstaHive - Grab Instagram Content   ║
╠══════════════════════════════════════════════╣
║ GitHub: https://github.com/imraj569          ║
╚══════════════════════════════════════════════╝
""",
        f"""{Fore.GREEN}
╔══════════════════════════════════════════════╗
║     🚀 InstaHive - Download Instagram Media  ║
╠══════════════════════════════════════════════╣
║ GitHub: https://github.com/imraj569          ║
╚══════════════════════════════════════════════╝
"""
    ]
    print(random.choice(banners))

session_file = "ig_session"


def get_system_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")


def get_saved_download_path():
    if not os.path.isfile(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as config:
            saved_path = config.read().strip()
            if saved_path:
                return os.path.abspath(os.path.expanduser(saved_path))
    except OSError:
        pass
    return None


def save_download_path(path):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as config:
            config.write(path)
    except OSError as e:
        print(Fore.RED + f"[X] Failed to save custom download directory: {e}")


def choose_download_path():
    system_default = get_system_download_path()
    prompt_default = get_saved_download_path() or system_default
    prompt = Fore.YELLOW + f"Download directory [{prompt_default}]: "
    chosen_input = input(prompt).strip()

    if chosen_input:
        selected_path = os.path.abspath(os.path.expanduser(chosen_input))
    else:
        selected_path = prompt_default

    try:
        os.makedirs(selected_path, exist_ok=True)
    except OSError as e:
        print(Fore.RED + f"[X] Cannot use download directory '{selected_path}': {e}")
        print(Fore.MAGENTA + f"[!] Falling back to default: {system_default}")
        selected_path = system_default
        try:
            os.makedirs(selected_path, exist_ok=True)
        except OSError as fallback_error:
            print(Fore.RED + f"[X] Failed to create fallback directory '{selected_path}': {fallback_error}")
            raise SystemExit(1)

    if chosen_input:
        save_download_path(selected_path)

    return selected_path

# Clear screen function
def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

# Extract shortcode from URL
def extract_shortcode(url):
    match = re.search(r"instagram\.com/(?:reel|p|tv)/([^/?#&]+)", url)
    return match.group(1) if match else None

# Setup Instaloader
L = instaloader.Instaloader(
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    post_metadata_txt_pattern="",
    filename_pattern="{shortcode}"
)

# Download a single post (photo/video/album)
def download_post(shortcode):
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    os.makedirs(temp_dir, exist_ok=True)
    L.dirname_pattern = temp_dir
    L.download_post(post, target="")

    files = [file for file in os.listdir(temp_dir) if (file.endswith((".mp4", ".jpg", ".jpeg", ".png")) and shortcode in file)]
    if not files:
        print(Fore.RED + "[X] Media file not found.")
        shutil.rmtree(temp_dir)
        return

    # Show progress bar during download
    for file in tqdm(files, desc="Downloading", colour="green"):
        old_path = os.path.join(temp_dir, file)
        new_filename = f"{post.owner_username}_{file}"
        new_path = os.path.join(download_path, new_filename)
        shutil.move(old_path, new_path)
        sleep(0.2)  # for progress bar effect

    print(Fore.GREEN + f"[✓] Saved {len(files)} file(s) successfully.")
    shutil.rmtree(temp_dir)
    sleep(2)
    clear_screen()
    show_banner()

# Start the script
clear_screen()
show_banner()
download_path = choose_download_path()
temp_dir = os.path.join(download_path, "temp_download")

# Login to Instagram
username = input(Fore.YELLOW + "Enter your Instagram username: ")
try:
    L.load_session_from_file(username, session_file)
    print(Fore.GREEN + "[✓] Logged in with saved session.")
    sleep(1)
    clear_screen()
    show_banner()
except FileNotFoundError:
    print(Fore.MAGENTA + "[!] No session found. Logging in...")
    password = input("Enter your Instagram password: ")
    try:
        L.login(username, password)
        L.save_session_to_file(session_file)
        print(Fore.GREEN + "[✓] Login successful. Session saved.")
        sleep(1)
        clear_screen()
        show_banner()
    except Exception as e:
        print(Fore.RED + f"[X] Login failed: {e}")
        exit()

# Main loop for downloading posts
while True:
    print()
    url = input(Fore.CYAN + "Paste Instagram URL (or type 'exit' to quit): ").strip()
    
    if url.lower() == "exit":
        print(Fore.YELLOW + "Goodbye! 👋")
        break

    shortcode = extract_shortcode(url)
    if not shortcode:
        print(Fore.RED + "[X] Unsupported or invalid URL.")
        continue
    try:
        download_post(shortcode)
    except Exception as e:
        print(Fore.RED + f"[X] Download failed: {e}")
