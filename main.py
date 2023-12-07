import streamlit as st
from llm_helpers.moviebot import get_chain
import utils.utils as utils
from langchain.callbacks.tracers import ConsoleCallbackHandler
from st_supabase_connection import SupabaseConnection
import utils.supabase as superdb

 

import yaml
from yaml import SafeLoader


def reset():
    st.session_state.messages=[]
    st.session_state.chathistory = ""
    st.session_state.titlehistory = ""
        

### definitions
STREAMING_PROVIDER = ["Disney Plus","Amazon Prime Video","Apple TV","MagentaTV", "Netflix"] 

# db
#duckdb.creattable()
modelchain = get_chain()
### content and porcessing

st.set_page_config(page_title="Moviebot", page_icon=":robot:")


#content
m = st.markdown("""
<style>
div.stDownloadButton > button:first-child {    
    background: transparent;
    border: none !important;
    font-size:0;                
}
</style>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.header("Ich bin Mobo!")
    st.markdown("Dein persönlicher Filmfinder \n\n Ich bin hier um den richtigen Film für dich zu finden. \n\n Sag mir einfach was du sehen möchtest, \n ich werde versuchen etwas passendes für dich zu finden!")
    with open('duck.db', 'rb') as f:
        st.download_button('', f, file_name='duck.db')
with col2:        
    st.image(image='mobo.jpg', width=350 )
providerselection = st.multiselect(
    'Streaminganbieter',STREAMING_PROVIDER)
st.session_state['providerselection'] = providerselection
#prompt = "Hi, Was möchtest du für einen Film sehen?"
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content":"Hi, was möchtest du für einen Film sehen?"}]
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# React to user input
if prompt := st.chat_input("Was möchtest du sehen?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner('Ok. Einen Moment. Bin gleich weieder da!  '):
        #lang = utils.detect_ipnut_lang(prompt) does not work
        #make the llm stuff    
        if 'titlehistory' not in st.session_state:
            print(f"initialize titelhistory for session")
            st.session_state.titlehistory = ""    
        titlehistory = st.session_state.titlehistory                
        print(f"titlehistory: ",titlehistory)
        
        if 'chathistory' not in st.session_state:
            print(f"initialize chathistory for session")
            st.session_state.chathistory = ""    
        chathistory = st.session_state.chathistory                
        print(f"chathistory: ",chathistory)
        
        response = modelchain.invoke({"input":prompt, "provider": providerselection, "blacklist": titlehistory, "history": chathistory}, config={'callbacks': [ConsoleCallbackHandler()]})
        newtitles = utils.getTitlesFromOutput(response)
        st.session_state.titlehistory = st.session_state.titlehistory + newtitles
        
        chathistory = prompt
        st.session_state.chathistory = st.session_state.chathistory + chathistory

        superdb.insert_conversation(prompt, response)
    #response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


st.button("Reset", type="primary", on_click=reset)
    