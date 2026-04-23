import streamlit as st
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import socket
import psycopg2 

# --- PAGE CONFIG ---
st_page = st.set_page_config(page_title="DS Engine Command Center", layout="wide")

# --- CSS INJECTION (The Magic for Responsiveness and Height) ---
st.markdown("""
    <style>
    /* This makes the column containers act like a Flexbox grid */
    /* When the screen gets small, the columns will wrap to the next line */
    [data-testid="column"] {
        flex-grow: 1;
        min-width: 250px; /* Minimum width of a tile before it wraps */
        max-width: 100%;
    }

    /* Ensures all containers have a consistent look and alignment */
    [data-testid="stVerticalBlockBorderWrapper"] {
        transition: transform 0.2s;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px);
        border-color: #ff4b4b !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Data Science Engine: Command Center")
st.markdown("---")

# --- LOGIC & CONFIG ---
load_dotenv()
base_url = os.getenv("BASE_URL", "http://localhost")
local_base_url = "http://localhost"

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")

# Detect URL context
try:
    page_url = st.query_params.get("url", "")
    hostname = urlparse(page_url).hostname if hasattr(st, 'url') else "" 
    current_base_url = local_base_url if "localhost" in hostname or "127.0.0.1" in hostname else base_url
except:
    current_base_url = base_url

SERVICES = {
    "JupyterLab": {"url": f"{current_base_url}:8888", "icon": "📓", "health_check_type": "http"},
    "MinIO": {"url": f"{current_base_url}:9001", "icon": "🗄️", "health_check_type": "http"},
    "PostgreSQL": {"host": f"{current_base_url}", "port": "5432", "icon": "🐘", "health_check_type": "postgres"},
    "Airflow": {"url": f"{current_base_url}:8080", "icon": "🌬️", "health_check_type": "http"},
}

def check_health(url, health_check_type):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port

    if health_check_type == "postgres":
        try:
            conn = psycopg2.connect(
                user=DB_USER, password=DB_PASSWORD, host=hostname,
                port=port, dbname=DB_NAME, connect_timeout=2
            )
            conn.close()
            return "✅ Online"
        except: return "❌ Offline"
    elif health_check_type == "socket":
        try:
            with socket.create_connection((hostname, port), timeout=2):
                return "✅ Online"
        except: return "❌ Offline"
    else:
        try:
            response = requests.get(url, timeout=2)
            return "✅ Online" if 200 <= response.status_code < 500 else "⚠️ Error"
        except: return "❌ Offline"

# --- UI RENDERING ---
services_list = list(SERVICES.items())

# We create a large number of columns, but the CSS 'flex-grow' and 'min-width' 
# will handle the responsive wrapping automatically.
cols = st.columns(5) 

for i, (name, info) in enumerate(services_list):
    # Use the column from our pre-defined 5 columns (cycling through them)
    col = cols[i % 5]
    
    with col:
        # 'height' parameter forces all containers to be exactly the same size
        with st.container(border=True, height=250):
            health_status = check_health(info['url'] if 'url' in info else f"{info['host']}:{info['port']}", info['health_check_type'])
            
            st.write(f"### {info['icon']} {name}")
            st.write(f"**Status:** {health_status}")
            is_online = "✅" in health_status

            # Add a spacer to push content to the bottom (helps with visual alignment)
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

            if is_online:
                if name == "PostgreSQL":
                    conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{info['host'].split('://')[1]}:{info['port']}/{DB_NAME}"
                    # Using text_input instead of code for an easier "Click to Select" experience
                    st.code(conn_str, language="plaintext")
                else:
                    st.link_button("Open Service", url=info['url'], key=f"btn_{name}")
            else:
                st.button("Offline", disabled=True, key=f"off_{name}", use_container_width=True)

st.markdown("---")
st.title("Projects")