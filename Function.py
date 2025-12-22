
import streamlit as st
import pandas as pd
import datetime

initial_players = 18

init_vote_display = pd.DataFrame({
            'Day': [0],
            'from': [0],
            'to': [0],
            'vote_count': [0],
        })
for player in range(1, initial_players + 1):
    # print(player)
    init_vote_display[f"{player}"] = False

init_vote_display['Note'] =  ''

init_char_table = pd.DataFrame({
            'Character': [''] * 8,
            'Status': [''] * 8,
            'Note': [''] * 8,
        })

# --- Session State Initialization ---
def init_session_state():
    # Track version to force-reset widgets
    if 'version' not in st.session_state:
        st.session_state.version = 0

    # Initialize Player Info if missing
    if 'ppl_info_df' not in st.session_state:
        
        st.session_state.ppl_info_df = pd.DataFrame({
            'No.': list(range(1, initial_players + 1)),
            'Inf': [''] * initial_players,
            '☀️': [''] * initial_players,
            '🌙': [''] * initial_players,
            '🔴': [''] * initial_players,
        }).set_index('No.')

    # Initialize Vote Table if missing
    if 'vote_df' not in st.session_state:
        st.session_state.vote_df = pd.DataFrame({
            'Day': [1, 1, 1],
            'Way': ['', '', ''],
            'Voters': ['', '', ''],
            'Note': ['', '', ''],
        })

    if 'vote_display_df' not in st.session_state:
        st.session_state.vote_display_df = init_vote_display.iloc[0:0]

    # Initialize Character Table if missing
    
    if 'char_dict' not in st.session_state:
        
        st.session_state.char_dict = {"Outsider":init_char_table,
                                      "Minion":init_char_table,
                                      "Demon":init_char_table,}
    else:
        for i,relate_df in st.session_state.char_dict.items():
            relate_df['Status'] = ''
            relate_df['Note'] = ''
        # pass

def tab_ppl_information():
    
    # Calculate height to show all rows (approx 35px per row + header)
    print(len(st.session_state.ppl_info_df))
    num_rows = len(st.session_state.ppl_info_df)
    calculated_height = (num_rows + 1) * 35 + 3

    st.markdown("### Player Information & Status")
    # st.info("Edit the table directly to record names and death/alignment status. 'Inf' is Name/Info. The symbols are for status.")

    # Define column configurations for help text
    column_config = {
        'Inf': st.column_config.TextColumn("Info", width="medium",help="Enter player name or brief description."),
        '☀️': st.column_config.TextColumn("☀️", help="Mark if player died before or during Night 3 (Baron/etc. calculation)."),
        '🌙': st.column_config.TextColumn("🌙", help="Mark if player died during a night (e.g., Demon attack)."),
        '🔴': st.column_config.TextColumn("🔴", help="Mark if player is suspected/confirmed Minion or Demon."),
    }

    # Display the editable table
    edited_df = st.data_editor(
        st.session_state.ppl_info_df,
        column_config=column_config,
        num_rows="fixed",
        hide_index=False,
        height=calculated_height,
        key=f"edit_ppl_info_v{st.session_state.version}"
    )
    # The return value (edited_df) is only used/processed when the form submits.
    return edited_df

def vote_display_table():
    st.markdown("### Record Voting")


    column_config = {
        'Day': st.column_config.NumberColumn("D", format="%d", min_value=1, width=25),
        'from': st.column_config.NumberColumn("F", format="%d", min_value=1, width=25),
        'to': st.column_config.NumberColumn("T", format="%d", min_value=1, width=25),
        'Note':st.column_config.TextColumn("Note",width="medium"),
        'vote_count': st.column_config.NumberColumn("Count", format="%d", min_value=1, width=25),
    }

    for player in range(1, initial_players + 1):
        column_config[f"{player}"] = st.column_config.CheckboxColumn(f"{player}", default=False, width=25)

    # column_config['Note'] =  st.column_config.TextColumn("Note")

    edited_df = st.dataframe(
        st.session_state.vote_display_df,
        column_config=column_config,
        # num_rows="fixed",
        hide_index=True,
        # use_container_width=True, # This helps with the layout
        
    )
    return edited_df



