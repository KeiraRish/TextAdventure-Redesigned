import html
import json
import random
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


st.set_page_config(page_title="Apartment Morning Adventure", page_icon="🏡", layout="wide")

LEADERBOARD_DB = Path(__file__).resolve().parent / "leaderboard.sqlite3"


def supabase_config():
    try:
        config = st.secrets["supabase"]
    except (KeyError, StreamlitSecretNotFoundError):
        return None

    try:
        url = config["url"].rstrip("/")
        api_key = config["anon_key"]
    except KeyError as error:
        raise RuntimeError("Configure both [supabase].url and [supabase].anon_key in Streamlit secrets.") from error

    if not url or not api_key:
        raise RuntimeError("Configure both [supabase].url and [supabase].anon_key in Streamlit secrets.")
    return url, api_key


def supabase_request(method, resource, params=None, payload=None, prefer=None):
    config = supabase_config()
    if config is None:
        raise RuntimeError("Supabase leaderboard storage is not configured.")
    url, api_key = config
    query = f"?{urlencode(params)}" if params else ""
    request = Request(
        f"{url}/rest/v1/{resource}{query}",
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            **({"Prefer": prefer} if prefer else {}),
        },
        method=method,
    )

    try:
        with urlopen(request, timeout=10) as response:
            body = response.read()
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Supabase leaderboard request failed (HTTP {error.code}): {detail}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach Supabase leaderboard: {error.reason}") from error

    return json.loads(body) if body else None


def initialize_leaderboard():
    if supabase_config() is not None:
        return
    with sqlite3.connect(LEADERBOARD_DB) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_leaderboard():
    if supabase_config() is not None:
        rows = supabase_request(
            "GET",
            "leaderboard",
            {
                "select": "id,name,score",
                "order": "score.desc,created_at.asc,id.asc",
                "limit": "5",
            },
        )
        return [(row["id"], row["name"], row["score"]) for row in rows]
    with sqlite3.connect(LEADERBOARD_DB) as connection:
        return connection.execute(
            "SELECT id, name, score FROM leaderboard ORDER BY score DESC, created_at ASC, id ASC LIMIT 5"
        ).fetchall()


def find_leaderboard_name(name):
    if supabase_config() is not None:
        escaped_name = name.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_").replace('"', '\\"')
        rows = supabase_request(
            "GET",
            "leaderboard",
            {
                "select": "id,name,score",
                "name": f'ilike."{escaped_name}"',
                "order": "score.desc,id.asc",
                "limit": "1",
            },
        )
        if rows:
            row = rows[0]
            return row["id"], row["name"], row["score"]
        return None
    with sqlite3.connect(LEADERBOARD_DB) as connection:
        return connection.execute(
            "SELECT id, name, score FROM leaderboard WHERE name = ? COLLATE NOCASE ORDER BY score DESC, id ASC LIMIT 1",
            (name,),
        ).fetchone()


def add_leaderboard_score(name, score):
    if supabase_config() is not None:
        supabase_request(
            "POST",
            "leaderboard",
            payload={"name": name, "score": score},
            prefer="return=minimal",
        )
        return
    with sqlite3.connect(LEADERBOARD_DB) as connection:
        connection.execute(
            "INSERT INTO leaderboard (name, score) VALUES (?, ?)",
            (name, score),
        )


