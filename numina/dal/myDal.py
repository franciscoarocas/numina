
from numina.core.oresult import oblock_from_dict

from numina.dal.customdaliface import CustomDALIface

import logging

logger = logging.getLogger(__name__)


class MyDal(CustomDALIface):


	def __init__(self, *args, **kwargs):
		
		super().__init__(*args, **kwargs)



	def oblock_from_id(self, obsid):

		self.ob_table[obsid]['images'] = [
			"0002649906-20200831-OSIRIS-OsirisBroadBandImage.fits.gz",
			"0002649921-20200831-OSIRIS-OsirisBroadBandImage.fits.gz",
			"0002649922-20200831-OSIRIS-OsirisBroadBandImage.fits.gz"
		] # CHIVATO

		este = self.ob_table[obsid]
		oblock = oblock_from_dict(este)

		return oblock


	def update_result(self, task, serialized, filename):
		pass


	def search_parameter(self, name, tipo, obsres, options=None):
		pass