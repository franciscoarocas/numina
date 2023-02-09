

from numina.core.oresult import oblock_from_dict

from .dictdal import BaseHybridDAL


class CustomDALIface(BaseHybridDAL):


    def __init__(self, *args, **kwargs) -> None:
        
        newArgs = list(args)
        newArgs[1] = {} # Change second parameter [] to {}
        newArgs = tuple(newArgs)

        super().__init__(*newArgs, **kwargs)



    def oblock_from_id(self, obsid):

        self.ob_table[obsid]['images'] = [
            "0002649906-20200831-OSIRIS-OsirisBroadBandImage.fits.gz",
            "0002649921-20200831-OSIRIS-OsirisBroadBandImage.fits.gz",
            "0002649922-20200831-OSIRIS-OsirisBroadBandImage.fits.gz"
        ] # CHIVATO

        este = self.ob_table[obsid]
        oblock = oblock_from_dict(este)
        
        return oblock
    

    def obsres_from_oblock_id(self, obsid, as_mode=None, configuration=None):
        """"
        Override instrument configuration if configuration is not None
        """

        oblock = self.oblock_from_id(obsid)

        return self.obsres_from_oblock(oblock, as_mode)
