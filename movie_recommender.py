import requests

def get_movies_from_tastedive(movieName, limit):
    baseurl="https://tastedive.com/api/similar"
    params_d = {}
    params_d["q"]= movieName
    params_d["k"]= "327878-course3p-I4ZNBN4A"
    params_d["type"]= "movies"
    params_d["limit"] = limit
    resp = requests.get(baseurl, params=params_d)
    respDic = resp.json()
    return respDic 

def extract_movie_titles(movieName):
    result=[]
    for listRes in movieName['Similar']['Results']:
        result.append(listRes['Name'])
    return result

def get_related_titles(listMovieName, limit):
    if listMovieName != []:
        auxList=[]
        relatedList=[]
        for movieName in listMovieName:
            auxList = extract_movie_titles(get_movies_from_tastedive(movieName, limit))
            for movieNameAux in auxList:
                if movieNameAux not in relatedList:
                    relatedList.append(movieNameAux)
        
        return relatedList
    return listMovieName

def get_movie_data(movieName, key="546c6742"):
    baseurl= "http://www.omdbapi.com/"
    params_d = {}
    params_d["t"]= movieName
    params_d["apikey"]= key
    params_d["r"]= "json"
    resp = requests.get(baseurl, params=params_d)
    respDic = resp.json()
    return respDic

def get_movie_rating(movieNameJson):
    strRanting=""
    for typeRantingList in movieNameJson["Ratings"]:
        if typeRantingList["Source"]== "Rotten Tomatoes":
            strRanting = typeRantingList["Value"]
    if strRanting != "":
        ranting = int(strRanting[:-1])
    else: ranting = 0
    return ranting

def get_sorted_recommendations(listMovieTitle, limit):
    listMovie= get_related_titles(listMovieTitle, limit)
    listMovie= sorted(listMovie, key = lambda movieName: (get_movie_rating(get_movie_data(movieName)), movieName), reverse=True)
    
    return listMovie

list_of_movies = input("Enter a list of movies:").split()
limits_of_suggestion = input("Enter the limit of suggestion:")

for movies in list_of_movies:
    m = movies
    if "-" in movies:
        movies = movies.replace("-", " ")
        list_of_movies[list_of_movies.index(m)] = movies


for item in get_sorted_recommendations(list_of_movies, limits_of_suggestion):
    print(item)
