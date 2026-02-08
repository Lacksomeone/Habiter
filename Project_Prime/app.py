import streamlit as st
import pandas as pd
from datetime import date
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="My Habit Tracker", page_icon="💪")

st.title("💪 Desi Habit Tracker")
st.write(f"**Date:** {date.today()}")

# --- DATA HANDLING ---
# Hum data ko ek CSV file mein save karenge taaki band karne par delete na ho
FILE_NAME = "habits.csv"

if not os.path.exists(FILE_NAME):
    # Agar file nahi hai, to nayi banao
    df = pd.DataFrame(columns=["Habit", "Date", "Done"])
    df.to_csv(FILE_NAME, index=False)

# Data load karo
df = pd.read_csv(FILE_NAME)

# --- SIDEBAR: ADD NEW HABIT ---
st.sidebar.header("Add New Habit")
new_habit = st.sidebar.text_input("Habit Name (e.g., Gym, Reading)")
if st.sidebar.button("Add Habit"):
    if new_habit:
        # Check karo agar habit already list mein hai aaj ke liye
        # (Simply hum ek nayi entry daal rahe hain unique habit list maintain karne ke liye)
        if new_habit not in df['Habit'].unique():
            new_row = pd.DataFrame([{"Habit": new_habit, "Date": str(date.today()), "Done": False}])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.sidebar.success(f"Added: {new_habit}")
            st.rerun() # Page refresh taaki naya habit dikhe
    else:
        st.sidebar.warning("Bhai kuch likh to sahi!")

# --- MAIN AREA: CHECKLIST ---
st.subheader("Aaj ka Target 🎯")

# Sirf unique habits nikalo
unique_habits = df['Habit'].unique()

if len(unique_habits) == 0:
    st.info("Abhi koi habit nahi hai. Sidebar se add kar! 👈")
else:
    # Har habit ke liye ek checkbox banao
    for habit in unique_habits:
        # Check karo aaj ka status kya hai
        today_str = str(date.today())
        
        # Filter data for specific habit and date
        row_idx = df.index[(df['Habit'] == habit) & (df['Date'] == today_str)].tolist()
        
        # Agar aaj ki date ki entry nahi hai, to create karo default False ke saath
        if not row_idx:
            new_row = pd.DataFrame([{"Habit": habit, "Date": today_str, "Done": False}])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.rerun()
        
        # Checkbox dikhao
        current_status = df.loc[(df['Habit'] == habit) & (df['Date'] == today_str), 'Done'].values[0]
        
        is_done = st.checkbox(habit, value=bool(current_status))
        
        # Agar user ne checkbox change kiya, to CSV update karo
        if is_done != current_status:
            df.loc[(df['Habit'] == habit) & (df['Date'] == today_str), 'Done'] = is_done
            df.to_csv(FILE_NAME, index=False)
            st.rerun()

    # --- PROGRESS BAR ---
    st.write("---")
    # Aaj ka total progress calculate karo
    today_data = df[df['Date'] == str(date.today())]
    if not today_data.empty:
        total = len(today_data)
        completed = len(today_data[today_data['Done'] == True])
        progress = completed / total
        st.progress(progress)
        st.write(f"Progress: {completed}/{total} Done")
        
        if progress == 1.0:
            st.balloons() # Full complete hone par balloons udao! 🎈