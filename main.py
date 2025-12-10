import streamlit as st
import pandas as pd
import datetime

# --- Configuration and Initialization ---

# Set up the page for mobile responsiveness
st.set_page_config(
    page_title="Clocktower Recorder",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Session State Initialization ---

def init_session_state():
    """Initializes the required DataFrames in Streamlit's session state."""

    # 1. Player Information Table (Tab 1)
    if 'ppl_info_df' not in st.session_state:
        initial_players = 18
        # Using concise headers for better mobile view in the editor
        st.session_state.ppl_info_df = pd.DataFrame({
            'No.': list(range(1, initial_players + 1)),
            'Inf': [''] * initial_players, # Name/Info
            '☀️': [''] * initial_players, # Dead Before N3
            '🌙': [''] * initial_players, # Dead At Night
            '🔴': [''] * initial_players, # Is Red Side (M/D)
        }).set_index('No.')

    # 2. Vote Table (Tab 2)
    if 'vote_df' not in st.session_state:
        st.session_state.vote_df = pd.DataFrame({
            'Day': [1 ],
            'from to': [''],
            'Voters': [''],
            'Note on Vote': [''],
        })

    # 3. Character Confirmation Table (Tab 3)
    if 'char_df' not in st.session_state:
        initial_chars = ['Outsiders']*5 + ['Minions']*5 + ['Demons']*5
        
        # MODIFICATION: Changed columns to Booleans for the three states
        st.session_state.char_df = pd.DataFrame({
            'Chap': initial_chars,
            'Character': [''] * 15,
            'A (Confirmed)': [False] * 15, # New tickbox column
            'B (Possible)': [False] * 15,    # New tickbox column (Default to True)
            'C (Not Exist)': [False] * 15,  # New tickbox column
        })

    # Helper for adding rows to Player Info
    if 'next_player_num' not in st.session_state:
        st.session_state.next_player_num = len(st.session_state.ppl_info_df) + 1

# Apply initialization
init_session_state()

# --- Utility Functions for Row Management ---

def add_vote_row():
    """Adds a new row to the Vote Table."""

    # This call to submitted_handle() here would require passing the dataframes, 
    # but since this function is commented out in the prompt, we'll keep it simple 
    # and just modify the session state directly as was likely intended.
    # submitted_handle() # If this function is called, it needs to be fixed.

    current_df = st.session_state.vote_df
    new_day = current_df['Day'].max() + 1 if not current_df.empty else 1
    new_row = pd.DataFrame({
        'Day': [new_day],
        'Nominator': [''],
        'Nominee': [''],
        'Voters (Comma Separated)': [''],
        'Note on Vote': [''],
    })
    st.session_state.vote_df = pd.concat([current_df, new_row], ignore_index=True)


# --- UI Functions for Tabs (Now contained within the form) ---

def tab_ppl_information():
    st.markdown("### Player Information & Status")
    # st.info("Edit the table directly to record names and death/alignment status. 'Inf' is Name/Info. The symbols are for status.")

    # Define column configurations for help text
    column_config = {
        'Inf': st.column_config.TextColumn("Info", help="Enter brief description.",width= "large"),
        '☀️': st.column_config.TextColumn("☀️", width="small",help="Mark if player died before or during Night 3 (Baron/etc. calculation)."),
        '🌙': st.column_config.TextColumn("🌙", width="small",help="Mark if player died during a night (e.g., Demon attack)."),
        '🔴': st.column_config.TextColumn("🔴", width="small",help="Mark if player is suspected/confirmed Minion or Demon."),
    }

    # Display the editable table
    edited_df = st.data_editor(
        st.session_state.ppl_info_df,
        column_config=column_config,
        num_rows="dynamic",
        hide_index=False,
        key='edit_ppl_info' # Key is important for form submission
    )
    # The return value (edited_df) is only used/processed when the form submits.
    return edited_df


def tab_vote_table():
    st.markdown("### Daily Nomination & Voting Record")
    st.warning("Use player numbers (P1, P2, etc.) or names for consistency.")

    # Define column configurations
    column_config = {
        'Day': st.column_config.NumberColumn("Day", width="small",format="%d", min_value=1),
        'Voters': st.column_config.TextColumn("Voters", width="medium",help=""),
        'Note on Vote': st.column_config.TextColumn("Note", width="small",help="Context, final count, or outcome."),
    }

    # Display the editable table
    edited_df = st.data_editor(
        st.session_state.vote_df,
        column_config=column_config,
        num_rows="dynamic",
        hide_index=True,
        key='edit_vote_table' # Key is important for form submission
    )
    # The button to add a row has been moved outside the form to fix the error.
    return edited_df


def tab_character_confirmation():
    st.markdown("### Possible Character Grid")
    st.info("Use the **tick boxes** to track the status: **A** (Confirmed), **B** (Possible), or **C** (Not Exist). Only one box should be ticked per row.")

    # MODIFICATION: 
    # 1. 'Character' column is now editable for better length/usability (col length adjustment)
    # 2. Status is now three boolean columns (3 tick boxes in 3 columns)
    column_config = {
        'Chap': st.column_config.TextColumn(
            "Alignment",
            disabled=True, # Keep 'Chap' (Alignment) column disabled
            width= "small"
        ),
        'Character': st.column_config.TextColumn(
            "Character Name",
            help="E.g., Washerwoman, Minion, Imp",
            width= "medium"
        ),
        'A (Confirmed)': st.column_config.CheckboxColumn(
            "YES", # Use short header for space saving
            help="Confirmed Character (A)",
            default=False,
            width= "small"
        ),
        'B (Possible)': st.column_config.CheckboxColumn(
            "Poss", # Use short header for space saving
            help="Possible Character (B)",
            default=False,
            width= "small"
        ),
        'C (Not Exist)': st.column_config.CheckboxColumn(
            "NO", # Use short header for space saving
            help="Not Exist (C)",
            default=False,
            width= "small"
        ),
    }

    # Display the editable table
    edited_df = st.data_editor(
        st.session_state.char_df,
        column_config=column_config,
        num_rows="dynamic",
        hide_index=True,
        key='edit_char_table' # Key is important for form submission
    )
    
    return edited_df


# --- Main App Structure ---

st.title("🩸 Blood Clocktower Game Recorder")
st.caption("A mobile-friendly tool for Storytellers and players to track game state.")

# 1. Start the Form (This blocks reruns from the editors)
with st.form("main_recorder_form"):
    
    # Create the tabs within the form
    tab1, tab2, tab3 = st.tabs([
        "👥 Player Info",
        "🗳️ Vote Table",
        "📜 Character Status"
    ])

    # Store the results of the data editors (which contain the latest edits)
    with tab1:
        new_ppl_df = tab_ppl_information()

    with tab2:
        new_vote_df = tab_vote_table()

    with tab3:
        new_char_df = tab_character_confirmation()

    st.markdown("---")
    
    # 2. Add the Submit Button
    # This button submits the form, unblocking the reruns and causing the final rerun
    submitted = st.form_submit_button("💾 Commit All Edits & Save")
    
    def submitted_handle():
        # Only when submitted, we overwrite the session state with the new data
        st.session_state.ppl_info_df = new_ppl_df
        st.session_state.vote_df = new_vote_df
        st.session_state.char_df = new_char_df
        st.success("Changes saved successfully!")
        
        # An explicit rerun here is optional, as the form submission already causes one
        st.rerun() # Commented out to prevent the second rerun caused by the button
        

    # 3. Handle Form Submission
    if submitted:
        submitted_handle()
        

## --- Additional Functionality Buttons (Moved outside the form to prevent errors) ---

# st.markdown("---")
# st.subheader("Action Buttons")

# col_add, col_reset = st.columns(2)

# with col_add:
#     # This button now works because it's outside the main form
#     if st.button("➕ Add New Day/Vote Row", help="Adds a new row to the Vote Table."):
#         # Note: This currently adds the row without saving the main form edits first.
#         # It should be OK since vote_df is also outside the form context (though edited inside).
#         add_vote_row()
#         st.rerun()

# with col_reset:
#     # This button now works because it's outside the main form
#     if st.button("🔄 Reset Character Status", help="Resets all Character Statuses to 'Possible (B)' and immediately saves it."):
#         # Reset A and C to False, B to True
#         st.session_state.char_df['A (Confirmed)'] = False
#         st.session_state.char_df['B (Possible)'] = True
#         st.session_state.char_df['C (Not Exist)'] = False
#         st.rerun()


# --- Footer (Outside of the form) ---

st.markdown("---")
st.markdown(f"**Current Session Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("All data is stored in the current session only. Use the 'Commit All Edits & Save' button for tables.")