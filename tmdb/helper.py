from tmdb.tmdb_api_client import get_basic_data_from_tmdb_for_titles, get_detail_data_from_tmdb_for_title, get_movies_with_recro
# import module 
import traceback 

#helpers
def get_movie_data(input: dict):
  try:
    titles = input["titles"]
    print(f"_get_movie_data titles input: ", titles)
    inputlist = titles.split(",")
    inputlist = [x.strip(' ') for x in inputlist]      
    result = get_basic_data_from_tmdb_for_titles(inputlist)
    print(f"get_movie_data result: ", result)
    return result
  except:    
     traceback.print_exc() 
     return None

def get_recro_movies(input: dict):
  try:
    #titles = input["titles"]
    titles = list(input["titles"]["text"].values())
    inputlist = titles
    provider = input["config"]["provider"]
    print(f"_get_movie_data titles input: ", titles)
    #inputlist = titles.split(",")
    #inputlist = [x.strip(' ') for x in inputlist]
    result = get_movies_with_recro(inputlist, provider)
    print(f"get_recro_movies result: ",result)
    return result  
  except:
      traceback.print_exc() 
      return None

def get_detail_moviedata(title: str):
  try:
    print(f"get_movie_data_from_tmdb","title=",title)
    fulldata = get_detail_data_from_tmdb_for_title(title)
    print(f"get_detail_moviedata","result:", fulldata)
    return fulldata
  except:
     traceback.print_exc() 
     return None
  

