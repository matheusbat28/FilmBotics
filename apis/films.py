from decouple import config
import requests
import json

def searchFilms(name_film):
    reponse = requests.get(f'https://www.omdbapi.com/?s={name_film}&apikey={config("TOKEN_FILM")}')
    return reponse.json()

def searchId(id):
    reponse = requests.get(f'https://www.omdbapi.com/?i={id}&apikey={config("TOKEN_FILM")}')
    return reponse.json()   