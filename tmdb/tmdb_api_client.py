# tmdb api
# moviedb tool singe title search
import requests
import json
from difflib import get_close_matches
import os
from dotenv import load_dotenv

# If you're curious of all the loggers
# print(streamlit.logger._loggers)

# streamlit_root_logger = logging.getLogger(streamlit.__name__)

load_dotenv()

headers = {"accept": "application/json", "Authorization": os.getenv("tmdb_bearer")}


def get_movies_with_recro(titles: list[str], providers: list[str]):
    print(f"get_basic_data_from_tmdb_for_titles", titles)
    movies = []
    # get movies from tmdb from given titles
    for title in titles:
        movie = get_basic_data_from_tmdb_for_title(title)
        if movie:
            print(f"movie: {movie}")
            movies.append(movie)
    # add similar recommendations from tmdb
    similar_movies = get_recro_movies(movies)
    if similar_movies:
        movies = movies + similar_movies
    # filter for providers
    rsult_movies = filter_movies(movies, providers)
    if rsult_movies and len(rsult_movies) > 5:
        rsult_movies = rsult_movies[:4]
    fulldata_as_string = create_data_list(rsult_movies)
    return fulldata_as_string


def get_basic_data_from_tmdb_for_titles(titles: list[str]):
    print(f"get_basic_data_from_tmdb_for_titles", titles)
    movies = []
    for title in titles:
        movie = get_basic_data_from_tmdb_for_title(title)
        if movie:
            movies.append(movie)
    fulldata_as_string = create_data_list(movies)
    return fulldata_as_string


def get_detail_data_from_tmdb_for_titles(titles: list[str]):
    print(f"get_detail_data_from_tmdb_for_titles", titles)
    movies = []
    for title in titles:
        movie = get_detail_data_from_tmdb_for_title(title)
        if movie:
            movies.append(movie)
    return movies


def get_basic_data_from_tmdb_for_title(title: str):
    try:
        print(f"get_movie_data_from_tmdb", "title=", title)
        fulldata = create_basic_movie_data(title)
        return fulldata
    except:
        return None


def get_detail_data_from_tmdb_for_title(title: str):
    try:
        print(f"get_movie_data_from_tmdb", "title=", title)
        fulldata = create_movie_data(title)
        return fulldata
    except:
        return None


def get_recro_movies(movies):
    if len(movies) > 0:
        searchId = movies[0]["id"]
        results = find_smilar_movies(searchId)
        if results:
            movies = parse_movies_from_search(results)
        return movies


def find_smilar_movies(id):
    url = (
        "https://api.themoviedb.org/3/movie/"
        + str(id)
        + "/recommendations?language=en-US&page=1"
    )
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    return None


def parse_movies_from_search(results):
    movies = []
    for movie in results["results"]:
        if movie and "id" in movie:
            id = get_movie_id(movie)
            providers = get_watch_providers(id)
            flatproviders = get_watch_providers_via_subtype(
                filter_watch_providers(providers, "DE"), "flatrate"
            )
            rentproviders = get_watch_providers_via_subtype(
                filter_watch_providers(providers, "DE"), "rent"
            )
            # buyproviders = get_watch_providers_via_subtype(filter_watch_providers(providers, "DE"),"buy" )

            filtered_data = {
                "title": movie["title"],
                "flatproviders": flatproviders,
                "rentproviders": rentproviders,
                "overview": movie["overview"],
                "release_date": movie["release_date"],
                "id": id,
            }
            movies.append(filtered_data)
    return movies


def find_movie_basic(title, lang):
    title = title.replace(" ", "+")
    url = (
        "https://api.themoviedb.org/3/search/movie?include_adult=false&language="
        + lang
        + "&page=1&query="
        + title
    )

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        # print(f"find_movie for", title, "response: ",data)

        if "results" in str(data) and len(data["results"]) > 0:
            # print(f"movie found!")
            movie = get_movie_form_search(data["results"], title)
            return movie

    return None


def find_movie(title, lang):
    title = title.replace(" ", "+")
    url = (
        "https://api.themoviedb.org/3/search/movie?include_adult=false&language="
        + lang
        + "&page=1&query="
        + title
    )

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        print(f"find_movie for", title, "response: ", data)

        if "results" in str(data) and len(data["results"]) > 0:
            print(f"movie found!")
            movie = get_movie_form_search(data["results"], title)
            movie = get_detail_moviedata(get_movie_id(movie))
            movie = json.loads(movie)
            return movie

    return None


def get_movie_id(movie):
    # print(f"get_movie_id for ", movie)
    if movie:
        return movie["id"]


def get_watch_providers(id):
    # print(id)
    url = "https://api.themoviedb.org/3/movie/" + str(id) + "/watch/providers"
    response = requests.get(url, headers=headers)
    return response.text


def get_detail_moviedata(id):
    url = "https://api.themoviedb.org/3/movie/" + str(id) + "?language=en-US"
    response = requests.get(url, headers=headers)
    return response.text


