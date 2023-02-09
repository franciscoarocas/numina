
from numina.dal.customdaliface import CustomDALIface

import logging

logger = logging.getLogger(__name__)

class MyDal(CustomDALIface):

	def __init__(self, *args, **kwargs):
		
		super().__init__(*args, **kwargs)