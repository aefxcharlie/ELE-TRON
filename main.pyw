import ctypes, glob, json, os, subprocess, sys, threading, time
import webview

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = getattr(sys, "_MEIPASS", HERE)
FROZEN = getattr(sys, "frozen", False)
DATA_DIR = os.path.join(os.environ.get("APPDATA", HERE), "ELE-TRON")
DATA = os.path.join(DATA_DIR, "data.json")
BG = os.path.join(DATA_DIR, "bg.txt")
NOWIN = 0x08000000
LA, AD = os.environ.get("LOCALAPPDATA", ""), os.environ.get("APPDATA", "")
PF = [os.environ.get(k, "") for k in ("PROGRAMFILES", "PROGRAMFILES(X86)")]
NAMES = {"chrome": "Chrome", "discord": "Discord", "steam": "Steam", "whatsapp": "WhatsApp", "telegram": "Telegram"}


def run(*args):
    try:
        return subprocess.run(list(args), creationflags=NOWIN, capture_output=True).returncode == 0
    except OSError:
        return False


def first(paths):
    return next((p for p in paths if p and os.path.exists(p)), None)


_start_apps = None


def start_app_id(name):
    """Find the real Windows app id (Store or installed apps) via Get-StartApps."""
    global _start_apps
    if _start_apps is None:
        try:
            out = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-StartApps | ConvertTo-Json -Compress"],
                                 capture_output=True, text=True, creationflags=NOWIN, timeout=25).stdout
            d = json.loads(out or "[]")
            _start_apps = d if isinstance(d, list) else [d]
        except Exception:
            _start_apps = []
    for a in _start_apps:
        if str(a.get("Name", "")).lower().startswith(name.lower()):
            return a.get("AppID")


def store_cmd(pkg_glob, name):
    if glob.glob(os.path.join(LA, "Packages", pkg_glob)):
        aid = start_app_id(name)
        if aid:
            return ["explorer.exe", "shell:AppsFolder\\" + aid]


def app_cmd(name):
    if name == "chrome":
        p = first([os.path.join(b, r"Google\Chrome\Application\chrome.exe") for b in PF + [LA]])
        return [p] if p else None
    if name == "discord":
        p = first([os.path.join(LA, "Discord", "Update.exe")])
        return [p, "--processStart", "Discord.exe"] if p else None
    if name == "steam":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as k:
                p = first([winreg.QueryValueEx(k, "SteamExe")[0]])
            if p:
                return [p]
        except OSError:
            pass
        p = first([os.path.join(b, "Steam", "steam.exe") for b in PF])
        return [p] if p else None
    if name == "whatsapp":
        p = first([os.path.join(LA, "WhatsApp", "WhatsApp.exe")])
        if p:
            return [p]
        return store_cmd("5319275A.WhatsAppDesktop_*", "WhatsApp")
    if name == "telegram":
        p = first([os.path.join(AD, "Telegram Desktop", "Telegram.exe"), os.path.join(LA, "Telegram Desktop", "Telegram.exe")] +
                  [os.path.join(b, "Telegram Desktop", "Telegram.exe") for b in PF])
        if p:
            return [p]
        return store_cmd("TelegramMessengerLLP.TelegramDesktop_*", "Telegram")
    return None