def filter_watch_providers(data, lang):
    # Filter data under "<lang>"
    data = json.loads(data)
    if lang in data["results"]:
        filtered_data = data["results"][lang]
        # Print the filtered JSON
        return filtered_data


def get_watch_providers_via_subtype(data, subtype):
    # subtype = "bye", "rent", "flatrate"

    provider_names = []
    if subtype in str(data):
        filtered_data = data[subtype]
        if len(filtered_data) > 0:
            provider_names = [item["provider_name"] for item in filtered_data]

    return provider_names


def create_movie_data(title):
    movie = find_movie(title, "de-DE")
    if movie and "id" in movie:
        id = get_movie_id(movie)
        providers = get_watch_providers(id)
        flatproviders = get_watch_providers_via_subtype(
            filter_watch_providers(providers, "DE"), "flatrate"
        )
        rentproviders = get_watch_providers_via_subtype(
            filter_watch_providers(providers, "DE"), "rent"
        )
        buyproviders = get_watch_providers_via_subtype(
            filter_watch_providers(providers, "DE"), "buy"
        )
        genres = [x["name"] for x in movie["genres"]]
        prodcountries = [x["name"] for x in movie["production_countries"]]
        filtered_data = {
            "title": movie["title"],
            "flatproviders": flatproviders,
            "rentproviders": rentproviders,
            "buyproviders": buyproviders,
            "adult": movie["adult"],
            "genres": genres,
            "budget": movie["budget"],
            "overview": movie["overview"],
            "popularity": movie["popularity"],
            "poster_path": movie["poster_path"],
            "release_date": movie["release_date"],
            "runtime": movie["runtime"],
            "revenue": movie["revenue"],
            "vote_average": movie["vote_average"],
            "vote_count": movie["vote_count"],
            "production_countries": prodcountries,
        }
        return filtered_data


def create_basic_movie_data(title):
    movie = find_movie_basic(title, "de-DE")
    if movie and "id" in movie:
        id = get_movie_id(movie)
        providers = get_watch_providers(id)
        flatproviders = get_watch_providers_via_subtype(
            filter_watch_providers(providers, "DE"), "flatrate"
        )
        rentproviders = get_watch_providers_via_subtype(
            filter_watch_providers(providers, "DE"), "rent"
        )
        buyproviders = get_watch_providers_via_subtype(
            filter_watch_providers(providers, "DE"), "buy"
        )

        filtered_data = {
            "title": movie["title"],
            "flatproviders": flatproviders,
            "rentproviders": rentproviders,
            "overview": movie["overview"],
            "release_date": movie["release_date"],
            "id": id,
        }
        return filtered_data


def create_recommendation_data(item):
    ## just importent info
    filtered_data = {
        "title": item["title"],
        "flatproviders": item["flatproviders"],
        "rentproviders": item["rentproviders"],
        "buyproviders": item["buyproviders"],
    }
    ##filter only movies that are for streaming or rent available
    item = filtered_data

    if "flatproviders" in item and len(item["flatproviders"]) > 0:
        if "rentproviders" in item and len(item["rentproviders"]) > 0:
            return {
                "title": item["title"],
                "flatproviders": item["flatproviders"],
                "rentproviders": item["rentproviders"],
            }
        else:
            return {"title": item["title"], "flatproviders": item["flatproviders"]}
    elif "rentproviders" in item and len(item["rentproviders"]) > 0:
        return {"title": item["title"], "rentproviders": item["rentproviders"]}


def get_movie_form_search(data: dict, search: str):
    try:
        titles = [x["title"] for x in data]
        title = closeMatches(titles, search)
        title = title[0]
        movie = [x for x in data if x["title"] == title]
        return movie[0]
    except:
        return None


# Function to find all close matches of
# input string in given list of possible strings
def closeMatches(patterns, word):
    return get_close_matches(word, patterns)


def create_data_list(fulldata):
    movieinfoasstring = ""
    for movie_info in fulldata:
        formatted_info = f"Title: {movie_info['title']}, "
        formatted_info += f"Overview: {movie_info['overview']}, "
        formatted_info += f"flatproviders: {', '.join(movie_info['flatproviders'])}, "
        formatted_info += f"rentproviders: {', '.join(movie_info['rentproviders'])}\n"
        movieinfoasstring += formatted_info
    return movieinfoasstring


def filter_movies(movies: dict, providers: list[str]):
    filtered_list = movies
    if providers and len(providers) > 0:
        filtered_list = [
            d
            for d in movies
            if (
                "flatproviders" in d
                and any(val in d["flatproviders"] for val in providers)
            )
            or (
                "rentproviders" in d
                and any(val in d["rentproviders"] for val in providers)
            )
        ]
        for movie in filtered_list:
            flatproviders = []
            rentproviders = []
            for provider in providers:
                if provider in movie["flatproviders"]:
                    flatproviders.append(provider)
                if provider in movie["rentproviders"]:
                    rentproviders.append(provider)
            movie["rentproviders"] = rentproviders
            movie["flatproviders"] = flatproviders

    return filtered_list
