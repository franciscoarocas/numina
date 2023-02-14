
from numina.core.oresult import oblock_from_dict
from numina.dal import StoredParameter, StoredProduct

from numina.dal.customdaliface import CustomDALIface

import logging

import requests

logger = logging.getLogger(__name__)


class GTC_API(CustomDALIface):


	def __init__(self, *args, **kwargs):
		
		super().__init__(*args, **kwargs)

		self.__host = "http://localhost:8080/"



	def __query(self, path, type = "GET", body = None):
		
		fullPath = self.__host + path

		try:

			result = None

			if type == "GET":

				result = requests.get(fullPath)

			elif type == "POST":

				result = requests.post(fullPath, json = body)

				if result.status_code != 200:

					result.raise_for_status()

			return result.json()

		except Exception as e:
			
			raise e



	def oblock_from_id(self, obsid):

		query = {
					"criterias":[
						{
							"type":"programidcriteria",
							"programID": self.programID
						},
						{
							"type":"observationblockidcriteria",
							"observationBlockID": self.obsBlock
						},
						{
							"type": "operatorcriteria",
							"operator": "AND"
						}
					]
				}
		
		data = self.__query("scidb/rest/frames/paths", "POST", query)

		# LA SIGUIENTE LÍNEA ES DE FORMA TEMPORAL HASTA QUE JOSUÉ ARREGLE EL BUG
		parsed = [("/").join(url.split("/")[:-1]) for url in data]

		self.ob_table[obsid]['images'] = parsed

		este = self.ob_table[obsid]
		oblock = oblock_from_dict(este)

		return oblock


	def update_result(self, task, serialized, filename):
		# Aquí actualizamos los valores de la base de datos
		pass


	def search_parameter(self, name, tipo, obsres, options=None):
		
		if name == 'obresult':
			return StoredParameter(obsres)
		

	def search_product(self, name, tipo, obsres, options):

		if name in self.products:
			return StoredProduct(id=0, tags={}, content=self.products[name])
		
		# Buscarlo en la API