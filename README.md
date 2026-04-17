# InstaHive 🐝 - Instagram Downloader CLI

**Author:** [Rajkishor Patra](https://github.com/imraj569)
**Tool:** `instagram_downloader.py`
**Platform:** Windows & Linux
**Repo:** https://github.com/imraj569/InstaHive

---

## 🚀 What is InstaHive?

**InstaHive** is a simple and powerful Python-based command-line tool to download **Instagram posts, reels, and videos**. It supports both **Windows** and **Linux** environments.

---

## ✨ Features

- 📥 Download Instagram **posts**, **reels**, and **IGTV** videos
- 💾 Saves files directly to your **Downloads** folder
- 🧠 Smart shortcode extractor
- 🔐 Login with **session saving**
- 💻 Works on both **Windows** and **Linux**
- ⚡ **Progress bar** during downloads for better visibility
- 🔒 **Log suppression** to minimize unnecessary logs
- 🧭 Mode picker: download a **single URL** or your **saved posts** in cautious batch mode

---

## 🧰 Requirements

- Python 3.8+
- Required packages are listed in `requirements.txt`

Install them using:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Usage

Clone the repository and run the script:

```bash
git clone https://github.com/imraj569/InstaHive
cd InstaHive
pip install -r requirements.txt
python instagram_downloader.py
```

Then follow the prompts to log in and paste any Instagram **post/reel** URL.

---

## 🧩 How It Works

1. **Login**: Upon first run, you'll be asked to log in with your Instagram credentials. The session is saved for future logins, so you won't need to log in again unless you choose to.
2. **Download**: Simply paste a URL from Instagram, and the tool will automatically extract the shortcode and start downloading the content.
3. **Progress Bar**: The download process now features a progress bar for better feedback on large files.
4. **Clean Interface**: The tool clears the screen after each download, ensuring a smooth user experience.

---

## 📂 Downloads Location

- **Default:** The standard user Downloads directory (`~/Downloads`, using OS-native path format)
- On startup, the CLI prompts for a download directory and shows the default path.
- Press **Enter** to use the shown default.
- If you choose a custom path, it is saved to `~/.insta-hive` and reused as the default on future runs.
- To reset the saved custom path, delete `~/.insta-hive` or enter a new path when prompted.

---

## ❄️ Nix Flake

You can use this repository as a flake and run InstaHive directly:

```bash
nix run --refresh github:Jones14021/InstaHive
```

If you're using a different fork, replace `Jones14021` with your repository owner.
This flake targets Linux and macOS systems (`x86_64-linux`, `aarch64-linux`, `x86_64-darwin`, `aarch64-darwin`).

To run from a branch (instead of default `main`), use `?ref=<branch-name>`:

```bash
# Example: run from branch "copilot/update-readme-and-add-interactive-mode"
nix run --refresh github:Jones14021/InstaHive?ref=copilot/update-readme-and-add-interactive-mode
```

To install from your NixOS configuration:

```nix
{
  inputs.instahive.url = "github:Jones14021/InstaHive";

  outputs = { self, nixpkgs, instahive, ... }: {
    nixosConfigurations.my-host = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ({ pkgs, ... }: {
          environment.systemPackages = [
            instahive.packages.${pkgs.system}.default
          ];
        })
      ];
    };
  };
}
```

---

## 🧑‍💻 Customization and Settings

- **Logging**: The script suppresses unnecessary logging from Instaloader to avoid cluttering the terminal.
- **Session File**: A session file is saved to avoid repeated logins. You can delete it to log in again.

---

## 🧪 Saved Posts Batch Mode (Interactive)

After you choose the download directory, InstaHive now asks for a mode:

1. **Single Instagram URL** (existing behavior)
2. **Saved posts batch mode** (for your logged-in account)

In batch mode, you can choose:

- **(a) Last X saved posts** (capped per run for safety)
- **(b) Select posts from a list** (with optional username/caption filtering, then index selection like `1,3-5`)

### ⚠️ Is this feasible/smart?

It is technically feasible, but Instagram can rate-limit or challenge accounts that automate too aggressively.  
This mode is intentionally conservative:

- small batch cap per run
- random delays between downloads
- periodic longer cooldown pauses
- one-at-a-time downloads (no parallel scraping)

Even with safeguards, there is still risk. Prefer small, infrequent runs and only use your own account/session.

---

## 🏷️ Topics

`instagram-downloader` `python-instagram-downloader` `download-instagram-posts`
`download-instagram-reels` `cli-tool` `linux` `windows` `instaloader`
`social-media-downloader` `automation` `python-tool`

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## ⭐ Give the repo a star if you found it useful!

---
