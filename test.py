import tmdb.helper as helper
import utils.utils as utils
import utils.duckdb as duckdb

def main():    
    testtitlelist =  "Transformers, RoboCop, Robot, Blade Runner"
    #resp = helper.get_recro_movies({"titles": testtitlelist,"config":{"provider": ["Disney Plus","MagentaTV"] }})     
    #resp =utils.detect_ipnut_lang("Film mit sprechenden Hunden")
        
    #resp = duckdb.creattable()
    #resp= duckdb.insert_conversation("user1","bot1")
    resp = helper.get_detail_moviedata("Planet der Affen - Prevolution")

    #resp=duckdb.fetchdata()
    print(resp)
if __name__ == "__main__":
    main()

