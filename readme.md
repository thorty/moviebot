# Movie Bot prototyp

Should help find movies in a conversational way.
Output Movie Recommendation and info howto stream.

## Steps

- [X] Get Movie Recommendations via LLM and userinput
- [X]  Use LLM function call to get the titles 
- [X]  search movies via TMDB Api and find streaming provider **AND AALL OTHER MOVIE_INFO DATA (PLAYTIME; ACTORS; GENRES)**
- [X]  write recommendation to chat output with context form 3

### Bonus Tasks
- [ ] find newer once via tmdb api and recommendet titles
- [X] if user asks further questions answer based on api call
- [ ] if user asks for new recros do this! - do not recro same movies in one session
- [X] build website with chat interface
- [ ] build website with images and direct links
- [ ] test with other cheaper llms
- [ ] filter for providers and pref to rent / flatrate
- [ ] filter this by user input
- [ ] use block/watch list / streaming source and so on
( - [ ] inputfield for api key)

### Todos

- [X] script jupyter norebook for proof of concept
- [X] use env variables for api keys 
- [X] build streamit site
- [ ] Use function calling for getting movie titles
- [ ] Multilingual


## Streamlit app

### Env Variables

need to set the following variables

tmndb_bearer
openai_api_key


</br> </br> </br> </br> </br> 




# Links

## tmdb ressources

#### Details
https://developer.themoviedb.org/reference/movie-details

#### Credits
https://developer.themoviedb.org/reference/movie-credits

### similar movies (for later use on algorithm side)
https://api.themoviedb.org/3/movie/{movie_id}/similar


# Idea

stick everything together with
https://python.langchain.com/docs/expression_language/how_to/routing


## streamlit

## general
https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps#introduction

## secure the app

https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/