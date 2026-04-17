# InstaHive 🐝 - Instagram Downloader CLI

**Author:** [Rajkishor Patra](https://github.com/imraj569)
**Tool:** `instagram_downloader.py`
**Platform:** Windows & Termux (Android)
**Repo:** https://github.com/imraj569/InstaHive

---

## 🚀 What is InstaHive?

**InstaHive** is a simple and powerful Python-based command-line tool to download **Instagram posts, reels, and videos**. It supports both **Windows** and **Termux** environments.

---

## ✨ Features

- 📥 Download Instagram **posts**, **reels**, and **IGTV** videos
- 💾 Saves files directly to your **Downloads** folder
- 🧠 Smart shortcode extractor
- 🔐 Login with **session saving**
- 💻 Works on both **Windows** and **Android-Termux**
- ⚡ **Progress bar** during downloads for better visibility
- 🔒 **Log suppression** to minimize unnecessary logs

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

- **Windows:** `C:/Users/YourName/Downloads`
- **Termux:** `/data/data/com.termux/files/home/storage/downloads`

---

## ❄️ Nix Flake

You can use this repository as a flake and run InstaHive directly:

```bash
nix run github:<owner>/InstaHive
```

Replace `<owner>` with the GitHub owner of the fork/repository you want to use.

To install from your NixOS configuration:

```nix
{
  inputs.instahive.url = "github:<owner>/InstaHive";

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

## 🏷️ Topics

`instagram-downloader` `python-instagram-downloader` `download-instagram-posts`
`download-instagram-reels` `cli-tool` `termux` `windows` `instaloader`
`social-media-downloader` `automation` `python-tool`

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## ⭐ Give the repo a star if you found it useful!

---
