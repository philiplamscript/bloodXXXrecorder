import streamlit as st
import pandas as pd
import datetime
import streamlit.components.v1 as components
from Function import *
# --- Configuration and Initialization ---

# Set up the page for mobile responsiveness
st.set_page_config(
    page_title="Clocktower Recorder",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        width: 50px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# JavaScript to prevent accidental page refresh/close
components.html(
    """
    <script>
    window.addEventListener('beforeunload', function (e) {
      e.preventDefault();
      e.returnValue = 'Data will be lost!';
    });
    </script>
    """,
    height=0,
)

def submitted_handle():
    # recode vote display result
    
    
    # Only when submitted, we overwrite the session state with the new data
    st.session_state.ppl_info_df = new_ppl_df
    # st.session_state.vote_df = record_vote_df
    st.session_state.char_dict = new_char_dict

    st.session_state.vote_display_df = record2dispaly_vote(record_vote_df)
    # st.write(st.session_state.vote_display_df)
    st.success("Changes saved successfully!")
    # An explicit rerun here is optional, as the form submission already causes one


# --- Main App Structure ---    

# Apply initialization
init_session_state()

# --- Sidebar Navigation ---
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("Jump to section:")

# Create navigation links using Markdown anchors
st.sidebar.markdown("- [Player Status](#player-information-status)")
st.sidebar.markdown("- [Daily Nomination](#daily-nomination-voting-record)")
st.sidebar.markdown("- [Note](#note)")
st.sidebar.markdown("- [Voting History](#record-voting)")
st.sidebar.markdown("- [Character Confirmation](#outsider)")

st.sidebar.divider()

# --- Global Save Button ---
st.sidebar.subheader("Controls")
submitted_sidebar = st.sidebar.button("💾 Commit All Edits & Save", use_container_width=True, key="side_save")

restart_button = st.sidebar.button("Restart simliar setting", use_container_width=True)


## df Tab for record and view
tab1, tab2 = st.columns(2)

with tab1:
    # with st.form("review"):
    new_ppl_df = tab_ppl_information()
    

with tab2:
    st.markdown("### Note")
    user_input = st.text_area("")

    record_vote_df = tab_vote_table()
    submitted = st.button("💾 Commit All Edits & Save")




review_vote_df = vote_display_table()
new_char_dict = tab_character_confirmation()
# # --- Additional Functionality Buttons (Moved outside the form to prevent errors) ---


if submitted or submitted_sidebar:
    submitted_handle()
    
    st.rerun()
    st.success("Changes saved successfully!")
    


st.write(f"Now is version {st.session_state.version}")
restart_button_2 = st.button("Restart simliar setting")


if restart_button or restart_button_2:
    st.session_state.version += 1
    submitted_handle()
    ## [update] save to DB
    
    # 2. Clear the data frames specifically
    if 'ppl_info_df' in st.session_state:
        del st.session_state.ppl_info_df
    if 'vote_df' in st.session_state:
        del st.session_state.vote_df
    if 'vote_display_df' in st.session_state:
        del st.session_state.vote_display_df

    init_session_state()
    
    st.rerun()
    st.success("Restarted!")
    






