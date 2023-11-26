from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.runnable import RunnableBranch
import os

from llm_helpers.openai_prompts import descisionprompt, recommedation_titels_prompt, general_prompt, recro_prompt, question_answering_prompt, extract_title_prompt
from tmdb.tmdb_api_client import get_detail_data_from_tmdb_for_title
from tmdb.helper import _get_movie_data


def get_chain():

    # Setup keys
    openai_api_key = os.environ['openai_api_key']

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=openai_api_key,
        max_tokens=1000
    )
    #define chains
    descissionchain = ( descisionprompt | llm | StrOutputParser() )
    #recommendation_chain = (recommedation_titels_prompt | llm )

    recommendation_chain = (
        {"context": recommedation_titels_prompt | llm | StrOutputParser() | RunnableLambda(_get_movie_data), "input":RunnablePassthrough(), "lang":RunnablePassthrough()}
        | recro_prompt
        | llm
        | StrOutputParser()
    )

    info_chain = (
        {"context": extract_title_prompt | llm |StrOutputParser() | RunnableLambda(get_detail_data_from_tmdb_for_title), "input":RunnablePassthrough()}
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
    full_chain = {"topic": descissionchain, "input": lambda x: x["input"], "lang":lambda x: x["lang"]} | branch

    return full_chain

