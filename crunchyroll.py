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
    for episode in searchResults["data"]["Page"]["media"][int(animeChoice) - 1]["streamingEpisodes"]:
        print(str(i) + ": " + episode["title"])
        i += 1
    print(printSpacing)


def playEpisode(searchResults, animeChoice, episodeChoice):
    print("Please wait... (5-10 secs)")
    os.system("mpv --slang=enUS " + searchResults["data"]["Page"]["media"][int(
        animeChoice) - 1]["streamingEpisodes"][int(episodeChoice) - 1]["url"])


searchResults = animeSearch()
animeChoice = numberChoice()
listEpisodes(searchResults, animeChoice)
episodeChoice = numberChoice()
playEpisode(searchResults, animeChoice, episodeChoice)
