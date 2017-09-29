import pymysql
import datetime
import json
import time
from pony.orm import *


def cleanDate(date):
	return date.strftime('%Y-%m-%d %H-%M-%S') if date is not None else ""


def prepareDb():
	db = Database()


	class Auteur(db.Entity):
		_table_ 			= "auteurs"
		id					= PrimaryKey(int, auto=True)
		created_at 			= Required(datetime.datetime, 6)		
		updated_at 			= Required(datetime.datetime, 6)
		pseudo				= Required(str)
		cheked_profil		= Required(int)
		pays 				= Required(str)
		nb_messages			= Required(int)
		img_lien			= Required(str)
		nb_relation			= Required(int)
		banni				= Required(int)
		date_inscription	= Required(datetime.datetime, 6)
		coord_X				= Required(float)
		coord_Y				= Required(float)
		sujets 				= Set('Sujet', reverse="auteur")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["created_at"] 			= ""
			base["updated_at"] 			= ""
			base["date_inscription"] 	= ""
			return base



	class Sujet(db.Entity):
		_table_ 			= "sujets"
		id					= PrimaryKey(int, auto=True)
		created_at 			= Required(datetime.datetime, 6)		
		updated_at 			= Required(datetime.datetime, 6)
		parcoured			= Required(int)
		url 				= Required(str)
		title				= Required(str)
		auteur				= Required(Auteur, reverse="sujets")
		nb_reponses			= Required(int)
		initialised_at		= Required(datetime.datetime, 6)

		def to_dict_prepara(self):
			base = self.to_dict()
			base["created_at"] 		= ""
			base["updated_at"] 		= ""
			base["initialised_at"] 	= ""
			return base


	db.bind(provider='mysql', host='localhost', user='root', passwd='root', db='scrapping')
	db.generate_mapping(create_tables=False)
	return db

