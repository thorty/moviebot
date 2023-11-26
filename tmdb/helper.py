from tmdb.tmdb_api_client import get_basic_data_from_tmdb_for_titles
import streamlit as st



#helpers
def _get_movie_data(titles: str):
  print(f"_get_movie_data titles input: ", titles)
  inputlist = titles.split(",")
  inputlist = [x.strip(' ') for x in inputlist]      
  result = get_basic_data_from_tmdb_for_titles(inputlist)
  #print(result)
  return result
