from django.shortcuts import render
from django.http import HttpResponse
from json import dumps
# Create your views here.

def index(request):
    return render(request, 'index.html')

def suggested_movies(request):
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
        rating = []
        listMovie= sorted(listMovie, key = lambda movieName: (get_movie_rating(get_movie_data(movieName)), movieName), reverse=True)
        for item in listMovie:
            result = get_movie_data(item)
            rating.append(result["Ratings"])
        return listMovie, rating


    if request.method == 'POST':
        movies_list = request.POST.get('movies')
        movies_limit = request.POST.get('movie_limit')
    list_of_movies = movies_list.split()
    limits_of_suggestion = movies_limit

    for movies in list_of_movies:
        m = movies
        if "-" in movies:
            movies = movies.replace("-", " ")
            list_of_movies[list_of_movies.index(m)] = movies

    movie_list, movie_rating = get_sorted_recommendations(list_of_movies, movies_limit)
    rating_list = []
    lst=[]
    for item2 in movie_rating:
        for item3 in item2:
            if item3["Source"] == "Rotten Tomatoes":
                rating_list.append(item3["Value"])
    for item, rat in zip(movie_list, rating_list):
        movie_dic = {}
        movie_dic["Name"] = item
        movie_dic["Count"] = rat[:-1]
        lst.append(movie_dic)
    
    data_set = dumps(lst)

        # print(request.POST.get('movies'))
    return render(request, 'final.html', {"Children":data_set})