def tab_vote_table():
    st.markdown("### Daily Nomination & Voting Record")
    # st.warning("player numbers.")

    # Define column configurations
    column_config = {
        'Day': st.column_config.NumberColumn("Day", format="%d", min_value=1),
        'Voters': st.column_config.TextColumn("Voters",width= "medium", help="formate like 1245692255"),
        'Note': st.column_config.TextColumn("Note", help="if any"),
    }

    # Display the editable table
    edited_df = st.data_editor(
        st.session_state.vote_df,
        column_config=column_config,
        num_rows="dynamic",
        hide_index=True,
        key=f'edit_vote_table_v{st.session_state.version}' # Key is important for form submission
    )
    # The button to add a row has been moved outside the form to fix the error.
    return edited_df

def vote2dict(votes_str):
    record_dict = {}
    votes_str = f"&{votes_str}&" # for easy handling
    str_len = len(votes_str)
    for i in range(1,str_len):
        target_str = votes_str[i]
        if (target_str != "&"): 
            if (target_str == votes_str[i+1]) & (target_str == votes_str[i-1]): # this case record both
                record_dict[f"1{target_str}"] =True
                record_dict[f"{target_str}"] =True

            if (target_str != votes_str[i+1]):# check next num. is not same, then record
                if target_str == votes_str[i-1]:
                    record_dict[f"1{target_str}"] =True
                else:
                    record_dict[f"{target_str}"] =True

            # check pervious number, see is +10
    return record_dict

def record2dispaly_vote(vote_df):
    vote_display = init_vote_display.iloc[0:0]

    vote_df["Day"] = vote_df["Day"].fillna(method='ffill')
    vote_df = vote_df.fillna('')


    vote_df["fromto"] = vote_df['Way'].apply(lambda x: x.split(" "))
    vote_df['from'] = vote_df["fromto"].apply(lambda x: x[0])
    vote_df['to'] = vote_df["fromto"].apply(lambda x: x[-1])


    vote_df['vote_dict'] = vote_df['Voters'].apply(lambda x: vote2dict(x))
    vote_df['vote_count'] = vote_df['vote_dict'].apply(lambda x: len(x))
    expanded_df = vote_df['vote_dict'].apply(pd.Series)
    vote_df = pd.concat([vote_df.drop('vote_dict', axis=1), expanded_df], axis=1)
    
    need_col = ['Day','from','to','vote_count']+ expanded_df.columns.to_list() + ['Note']

    vote_display = pd.concat([vote_display,vote_df[need_col]])
    
    return vote_display


def tab_character_confirmation(fixed=True):
    
    # st.info("Use the 'Status' column to track.")

    # Define column configurations, specifically for the Status selectbox
    column_config = {
        'Character': st.column_config.TextColumn(
            "Char",
            width = "small",
            # disabled=True
        ),
        'Status': st.column_config.SelectboxColumn(
            "S",
            help="0: not possible, 1: possible, 2: exist",
            options=['0', '1', '2'],
            width = 50,
            # default='Possible (B)'
        ),
        'Note': st.column_config.TextColumn(
            "Note",
            width = "medium",
            # disabled=True
        ),
    }

    # Display the editable table
    edited_dict = {}
    cols = st.columns(3) 
    i = 0
    for faction,char_df in st.session_state.char_dict.items():
        with cols[i]:
            st.markdown(f"#### {faction}")
            edited_dict[faction] = st.data_editor(
                char_df,
                column_config=column_config,
                num_rows="fixed",
                hide_index=True,
                key=f'edit_{faction}_table_v{st.session_state.version}'# Key is important for form submission
            )
        i = i+1

    # The button to reset status has been moved outside the form to fix the error.
    
    return edited_dict

