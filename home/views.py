from pickle import FALSE
import string
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.font_manager import json_load
from . import views
from django.views.decorators.csrf import csrf_protect
import pandas as pd
import random,json,ast
genre = [
    'Action',
'Comedy',
'Drama',
'Fantasy',
'Horror',
'Mystery',
'Romance',
'Thriller',
'Family',
'Crime',
'Animation'
]
years = list(range(1900,2018))

def randomizer(by,len,mvs):
    ind = []
    if by == 'Random':
        k=1
        while(k<5):
            n = random.randint(1,len-2)
            if n in ind:
                k = k
            else:
                ind.append(n)
                k=k+1
        return ind
    elif by in genre:
        k=1
        while(k<5):
            n = random.randint(1,len-2)
            if n in ind or (by in genre_sep(ast.literal_eval(mvs['genres'][n])))==False:
                k = k
            else:
                ind.append(n)
                k=k+1
        return ind
    else:
        k=1
        while(k<5):
            n = random.randint(1,len-2)
            if n in ind or (by == str(mvs['release_date'][n]).split('-')[0])==False:
                k = k
            else:
                ind.append(n)
                k=k+1
        return ind

def genre_sep(g):
    genre = []
    for x in g:
        genre.append(x['name'])
    return ' '.join(genre)

def fetchMovies(by):
    movie_set={}
    
    mvs = pd.read_csv('movies_metadata.csv',low_memory=False)
    nn = 1
    for x in randomizer(by,len(mvs['title']),mvs):
        movie_set['mv'+str(nn)]={
            'ti':mvs['title'][x],
            'ov':mvs['overview'][x],
            'ge':genre_sep(ast.literal_eval(mvs['genres'][x])),
            'yr':str(mvs['release_date'][x]).split('-')[0],
            'ra':mvs['vote_average'][x],
            'la':mvs['original_language'][x]
        }
        nn = nn+1
    return(movie_set)

def home(req):
    if req.method == 'POST':
        if req.POST.get('byGenre')!='--no--':
            return render(req,'home/index.html',fetchMovies(req.POST.get('byGenre')))
        elif req.POST.get('byYear')!='--no--':
            return render(req,'home/index.html',fetchMovies(req.POST.get('byYear')))
        else:
            return render(req,'home/index.html',fetchMovies('Random'))    
    else:
        return render(req,'home/index.html',fetchMovies('Random'))
            

    

