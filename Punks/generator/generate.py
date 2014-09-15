# -*- coding: utf-8 -*-
from home.models import UserProfile
from article.models import Article
from django.db import models
from django.contrib.auth.models import User
import re
from random import randint
from django.db import IntegrityError
from gallery.models import Category, Artwork
import sys

usersRead = open("generator/users.txt", "r+")
sentencesRead = open("generator/sentences.txt", "r+")
profilePicRead = open("generator/profile_pictures.txt", "r+")
titlesRead = open("generator/titles.txt", "r+")
articleUrlRead = open("generator/article_urls.txt", "r+")
coverUrlRead = open("generator/covers.txt", "r+")
categoryRead = open("generator/categories.txt", "r+")

# list of the file container
names = usersRead.read().split("\n");
profilePic = profilePicRead.read().split("\n")
sentences = re.findall(r"\s+[^.!?]*[.!?]", sentencesRead.read())
titles = titlesRead.read().split("\n")
articleUrl = articleUrlRead.read().split("\n")
coverUrl = coverUrlRead.read().split("\n")
categoriesTitle = categoryRead.read().split("\n")

# their respective length
namesLen = len(names)-1
profilePicLen = len(profilePic)-1
sentenceLen = len(sentences)-1
titlesLen = len(titles)-1
articleUrlLen = len(articleUrl)-1
coverUrlLen = len(coverUrl)-1
categoriesTitleLen = len(categoriesTitle)-1

# delete previous crap
UserProfile.objects.all().delete()
# User.objects.all().delete().exclude(username=root)

names = ["Bryant","Burgess","Burns","Butler","Cannon","Carla","Carlson","Carlton","Carr","Carson","Carter","Casey","Cassandra","Castillo","Catherine","Cecil","Cecilia","cgee","Chambers","Chris","Christine","Christopher","Clarence","Clark","Clay","Collins","Conrad","Constance","Cook","Cooper","Craig","Cross","Cummings","Curry","Cynthia","Daisy","Dana","Danny","Darnell","Davis","Delgado","Delia","Derek","Dianna","Dianne","Domingo","Dominick","Doris","Dorothy","Douglas","Doyle","Duncan","Earl","Edwards","eed","eid","Ella","Eloise","Elsa","Elvira","Emmett","ena","Eric","Erica","Erick","Estelle","Estrada","Eula","Eunice","Eva","Evan","Evelyn","ewman","ewton","eyes","Fannie","Faye","Ferguson","Fernando","Figueroa","Flores","Fowler","Fox","Francis","Franklin","Freda","Fredrick","Freeman","French","Fuller","Garrett","Geoffrey","Gerardo","Gibson","Gilbert","Gill","Glen","Glenn","Gonzalez","Gordon","Graham","Grant","Green","Greene","Gregg","Guadalupe","Guy","Hale","Hall","Hampton","Hannah","Hardy",]
for i in range(6):
    seed = randint(0,50)

    user = User(username= (names[i]))
    user.set_password(names[seed%namesLen])
    user.save()

    userProfile = UserProfile()
    userProfile.user = user
    userProfile.firstname = (names[i])
    userProfile.lastname = (names[i+1])
    userProfile.email = (names[seed%namesLen]) +"@punk.com"
    userProfile.image = (profilePic[seed%profilePicLen])
    userProfile.coverPhoto = (coverUrl[seed%coverUrlLen])
    userProfile.description = (titles[seed%titlesLen])
    userProfile.key_skills = (titles[seed%titlesLen])
    userProfile.description = sentences[seed%sentenceLen]
    userProfile.save()

    for i in range(5):
      theCategory = Category()
      theCategory.title = categoriesTitle[(seed+i)%categoriesTitleLen]
      theCategory.owner = userProfile
      theCategory.thumbnail = profilePic[(seed+i)%profilePicLen]
      theCategory.save()

      for z in range(10):
        theArtwork = Artwork()
        theArtwork.title = titles[(seed+z)%titlesLen]
        theArtwork.url_path = articleUrl[(seed+z)%articleUrlLen]
        theArtwork.category = theCategory
        theArtwork.owner = userProfile
        theArtwork.save()

    for i in range(20):

      articleseed = randint(0,1000)
      article = Article()
      article.title = (titles[articleseed%titlesLen])
      article.body=sentences[articleseed%sentenceLen]
      if (i % 2) == 0:
        article.is_project=True
      else:
        article.is_project=False
      article.image = articleUrl[articleseed%articleUrlLen]
      article.owner = userProfile
      article.save()

      theCategory = Category()



    

sentencesRead.close()
usersRead.close()
profilePicRead.close()
titlesRead.close()
articleUrlRead.close()



