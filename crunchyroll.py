import requests
import json
import os

# Here we define our query as a multi-line string
query = '''
query ($search: String) { # Define which variables will be used in the query (id)
  Page(page: 1, perPage: 10) {
    media(search: $search, type: ANIME) {
      id
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

variables = {
}

url = 'https://graphql.anilist.co'

print("\n-----------------------------------\n")
search = input("Search for an anime: ")
variables["search"] = search
print("\n-----------------------------------\n")

# Make the HTTP Api request
response = requests.post(url, json={'query': query, 'variables': variables})

print("SEARCH RESULTS:")
i = 1
for anime in response.json()["data"]["Page"]["media"]:
  print(str(i) + ": " + anime["title"]["romaji"])
  i += 1

print("\n-----------------------------------\n")
animeChoice = input("Enter number: ")
print("\n-----------------------------------\n")

i = 1
print("AVAILABLE EPISODES:")
for episode in response.json()["data"]["Page"]["media"][int(animeChoice) - 1]["streamingEpisodes"]:
  print(str(i) + ": " + episode["title"])
  i += 1

print("\n-----------------------------------\n")
episodeChoice = input("Enter number: ")
print("\n-----------------------------------\n")
print("Please wait... (10-15 secs)")

os.system("mpv --slang=enUS " + response.json()["data"]["Page"]["media"][int(animeChoice) - 1]["streamingEpisodes"][int(episodeChoice) - 1]["url"])