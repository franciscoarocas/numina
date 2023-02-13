

from .dictdal import BaseHybridDAL

from abc import ABC, abstractmethod

class CustomDALIface(ABC, BaseHybridDAL):


    def __init__(self, *args, **kwargs) -> None:
        
        newArgs = list(args)
        newArgs[1] = {} # Change second parameter [] to {}
        newArgs = tuple(newArgs)

        super(CustomDALIface, self).__init__(*newArgs, **kwargs)


    @abstractmethod
    def oblock_from_id(self, obsid):
        """
            Called to generate the recipe Input
        """
        pass


    @abstractmethod    
    def update_result(self, task, serialized, filename):
        """
            Called when finish the recipe
            serialized params contents the same data as the result.json file
        """
        pass


    @abstractmethod
    def search_parameter(self, name, tipo, obsres, options=None):
        """
            Called for each "Requeriment" in each recipe
            'obresult' is for each ObservationResultType requeriment
        """
        pass