import asyncio, base64, ctypes, glob, json, os, subprocess, sys, threading, time
from datetime import datetime, timezone
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
NAMES = {"chrome": "Chrome", "discord": "Discord", "steam": "Steam", "whatsapp": "WhatsApp",
         "telegram": "Telegram", "applemusic": "Apple Music", "spotify": "Spotify"}
LIVE_SRC = {"applemusic": "apple", "spotify": "spotify"}

try:
    from mutagen import File as MutaFile
    HAS_MUTAGEN = True
except Exception:
    HAS_MUTAGEN = False

try:
    from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
    from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as PBStatus
    from winrt.windows.storage.streams import DataReader
    HAS_SMTC = True
except Exception:
    HAS_SMTC = False

try:
    import pystray
    from PIL import Image as PILImage, ImageDraw
    HAS_TRAY = True
except Exception:
    HAS_TRAY = False


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
    if name == "applemusic":
        return store_cmd("AppleInc.AppleMusic*", "Apple Music")
    if name == "spotify":
        p = first([os.path.join(AD, "Spotify", "Spotify.exe")])
        if p:
            return [p]
        return store_cmd("SpotifyAB.SpotifyMusic_*", "Spotify")
    return None


# ---------------- Music: local MP3/WAV library ----------------
AUDIO_EXT = {"mp3": (".mp3",), "wav": (".wav", ".wave")}


def _scan(folder, exts, limit=1000):
    out = []
    if not folder or not os.path.isdir(folder):
        return out
    for root, _dirs, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(exts):
                out.append(os.path.join(root, f))
                if len(out) >= limit:
                    return out
    return out


def _track_meta(path):
    title = os.path.splitext(os.path.basename(path))[0]
    artist = album = ""
    duration = 0
    if HAS_MUTAGEN:
        try:
            mf = MutaFile(path, easy=True)
            if mf:
                title = (mf.get("title") or [title])[0]
                artist = (mf.get("artist") or [""])[0]
                album = (mf.get("album") or [""])[0]
                if mf.info is not None and getattr(mf.info, "length", None):
                    duration = int(mf.info.length)
        except Exception:
            pass
    return {"path": path, "title": title, "artist": artist, "album": album, "duration": duration}


