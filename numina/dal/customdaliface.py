
from numina.core.oresult import ObservingBlock 

from .dictdal import BaseHybridDAL

from abc import ABC, abstractmethod

from typing import Union

class CustomDALIface(ABC, BaseHybridDAL):


    def __init__(self, *args, **kwargs) -> None:

        controlYaml = args[2]

        if 'programID' not in controlYaml or 'obsBlock' not in controlYaml:
            raise KeyError("ProgramID and obsBlock keys must be in the control.yaml file")
        
        self.programID = controlYaml['programID']
        self.obsBlock = controlYaml['obsBlock']
        
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
    def update_result(self, task, serialized, filename) -> None:
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