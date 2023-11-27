import tmdb.helper as helper
import utils.utils as utils

def main():    
    testtitlelist =  "Transformers, RoboCop, Robot, Blade Runner"


    resp = helper.get_recro_movies({"titles": testtitlelist,"config":{"provider": ["Disney Plus","MagentaTV"] }}) 
    


    #resp =utils.detect_ipnut_lang("Film mit sprechenden Hunden")
        
    print(resp)
if __name__ == "__main__":
    main()