# ---------------- Music: Apple Music via System Media Transport Controls ----------------
def _run_async(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


def _smtc_session(source="applemusic"):
    key = LIVE_SRC.get(source, "apple")

    async def _get():
        mgr = await MediaManager.request_async()
        sessions = list(mgr.get_sessions())
        for s in sessions:
            aid = (s.source_app_user_model_id or "").lower()
            if key in aid and (key != "apple" or "music" in aid):
                return s
        for s in sessions:
            if key in (s.source_app_user_model_id or "").lower():
                return s
        return None
    return _run_async(_get())


_TRK = {"key": None, "t0": 0.0}


def _live_pos(tl, title, pos, dur, playing):
    """SMTC only refreshes `position` on play/pause/seek, so extrapolate it to 'now'."""
    if not playing:
        return pos
    try:
        lu = tl.last_updated_time
        if lu.tzinfo is None:
            lu = lu.replace(tzinfo=timezone.utc)
        d = (datetime.now(timezone.utc) - lu).total_seconds()
        if 0 <= d <= (dur if dur > 0 else 3600):
            return pos + d
    except Exception:
        pass
    # Fallback: count time ourselves from the first moment we saw this position.
    key = (title, round(pos, 1))
    if _TRK["key"] != key:
        _TRK["key"], _TRK["t0"] = key, time.time()
    return pos + (time.time() - _TRK["t0"])


async def _read_thumb(stream_ref):
    try:
        stream = await stream_ref.open_read_async()
        size = stream.size
        if not size:
            return None
        reader = DataReader(stream)
        await reader.load_async(size)
        buf = bytearray(size)
        reader.read_bytes(buf)
        return "data:image/png;base64," + base64.b64encode(bytes(buf)).decode()
    except Exception:
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
        def _q():
            if TRAY["icon"] is not None:
                try:
                    TRAY["icon"].stop()
                except Exception:
                    pass
            os._exit(0)
        threading.Timer(0.2, _q).start()

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

    def set_tray_pref(self, a):
        TRAY["minimize"] = bool(a.get("on"))
        return True

    def has_music_extras(self, a=None):
        return {"mutagen": HAS_MUTAGEN, "smtc": HAS_SMTC, "tray": HAS_TRAY}

    def music_scan(self, a):
        exts = AUDIO_EXT.get(a.get("kind"))
        if not exts:
            return []
        return [_track_meta(p) for p in _scan(a.get("folder") or "", exts)]

    def music_artwork(self, a):
        if not HAS_MUTAGEN:
            return None
        path = a.get("path") or ""
        try:
            mf = MutaFile(path)
            pics = getattr(mf, "pictures", None)
            data = mime = None
            if pics:
                data, mime = pics[0].data, pics[0].mime
            elif mf is not None and mf.tags:
                for k in list(mf.tags.keys()):
                    if str(k).startswith("APIC"):
                        p = mf.tags[k]
                        data, mime = p.data, p.mime
                        break
            if data:
                return f"data:{mime or 'image/jpeg'};base64,{base64.b64encode(data).decode()}"
        except Exception:
            pass
        return None

    def music_stream(self, a):
        """Read a local audio file and hand it back as a data: URI.
        file:// playback is unreliable/blocked inside WebView2 for paths
        outside the app folder, so we stream bytes through the JS bridge
        instead (same trick music_artwork already uses for cover art)."""
        path = a.get("path") or ""
        try:
            if not os.path.isfile(path):
                return None
            with open(path, "rb") as f:
                data = f.read()
            ext = os.path.splitext(path)[1].lower()
            mime = "audio/mpeg" if ext == ".mp3" else "audio/wav"
            return f"data:{mime};base64,{base64.b64encode(data).decode()}"
        except Exception:
            return None

    def music_now_playing(self, a=None):
        if not HAS_SMTC:
            return None
        a = a or {}
        try:
            s = _smtc_session(a.get("source") or "applemusic")
            if not s:
                return None
            known = a.get("artkey") or ""

            async def _info():
                props = await s.try_get_media_properties_async()
                pb = s.get_playback_info()
                tl = s.get_timeline_properties()
                title = (props.title if props else "") or ""
                artist = (props.artist if props else "") or ""
                album = (props.album_title if props else "") or ""
                key = f"{title}|{artist}|{album}"
                art, artkey = None, ""
                if props and props.thumbnail:
                    if known and known == key:
                        artkey = key  # front-end already has this artwork
                    else:
                        art = await _read_thumb(props.thumbnail)
                        artkey = key if art else ""
                playing = pb.playback_status == PBStatus.PLAYING if pb else False
                st = tl.start_time.total_seconds() if tl and tl.start_time else 0
                en = tl.end_time.total_seconds() if tl and tl.end_time else 0
                dur = max(0, en - st)
                pos = max(0, (tl.position.total_seconds() if tl and tl.position else 0) - st)
                if tl:
                    pos = _live_pos(tl, title, pos, dur, playing)
                if dur:
                    pos = min(pos, dur)
                return {"title": title, "artist": artist, "album": album, "art": art, "artkey": artkey,
                        "playing": playing, "position": pos, "duration": dur}
            return _run_async(_info())
        except Exception:
            return None

    def music_control(self, a):
        if not HAS_SMTC:
            return False
        try:
            s = _smtc_session(a.get("source") or "applemusic")
            if not s:
                return False
            action = a.get("action")

            async def _do():
                if action == "playpause":
                    await s.try_toggle_play_pause_async()
                elif action == "pause":
                    await s.try_pause_async()
                elif action == "next":
                    await s.try_skip_next_async()
                elif action == "prev":
                    await s.try_skip_previous_async()
                elif action == "seek":
                    await s.try_change_playback_position_async(int(float(a.get("pos") or 0) * 10_000_000))
            _run_async(_do())
            return True
        except Exception:
            return False


# ---------------- System tray ----------------
TRAY = {"icon": None, "minimize": True, "ready": False}


def _tray_image():
    for base in (BASE, HERE):
        try:
            return PILImage.open(os.path.join(base, "icon.ico")).convert("RGBA")
        except Exception:
            continue
    img = PILImage.new("RGBA", (64, 64), (0, 0, 0, 0))  # fallback so the tray never fails on a missing icon
    d = ImageDraw.Draw(img)
    d.ellipse((4, 4, 60, 60), fill=(124, 140, 255, 255))
    d.ellipse((20, 20, 44, 44), fill=(9, 11, 20, 255))
    return img


def _show_window(window):
    window.show()
    try:
        window.restore()
    except Exception:
        pass
    try:
        window.evaluate_js("window.onAppShown&&window.onAppShown()")
    except Exception:
        pass


def _tray_start(window):
    if not HAS_TRAY:
        return
    try:
        def _show(icon, item):
            _show_window(window)

        def _quit(icon, item):
            icon.stop()
            os._exit(0)

        def _setup(icon):
            icon.visible = True
            TRAY["ready"] = True

        menu = pystray.Menu(
            pystray.MenuItem("Show ELE-TRON", _show, default=True),
            pystray.MenuItem("Quit", _quit),
        )
        TRAY["icon"] = pystray.Icon("ELE-TRON", _tray_image(), "ELE-TRON", menu)
        TRAY["icon"].run_detached(_setup)
    except Exception:
        TRAY["icon"], TRAY["ready"] = None, False


def _on_closing():
    # Only hide when the tray icon is really up, otherwise the window could never be brought back.
    if TRAY["ready"] and TRAY["minimize"]:
        window.hide()
        return False
    return True


if __name__ == "__main__":
    window = webview.create_window("ELE-TRON", os.path.join(BASE, "ui", "index.html"), js_api=Api(),
                                    width=1080, height=720, min_size=(860, 580), background_color="#090b14")
    try:
        window.events.closing += _on_closing
    except Exception:
        pass
    webview.start(_tray_start, window)
