import tmdb.helper as helper
import utils.utils as utils

def main():    
    testtitlelist =  ['beverly hills chihuahua', 'beethoven', 'air bud', 'hachiko', 'marley & me']

    #resp = tmdb_api_client.get_detail_data_from_tmdb_for_titles(testtitlelist)
    #resp = helper.get_basic_data_from_tmdb_for_titles(testtitlelist)

    resp =utils.detect_ipnut_lang("Film mit sprechenden Hunden")
        
    print(resp)
if __name__ == "__main__":
    main()

