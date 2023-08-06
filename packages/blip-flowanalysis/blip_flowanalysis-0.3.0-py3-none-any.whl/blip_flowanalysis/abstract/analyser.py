import typing as tp
from abc import ABC, abstractmethod
from blip_flowanalysis.core import Flow


class Analyser(ABC):
    """Implements different structural analysis on chatbot flow data.
    
    This abstract base class defines that any subclass must implement its own `analyse` method.
    All subclasses must:
        * perform the analysis in the `analyse` method;
        * keep `analyse` parameters as in the abstract class;
        * implement additional inputs for `analyse` method as class/object attributes.
        
    Additional methods (public or non public) should be implemented only if they are necessary
    to the `analyse` method.
    """
    
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def analyse(self, flow: Flow) -> tp.Any:
        """Implements structural analysis.
        
        :param flow: Chatbot flow structure.
        :type flow: ``blip_flowanalysis.core.Flow``
        """
        raise NotImplementedError()
