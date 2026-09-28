<p align="center">
  <img src="icon.ico" width="120" alt="ELE-TRON">
</p>

# ELE-TRON

A lightweight, glass-style launcher that starts with Windows and opens your saved workspaces (Chrome profiles, Discord, Steam, WhatsApp, Telegram, any app, file, folder or link) automatically, along with a clean dashboard for notes, quick links and apps.

Hi, I'm **Chaitany**, also known as **aefxcharlie** on the internet. I built ELE-TRON as a small, fast, fully local startup launcher: no cloud, no accounts, no background AI, just a tidy panel that sets up your PC the way you left it.

**ELE-TRON is open source. Enjoy!**

---

## Features

- **Auto-start at login.** Launches when you sign in to Windows, shows a short countdown, then opens your default workspace. Cancel or switch workspace during the countdown.
- **Workspaces.** Group anything you want into one-click setups (Work, Study, Gaming, and so on).
- **Auto-detected apps.** Chrome, Discord, Steam, WhatsApp and Telegram show up as one-click options, but only if they are installed on your PC.
- **Chrome profiles.** Pick which of your Chrome accounts to open and which website to load, for example a mail site in your work profile.
- **Custom apps.** Add any app, file, folder or URL by path, with Browse buttons.
- **Notes.** Colour-coded cards with search, pinning, checklists and word count.
- **Quick Links and Apps.** Pin favourite sites and programs on your dashboard.
- **Custom background.** Use your own image, choose how it fits (fill, fit, stretch, original size) and tune background blur, dimming, glass blur and glass tint.
- **Light on resources.** Roughly 50-80 MB of RAM. It exits itself after an automatic startup launch, so it uses nothing while you work.
- **100% local.** All data stays on your PC.

---

## Requirements

| Requirement | Details |
|---|---|
| OS | Windows 10 or Windows 11 |
| Python | **3.10 to 3.13**. Avoid brand-new releases such as 3.14 until `pythonnet` supports them. Not needed if you only use the built `.exe`. |
| WebView2 Runtime | Preinstalled on Windows 11 and up-to-date Windows 10. If the window stays blank, install it from Microsoft. |
| Python packages | `pywebview` (installed for you, see below) |
| Internet | Only needed once to download the packages. About 15-20 MB for `pywebview`, plus about 3 MB for `pyinstaller` if you build the `.exe`. |

When installing Python, tick **"Add python.exe to PATH"** in the installer.

---

## Quick start (run from source)

```
git clone https://github.com/aefxcharlie/ELE-TRON.git
cd ELE-TRON
pip install pywebview
python main.pyw
```

Or download the ZIP, extract it, open a terminal in the folder and run the last two commands.

After the first run you can simply double-click `main.pyw`.

---

## Build a standalone `.exe`

Double-click **`build_exe.bat`**. It runs, in order:

1. `pip install pyinstaller pywebview` installs the build tool and the UI library.
2. `pyinstaller --noconsole --noconfirm --name ELE-TRON --icon icon.ico --add-data "ui;ui" main.pyw` packages the app without a console window, includes the `ui` folder and sets the icon.
3. Prints the location of the finished app.

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

## Where your data lives

Everything is stored in `%APPDATA%\ELE-TRON\`:

- `data.json` holds workspaces, notes, links, apps and settings.
- `bg.txt` holds your background image.

It is never stored in the app folder, so sharing the app never shares your data. To reset the app, close it and delete that folder.

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
| `pywebview` fails to install | Use Python 3.10-3.13. |
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
└── requirements.txt  Python dependencies
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
