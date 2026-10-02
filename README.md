<p align="center">
  <img src="icon.ico" width="120" alt="ELE-TRON">
</p>

> [!TIP]
> **This is the official ELE-TRON repository: [github.com/aefxcharlie/ELE-TRON](https://github.com/aefxcharlie/ELE-TRON).** If you find the same project anywhere else, it may contain malware. Please always verify the source before downloading or running anything.

# ELE-TRON

![ELE-TRON Live-Demo](assets/ele-tron.gif)

A lightweight, glass-style launcher that starts with Windows and opens your saved workspaces (Chrome profiles, Discord, Steam, WhatsApp, Telegram, any app, file, folder or link) automatically, along with a clean dashboard for notes, quick links and your own screen-time activity.

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
- **Your Activity.** Tracks how long you actually use each app, logged automatically in the background. Switch between Day, Week and Month views with back/forward navigation, plus 7-day, 30-day, 6-month and 1-year trend graphs with a daily average. Windows' own background processes and shell surfaces are filtered out automatically. Fully local, and can be turned off in Settings.
- **Custom background.** Use your own image, choose how it fits (fill, fit, stretch, original size) and tune background blur, dimming, glass blur and glass tint.
- **Music widget.** A compact glass pill in the bottom-right corner shows what's playing and expands into a full panel with a left sidebar for MP3, WAV and Apple Music, list/icon library views, and hover tooltips on the icon-only controls. Fully local. Apple Music and Spotify (Microsoft Store or desktop app) are auto-detected and show up live in the widget if installed.
- **System tray.** Runs from the tray; closing the window minimizes it instead of quitting (toggle in Settings).
- **Light on resources.** Roughly 50-80 MB of RAM. It exits itself after an automatic startup launch, so it uses nothing while you work.
- **100% local.** All data stays on your PC.

---

## v1.1.0 vs v1.2.0

Comparison between [v1.1.0](https://github.com/aefxcharlie/ELE-TRON/releases/tag/v1.1.0) and [v1.2.0](https://github.com/aefxcharlie/ELE-TRON/releases/tag/v1.2.0) (this version).

| | v1.1.0 | v1.2.0 |
|---|---|---|
| Sidebar | Home, Workspaces, Notes, **Apps**, Settings | Home, Workspaces, Notes, **Your Activity**, Settings |
| Custom Apps list | A separate "Apps" page for saving custom app/folder shortcuts | Removed. Use **Workspaces → ＋ Other app / file / folder** instead, which already covered the same job |
| App usage tracking | None | Background tracker logs which app is in the foreground and for how long, entirely offline |
| Activity views | — | **Day**, **Week** and **Month**, each with back/forward navigation to any past period |
| Activity trends | — | Graphs for **7 days**, **30 days**, **6 months** and **1 year**, each with a daily average and a top-apps breakdown |
| Missing-data days | — | Handled gracefully: a day, week or month with nothing recorded shows "No activity recorded", never a crash |
| Ignored processes | — | Windows shell/background surfaces (Explorer, `dwm.exe`, `svchost.exe`, `RuntimeBroker.exe`, Search, Lock Screen, and more) and ELE-TRON itself are never counted |
| Activity data file | — | `activity.json` in `%APPDATA%\ELE-TRON\`, one entry per day with each app's accumulated seconds that day |
| Privacy control | — | **Track app activity** toggle in Settings; turning it off stops tracking immediately |
| New Python dependencies | — | `pywin32` and `psutil` (already in `requirements.txt`), used to identify the foreground window's process |

Greetings in v1.2.0 (unchanged since v1.1.0):

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

## Your Activity

ELE-TRON quietly watches which window is in the foreground, roughly every 5 seconds, and adds the time to that app's tally for the day. No typing, URLs, screenshots or window titles are ever recorded, only **which app** and **for how long**.

Open **Your Activity** from the sidebar:

- **Day / Week / Month** pills at the top switch the view. It opens on **Day** (today) by default.
- **‹ ›** step one period back or forward; **Back to today** jumps straight home again.
- The **Day** view lists every app you used that day with its total time, longest first.
- **Week** and **Month** add a small bar chart of totals per day across the period, plus the same per-app breakdown combined for the whole range.
- The **Trends** card at the bottom graphs **7 days**, **30 days**, **6 months** or **1 year**, each with a daily average, a running total and the top apps for that range.
- A day, week, month or range with nothing recorded simply says **"No activity recorded"** instead of showing broken or missing data.

What gets ignored automatically, so your numbers reflect real usage:

- Windows shell and background surfaces: File Explorer, the desktop, `dwm.exe`, Search, the Start menu, Lock Screen, `svchost.exe`, `RuntimeBroker.exe`, and similar system processes.
- ELE-TRON itself, so having the launcher open never counts against you.
- Blips under 2 seconds (an accidental alt-tab, a flash of focus while switching windows).
- Windows Store (UWP) apps are resolved to their real process, not the generic host that launches them, so they show up under their own name instead of being skipped.

Tracking can be switched off entirely from **Settings → Track app activity**. Turning it off stops logging immediately; turning it back on resumes from that point, it never retroactively fills in the gap.

---

## Where your data lives

Everything is stored in `%APPDATA%\ELE-TRON\`:

- `data.json` holds workspaces, notes, links and settings.
- `bg.txt` holds your background image.
- `activity.json` holds your app-usage log: one entry per day, with each app's total tracked seconds for that day.

It is never stored in the app folder, so sharing the app never shares your data. Your MP3/WAV folder locations are stored here too, not the audio files themselves. To reset the app, close it and delete that folder. To reset just the activity log, delete `activity.json` alone, the rest of your data is untouched.

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
| Your Activity shows nothing | Give it a few minutes of normal use first, it logs in real time and does not back-fill history from before tracking was on. Also check **Settings → Track app activity** is turned on. |
| A Store app isn't showing up by name | Close and reopen it once after updating; ELE-TRON resolves the real process behind the Store host window the next time it's brought to the foreground. |

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
