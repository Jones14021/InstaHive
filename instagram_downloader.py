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
SAFE_BATCH_MAX = 25
BATCH_DELAY_RANGE = (8, 18)
BATCH_COOLDOWN_EVERY = 5
BATCH_COOLDOWN_RANGE = (45, 90)


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


def choose_download_mode():
    print()
    print(Fore.CYAN + "Choose download mode:")
    print(Fore.CYAN + "  1) Single Instagram URL")
    print(Fore.CYAN + "  2) Saved posts batch mode (your account)")
    while True:
        choice = input(Fore.YELLOW + "Mode [1/2]: ").strip()
        if choice in ("1", "2"):
            return "single" if choice == "1" else "saved_batch"
        print(Fore.RED + "[X] Invalid choice. Please enter 1 or 2.")

# Clear screen function
def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

# Extract shortcode from URL
def extract_shortcode(url):
    match = re.search(r"instagram\.com/(?:reel|p|tv)/([^/?#&]+)", url)
    return match.group(1) if match else None


def parse_index_selection(selection_text, max_index):
    chosen = set()
    for part in selection_text.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if start > end:
                start, end = end, start
            if start < 1 or end > max_index:
                raise ValueError("Range out of bounds.")
            chosen.update(range(start, end + 1))
        else:
            index = int(token)
            if index < 1 or index > max_index:
                raise ValueError("Selection out of bounds.")
            chosen.add(index)
    return sorted(chosen)


def get_saved_posts(username, limit):
    profile = instaloader.Profile.from_username(L.context, username)
    saved_posts = []
    for post in profile.get_saved_posts():
        saved_posts.append(post)
        if len(saved_posts) >= limit:
            break
    return saved_posts


def format_post_label(post):
    caption_preview = (post.caption or "").strip().replace("\n", " ")
    if len(caption_preview) > 60:
        caption_preview = caption_preview[:57] + "..."
    if not caption_preview:
        caption_preview = "(no caption)"
    return f"@{post.owner_username} | {post.shortcode} | {post.date_utc.date()} | {caption_preview}"


def prompt_saved_post_targets(username):
    while True:
        print()
        print(Fore.CYAN + "Saved posts options:")
        print(Fore.CYAN + "  a) Download last X saved posts")
        print(Fore.CYAN + "  b) Select posts from a recent list (search by username/caption)")
        print(Fore.CYAN + "  q) Back/quit")
        choice = input(Fore.YELLOW + "Choose [a/b/q]: ").strip().lower()

        if choice == "q":
            return []

        if choice == "a":
            while True:
                requested = input(Fore.YELLOW + f"How many recent saved posts? [1-{SAFE_BATCH_MAX}]: ").strip()
                try:
                    count = int(requested)
                    if count < 1:
                        raise ValueError
                    if count > SAFE_BATCH_MAX:
                        print(Fore.MAGENTA + f"[!] Limiting to {SAFE_BATCH_MAX} posts per run for safety.")
                        count = SAFE_BATCH_MAX
                    posts = get_saved_posts(username, count)
                    if not posts:
                        print(Fore.RED + "[X] No saved posts found.")
                    return posts
                except ValueError:
                    print(Fore.RED + "[X] Enter a valid number.")

        if choice == "b":
            inspect_count = min(20, SAFE_BATCH_MAX)
            posts = get_saved_posts(username, SAFE_BATCH_MAX)
            if not posts:
                print(Fore.RED + "[X] No saved posts found.")
                return []

            print(Fore.CYAN + f"\nRecent saved posts (showing up to {inspect_count}):")
            for i, post in enumerate(posts[:inspect_count], start=1):
                print(Fore.CYAN + f"  {i}) {format_post_label(post)}")

            query = input(Fore.YELLOW + "Filter by username/caption (optional): ").strip().lower()
            candidates = posts[:inspect_count]
            if query:
                filtered = []
                for post in candidates:
                    searchable = f"{post.owner_username} {(post.caption or '')}".lower()
                    if query in searchable:
                        filtered.append(post)
                candidates = filtered
                if not candidates:
                    print(Fore.RED + "[X] No posts matched that filter.")
                    continue
                print(Fore.CYAN + "\nMatching posts:")
                for i, post in enumerate(candidates, start=1):
                    print(Fore.CYAN + f"  {i}) {format_post_label(post)}")

            selection = input(Fore.YELLOW + "Select indexes (e.g. 1,3-5): ").strip()
            if not selection:
                print(Fore.RED + "[X] No selection provided.")
                continue
            try:
                indexes = parse_index_selection(selection, len(candidates))
                return [candidates[i - 1] for i in indexes]
            except ValueError as e:
                print(Fore.RED + f"[X] Invalid selection: {e}")
                continue

        print(Fore.RED + "[X] Invalid choice.")


def human_wait(seconds, reason):
    print(Fore.MAGENTA + f"[~] {reason}: waiting {seconds} seconds...")
    sleep(seconds)

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
def download_post(shortcode, download_path, refresh_ui=True):
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    temp_dir = os.path.join(download_path, "temp_download")
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
    if refresh_ui:
        sleep(2)
        clear_screen()
        show_banner()


def run_saved_batch_mode(username, download_path):
    print()
    print(Fore.MAGENTA + "[!] Batch mode warning:")
    print(Fore.MAGENTA + "[!] Instagram may limit accounts that perform aggressive download activity.")
    print(Fore.MAGENTA + "[!] This mode uses conservative pauses and a capped batch size to reduce risk.")
    print(Fore.MAGENTA + "[!] Keep usage small and infrequent. Use at your own risk.")
    proceed = input(Fore.YELLOW + "Continue with batch mode? [y/N]: ").strip().lower()
    if proceed not in ("y", "yes"):
        print(Fore.YELLOW + "Batch mode cancelled.")
        return

    posts = prompt_saved_post_targets(username)
    if not posts:
        return

    total = len(posts)
    print(Fore.CYAN + f"\nStarting batch download for {total} post(s).")
    completed = 0
    failed = 0
    for idx, post in enumerate(posts, start=1):
        print(Fore.CYAN + f"\n[{idx}/{total}] Downloading {format_post_label(post)}")
        try:
            download_post(post.shortcode, download_path, refresh_ui=False)
            completed += 1
        except Exception as e:
            failed += 1
            print(Fore.RED + f"[X] Download failed: {e}")

        if idx < total:
            delay = random.randint(*BATCH_DELAY_RANGE)
            human_wait(delay, "Rate-limit safety pause")
            if idx % BATCH_COOLDOWN_EVERY == 0:
                cooldown = random.randint(*BATCH_COOLDOWN_RANGE)
                human_wait(cooldown, "Extended cooldown")

    print()
    print(Fore.GREEN + f"[✓] Batch complete. Success: {completed}, Failed: {failed}")

# Start the script
clear_screen()
show_banner()
download_path = choose_download_path()
download_mode = choose_download_mode()

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
if download_mode == "single":
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
            download_post(shortcode, download_path)
        except Exception as e:
            print(Fore.RED + f"[X] Download failed: {e}")
else:
    run_saved_batch_mode(username, download_path)
