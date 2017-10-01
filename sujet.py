import pymysql
import auteur as m_auteur
from pony.orm import *
import datetime


def default():
	return {
		"created_at" : datetime.datetime.now(),
		"updated_at" : datetime.datetime.now(),
		"parcoured" : 0,
		"url" : "",
		"title" : "inconnu",
		"auteur" : "inconnu",
		"nb_reponses" : 0,
		"initialised_at" : datetime.datetime.now()
	}


def get(db, id):
	with db_session:
		sujet = db.Sujet[id]
		return sujet


def getByUrl(db, url):
	try:
		with db_session:
			sujet = db.Sujet.get(url = url)
			return sujet
	except Exception as e:
		print("sujet>getByUrl", e)
		return None


def add(db, candidat):
	try:
		auteur = m_auteur.getByPseudo(db, candidat["auteur"])
		
		if auteur == None :
			auteur = m_auteur.addOnlyPseudo(db, candidat["auteur"])

		if auteur == None :
			return (False, "Echec lors de l'insertion du pseudo - " + candidat["auteur"])

		if getByUrl(db, candidat["url"]) != None :
			return (False, "Le sujet (" + candidat["url"] + ") existe déja !")

		val = default()
		val["url"] = candidat["url"]
		val["initialised_at"] = candidat["date"]
		val["nb_reponses"] = candidat["nbReponse"]
		val["auteur"] = auteur.id
		
		with db_session:
			return (db.Sujet(**val), "le sujet a bien été ajouter")
	except Exception as e:
		print("sujet>add", e)
		return (False, "Erreur Critique")


def addMultiple(db, candidats):
	bilan = {
		"nbAjouter": 0, 
		"nbNonAjouter": 0,
		"notificationOk": [],
		"notificationError": []
	}
	
	for candidat in candidats:
		resultat = add(db, candidat)
		if resultat[0] == False :
			bilan["nbNonAjouter"] += 1
			bilan["notificationError"].append(resultat[1])
		else:
			bilan["nbAjouter"] += 1
			bilan["notificationOk"].append(resultat[1])

	return bilan