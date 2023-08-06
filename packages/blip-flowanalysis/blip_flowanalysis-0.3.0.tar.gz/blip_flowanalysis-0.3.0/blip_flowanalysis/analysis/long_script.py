import typing as tp

from blip_flowanalysis.abstract import Analyser
from blip_flowanalysis.core import Flow

Action = tp.Dict[str, tp.Any]
Interface = str
State = tp.Dict[str, tp.Any]
Context = tp.Tuple[State, Interface, Action]
Script = str
AnalysisValues = tp.Tuple[Script, int, int]
AnalysisChecks = tp.Tuple[bool, bool]
Detection = tp.Tuple[AnalysisValues, AnalysisChecks, State, Interface]
ReportDetection = tp.Dict[str, tp.Any]
Report = tp.Dict[str, tp.Any]


class LongScript(Analyser):
    """Check if bot scripts are too long.
    
    It is known, from bots development experience, that scripts on each state
    should be short. Long scripts would be considered as problem for bot
    maintainability and also a vulnerability to bugs occurrence.
    
    This analysis finds all scripts on bot states and measures their length as
    characters and non-blank lines quantities. For each measure, there is a
    threshold. Default values are `1240` characters and `40` non-blank lines.
    
    For each script, if any of these measures is above the threshold, this is
    reported in the analysis. See `analysis` for more details.
    
    Attributes:
        * max_length (`int`) - Maximum number of characters a script can have.
        * max_lines (`int`) - Maximum number of non-blank lines a script can
        have.
        * script_show_limit (`int`) - Limit of characters for displaying a
        script on the report.
        * execute_script_type (`str`) - Action type that execute a script on
        bot flow.
        * io_actions (`tuple`) - Interfaces on states to search for scripts.
    
    Methods:
        * analyse - Detects too long scripts on bot flow.
    """
    
    _CAUSES = {
        (True, True): 'Too many chars and lines on script',
        (True, False): 'Too many chars on script',
        (False, True): 'Too many lines on script'
    }
    
    def __init__(
            self,
            max_length: int = 1240,
            max_lines: int = 30,
            script_show_limit: int = 200,
            execute_script_type: str = 'ExecuteScript',
            io_actions: tuple = ('inputActions', 'outputActions')) -> None:
        super().__init__()
        self.max_length = max_length
        self.max_lines = max_lines
        self.script_show_limit = script_show_limit
        self.execute_script_type = execute_script_type
        self.io_actions = io_actions
    
    def analyse(self, flow: Flow) -> Report:
        """Detects too long scripts on bot flow.
        
        For each one, details are included on report.
        Summary on report shows number of scripts, too long scripts, states
        and irregular states (with too long scripts).
        Finally, returns this report.
        See `report` for details on report format.
        
        :param flow: Bot flow structure.
        :type flow: ``blip_flowanalysis.core.Flow``
        :return: Report with analysis of scripts on bot flow.
        :rtype: `dict` from `str` to `any`
        """
        states = flow.get_states_list()
        n_states = len(states)
        n_scripts = 0
        detections = list()
        for state, io_action, action in self._iterate_actions(states):
            if self._is_execute_script(action):
                values = self._get_analysis_values(action)
                checks = self._check_analysis_values(values)
                if any(checks):
                    detections.append((values, checks, state, io_action))
                n_scripts += 1
        return self._report((n_scripts, n_states, detections))
    
    def _iterate_actions(self, states: tp.List[State]) -> Context:
        """Yield state, io_actions and action by all actions on states.
        
        State is state on bot flow.
        Interface is any of 'inputActions' and 'outputActions'.
        Action is action on state inputAction or outputAction.
        
        :param states: States on bot flow.
        :type states: `list` of `dict`
        :return: Tuple with state, io_action and action for each action.
        :rtype: (`dict`, `str`, `dict`)
        """
        for state in states:
            for io_action in self.io_actions:
                for action in state[io_action]:
                    yield state, io_action, action
    
    def _is_execute_script(self, action: Action) -> bool:
        """Check if action is typed to execute script.
        
        :param action: Action on bot flow.
        :type action: `dict`
        :return: True on action as execute script, false otherwise.
        :rtype: `bool`
        """
        return action['type'] == self.execute_script_type
    
    def _check_analysis_values(self, values: AnalysisValues) -> AnalysisChecks:
        """Check if each measure is greater than defined threshold for it.
        
        :param values: Tuple with script and measures as analysis values.
        :type values: (`str`, `int`, `int`)
        :return: Tuple with check for each measure.
        :rtype: (`bool`, `bool`)
        """
        _, length, lines = values
        return (
            (length > self.max_length),
            (lines > self.max_lines)
        )
    
    def _report_analysis_values(self, detection: Detection) -> ReportDetection:
        """Build a report for long script detection.
        
        This report is like:
        ```
        {
            'state_id': state_id,  # State ID on bot flow.
            'state_name': state_name,  # State name on bot flow.
            'io_action': io_action,  # Any of inputActions and outputActions.
            'script': script,  # Script (limited by `script_show_limit`).
            'length': length,  # Characters quantity.
            'lines': lines,  # Not blank lines quantity.
            'cause': cause  # Explain why this script was detected.
        }
        ```
        
        :param detection: Detection for too long script.
        :type detection:
            ((`str`, `int`, `int`), (`bool`, `bool`), `dict`, `str`)
        :return: Report for long script detection.
        :rtype: `dict` from `str` to `any`
        """
        values, checks, state, io_action = detection
        script, length, lines = values
        return {
            'state_id': state['id'],
            'state_name': state['name'],
            'io_action': io_action,
            'script': script[:min(len(script), self.script_show_limit)],
            'length': length,
            'lines': lines,
            'cause': LongScript._CAUSES[checks]
        }
    
    def _report(self, results: tp.Tuple[int, int, tp.List[Detection]]) -> Report:
        """Build a report with long scripts detection on bot flow.
        
        Parameter `results` contains number of scripts, number of states and
        too long scripts detections.
        
        This report is like:
        ```
        {
            'summary': {
                'scripts count': n_scripts,
                'scripts too long': n_long_scripts,
                'states count': n_states,
                'states with too long scripts': n_irregular_states
            },
            'details': [
                {...},  # Reports for detections. See `report_analysis_values`
                ...
            ]
        }
        ```
        
        :param results: Results to report.
        :type results: (`int`, `int`, `list` of `tuple`)
        :return: Report with long scripts detection on bot flow.
        :rtype: `dict` from `str` to `any`
        """
        n_scripts, n_states, detections = results
        n_long_scripts = len(detections)
        n_irregular_states = self._count_irregular_states(detections)
        summary = {
            'scripts count': n_scripts,
            'scripts too long': n_long_scripts,
            'states count': n_states,
            'states with too long scripts': n_irregular_states
        }
        details = list(map(self._report_analysis_values, detections))
        return {
            'summary': summary,
            'details': details
        }
    
    @staticmethod
    def _get_script(action: Action) -> Script:
        """Get script on action.
        
        :param action: Action on bot flow.
        :type action: `dict`
        :return: Script on action.
        :rtype: `str`
        """
        return action['settings']['source']
    
    @staticmethod
    def _get_script_length(script: Script) -> int:
        """Get script characters quantity.
        
        :param script: Script on action.
        :type script: `str`
        :return: Script characters quantity.
        :rtype: `int`
        """
        return len(script)
    
    @staticmethod
    def _get_script_lines(script: Script) -> int:
        """Get script non-blank lines quantity.
        
        :param script: Script on action.
        :type script: `str`
        :return: Script non-blank lines quantity.
        :rtype: `int`
        """
        return len(list(filter(len, map(str.strip, script.splitlines()))))
    
    @staticmethod
    def _get_analysis_values(action: Action) -> AnalysisValues:
        """Get script and measures for analysis.
        
        The measures are number of characters and number of non-blank lines.
        
        :param action: Action on bot flow.
        :type action: `dict`
        :return: Tuple with script and measures as analysis values.
        :rtype: (`str`, `int`, `int`)
        """
        script = LongScript._get_script(action)
        length = LongScript._get_script_length(script)
        lines = LongScript._get_script_lines(script)
        return script, length, lines
    
    @staticmethod
    def _count_irregular_states(detections: tp.List[Detection]) -> int:
        """Count irregular states on detections.
        
        An action on each detection belongs to a state. This counts how many
        distinct states contains all actions on detections.
        
        :param detections: Detections for too long scripts.
        :type: detections: `list` of `tuple`
        :return: Number of irregular states.
        :rtype: `int`
        """
        return len({state['id'] for _, __, state, ___ in detections})
