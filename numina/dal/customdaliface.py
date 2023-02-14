
from numina.core.oresult import ObservingBlock, ObservationResult
from numina.types.product import DataProductMixin

from .dictdal import BaseHybridDAL

from abc import ABC, abstractmethod

from typing import Union

class CustomDALIface(ABC, BaseHybridDAL):


    def __init__(self, *args, **kwargs) -> None:

        controlYaml = args[2]

        if 'programID' not in controlYaml or 'obsBlock' not in controlYaml:
            raise KeyError("ProgramID and obsBlock keys must be in the control.yaml file")
        
        self.programID : str = controlYaml['programID']
        self.obsBlock : str = controlYaml['obsBlock']
        
        self.products : dict = dict()

        newArgs = list(args)
        newArgs[1] = {} # Change second parameter [] to {}
        newArgs = tuple(newArgs)

        super(CustomDALIface, self).__init__(*newArgs, **kwargs)


    @abstractmethod
    def oblock_from_id(self, obsid : Union[str, int]) -> ObservingBlock:
        """
            Called to generate the recipe Input observation block images
        """
        pass


    @abstractmethod    
    def update_result(self, task, serialized, filename : str) -> None:
        """
            Called when finish the recipe
            serialized params contents the same data as the result.json file
        """
        pass


    @abstractmethod
    def search_parameter(self, name : str, tipo, obsres : ObservationResult, options : dict = None):
        """
            Called for each "Requeriment" in each recipe
            'obresult' is for each ObservationResultType requeriment
        """
        pass


    @abstractmethod
    def search_product(self, name : str, tipo : DataProductMixin, obsres : ObservationResult, options : dict = None):
        """
            A result can be a MasterBias, MasterFlat, etc.
            The products are required into the recipes using the "Requeriment()" function
            Products usually are stored in self.products. If not, you need to find it 
        """
        pass