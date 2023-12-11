try:
    from tmdb.tmdb_api_client import (
        get_basic_data_from_tmdb_for_titles,
        get_detail_data_from_tmdb_for_title,
        get_movies_with_recro,
    )
except:
    from tmdb_api_client import (
        get_basic_data_from_tmdb_for_titles,
        get_detail_data_from_tmdb_for_title,
        get_movies_with_recro,
    )

# import module
import traceback


# helpers
def get_movie_data(input: dict):
    try:
        titles = input["titles"]
        print(f"_get_movie_data titles input: ", titles)
        inputlist = titles.split(",")
        inputlist = [x.strip(" ") for x in inputlist]
        result = get_basic_data_from_tmdb_for_titles(inputlist)
        print(f"get_movie_data result: ", result)
        return result
    except:
        traceback.print_exc()
        return None


def get_recro_movies(input: dict):
    try:
        print(f"get_recro_movies, input: {input}")
        for line in input["titles"]["input"].split("\n"):
            if "[" in line:
                line = line.replace("[", "")
                line = line.replace("]", "")
                line = line.replace("'", "")
                line = line.replace('"', "")
                line_split = line.split(", ")
                input_list = line_split
                print(line_split)

        # titles = list(input["titles"]["text"].values())
        # inputlist = titles
        provider = input["config"]["provider"]
        # print(f"_get_movie_data titles input: ", titles)
        # # inputlist = titles.split(",")
        # # inputlist = [x.strip(' ') for x in inputlist]
        result = get_movies_with_recro(input_list, provider)
        print(f"get_recro_movies result: ", result)
        return result
    except:
        traceback.print_exc()
        return None


def get_detail_moviedata(title: str):
    try:
        print(f"get_movie_data_from_tmdb", "title=", title)
        fulldata = get_detail_data_from_tmdb_for_title(title)
        print(f"get_detail_moviedata", "result:", fulldata)
        return fulldata
    except:
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_input = {
        "titles": {
            "input": "\nSure, I'd be happy to help! Based on your inquiry, here are five action movies that do not include any of the following titles:\n\n['The Matrix', 'Mad Max: Fury Road', 'The Avengers', 'John Wick', 'Fast and Furious']\n\nI hope you find this list helpful! Let me know if you have any other questions or if you'd like more recommendations."
        },
        "config": {
            "topic": "Recommendation",
            "input": "action aber keinen der folgenden titel: ",
            "lang": "en",
            "provider": ["MagentaTV"],
        },
    }
    get_recro_movies(test_input)
