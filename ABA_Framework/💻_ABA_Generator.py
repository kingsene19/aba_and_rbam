import streamlit as st
from helpers.aba_generator import ABA_Generator, ConversionNotNeededError, ConvertTo

st.set_page_config(
    page_title='ABA Generator',
    layout='wide',
    page_icon='💻'
)

st.sidebar.image("https://i.ibb.co/w4mGQk4/image-removebg-preview.png")

st.title("ABA Generator")

# Initialize session state variables
if 'show_arg' not in st.session_state:
    st.session_state.show_arg = False
if 'show_att' not in st.session_state:
    st.session_state.show_att = False
if 'show_pref' not in st.session_state:
    st.session_state.show_pref = False
if 'output' not in st.session_state:
    st.session_state.output = ""
if "hide_select" not in st.session_state:
    st.session_state.hide_select = True

# Function to set default inputs based on selected option
def get_default_inputs(option):
    if option == 'Building arguments with ABA':
        return "a,b,c,q,p,r,s,t", "a,b,c", "(p,(q,a)),(q,),(r,(b,c)),(t,(p,c)),(s,t)", "(a,r),(b,s),(c,t)", ""
    elif option == 'Rewriting arguments':
        return "a,b,x,y,z", "a,b", "(y,b),(y,y),(x,x),(x,a),(z,(x,y))", "(a,y),(b,x)", ""
    elif option == 'Computing preferences with ABA+':
        return "a,b,c,q,p,r,s,t", "a,b,c", "(p,(q,a)),(q,),(r,(b,c)),(t,(p,c)),(s,t)", "(a,r),(b,s),(c,t)", "(b,a)"
    return '', '', '', '', ''

col1, col2, col3 = st.columns([1, 1, 2])
# Selectbox for loading class examples
with col3:
    option = st.selectbox(
        'Load class examples',
        ['Building arguments with ABA', 'Rewriting arguments', 'Computing preferences with ABA+']
    )

# Set default inputs
default_input1, default_input2, default_input3, default_input4, default_input5 = get_default_inputs(option)

# Input fields
input1 = st.text_input("Language", value=default_input1)
input2 = st.text_input("Assumptions", value=default_input2)
input3 = st.text_input("Rules", value=default_input3)
input4 = st.text_input("Contraries", value=default_input4)
input5 = st.text_input("Preferences", value=default_input5)

# Function to display and process the output for each type
def process_and_display(func, convert_to=None):
    try:
        if convert_to:
            aba = func(input1, input2, input3, input4, input5, convert_to=convert_to)
        else:
            aba = func(input1, input2, input3, input4, input5)
        st.session_state.output = aba
    except ConversionNotNeededError as cne:
        st.session_state.output = str(cne)
    except TimeoutError as te:
        st.session_state.output = str(te)
    except Exception as e:
        st.session_state.output = f"An error occurred: {str(e)}"

# Action buttons
col1, col2, col3 = st.columns(3)
if col1.button("Generate framework"):
    st.session_state.hide_select = True
    process_and_display(ABA_Generator.create_aba_framework)

if col2.button("Convert to atomic"):
    st.session_state.hide_select = True
    process_and_display(ABA_Generator.convert_to_atomic)
if col3.button("Convert to non circular"):
    st.session_state.hide_select = True
    process_and_display(ABA_Generator.convert_to_non_circular)

# Buttons to show arguments, attacks, and preferences
col4, col5, col6 = st.columns(3)

# Reset outputs when switching contexts
if col4.button("Create Arguments"):
    st.session_state.show_arg = True
    st.session_state.show_att = False
    st.session_state.show_pref = False
    st.session_state.hide_select = False
    st.session_state.output = ""

if col5.button("Create Attacks"):
    st.session_state.show_att = True
    st.session_state.show_arg = False
    st.session_state.show_pref = False
    st.session_state.hide_select = False
    st.session_state.output = "" 

if col6.button("Create normal/reverse attacks"):
    st.session_state.show_pref = True
    st.session_state.show_arg = False
    st.session_state.show_att = False
    st.session_state.hide_select = False
    st.session_state.output = "" 

# Arguments, Attacks and Normal/Reverse Attacks creation logic
if not st.session_state.hide_select:
    choice = st.selectbox(
            'Do you want to convert to atomic or non circular (Note that atomic conversion includes non circular)?',
            ['None', 'Atomic', 'Non circular'], key='choice')
    convert_to = ConvertTo.ATOMIC if choice == "Atomic" else ConvertTo.NON_CIRCULAR if choice == "Non circular" else None
    if st.session_state.show_arg:
        func = ABA_Generator.create_arguments
        process_and_display(func, convert_to)
    elif st.session_state.show_att:
        func = ABA_Generator.create_attacks
        process_and_display(func, convert_to)
    elif st.session_state.show_pref:
        func = ABA_Generator.create_normal_reverse_attacks
        process_and_display(func, convert_to)

# Display output
st.text_area("Output", st.session_state.output, height=600)
