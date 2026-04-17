import streamlit as st
import requests
from urllib.parse import urlparse

st_page = st.set_page_config(page_title="DS Engine Command Center", layout="wide")

st.title("🚀 Data Science Engine: Command Center")
st.markdown("---")

base_url = "http://pop-os.tailfd76bc.ts.net"
local_base_url = "http://localhost"

# Detect which URL the user is accessing from
try:
    # Try to get the request context
    from streamlit.web.server import Server
    page_url = st.request.base_url if hasattr(st, 'request') else None
    
    if page_url:
        # Parse the hostname to determine which URL was used
        hostname = urlparse(page_url).hostname or ""
        if "localhost" in hostname or "127.0.0.1" in hostname:
            current_base_url = local_base_url
        else:
            current_base_url = base_url
    else:
        current_base_url = base_url  # Default to base_url
except:
    current_base_url = base_url  # Default to base_url if detection fails

SERVICES = {
    "JupyterLab": {"url": f"{current_base_url}:8888", "icon": "📓"}
}

def check_health(url):
    """Checks if a service is reachable via its web port."""
    try:
        response = requests.get(url, timeout=2, allow_redirects=False)
        if 200 <= response.status_code < 500:
            return "✅ Online"
        else:
            return "⚠️ Server Error"
    except requests.exceptions.Timeout:
        return "⏱️ Timeout"
    except requests.exceptions.ConnectionError:
        return "❌ Offline"
    except requests.exceptions.RequestException:
        return "❌ Error"

# Create columns for a clean UI - 5 tiles per row
services_list = list(SERVICES.items())
cols_per_row = 5

for row_idx in range(0, len(services_list), cols_per_row):
    cols = st.columns(cols_per_row)  # Always create 5 columns
    for col_idx in range(cols_per_row):
        if row_idx + col_idx < len(services_list):
            name, info = services_list[row_idx + col_idx]
            with cols[col_idx]:
                with st.container(border=True):
                    health_status = check_health(info['url'])
                    st.write(f"### {info['icon']} {name}")
                    st.write(f"**Status:** {health_status}")
                    is_online = "✅" in health_status
                    if is_online:
                        st.link_button(label="Open", url=info['url'], key=f"link_{name}")
                    else:
                        st.button(label="Open", disabled=True, key=f"btn_{name}")