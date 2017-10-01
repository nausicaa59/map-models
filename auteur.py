import pymysql
import datetime
import json
import time
from pony.orm import *


def default():
	return {
		"created_at" : datetime.datetime.now(),
		"updated_at" : datetime.datetime.now(),
		"pseudo" : "",
		"cheked_profil" : 0,
		"pays" : "France",
		"nb_messages" : 0,
		"img_lien" : "http://image.jeuxvideo.com/avatar-sm/default.jpg",
		"nb_relation" : 0,
		"banni" : 0,
		"date_inscription" : datetime.datetime.now(),
		"coord_X" : 0,
		"coord_Y" : 0,	
	}

def get(db, id):
	with db_session:
		auteur = db.Auteur[id]
		return auteur


def getFull(db, id):
	with db_session:
		auteur = get(db, id)
		sujets = [s.to_dict_prepara() for s in auteur.sujets]
		result = auteur.to_dict_prepara()
		result["sujets"] = sujets
		return result


def gets(db, nb = 10):
	with db_session:
		tab = select(p for p in db.Auteur)[:nb]
		return tab


def getByPseudo(db, pseudo):
	try:
		with db_session:
			auteur = db.Auteur.get(pseudo = pseudo)
			return auteur
	except Exception as e:
		print("auteur>getByPseudo", e)
		return None


def getUntreated(db):
	try:
		with db_session:
			auteur = db.Auteur.select_by_sql('SELECT * FROM auteurs a WHERE a.cheked_profil = 0 ORDER BY RAND() LIMIT 0,1')
			return auteur
	except Exception as e:
		print("auteur>getUntreated", e)
		return None


def multipleLikeFirst(letters):
	isFirst = True
	conditions = "a.cheked_profil = 0 AND ("
	for x in letters:
		conditions += "" if isFirst else " OR "
		conditions += "pseudo LIKE '" + x + "%'"
		isFirst = False
	conditions += ")"
	return conditions	


def getUntreatedByLetters(db, letters):
	try:
		with db_session:
			conditions = multipleLikeFirst(letters)
			print(conditions)
			auteurs = db.Auteur.select_by_sql('SELECT * FROM auteurs a WHERE ' + conditions)
			return auteurs
	except Exception as e:
		print("auteur>getUntreated", e)
		return None


def addOnlyPseudo(db, pseudo):
	if getByPseudo(db, pseudo) != None:
		return False

	val = default()
	val["pseudo"] = pseudo

	try:
		with db_session:
			return db.Auteur(**val)
	except Exception as e:
		print("addOnlyPseudo", e)
		return False


def update(db, info):
	try:
		with db_session:
			auteur = getByPseudo(db, info["pseudo"])
			if auteur != None :
				auteur.img_lien = info["img_lien"]
				auteur.date_inscription = info["date_inscription"]
				auteur.nb_messages = info["nb_messages"]
				auteur.nb_relation = info["nb_relation"]
				auteur.banni = info["banni"]
				auteur.cheked_profil = 1
				auteur.updated_at = datetime.datetime.now()
				commit()
	except Exception as e:
		print("update", e)



def countAll(db):
	with db_session:
		return count(c for c in db.Auteur)