def replace_leaderboard_score(entry_id, name, score):
    if supabase_config() is not None:
        rows = supabase_request(
            "PATCH",
            "leaderboard",
            {"id": f"eq.{entry_id}", "select": "id"},
            {
                "name": name,
                "score": score,
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            prefer="return=representation",
        )
        if not rows:
            raise RuntimeError("The selected leaderboard entry no longer exists.")
        return
    with sqlite3.connect(LEADERBOARD_DB) as connection:
        connection.execute(
            "UPDATE leaderboard SET name = ?, score = ?, created_at = CURRENT_TIMESTAMP WHERE id = ?",
            (name, score, entry_id),
        )


initialize_leaderboard()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@600;700&display=swap');
    :root { --ink:#4d3a45; --muted:#806875; --line:#f2d8e3; --paper:#fffdfd; }
    .stApp { background: radial-gradient(circle at top right, #ffe5ef 0, #fffafc 34rem, #fff7fa 100%); color:var(--ink); font-family:'DM Sans', sans-serif; }
    .block-container { max-width:1180px; padding-top:4.5rem; padding-bottom:1.5rem; }
    h1,h2,h3,h4 { font-family:'Playfair Display', serif; }
    .hero { padding:1rem 1.3rem; border:1px solid var(--line); border-radius:18px; background:linear-gradient(110deg,#fff 15%,#ffe8f0); box-shadow:0 16px 35px rgba(210,126,158,.14); margin-bottom:.8rem; }
    .hero h1 { color:#a95278; margin:0; font-size:2.1rem; }
    .hero p { color:var(--muted); margin:.35rem 0 0; }
    .leaderboard-card { overflow:hidden; border:1px solid var(--line); border-radius:18px; background:rgba(255,255,255,.94); box-shadow:0 12px 30px rgba(210,126,158,.12); }
    .leaderboard-table { width:100%; border-collapse:collapse; color:var(--ink); font-size:1rem; }
    .leaderboard-table th { padding:.9rem 1.1rem; color:#a95278; background:#fff5f8; text-align:left; font-size:.78rem; text-transform:uppercase; letter-spacing:.1em; }
    .leaderboard-table td { padding:.85rem 1.1rem; border-top:1px solid #f7e8ed; }
    .leaderboard-table tbody tr { background:#fff; }
    .leaderboard-place { width:22%; font-weight:700; color:#a95278; }
    .leaderboard-name { font-weight:500; }
    .leaderboard-table tbody tr:nth-child(-n+3) .leaderboard-name { color:#a95278; font-weight:700; }
    .leaderboard-table tbody tr:nth-child(n+4) td { color:#000; }
    .leaderboard-score { text-align:right; font-weight:700; font-variant-numeric:tabular-nums; }
    .leaderboard-empty { padding:1.5rem !important; color:var(--muted); text-align:center; }
    .st-key-leaderboard_back_button { margin-top:1.5rem; }
    .welcome-screen { width:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; }
    .welcome-card { width:min(100%, 650px); text-align:center; }
    .welcome-card .hero { padding:2.2rem 2rem; border-radius:24px; }
    .welcome-card .hero h1 { font-size:clamp(2rem, 5vw, 3.4rem); }
    .welcome-card .hero p { font-size:1.05rem; }
    form:has(.welcome-card) { width:min(100%, 650px); min-height:78vh; box-sizing:border-box; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:2rem; border:0; background:transparent; box-shadow:none; margin:0 auto; }
    form:has(.welcome-card) .welcome-card { width:100%; }
    form:has(.welcome-card) .welcome-card .hero { padding:0; border:0; border-radius:0; background:transparent; box-shadow:none; margin-bottom:1.2rem; }
    form:has(.welcome-card) button { display:block; width:180px; margin:.07rem auto 0; }
    [data-testid="stForm"]:has(.welcome-card) { width:min(100%, 650px); min-height:78vh; box-sizing:border-box; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:2rem; border:0; background:transparent; box-shadow:none; margin:0 auto; }
    [data-testid="stForm"]:has(.welcome-card) > div { height:auto; flex:0 0 auto; }
    [data-testid="stForm"]:has(.welcome-card) [data-testid="stVerticalBlock"] { gap:14px; }
    [data-testid="stForm"]:has(.welcome-card) [data-testid="stFormSubmitButton"] { width:180px; margin:.07rem auto 0; }
    .st-key-leaderboard_button button { background:#fff !important; color:#a95278 !important; border:1px solid var(--line) !important; }
    form:has(.welcome-card), [data-testid="stForm"]:has(.welcome-card) { width:min(100%, 650px) !important; min-height:78vh !important; box-sizing:border-box; }
    [data-testid="stDialog"] { background:rgba(255,255,255,.72) !important; }
    [role="dialog"] { width:min(420px, calc(100vw - 2rem)) !important; background:#fff !important; color:var(--ink) !important; }
    [role="dialog"] input { background:#fff !important; }
    .panel { background:rgba(255,255,255,.88); border:1px solid var(--line); border-radius:16px; padding:.8rem 1rem; box-shadow:0 8px 22px rgba(210,126,158,.1); margin-bottom:.7rem; }
    .story { height:260px; overflow:auto; padding:.8rem; border:1px solid var(--line); border-radius:12px; background:var(--paper); display:flex; flex-direction:column; justify-content:flex-end; gap:.45rem; }
    .story p { margin:0; line-height:1.5; }
    .story:has([data-testid="stMarkdownPre"]) { height:420px; justify-content:flex-start; }
    .story [data-testid="stMarkdownPre"] { white-space:pre; overflow:visible; color:#a95278; font:10px/1 ui-monospace, SFMono-Regular, Menlo, monospace; background:#fff5f8; padding:.8rem; border-radius:12px; min-width:max-content; }
    .eyebrow { color:#b45d81; text-transform:uppercase; letter-spacing:.12em; font-size:.74rem; font-weight:700; }
    .rules { color:#a95278; font-size:.78rem; line-height:1.45; }
    .rules strong { color:#b45d81; }
    .metric { display:flex; justify-content:space-between; align-items:baseline; }
    .metric strong { color:#a95278; font-size:1.5rem; }
    .meter { height:10px; border-radius:99px; overflow:hidden; background:#f7dce6; }
    .meter span { display:block; height:100%; background:linear-gradient(90deg,#f7b6c8,#d9719d); }
    .tag { display:inline-block; padding:.3rem .6rem; margin:.2rem .2rem 0 0; border-radius:99px; background:#ffe8f0; color:#9b4f6b; font-size:.84rem; }
    .objective { padding:.45rem 0; color:var(--muted); border-bottom:1px solid #f7e8ed; }
    .objective:last-child { border-bottom:0; }
    </style>
    """,
    unsafe_allow_html=True,
)

ACTION_BREAK = "__ACTION_BREAK__"
PANCAKE_ART = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠲⢉⡽⢈⣠⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⢀⠄⢢⠫⡀⠸⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠃⡠⠃⠀⡇⠀⠱⠀⠀⠀⠉⠒⠤⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠤⠋⢀⠇⠀⠀⠱⡀⠀⠑⢄⠀⠈⠐⠒⠤⡀⠑⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣜⣻⣿⠿⠃⠠⠜⠃⠀⠀⠀⠀⠘⢄⡀⠀⠛⠤⠀⠀⠀⠘⡄⣸⣧⣘⡠⠤⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⢤⢲⠽⣿⣿⡿⠁⡄⠀⠀⠀⢀⠡⢄⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿⣿⣶⣬⣑⡠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢤⠲⣍⡾⢣⢋⡕⣊⠿⡇⠀⣧⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣷⣦⣑⢄⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⢊⢧⣋⢛⣥⣲⣥⣮⣴⣵⣾⣧⠀⢣⠱⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣂⠄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⢧⣛⣴⣾⣿⡿⣿⣿⢿⣿⡿⣿⣿⣷⣄⣀⠈⠢⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⢦⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⠘⣿⣿⣯⣷⣿⢿⣾⡿⣟⣿⣟⣯⣿⣿⣿⣿⣶⣶⣶⣤⣤⣀⣀⡀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢾⠀⠀
⠀⠀⠀⠀⠀⢀⡼⣆⢹⣿⣿⢷⣿⣻⣯⠿⣛⠫⠭⡍⡭⢭⣙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⡇⠀⠀
⠀⠀⠀⠀⣰⣍⣶⠛⣄⠙⠻⢿⡛⠍⣆⠳⢌⢣⠓⣬⠱⢦⡩⢝⡲⣌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢁⡔⢠⠇
⠀⠀⠀⠀⡟⣷⢣⠘⡄⣓⢄⡀⠉⠳⢬⣚⣌⡲⣉⠦⣋⢖⡩⢎⡵⢊⠷⣡⢿⣿⣿⣯⣿⣿⣿⡿⣿⣿⡿⣿⢿⡿⣿⢿⡿⣿⢿⣿⡿⠿⠛⠁⠀⠀⡎⣀⠎⠀⠀⠀
⠀⠀⠀⠀⢧⠸⣇⠎⡰⢌⢊⡙⠲⣄⡀⠀⠈⠉⠉⠛⠚⠒⠛⠚⠒⠛⠓⠓⠚⢿⡿⣿⣿⣿⣿⣿⣏⣷⣹⡮⠷⠽⠾⠗⠛⠋⠉⠀⠀⠀⠀⠀⢀⣠⣿⠟⡆⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠙⢆⡱⣈⠦⣉⠳⢄⢫⠱⠦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡽⣖⡳⣞⢶⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣴⣶⢿⡿⠋⠀⡆⠀⠀⠀
⠀⠀⠀⠀⠘⡆⠀⡀⠑⢦⡒⠥⡚⣌⠲⣉⠞⣰⠪⡝⢭⡓⢶⡒⣖⠲⣖⢲⢖⡺⣿⣷⣿⣾⣷⣿⣿⣤⣤⣤⣤⣤⢶⣶⢻⡟⡿⢯⡿⣽⣳⣯⠟⠁⡔⡀⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠙⣤⡈⠀⠀⠉⠓⠵⣌⡓⡌⡎⢥⡓⡜⡣⢞⡡⢏⡜⡳⢬⣋⢮⣕⢫⣝⣻⣛⢿⡹⢧⡳⣞⢶⡹⣎⠿⣜⣻⣼⣛⣯⢷⣯⠗⠋⢠⠞⡴⡯⣅⠀⠀⠀
⠀⠀⠀⢀⠄⠊⢡⣿⣶⣄⠀⠀⠀⠈⠉⠓⠺⢥⣎⡵⣙⢬⠳⣩⢞⡱⢫⡜⡖⢮⣓⠾⣔⢯⣚⡽⣣⢟⡼⣣⡟⣭⠿⣭⣳⣞⡽⠞⠋⠁⠀⠀⣸⠾⡳⢦⡄⠱⢠⠀⠀
⠀⢀⡔⠁⠀⠀⣿⣿⢯⣟ⷦ⣄⣀⠀⠀⠀⠀⠀⠈⠉⠉⠓⠓⠚⠓⠓⠛⠞⢣⣿⢾⡿⣾⢷⡿⣿⢿⡿⣿⢿⡿⣿⡿⠉⠁⠀⠀⢀⣠⠖⣫⠡⢒⡉⠳⣽⡀⠀⠑⢀⠀
⢠⠏⢠⠎⠀⠸⡿⣿⣿⣞ⷻ⡾⣽⣻⢶⣦⢤⣤⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠘⠻⠷⠿⠾⠷⢯⣽⢾⡽⠛⠋⠛⠋⢁⣀⡤⢴⡚⡍⢆⡓⠤⢃⠥⢨⣱⠏⠀⠈⢢⠈⢣⠀
⠛⢨⡇⠀⠀⠀⢣⠉⢻⣾⢳⣿⣽⢳⣽⡞⣵⢻⡜⢳⣯⣽⠛⣿⠛⡟⢻⢳⡞⣶⣶⡖⣶⠒⣶⠒⣿⣿⢲⠒⣶⠛⣭⠋⣦⢱⢢⢱⠘⣦⠘⠑⠊⡜⣶⠃⡆⠀⠀⠀
⣻⠙⡄⠀⠀⠀⠈⠣⡄⠈⠙⠺⢷⣯⣗⣻⡭⣷⢻⡝⣮⢳⡻⣜⢯⡝⣧⢻⠼⣱⢎⡵⢣⣛⣴⣻⣼⣿⣿⣜⣦⣷⣼⣾⣾⣦⢉⡆⢳⡈⢖⣩⠶⠋⠀⢠⠃⠀⠀⠀
⠸⣤⠐⡄⠀⠀⠀⠀⠈⢦⣑⠠⠀⡀⠈⠉⠛⠺⠷⣯⣳⣏⡷⣹⢮⡝⣮⠽⣭⠳⢮⣙⠧⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⡶⡬⠗⠚⢉⠀⠀⣀⠔⠁⠀⠀⠀
⠀⠈⢆⠈⠢⡀⠀⠀⠀⠀⠀⠉⠒⠦⢄⣀⠒⠠⠄⠀⠀⠈⠉⠉⠛⠚⠓⠻⠶⠯⠷⠭⠾⠥⠯⠯⠿⠿⣷⠟⠛⠛⠉⣉⣥⣴⣶⣾⣿⣿⣿⣿⠋⠀⠀⠀⠀⣀⠔⠀
⠀⠀⠀⠑⢤⠈⠒⠄⡀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠒⠒⠦⠤⠤⣀⣀⣀⣀⡀⠀⠀⢀⣤⣤⣤⣤⣤⣤⣴⢿⣶⣶⡾⣿⠿⣟⣻⢻⣽⣹⠾⠋⠁⠀⠀⢀⠤⠊⢀⡴⠋
⠀⠀⠀⠀⠀⠈⠒⢄⡈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠘⢥⣈⣆⣑⣪⣑⣎⣭⣓⣬⠷⠼⠿⠚⠋⠉⠀⠀⠀⠀⠀⠀⠈⣀⠤⠚⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠒⠠⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠔⠚⠉⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠐⠢⠤⠤⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣤⠤⠦⠶⠒⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠉⠈⠁⠉⠈⠁⠈⠁⠁⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
RECIPES = {
    "Scrambled eggs": {"needs": {"Eggs", "Butter", "Milk"}, "fridge": ["Eggs", "Butter", "Milk"]},
    "Pancakes": {"needs": {"Pancake mix", "Water", "Butter"}, "fridge": ["Water", "Butter"], "pantry": ["Pancake mix"]},
    "Oatmeal": {"needs": {"Oatmeal pack", "Water"}, "fridge": ["Water"], "pantry": ["Oatmeal pack"]},
}
KITCHEN_STORAGE = {
    "fridge": ["Eggs", "Butter", "Milk", "Water"],
    "pantry": ["Pancake mix", "Oatmeal pack"],
}
BACKPACK_ITEMS = [("Computer", 10), ("Computer charger", 10), ("Waterbottle", 10), ("Phone charger", 5), ("Airpods", 5), ("Lipgloss", 0), ("Perfume", 0), ("Clawclip", 0)]


def init_game():
    st.session_state.update(health=50, temperature=random.randint(20, 81), story=["The morning sun spills across your apartment, and your day is about to begin.", ACTION_BREAK], stage="intro", screen="welcome", leaderboard_return_screen="welcome", backpack=[], recipe=None, ingredients=[], source=None, room=None, completed_rooms=[], outfit_base_health=None, pancake_shown=False, makeup_then_hair=False, score_dialog_open=False, pending_score_submission=None, score_saved=False, submitted_score_name="")


if "stage" not in st.session_state:
    init_game()
elif "screen" not in st.session_state:
    st.session_state.screen = "welcome" if st.session_state.stage == "intro" else "game"


def tell(text):
    st.session_state.story.append(text)


def break_story():
    if not st.session_state.story or st.session_state.story[-1] != ACTION_BREAK:
        st.session_state.story.append(ACTION_BREAK)


def clear_output(text=None):
    st.session_state.story = []
    if text:
        tell(text)


def reroute(stage, clear=False, intro=None):
    if clear:
        clear_output(intro)
    elif intro:
        tell(intro)
    st.session_state.stage = "game_over" if st.session_state.health <= 0 else stage
    break_story()
    st.rerun()


def reward(amount, text):
    st.session_state.health += amount
    tell(text)
    if st.session_state.health <= 0:
        st.session_state.health = 0
        clear_output()
        tell("Your happiness hit zero. The apartment wins, and the morning ends in a glittery little disaster.")
        st.session_state.stage = "game_over"


def finish_room(room):
    if room not in st.session_state.completed_rooms:
        st.session_state.completed_rooms.append(room)
    reroute("ending" if len(st.session_state.completed_rooms) == 3 else "destination")


def finish_bedroom():
    if "Bedroom" not in st.session_state.completed_rooms:
        st.session_state.completed_rooms.append("Bedroom")


def choose_outfit(item, category):
    cold = st.session_state.temperature < 60
    very_cold = st.session_state.temperature < 35
    warm_choice = item in ({"Sweatpants", "Leggings", "Sweatshirt", "Long sleeve"} if category != "coat" else {"Yes, wear a coat"})
    good = (warm_choice == cold) if category != "coat" else (warm_choice == very_cold)
    reward(5 if good else -15, "Good choice! You will be comfortable. Happiness increases by 5." if good else "Bad choice! That outfit does not suit the weather. Happiness decreases by 15.")


def dismiss_score_submission():
    st.session_state.score_dialog_open = False
    st.session_state.pending_score_submission = None


@st.dialog("Add your score", width="small", on_dismiss=dismiss_score_submission)
def score_submission_dialog():
    pending = st.session_state.pending_score_submission
    if pending:
        st.metric("Your score", pending["score"])
        st.write(
            f'"{pending["name"]}" is already on the leaderboard. '
            "Would you like to replace that entry or add a new row?"
        )
        replace_column, add_column = st.columns(2)
        if replace_column.button("Replace existing entry", type="primary", use_container_width=True):
            replace_leaderboard_score(pending["existing_id"], pending["name"], pending["score"])
            st.session_state.score_saved = True
            st.session_state.submitted_score_name = pending["name"]
            st.session_state.pending_score_submission = None
            st.session_state.score_dialog_open = False
            st.rerun()
        if add_column.button("Add a new row", use_container_width=True):
            add_leaderboard_score(pending["name"], pending["score"])
            st.session_state.score_saved = True
            st.session_state.submitted_score_name = pending["name"]
            st.session_state.pending_score_submission = None
            st.session_state.score_dialog_open = False
            st.rerun()
        if st.button("Cancel", key="cancel_duplicate_score"):
            st.session_state.pending_score_submission = None
            st.session_state.score_dialog_open = False
            st.rerun()
        return

    st.metric("Your score", st.session_state.health)
    with st.form("score_submission_form"):
        player_name = st.text_input("Name", max_chars=40, key="leaderboard_player_name")
        submitted = st.form_submit_button("Add to leaderboard", type="primary", use_container_width=True)
    if submitted:
        name = player_name.strip()
        if not name:
            st.error("Enter a name before adding your score.")
        else:
            existing_entry = find_leaderboard_name(name)
            if existing_entry:
                st.session_state.pending_score_submission = {
                    "existing_id": existing_entry[0],
                    "name": name,
                    "score": st.session_state.health,
                }
                st.rerun()
            else:
                add_leaderboard_score(name, st.session_state.health)
                st.session_state.score_saved = True
                st.session_state.submitted_score_name = name
                st.session_state.score_dialog_open = False
                st.rerun()
    if st.button("Cancel", key="cancel_score_submission"):
        st.session_state.score_dialog_open = False
        st.rerun()


if "score_dialog_open" not in st.session_state:
    st.session_state.score_dialog_open = False
    st.session_state.pending_score_submission = None
    st.session_state.score_saved = False
    st.session_state.submitted_score_name = ""

if st.session_state.score_dialog_open:
    score_submission_dialog()
    st.stop()


if st.session_state.screen == "leaderboard":
    st.markdown('<div class="hero"><div class="eyebrow">Apartment Morning Adventure</div><h1>Leaderboard</h1><p>Top happiness scores from completed mornings.</p></div>', unsafe_allow_html=True)
    leaderboard = get_leaderboard()
    if leaderboard:
        rows = "".join(
            f'<tr><td class="leaderboard-place">{place}</td><td class="leaderboard-name">{html.escape(name)}</td><td class="leaderboard-score">{score}</td></tr>'
            for place, (_, name, score) in enumerate(leaderboard, start=1)
        )
    else:
        rows = '<tr><td class="leaderboard-empty" colspan="3">No scores yet. Be the first to add yours!</td></tr>'
    st.markdown(
        '<div class="leaderboard-card"><table class="leaderboard-table"><thead><tr><th>Place</th><th>Name</th><th style="text-align:right">Score</th></tr></thead>'
        f"<tbody>{rows}</tbody></table></div>",
        unsafe_allow_html=True,
    )
    if st.button("Back", type="primary", key="leaderboard_back_button"):
        st.session_state.screen = st.session_state.leaderboard_return_screen
        st.rerun()
    st.stop()


if st.session_state.stage == "intro":
    with st.form("welcome_form"):
        st.markdown('<div class="welcome-screen"><div class="welcome-card"><div class="hero"><div class="eyebrow">A cozy text adventure</div><h1>Apartment Morning Adventure</h1><p>Get ready, gather your things, and make it out the door with your happiness intact.</p></div></div></div>', unsafe_allow_html=True)
        _, welcome_button, _ = st.columns([1, 1, 1])
        with welcome_button:
            if st.form_submit_button("Start my morning", type="primary", use_container_width=True):
                st.session_state.screen = "game"
                tell("You wake up in your big, comfy bed, perfectly content with staying there all day.")
                tell("Unfortunately, it is a school day and you have lots to do.")
                tell("You really should get out of bed, but what do you want to do?")
                reroute("bed_choice")
            if st.form_submit_button("Leaderboard", type="secondary", use_container_width=True, key="leaderboard_button"):
                st.session_state.leaderboard_return_screen = "welcome"
                st.session_state.screen = "leaderboard"
                st.rerun()
    st.stop()


left, right = st.columns([2.1, 1], gap="large")

with left:
    lines = []
    for line in st.session_state.story:
        if line == ACTION_BREAK:
            lines.append('<div style="height:.45rem"></div>')
        elif line == "PANCAKE_ART":
            lines.append(f'<pre class="art">{html.escape(PANCAKE_ART)}</pre>')
        else:
            lines.append(f'<p>{html.escape(line)}</p>')
    st.markdown(f'<div class="panel"><div class="eyebrow">Story</div><div class="story">{"".join(lines)}</div></div>', unsafe_allow_html=True)

    stage = st.session_state.stage
    if stage == "bed_choice":
        st.markdown('<div class="panel"><p>Would you like to get up or stay in bed?</p></div>', unsafe_allow_html=True)
        a, b = st.columns(2)
        if a.button("Get up", use_container_width=True):
            tell("Yay! Good morning. Time to start your day.")
            reroute("bed_make")
        if b.button("Stay in bed", use_container_width=True):
            reward(-10, "How lazy of you. Happiness decreases by 10.")
            reroute("bed_choice")
    elif stage == "bed_make":
        st.markdown('<div class="panel"><p>Your bed is messy. Would you like to make it?</p></div>', unsafe_allow_html=True)
        a, b = st.columns(2)
        if a.button("Make the bed", use_container_width=True):
            reward(10, "Your bed looks so nice and pretty. Happiness increases by 10.")
            st.session_state.outfit_base_health = st.session_state.health
            reroute("outfit_intro")
        if b.button("Leave it messy", use_container_width=True):
            reward(-10, "How lazy of you. Happiness decreases by 10.")
            st.session_state.outfit_base_health = st.session_state.health
            reroute("outfit_intro")
    elif stage == "outfit_intro":
        st.markdown('<div class="panel"><p>It is time to pick your outfit for the day. Let\'s move to your closet.</p></div>', unsafe_allow_html=True)
        if st.button("Let\'s go", type="primary", use_container_width=True):
            reroute("closet_bottoms", clear=True, intro="You walk over to your closet and begin choosing an outfit.")
    elif stage == "closet_bottoms":
        st.markdown(f'<div class="panel"><p>It is <strong>{st.session_state.temperature} degrees</strong> outside. Choose your bottoms.</p><div class="rules"><strong>Rules:</strong><br>Below 60 means you should be wearing long pants.<br>Shorts are better at 60 or above.</div></div>', unsafe_allow_html=True)
        for item in ["Sweatpants", "Leggings", "Shorts"]:
            if st.button(item, use_container_width=True):
                choose_outfit(item, "bottoms")
                reroute("closet_tops")
    elif stage == "closet_tops":
        st.markdown('<div class="panel"><p>Now choose a top that fits the weather.</p><div class="rules"><strong>Rules:</strong><br>Below 60 means you should wear a sweatshirt or long sleeve.<br>A T-shirt or tank top is better at 60 or above.</div></div>', unsafe_allow_html=True)
        for item in ["Sweatshirt", "Long sleeve", "T-shirt", "Tank top"]:
            if st.button(item, use_container_width=True):
                choose_outfit(item, "tops")
                reroute("closet_coat")
    elif stage == "closet_coat":
        st.markdown('<div class="panel"><p>Would you like to wear a coat?</p><div class="rules"><strong>Rules:</strong><br>Below 35 means you should wear a coat.<br>Skipping it above 35 keeps you from overheating.</div></div>', unsafe_allow_html=True)
        for item in ["Yes, wear a coat", "No, skip the coat"]:
            if st.button(item, use_container_width=True):
                choose_outfit(item, "coat")
                reroute("outfit_redo")
    elif stage == "outfit_redo":
        base = st.session_state.outfit_base_health or st.session_state.health
        st.markdown(f'<div class="panel"><p>Your outfit is chosen. Redo it? A redo resets happiness to <strong>{base - 15}</strong> because extra laundry is its own kind of chaos.</p></div>', unsafe_allow_html=True)
        if st.button("Redo my outfit", use_container_width=True):
            st.session_state.health = max(0, base - 15)
            tell("You decide to redo your outfit. Dramatic, but occasionally necessary.")
            reroute("closet_bottoms", clear=True, intro="You clear the outfit from your mind and start again at the closet.")
        if st.button("Keep this outfit", use_container_width=True):
            tell("Great! You walk over to your desk and notice your backpack is a tiny disaster.")
            reroute("desk_choice")
    elif stage == "desk_choice":
        st.markdown('<div class="panel"><p>You have a little time at your desk. What would you like to do?</p></div>', unsafe_allow_html=True)
        for item in ["Makeup", "Hair", "Both", "Neither"]:
            if st.button(item, use_container_width=True):
                if item in {"Makeup", "Both"}:
                    st.session_state.makeup_then_hair = item == "Both"
                    reroute("makeup_choice")
                elif item == "Hair":
                    reroute("hair_choice")
                else:
                    reroute("backpack_pack")
    elif stage == "makeup_choice":
        st.markdown('<div class="panel"><p>How would you like to do your makeup?</p></div>', unsafe_allow_html=True)
        makeup_options = {
            "Just lip gloss": "You add a little lip gloss. Happiness increases by 10.",
            "Mascara and lip gloss": "You put on mascara and lip gloss. Happiness increases by 10.",
            "Full face": "You take your time and create a full face. Happiness increases by 10.",
        }
        for item, message in makeup_options.items():
            if st.button(item, use_container_width=True):
                reward(10, message)
                reroute("hair_choice" if st.session_state.makeup_then_hair else "backpack_pack")
    elif stage == "hair_choice":
        st.markdown('<div class="panel"><p>How would you like to do your hair?</p></div>', unsafe_allow_html=True)
        for item in ["Leave down", "Claw clip", "Ponytail"]:
            if st.button(item, use_container_width=True):
                reward(10, f"Your {item.lower()} looks great. Happiness increases by 10.")
                reroute("backpack_pack")
    elif stage == "backpack_pack":
        st.markdown('<div class="panel"><p>Repack your backpack. Practical items increase happiness; the extras are simply fabulous.</p></div>', unsafe_allow_html=True)
        for item, amount in BACKPACK_ITEMS:
            if st.button(item, use_container_width=True):
                if item not in st.session_state.backpack:
                    st.session_state.backpack.append(item)
                    reward(amount, f"You packed {item}. Happiness increases by {amount}." if amount else f"You packed {item}. A little extra chaos never hurt.")
                reroute("backpack_pack")
        if st.button("Done packing", type="primary", use_container_width=True):
            tell("You step back and admire your overpacked backpack.")
            finish_bedroom()
            reroute("destination")
    elif stage == "destination":
        remaining = [room for room in ["Kitchen", "Living Room"] if room not in st.session_state.completed_rooms]
        st.markdown(f'<div class="panel"><p>Where would you like to go next? Remaining: <strong>{" and ".join(remaining)}</strong>.</p></div>', unsafe_allow_html=True)
        for room in remaining:
            if st.button(room, use_container_width=True):
                st.session_state.room = room
                reroute("kitchen_intro" if room == "Kitchen" else "living_room", clear=True, intro=f"You walk into the {room.lower()}.")
    elif stage == "kitchen_intro":
        st.markdown('<div class="panel"><p>You walk into the kitchen and realize how hungry you are. Make breakfast?</p></div>', unsafe_allow_html=True)
        if st.button("Yes, make breakfast", use_container_width=True):
            reroute("kitchen_recipe")
        if st.button("No, skip breakfast", use_container_width=True):
            reward(-20, "Breakfast is good for you. Happiness decreases by 20.")
            reroute("water_bottle")
    elif stage == "kitchen_recipe":
        st.markdown('<div class="panel"><p>Choose a recipe, then gather exactly what it needs.</p></div>', unsafe_allow_html=True)
        for recipe in RECIPES:
            if st.button(recipe, use_container_width=True):
                st.session_state.recipe = recipe
                st.session_state.ingredients = []
                reroute("kitchen_gather")
    elif stage == "kitchen_gather":
        recipe = RECIPES[st.session_state.recipe]
        missing = recipe["needs"] - set(st.session_state.ingredients)
        st.markdown(f'<div class="panel"><p><strong>{st.session_state.recipe} Recipe:</strong> {", ".join(sorted(recipe["needs"]))}<br><strong>Missing:</strong> {", ".join(sorted(missing)) or "nothing"}</p></div>', unsafe_allow_html=True)
        for source in KITCHEN_STORAGE:
            if st.session_state.source == source:
                allowed = KITCHEN_STORAGE[source]
                st.markdown(f'<div class="panel"><div class="eyebrow">Open {source}</div><p>Choose what to take. This stays open until you close it.</p></div>', unsafe_allow_html=True)
                for item in allowed:
                    if st.button(item, key=f"pick_{source}_{item}", use_container_width=True):
                        if item not in st.session_state.ingredients:
                            st.session_state.ingredients.append(item)
                        st.rerun()
                if st.button(f"Close the {source}", key=f"close_{source}", use_container_width=True):
                    st.session_state.source = None
                    st.rerun()
            elif st.session_state.source is None and st.button(f"Open the {source}", key=f"open_{source}", use_container_width=True):
                st.session_state.source = source
                st.rerun()
        if st.button("Cook breakfast", type="primary", use_container_width=True):
            if not missing:
                tell("You have everything you need and breakfast comes together beautifully.")
                if st.session_state.recipe == "Pancakes" and not st.session_state.pancake_shown:
                    clear_output("Your pancakes are ready!")
                    st.session_state.story.append("PANCAKE_ART")
                    st.session_state.pancake_shown = True
                reward(20, "Yay! You eat your delicious breakfast. Happiness increases by 20.")
                reroute("water_bottle")
            else:
                tell("You still need a few more ingredients before you can cook.")
                break_story()
                st.rerun()
    elif stage == "water_bottle":
        st.markdown('<div class="panel"><p>Fill your water bottle before heading out.</p></div>', unsafe_allow_html=True)
        for drink in ["Water", "Mio", "Iced Tea"]:
            if st.button(drink, use_container_width=True):
                reward(5, f"Your bottle is filled with {drink}. Happiness increases by 5.")
                finish_room("Kitchen")
    elif stage == "living_room":
        st.markdown('<div class="panel"><p>You notice your iPad and book in the living room. Put them in your backpack?</p></div>', unsafe_allow_html=True)
        if st.button("Pack the iPad and book", use_container_width=True):
            st.session_state.backpack.extend(item for item in ["Ipad", "Book"] if item not in st.session_state.backpack)
            tell("Perfect! Your backpack is a little more prepared.")
            finish_room("Living Room")
        if st.button("Leave them behind", use_container_width=True):
            tell("You leave them behind and head out slightly more chaotic than before.")
            finish_room("Living Room")
    elif stage == "ending":
        score = st.session_state.health
        note = "You did amazing!" if score > 100 else "You did good!" if score >= 50 else "Do more things that make you happy tomorrow."
        st.markdown(f'<div class="panel"><h2>You made it out the door</h2><p>Thanks for playing. Your happiness ended at <strong>{score}</strong>.</p><p>{note}</p></div>', unsafe_allow_html=True)
        if st.session_state.score_saved:
            st.success(f"Score added to the leaderboard for {st.session_state.submitted_score_name}.")
            if st.button("View leaderboard", type="secondary", use_container_width=True, key="ending_view_leaderboard_button"):
                st.session_state.leaderboard_return_screen = "game"
                st.session_state.screen = "leaderboard"
                st.rerun()
        elif st.button("Add your score to leaderboard", type="secondary", use_container_width=True, key="add_ending_score_button"):
            st.session_state.score_dialog_open = True
            st.rerun()
    elif stage == "game_over":
        st.markdown('<div class="panel"><h2>Game Over</h2><p>Your happiness reached zero. The morning went completely off the rails.</p></div>', unsafe_allow_html=True)
        if st.session_state.score_saved:
            st.success(f"Score added to the leaderboard for {st.session_state.submitted_score_name}.")
            if st.button("View leaderboard", type="secondary", use_container_width=True, key="game_over_view_leaderboard_button"):
                st.session_state.leaderboard_return_screen = "game"
                st.session_state.screen = "leaderboard"
                st.rerun()
        elif st.button("Add your score to leaderboard", type="secondary", use_container_width=True, key="add_game_over_score_button"):
            st.session_state.score_dialog_open = True
            st.rerun()

with right:
    st.markdown('<div class="panel"><div class="eyebrow">Current status</div><div class="metric"><span>Happiness</span><strong>{}</strong></div><div class="meter"><span style="width:{}%"></span></div><p style="color:#806875">Outside temperature: <strong>{}°</strong></p></div>'.format(st.session_state.health, min(max(st.session_state.health, 0), 100), st.session_state.temperature), unsafe_allow_html=True)
    done = len(st.session_state.completed_rooms)
    objectives = [("Bedroom ready", st.session_state.stage not in {"intro", "bed_choice", "bed_make", "closet_bottoms", "closet_tops", "closet_coat", "outfit_redo", "desk_choice", "hair_choice"}), ("Kitchen complete", "Kitchen" in st.session_state.completed_rooms), ("Living Room complete", "Living Room" in st.session_state.completed_rooms)]
    objective_html = "".join(f'<div class="objective">{"✓" if complete else "○"} {name}</div>' for name, complete in objectives)
    st.markdown(f'<div class="panel"><div class="eyebrow">Progress</div>{objective_html}<p style="color:#806875">Objectives complete: {done}/3</p></div>', unsafe_allow_html=True)
    backpack = "".join(f'<span class="tag">{html.escape(item)}</span>' for item in st.session_state.backpack) or '<p style="color:#806875">Your backpack is empty.</p>'
    st.markdown(f'<div class="panel"><div class="eyebrow">Backpack</div>{backpack}</div>', unsafe_allow_html=True)
    if st.button("Start over", use_container_width=True):
        init_game()
        st.rerun()
    if st.session_state.stage not in {"ending", "game_over"} and st.button("Leaderboard", type="secondary", use_container_width=True, key="gameplay_leaderboard_button"):
        st.session_state.leaderboard_return_screen = "game"
        st.session_state.screen = "leaderboard"
        st.rerun()
