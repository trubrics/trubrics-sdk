import time
from datetime import datetime

import streamlit as st

local_now = datetime.now().astimezone()
local_time = time.localtime()

st.markdown(
    """
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/Franky1/Streamlit-Timezone-Test)
![Python](https://img.shields.io/badge/Python-3.7%20|%203.8%20|%203.9-blue?logo=python)
![Issues](https://img.shields.io/github/issues/Franky1/Streamlit-Timezone-Test?logo=github)
![Last Commit](https://img.shields.io/github/last-commit/Franky1/Streamlit-Timezone-Test?logo=github)
"""
)
st.title("Timezone Check for Streamlit Cloud")
st.markdown("Just a quick check of the time and timezone used by the cloud instance")
st.markdown("""---""")

st.markdown("### Using `datetime` module from standard library")
body_datetime = """
from datetime import datetime
local_now = datetime.now().astimezone()

print(local_now.isoformat())
print(local_now.tzname())
"""
st.code(body_datetime, language="python")
st.text(f"local_now.isoformat(): {local_now.isoformat()}")
st.text(f"local_now.tzname(): {local_now.tzname()}")
st.markdown("""---""")

st.markdown("### Using `time` module from standard library")
body_time = """
import time
local_time = time.localtime()

print(time.timezone)
print(time.tzname)
print(local_time.tm_zone)
print(local_time.tm_isdst)
"""
st.code(body_time, language="python")
st.text(f"time.timezone: {time.timezone}")
st.text(f"time.tzname: {time.tzname}")
st.text(f"local_time.tm_zone: {local_time.tm_zone}")
st.text(f"local_time.tm_isdst: {local_time.tm_isdst}")
st.markdown("""---""")