class Api:
    def load_data(self, a=None):
        try:
            with open(DATA, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def save_data(self, a):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(a["data"], f, indent=2, ensure_ascii=False)

    def load_bg(self, a=None):
        try:
            with open(BG, encoding="utf-8") as f:
                return f.read()
        except OSError:
            return ""

    def save_bg(self, a):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(BG, "w", encoding="utf-8") as f:
            f.write(a.get("data") or "")

    def is_autostart(self, a=None):
        return "--autostart" in sys.argv

    def quit(self, a=None):
        threading.Timer(0.2, lambda: os._exit(0)).start()

    def detect_apps(self, a=None):
        return {k: app_cmd(k) is not None for k in NAMES}

    def chrome_profiles(self, a=None):
        p = os.path.join(LA, r"Google\Chrome\User Data\Local State")
        try:
            with open(p, encoding="utf-8-sig") as f:
                cache = json.load(f)["profile"]["info_cache"]
            return [{"dir": k, "name": v.get("name"), "email": v.get("user_name")} for k, v in cache.items()]
        except (OSError, ValueError, KeyError):
            return []

    def pick(self, a):
        try:
            dt = webview.FileDialog.FOLDER if a.get("folder") else webview.FileDialog.OPEN
        except AttributeError:
            dt = webview.FOLDER_DIALOG if a.get("folder") else webview.OPEN_DIALOG
        r = webview.windows[0].create_file_dialog(dt)
        return r[0] if r else None

    def launch(self, a):
        groups, missing = {}, []
        for it in a["items"]:
            t = (it.get("target") or "").strip()
            kind = it.get("kind")
            if kind == "app":
                cmd = app_cmd(it.get("app", ""))
                if cmd:
                    subprocess.Popen(cmd)
                    time.sleep(0.4)
                else:
                    missing.append(NAMES.get(it.get("app"), "app"))
            elif kind == "chrome" and t:
                groups.setdefault(it.get("profile") or "", []).append(t)
            elif t:
                try:
                    os.startfile(t)
                except OSError:
                    missing.append(t)
                time.sleep(0.25)
        for profile, urls in groups.items():
            exe = app_cmd("chrome")
            if exe:
                subprocess.Popen(exe + ([f"--profile-directory={profile}"] if profile else []) + urls)
            else:
                for u in urls:
                    os.startfile(u)
            time.sleep(0.4)
        return {"missing": missing}

    def set_autostart(self, a):
        if FROZEN:
            cmd = f'"{sys.executable}" --autostart'
        else:
            py = sys.executable
            if py.lower().endswith("python.exe"):
                py = py[:-10] + "pythonw.exe"
            cmd = f'"{py}" "{os.path.join(HERE, "main.pyw")}" --autostart'
        key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
        if a["on"]:
            ok = run("schtasks", "/Create", "/TN", "ELE-TRON", "/TR", cmd, "/SC", "ONLOGON", "/F")
            if not ok:  # ask Windows for admin (UAC prompt) just for this one command
                tr = cmd.replace('"', '\\"')
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "schtasks.exe",
                                                    f'/Create /TN ELE-TRON /TR "{tr}" /SC ONLOGON /F', None, 0)
                for _ in range(30):
                    time.sleep(1)
                    if run("schtasks", "/Query", "/TN", "ELE-TRON"):
                        ok = True
                        break
            if ok:
                run("reg", "delete", key, "/v", "ELE-TRON", "/f")
                return "Startup enabled (Task Scheduler, runs at logon)"
            if run("reg", "add", key, "/v", "ELE-TRON", "/t", "REG_SZ", "/d", cmd, "/f"):
                return "Startup enabled (Run key). Allow the admin prompt next time for Task Scheduler mode."
            raise RuntimeError("Could not enable startup")
        run("reg", "delete", key, "/v", "ELE-TRON", "/f")
        if run("schtasks", "/Query", "/TN", "ELE-TRON"):  # task exists
            if not run("schtasks", "/Delete", "/TN", "ELE-TRON", "/F"):  # needs admin, ask via UAC
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "schtasks.exe", "/Delete /TN ELE-TRON /F", None, 0)
                for _ in range(30):
                    time.sleep(1)
                    if not run("schtasks", "/Query", "/TN", "ELE-TRON"):
                        break
                else:
                    raise RuntimeError("Startup task not removed. Allow the admin prompt and try again.")
        return "Startup disabled"


if __name__ == "__main__":
    webview.create_window("ELE-TRON", os.path.join(BASE, "ui", "index.html"), js_api=Api(),
                          width=1080, height=720, min_size=(860, 580), background_color="#090b14")
    webview.start()
