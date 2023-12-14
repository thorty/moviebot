from operator import itemgetter
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.runnable import RunnableBranch
from langchain.prompts import PromptTemplate
from langchain.chains import create_extraction_chain
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableMap, RunnablePassthrough, RunnableLambda

from llm_helpers.openai_prompts import descisionprompt, recommedation_titels_prompt, general_prompt, recro_prompt, question_answering_prompt, extract_title_prompt
from tmdb.helper import get_recro_movies, get_detail_moviedata
    
import streamlit as st



def get_chain(ressources):


    openai_functioncall_to_get_the_titles = create_functioncall_chain_for_titles(ressources)

    if ressources == "azure":

        # Setup keys        
        t_openai_api_key = st.secrets['t_openai_api_key']
        t_openai_api_base = st.secrets['t_openai_api_base']
        t_openai_api_version = st.secrets['t_openai_api_version']

        
        llm_t_openai_4 = AzureChatOpenAI(     
            azure_deployment="gpt-4-32k",
            openai_api_version=t_openai_api_version,
            openai_api_key=t_openai_api_key,
            openai_api_base=t_openai_api_base
        )

        llm_t_openai_4_turbo = AzureChatOpenAI(     
            azure_deployment="gpt-4-1106-preview",
            openai_api_version=t_openai_api_version,
            openai_api_key=t_openai_api_key,
            openai_api_base=t_openai_api_base
        )

        #define chains
        descissionchain = ( descisionprompt | llm_t_openai_4_turbo | StrOutputParser() )
   
        recommendation_chain = (
        
            {"context": {"titles": recommedation_titels_prompt | llm_t_openai_4 | StrOutputParser() | {"input": RunnablePassthrough()} | openai_functioncall_to_get_the_titles , "config":RunnablePassthrough() }| RunnableLambda(get_recro_movies), "input":RunnablePassthrough(), "history":RunnablePassthrough()}
            | recro_prompt
            | llm_t_openai_4_turbo
            | StrOutputParser()
        )


        info_chain = (
            {"context": extract_title_prompt | llm_t_openai_4_turbo | StrOutputParser() | RunnableLambda(get_detail_moviedata), "input":RunnablePassthrough(), }
            | question_answering_prompt
            | llm_t_openai_4_turbo
            | StrOutputParser())


        general_chain = (general_prompt | llm_t_openai_4_turbo)


    else:
        openai_api_key = st.secrets['openai_api_key']

        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            max_tokens=1000
        )   
        llm_gpt4_temp = ChatOpenAI(
            model="gpt-4",
            openai_api_key=openai_api_key,
            max_tokens=1000,
            temperature=0.3,
        )
        
        llm_gpt4 = ChatOpenAI(
            model="gpt-4",
            openai_api_key=openai_api_key,
            max_tokens=1000,        
        )
    
        #define chains
        descissionchain = ( descisionprompt | llm_gpt4 | StrOutputParser() )
        
        recommendation_chain = (        
            {"context": {"titles": recommedation_titels_prompt | llm_gpt4_temp | StrOutputParser() | {"input": RunnablePassthrough()} | openai_functioncall_to_get_the_titles , "config":RunnablePassthrough() }| RunnableLambda(get_recro_movies), "input":RunnablePassthrough(), "history":RunnablePassthrough()}
            | recro_prompt
            | llm
            | StrOutputParser()
        )


        info_chain = (
            {"context": extract_title_prompt | llm | StrOutputParser() | RunnableLambda(get_detail_moviedata), "input":RunnablePassthrough(), }
            | question_answering_prompt
            | llm
            | StrOutputParser())


        general_chain = (general_prompt | llm)




    # stick everything together    
    branch = RunnableBranch(
        (lambda x: "recommendation" in x["topic"].lower(), recommendation_chain),
        (lambda x: "question" in x["topic"].lower(), info_chain),
        general_chain,
    )
    full_chain = {"topic": descissionchain, "input": lambda x: x["input"], "provider":lambda x: x["provider"], "blacklist":lambda x: x["blacklist"], "history":lambda x: x["history"] }| branch

    return full_chain




def create_functioncall_chain_for_titles(ressources):
    openai_api_key = st.secrets['openai_api_key']
    template = """
        You have to extract the movie titles form given input and return them as a Python List of strings

        input: {input}
        output:
        """

    prompt_template = PromptTemplate(input_variables=["input"], template=template)

    # Schema
    schema = {
      "properties": {
          "movie_title_{i}": {"type": "string"},
      },
      "required": ["movie_title"],
    }

    #create chain
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613",  openai_api_key=openai_api_key)

    chain = create_extraction_chain(schema=schema, llm=llm, verbose=True, prompt=prompt_template)

    return chain
