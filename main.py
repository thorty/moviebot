import streamlit as st
from llm_helpers.moviebot import get_chain
import utils.utils as utils

### definitions
STREAMING_PROVIDER = [
    "Disney Plus",
    "Amazon Prime Video",
    "Apple TV",
    "MagentaTV",
    "Netflix",
]

### content and porcessing

st.set_page_config(page_title="Moviebot", page_icon=":robot:")
st.header("Hi! Ich bin Mobo!")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        "Dein persönlicher Filmfinder \n\n Ich bin hier um den richtigen Film für dioch zu finden. \n\n Sag mir einfach was du sehen möchtest, \n ich werde versuchen etwas passendes dich zu finden!"
    )

with col2:
    st.image(image="mobo.jpg", width=350)


providerselection = st.multiselect("Streaminganbieter", STREAMING_PROVIDER)
st.session_state["providerselection"] = providerselection


# prompt = "Hi, Was möchtest du für einen Film sehen?"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, Was möchtest du für einen Film sehen?"}
    ]


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

    with st.spinner("Ok. Einen Moment. Bin gleich wieder da!  "):
        lang = utils.detect_ipnut_lang(prompt)
        # make the llm stuff
        if "titlehistory" not in st.session_state:
            print(f"initialize titelhistory for session")
            st.session_state.titlehistory = ""
        titlehistory = st.session_state.titlehistory
        print(f"titlehistory: ", titlehistory)

        modelchain = get_chain()
        response = modelchain.invoke(
            {
                "input": prompt + " aber keinen der folgenden titel: " + titlehistory,
                "config": st.session_state["providerselection"],
                "lang": lang,
                "provider": providerselection,
            }
        )

        newtitles = utils.getTitlesFromOutput(response)
        st.session_state.titlehistory = st.session_state.titlehistory + newtitles

    # response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
