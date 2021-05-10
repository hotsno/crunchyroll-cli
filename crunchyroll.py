import requests
import json
import os

printSpacing = "\n-----------------------------------\n"

def anilistCall(query, variables):
    url = 'https://graphql.anilist.co'
    response = requests.post(
        url, json={'query': query, 'variables': variables})
    return response.json()


def numberChoice():
    choice = input("Enter number: ")
    print(printSpacing)
    return choice


def animeSearch():
    variables = {}
    print(printSpacing)
    searchTerm = input("Search for an anime: ")
    variables["search"] = searchTerm
    query = '''
    query ($search: String) {
      Page(page: 1, perPage: 10) {
        media(search: $search, type: ANIME) {
          title {
            romaji
            english
            native
          }
          streamingEpisodes {
            url
            title
          }
        }
      }
    }
    '''
    results = anilistCall(query, variables)
    print(printSpacing)
    print("SEARCH RESULTS:")
    i = 1
    for anime in results["data"]["Page"]["media"]:
        print(str(i) + ": " + anime["title"]["romaji"])
        i += 1
    print(printSpacing)
    return results


def listEpisodes(searchResults, animeChoice):
    i = 1
    print("AVAILABLE EPISODES:")
    streamingEpisodes = searchResults["data"]["Page"]["media"][int(animeChoice) - 1]["streamingEpisodes"][::-1] # the [::1] reverses the list
    for episode in streamingEpisodes:
        print(str(i) + ": " + episode["title"])
        i += 1
    print(printSpacing)
    return streamingEpisodes


def playEpisode(streamingEpisodes, episodeChoice):
    
    os.system("mpv --slang=enUS --no-terminal " + streamingEpisodes[int(episodeChoice) - 1]["url"])


searchResults = animeSearch()
animeChoice = numberChoice()
streamingEpisodes = listEpisodes(searchResults, animeChoice)
episodeChoice = numberChoice()
playEpisode(streamingEpisodes, episodeChoice)

continueChoosing = True
while(continueChoosing):
  print("Type \"q\" to quit\n")
  episodeChoice = numberChoice()
  if(episodeChoice != "q"):
    playEpisode(searchResults, animeChoice, episodeChoice)
  else:
    continueChoosing = False
    print("See you next time! o/")
