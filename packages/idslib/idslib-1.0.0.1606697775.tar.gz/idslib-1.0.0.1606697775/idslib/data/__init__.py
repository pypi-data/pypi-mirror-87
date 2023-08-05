#!/usr/bin/env python3

import requests
import uuid

class DataBackend():

def __init__(self, repository_url, repository_key):
	
	self.repository = repository_url
	self.key = repository_key

	def upload_file(local_filename):
		
		url = self.repository + "upload"
		
		h = {'Authorization': self.key}
		
		f = {'file': open(local_filename, 'rb')}
		
		r = requests.post(url, files=f, headers=h)
		
		if not r.status_code == 200:
			print("Error uploading file!")
			return None
		else:
			
			return r.json()['data']['id']


	def download_file(url, local_filename):
		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk)
		return local_filename
