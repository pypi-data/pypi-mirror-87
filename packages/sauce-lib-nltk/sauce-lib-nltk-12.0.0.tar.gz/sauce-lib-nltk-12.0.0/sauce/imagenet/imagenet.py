import requests
import os
import sys
import re
from rdflib import Namespace
from nltk.corpus import wordnet as wn
from rdflib import Graph, plugin
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from nltk.tokenize import TreebankWordTokenizer
from rdflib import URIRef, BNode, Literal
from os import path


class ImagenetGenerator():

	IMAGENET_FILE_PATH = "/home/williamgreenly/dev/data/sauce/imagenet" if os.getenv('IMAGENET_FILE_PATH') is None else os.getenv('IMAGENET_FILE_PATH')
	SYNSET_IDS = "http://www.image-net.org/api/text/imagenet.synset.obtain_synset_list"
	SYNSET_BASE = "http://www.image-net.org/api/text/imagenet.synset.geturls?wnid="
	MIMES = ["image/png", "image/jpg", "image/jpeg", "image/gif"]

	def __init__(self, base_file_path, synset_ids, synset_base, offset=0, limit=0, maximum=0):
		self.base_file_path = base_file_path
		self.raw_file_path = base_file_path + "/raw"
		self.cleansed_file_path = base_file_path + "/cleansed"
		self.output_file_path = base_file_path + "/output"
		self.synset_ids = synset_ids
		self.synset_base = synset_base
		self.offset = offset
		self.limit = limit
		self.maximum = maximum
		self.prepare_directories()

	def generate(self):
		print("extracting")
		self.extract()
		print("cleansing")
		self.cleanse_synsets(self.maximum)

	def prepare_directories(self):
		print("preparing directories")
		self.ensure_dir(self.base_file_path)
		self.ensure_dir(self.raw_file_path)
		self.ensure_dir(self.cleansed_file_path)
		self.ensure_dir(self.output_file_path)
		self.ensure_dir(self.output_file_path + "/ttl")
		self.ensure_dir(self.output_file_path + "/json")

	def ensure_dir(self, file_path):
		if not os.path.exists(file_path):
			os.makedirs(file_path)

	def downloadUrl(self, wnid):
		print("trying to extract " + self.synset_base + wnid)

		return re.sub('\n','', self.synset_base + wnid)

	def extract(self):
		self.extract_synset_list()
		self.extract_synsets()


	def extract_synset_list(self):
		resp = requests.get(self.synset_ids)
		f = open(self.base_file_path + "/synsets.txt", "w")
		f.write(resp.text)
		f.close()
		return resp.text.splitlines()

	def extract_synsets(self):
		f = open(self.base_file_path + "/synsets.txt")
		lines = f.readlines()
		count = 1
		res = []
		for line in lines:
			if ((self.limit == 0) or (count <= self.limit )) and self.offset <= count:
				print("found " + line)
				resp = requests.get(self.downloadUrl(line))
				print(resp.text)
				f = open(self.raw_file_path + "/" + re.sub('[^a-zA-Z0-9]','',line) + ".urls", "w") 
				f.write(resp.text)
				f.close()
				res.append(line)
				count = count + 1
		f.close()
		return res

	def get_id(self, path):
		fn = path.split('/')[-1]
		return fn.split('.')[0]

	def cleanse_synset(self, synset, maximum=0):
		valid_urls = []
		f = open(synset)
		lines = f.readlines()
		try:
			os.remove(self.cleansed_file_path + "/" + self.get_id(synset) + ".urls")
		except Exception:
			print("no file")
		target_file = open(self.cleansed_file_path + "/" + self.get_id(synset) + ".urls", "w+")
		count = 0
		for line in lines:
			if maximum != 0 and count >= maximum:
				break
			else:
				id = line.replace("\n","")
				try:
					r = requests.head(id, timeout=1)
					print(r.headers['content-type'])
					if str(r.status_code)[:2] == "20" and r.headers['content-type'] in ImagenetGenerator.MIMES:
						print("success for " + id)
						valid_urls.append(id)
						#target_file = open(self.cleansed_file_path + "/" + self.get_id(synset) + ".urls", "a+")
						target_file.write(id + "\n")
						print("appended " + id)
						count += 1
					else:
						print("failure for " + id)
				except Exception as error:
					print("failure for " + id) 

		target_file.close()
		f.close()
		return valid_urls

	def cleanse_synsets(self, maximum=0):
		f = open(self.base_file_path + "/synsets.txt")
		synsets = f.readlines()
		for synset in synsets:
			filename = self.raw_file_path + "/" + re.sub('[^a-zA-Z0-9]','',synset) + ".urls"
			print("checking for file " + filename)
			if path.exists(filename):
				print("cleansing " + filename)
				self.cleanse_synset(filename, maximum)
		f.close()

	def get_labels_from_wnid(self, wnid):
		wn.synset_from_pos_and_offset('n',re.sub('[^0-9]','', wnid))