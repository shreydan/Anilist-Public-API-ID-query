import requests
import json
import time

url = 'https://graphql.anilist.co'

anime_data = {}

def buildAnimeData(resjson):
    global anime_data
    anime_data['id'] = resjson['data']['Media']['idMal']
    anime_data['status'] = resjson['data']['Media']['status']
    anime_data['title_r'] = resjson['data']['Media']['title']['romaji']
    anime_data['description'] = resjson['data']['Media']['description']
    anime_data['nextEpTimeSec'] = resjson['data']['Media']['nextAiringEpisode']['timeUntilAiring']
    anime_data['nextEpTimeFormat'] = time.strftime("%d days %H hours %M mins %S seconds", time.gmtime(anime_data['nextEpTimeSec']))
    anime_data['nextEpNum'] = resjson['data']['Media']['nextAiringEpisode']['episode']
    anime_data['totalEps'] = resjson['data']['Media']['episodes']
    anime_data['episodesRemToWatch'] = anime_data['totalEps'] - anime_data['nextEpNum'] - 1
    anime_data['cover-large'] = resjson['data']['Media']['coverImage']['large']
    print(anime_data)


def getMoreInfo(id):
    mainQuery = '''
    query ($idMal: Int) {
    Media (idMal: $idMal, type: ANIME) {
        idMal
        status
        title {
        romaji
        }
        episodes
        nextAiringEpisode {
        timeUntilAiring
        episode
        }
        description
        coverImage {
        large
        }
    }
    }
    '''
    variables = {
    'idMal': id
    }

    

    response = requests.post(url, json={'query': mainQuery, 'variables': variables})
    resjson = response.json()
    if(response.status_code == 200):
        buildAnimeData(resjson)
        print(anime_data)
    elif(response.status_code == 404):
        print('invalid ID')
    else:
        print('error: ', response.status_code)



def checkStatus(id):


    query = '''
    query ($idMal: Int) {
    Media (idMal: $idMal, type: ANIME) {
        idMal
        status
        title {
        romaji
        }
    }
    }
    '''
    variables = {
    'idMal': id
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    resjson = response.json()
    if(response.status_code == 200):
        if resjson['data']['Media']['status'] == 'FINISHED':
            return (False, True, 200)
        else:
            return (True, True, 200) 
    elif(response.status_code == 404):
        return(False, False, 404)
    else:
        return(False, False, response.status_code)

    # return tuple: (activeFlag, validFlag, statusCode)


def anime():
    id = int(input('enter MyAnimeList ID >>> '))
    (activeFlag, validFlag, statusCode) = checkStatus(id)
    if activeFlag and validFlag:
        getMoreInfo(id)
    elif not activeFlag and validFlag:
        print('anime has finished airing')
    elif not activeFlag and not validFlag:
        print('Invalid ID or error', statusCode)

if __name__ == '__main__':
    anime()