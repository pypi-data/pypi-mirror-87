from blip_flowanalysis.abstract import Analyser
from blip_flowanalysis.core import Flow


class MissingTrackings(Analyser):
    """Verify if flow has minimum Tracking amount.
    
    This method verifies the amount of trackings, considering a minimum that can be changed by the user.
    There is no other method in this class.
    
    Methods:
      * analyse - Return `True` if amount of Trackings is above minimum, `False` otherwise.
    """
    
    def __init__(self, minimum: int = 1) -> None:
        super().__init__()
        self.minimum = minimum
    
    def analyse(self, flow: Flow) -> bool:
        """Return `True` if amount of Trackings is above minimum, `False` otherwise.
        
        :param flow: Chatbot flow structure.
        :type flow: ``blip_flowanalysis.core.Flow``
        :return: `True` if amount of Trackings is above minimum, `False` otherwise.
        :rtype: ``bool``
        
        :raise ValueError: if `minimum` < 1
        :raise TypeError: if `minimum` not type `int`
        """
        if not isinstance(self.minimum, int):
            raise TypeError(f"`minimum` must be `int`, came {type(self.minimum)}")
        if self.minimum < 1:
            raise ValueError(f"`minimum` must be greater than 1")
        
        trackings = flow.get_tracks_id()
        if len(trackings.keys()) < self.minimum:
            return False
        return True
