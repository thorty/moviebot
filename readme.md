# Movie Bot prototyp

Should help find movies in a conversational way.
Output Movie Recommendation how to stream and answers questions about movies.

Currently useage of

OpenAI https://openai.com/
TMDB https://www.themoviedb.org/?language=de

examples:

![emaple 1](examples/example1.png)
![emaple 2](examples/example2.png)
![emaple 3](examples/example3.png)

## Steps

- [X] Get Movie Recommendations via LLM and userinput
- [X]  Use LLM function call to get the titles 
- [X]  search movies via TMDB Api and find streaming provider
- [X]  write recommendation to chat output with context from tmdb api

### Bonus Tasks
- [X] find newer once via tmdb api and recommendet titles
- [X] if user asks further questions answer based on api call
- [X] if user asks for new recros do this! - do not recro same movies in one session
- [X] build website with chat interface
- [ ] build website with images and direct links
- [ ] test with other cheaper llms
- [X] filter for providers
- [ ] filter for other preferences like rent or free streaming
- [ ] use block/watch list
- [ ] Use mood as input and find the movie. 
- [ ] inputfield for api key

### Todos

- [X] script jupyter norebook for proof of concept
- [X] use env variables for api keys 
- [X] build streamit site
- [X] Use function calling for getting movie titles
- [ ] Multilingual


## Streamlit app

### Env Variables

need to set the following variables

tmndb_bearer
openai_api_key


</br> </br> </br> </br> </br> 


