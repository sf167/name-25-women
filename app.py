import streamlit as st
import time
import sqlite3
from validate import is_real_woman


conn = sqlite3.connect('leaderboard.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS scores (name TEXT, time INTEGER)")

st.set_page_config(page_title="Name 25 Women", layout="centered")

if "names" not in st.session_state:
    st.session_state["names"] = []
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "end_time" not in st.session_state:
    st.session_state["end_time"] = None
if "name_input" not in st.session_state:
    st.session_state["name_input"] = ""
if "game_started" not in st.session_state:
    st.session_state["game_started"] = False

st.title("Celestial Name 25 Women Challenge")

if not st.session_state["game_started"]:
    if st.button("Start Game"):
        st.session_state["game_started"] = True
        st.session_state["start_time"] = time.time()
        st.rerun()
    st.stop()

timer_placeholder = st.empty()


if st.session_state["game_started"] and not st.session_state["end_time"]:
    elapsed = int(time.time() - st.session_state["start_time"])
    timer_placeholder.markdown(f"### ⏱ Time: {elapsed} seconds")
else:
    final_time = st.session_state["end_time"] or 0
    timer_placeholder.markdown(f"### ⏱ Time: {final_time} seconds")





st.write(f"Progress: {len(st.session_state["names"])} / 25")

def handle_submit():
    name = st.session_state["name_input"].strip().lower()
    if name in st.session_state["names"]:
        st.error("Duplicate name.")
    elif not name:
        st.warning("Please enter a name.")
    else:
        if st.session_state["start_time"] is None:
            st.session_state["start_time"] = time.time()
        with st.spinner("Checking name..."):
            if is_real_woman(name):
                st.session_state["names"].append(name)
                st.session_state["name_input"] = ""
                st.success(f"{name} accepted!")
                if len(st.session_state["names"]) == 25:
                   st.session_state["end_time"] = int(time.time() - st.session_state["start_time"])
                st.rerun()
            else:
                st.error("Not recognized real woman")
                st.session_state["name_input"] = ""

if st.session_state["game_started"] and not st.session_state["end_time"]:
    st.text_input(
        "Enter a woman's name:",
        key="name_input",
        on_change=handle_submit,
    )

if st.session_state["end_time"] and len(st.session_state["names"]) == 25:
    username = st.text_input("Enter a username:")
    if st.button("Submit Score"):
        cursor.execute("INSERT INTO scores VALUES (?, ?)", (username, st.session_state["end_time"]))
        conn.commit()
        st.success("Score submitted")

    if st.button("Play Again"):
        for key in ["names", "start_time", "end_time", "name_input", "game_started"]:
            st.session_state[key] = None if key in ["start_time", "end_time"] else False if key == "game_started" else []
        st.rerun()

if st.checkbox("Show Leaderboard"):
    st.subheader("Leaderboard")
    rows = cursor.execute("SELECT name, time FROM scores ORDER BY time ASC").fetchall()
    for i, (n, t) in enumerate(rows, start=1):
        minutes = t // 60
        seconds = t % 60
        st.write(f"{i}. {n} - {minutes}:{seconds:02d}")

