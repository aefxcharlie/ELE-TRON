<p align="center">
  <img src="icon.ico" width="120" alt="ELE-TRON">
</p>

> [!TIP]
> **This is the official ELE-TRON repository: [github.com/aefxcharlie/ELE-TRON](https://github.com/aefxcharlie/ELE-TRON).** If you find the same project anywhere else, it may contain malware. Please always verify the source before downloading or running anything.

# ELE-TRON

A lightweight, glass-style launcher that starts with Windows and opens your saved workspaces (Chrome profiles, Discord, Steam, WhatsApp, Telegram, any app, file, folder or link) automatically, along with a clean dashboard for notes, quick links and apps.

Hi, I'm **Chaitany**, also known as **aefxcharlie** on the internet. I built ELE-TRON as a small, fast, fully local startup launcher: no cloud, no accounts, no background AI, just a tidy panel that sets up your PC the way you left it.

**ELE-TRON is open source. Enjoy!**

---

## Features

- **Auto-start at login.** Launches when you sign in to Windows, shows a short countdown, then opens your default workspace. Cancel or switch workspace during the countdown.
- **Workspaces.** Group anything you want into one-click setups (Work, Study, Gaming, and so on).
- **Auto-detected apps.** Chrome, Discord, Steam, WhatsApp, Telegram, Apple Music and Spotify (including the Microsoft Store versions) show up as one-click options, but only if they are installed on your PC.
- **Live greeting.** The home page greets you by time of day and updates in real time: *This early* (12am-5:59am), *Good morning* (6am-11:59am), *Good afternoon* (12pm-5:59pm), *Good evening* (6pm-8:59pm), *This late* (9pm-11:59pm).
- **Chrome profiles.** Pick which of your Chrome accounts to open and which website to load, for example a mail site in your work profile.
- **Custom apps.** Add any app, file, folder or URL by path, with Browse buttons.
- **Notes.** Colour-coded cards with search, pinning, checklists and word count.
- **Quick Links and Apps.** Pin favourite sites and programs on your dashboard.
- **Custom background.** Use your own image, choose how it fits (fill, fit, stretch, original size) and tune background blur, dimming, glass blur and glass tint.
- **Music widget.** A compact glass pill in the bottom-right corner shows what's playing and expands into a full panel with a left sidebar for MP3, WAV and Apple Music, list/icon library views, and hover tooltips on the icon-only controls. Fully local. Apple Music and Spotify (Microsoft Store or desktop app) are auto-detected and show up live in the widget if installed.
- **System tray.** Runs from the tray; closing the window minimizes it instead of quitting (toggle in Settings).
- **Light on resources.** Roughly 50-80 MB of RAM. It exits itself after an automatic startup launch, so it uses nothing while you work.
- **100% local.** All data stays on your PC.

---

## v1.0.0 vs v1.1.0

Comparison between [v1.0.0](https://github.com/aefxcharlie/ELE-TRON/releases/tag/v1.0.0) (initial public release) and v1.1.0 (this version).

| | v1.0.0 | v1.1.0 |
|---|---|---|
| Python | 3.10 to 3.13 | **3.13 or newer only** |
| Python packages | `pywebview` only | `pywebview`, `mutagen`, `pystray`, `pillow`, `winrt-*` (all required, `pip install -r requirements.txt`) |
| Music widget | None | Glass pill in the bottom-right that expands into a full panel (MP3, WAV, Apple Music, Spotify) with scrollable list/icon views, looping title marquee, real-time timeline with seek, and a size-adaptive layout |
| MP3 / WAV library | None | Local folder scan with title, artist, album and artwork |
| Apple Music | Not supported | Auto-detected (Store app), live now-playing card and controls |
| Spotify | Not supported | Auto-detected (Store or desktop app), live now-playing card and controls |
| Windows media API | None | `winrt-*` packages (replaces `winsdk`, which does not support Python 3.13) |
| System tray | None | Tray icon with **Minimize to tray** toggle (window hides only when the tray icon is running) |
| Recently played | None | Local history of Apple Music/Spotify tracks, with playback from your MP3/WAV library when a match exists |
| Auto-detected apps | Chrome, Discord, Steam, WhatsApp, Telegram | Same, plus Apple Music and Spotify (Store versions included) |
| Home greeting | Good morning / afternoon / evening, refreshed every 15 seconds | Five time-based greetings, updated in real time (every second) |
| `requirements.txt` | `pywebview` | Full dependency list |
| `build_exe.bat` | Installs `pyinstaller` and `pywebview`, then builds | Checks for Python 3.13+, installs all requirements (stops on failure), bundles every package |

Greetings in v1.1.0:

| Time | Greeting |
|---|---|
| 12:00 am to 5:59 am | This early, *name*? |
| 6:00 am to 11:59 am | Good morning, *name* |
| 12:00 pm to 5:59 pm | Good afternoon, *name* |
| 6:00 pm to 8:59 pm | Good evening, *name* |
| 9:00 pm to 11:59 pm | This late, *name*? |

---

## Requirements

| Requirement | Details |
|---|---|
| OS | Windows 10 or Windows 11 |
| Python | **3.13 or newer only.** Older versions (3.12 and below) are not supported. Not needed if you only use the built `.exe`. |
| WebView2 Runtime | Preinstalled on Windows 11 and up-to-date Windows 10. If the window stays blank, install it from Microsoft. |
| Python packages | All required, installed with `pip install -r requirements.txt`: `pywebview`, `mutagen`, `pystray`, `pillow`, and the `winrt-*` packages (`winrt-runtime`, `winrt-Windows.Foundation`, `winrt-Windows.Foundation.Collections`, `winrt-Windows.Storage`, `winrt-Windows.Storage.Streams`, `winrt-Windows.Media.Control`). |
| Internet | Only needed once to download the packages. Roughly 30-40 MB of packages, plus about 3 MB for `pyinstaller` if you build the `.exe`. |

When installing Python, tick **"Add python.exe to PATH"** in the installer.

---

## Quick start (run from source)

```
git clone https://github.com/aefxcharlie/ELE-TRON.git
cd ELE-TRON
pip install -r requirements.txt
python main.pyw
```

Or download the ZIP, extract it, open a terminal in the folder and run the last two commands.

After the first run you can simply double-click `main.pyw`.

---

## Build a standalone `.exe`

Double-click **`build_exe.bat`**. It runs, in order:

1. Checks that Python is 3.13 or newer.
2. `pip install pyinstaller` installs the build tool.
3. `pip install -r requirements.txt` installs every dependency. The build stops if this fails.
4. Runs PyInstaller, bundling all packages, without a console window, with the `ui` folder and the icon included.
5. Prints the location of the finished app.

Result:

```
dist\ELE-TRON\ELE-TRON.exe
```

Always run the app from `dist\ELE-TRON`, never from the `build` folder (that one is only temporary build output and will not start). Keep the whole `dist\ELE-TRON` folder together. The `.exe` needs the files next to it, so do not move it out on its own. You can move or rename the entire folder, and share it (zipped) with friends who do not have Python.

The `build` folder and `ELE-TRON.spec` file created during the build are safe to delete.

---

## Start with Windows

1. Open ELE-TRON and go to **Settings**.
2. Turn **Start with Windows** on.
3. Approve the Windows admin (UAC) prompt.

With approval, ELE-TRON registers a **Task Scheduler** task that runs at logon, which is the earliest reliable point for a user app, ahead of most startup programs. If you decline the prompt, it falls back to the normal Windows **Run** startup key, which works but starts a bit later.

Also set:

- **Auto-launch default workspace after login**: on or off
- **Default workspace**: which workspace opens
- **Countdown**: seconds before it launches (you can cancel)

To check it: `schtasks /Query /TN ELE-TRON`

If you move the app folder, turn **Start with Windows** off and on again so the new path is registered.

---

## Music

The music widget sits bottom-right: pick a **MP3 folder** and/or **WAV folder** the first time you open a source (or from Settings), and ELE-TRON scans it for playable files. Playback, browsing (List or Icon view, both scrollable) and artwork all stay fully local. Long titles scroll smoothly in a loop inside their own box, the timeline updates in real time (also right after the app is reopened from the tray), and the widget shrinks with the window so it never covers your content.

Required packages (all included in `requirements.txt`):

- **`mutagen`** reads track title/artist/album and embedded artwork.
- **`winrt-*`** packages give **Apple Music** and **Spotify** their live now-playing card (track, art, play/pause/next/previous, progress) via Windows' System Media Transport Controls, the same public interface Windows uses for its own media overlay. These replace the older `winsdk` package, which does not support Python 3.13.
- **`pystray`** and **`pillow`** provide the tray icon behind **Minimize to tray**. The window only hides to the tray once the tray icon is actually running, so it can always be brought back.

Apple Music and Spotify only appear as a source, and as Workspace apps, if they are installed on your PC (Microsoft Store or desktop version). Both are detected automatically, so they cannot and need not be added as custom apps. ELE-TRON never bypasses their login, subscription or DRM. Because of that, streamed songs can only play inside their own app. ELE-TRON keeps a local **Recently played** list (stored in `data.json`); if a listed song also exists in your MP3/WAV folders, you can play it from there even after closing Apple Music or Spotify.

---

## Where your data lives

Everything is stored in `%APPDATA%\ELE-TRON\`:

- `data.json` holds workspaces, notes, links, apps and settings.
- `bg.txt` holds your background image.

It is never stored in the app folder, so sharing the app never shares your data. Your MP3/WAV folder locations are stored here too, not the audio files themselves. To reset the app, close it and delete that folder.

---

## Uninstall

1. In **Settings**, turn **Start with Windows** off.
2. Delete the app folder.
3. Optionally delete `%APPDATA%\ELE-TRON\`.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` is not recognized | Reinstall Python with **Add to PATH** ticked, then open a new terminal. |
| `pip` or `python` blocked in PowerShell | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, or use Command Prompt. |
| Blank window | Install the Microsoft **WebView2 Runtime**. |
| `pywebview` or a `winrt-*` package fails to install | Use Python 3.13 or newer (64-bit) and run `python -m pip install --upgrade pip` first. |
| Apple Music or Spotify not showing | Make sure the app is installed and has been opened once, then restart ELE-TRON. |
| An app says "Not found" | It is not installed in a standard location. Add it as a **custom app** using its path. |
| Startup did not run | Turn **Start with Windows** off and on, and approve the admin prompt. |

---

## Project structure

```
ELE-TRON/
├── main.pyw          Python backend (launching, detection, startup, storage)
├── ui/index.html     Frontend (HTML, CSS, JS in a single file)
├── build_exe.bat     One-click .exe builder
├── icon.ico          App icon
└── requirements.txt  Python dependencies (all required)
```

Built with Python, [pywebview](https://pywebview.flowrl.com/) and plain HTML/CSS/JS.

---

## Contributing

Issues, ideas and pull requests are welcome. Fork the repo, make your change and open a pull request.

---

## License

Released under the **MIT License**. See [LICENSE.md](LICENSE.md). You are free to use, modify and share it.

---

## Author

**Chaitany** (aefxcharlie)
GitHub: [github.com/aefxcharlie](https://github.com/aefxcharlie)

If ELE-TRON helps you, a star on the repo is appreciated. Enjoy!
