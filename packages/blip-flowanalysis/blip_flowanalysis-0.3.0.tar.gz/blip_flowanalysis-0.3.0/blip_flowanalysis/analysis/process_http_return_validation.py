import typing as tp

from blip_flowanalysis.abstract import Analyser
from blip_flowanalysis.core import Flow


class ProcessHTTPReturnValidation(Analyser):
    """Validate each HTTP request in chatbot flow structure.
    
    Chatbots implemented in Blip Builder can make HTTP requests. The purpose here is to analyse all
    HTTP requests in a given flow structure and return a validation report.
    
    Two types of validation are performed for each HTTP request:
        * Next action validation: check if request is validated by the action immediately after it.
        * Outputs validation: check if the request is validated by the outputs of the request's state.
    
    The HTTP request validation process has three possible outcomes:
        * status validation: validation found using the request's status variable (best practice);
        * body validation: validation found using the request's body variable (warning);
        * no validation: validation wasn't found using either status or body variable (warning).
    
    The validation report is described in the documentation of `analyse` method.
    
    Methods:
        * analyse - Execute validation on flow and return a report with summary and warnings.
        * validate_states - Loop over flow states and validate those that have HTTP requests.
        * iterate_http_actions - Generate list with necessary information for validation of each HTTP request.
        * validate_next_action - Return validation status according to action after HTTP request.
        * validate_outputs - Return validation status according to outputs of the HTTP request's state.
    """
    
    __total: str = "total"
    __status_validation: str = "status validation"
    __body_validation: str = "body validation"
    __no_validation: str = "no validation"
    __action_types: tp.Tuple[str, str] = ("inputActions", "outputActions")
    __http_types: tp.Tuple[str] = ("ProcessHttp",)
    __accepted_next_actions: tp.Tuple[str, str] = ("SetVariable", "ExecuteScript")
    
    def __init__(self) -> None:
        super().__init__()
        self.validation_report = self.__create_report_structure()
    
    def __create_report_structure(self) -> dict:
        """Create validation report structure.
        
        :return: Report structure with summary and warnings initialized.
        :rtype: dict
        """
        return {
            "summary": {
                self.__total: 0,
                self.__status_validation: 0,
                self.__body_validation: 0,
                self.__no_validation: 0,
            },
            "warnings": []
        }
    
    def __increment_summary_field(self, field: str, increment: int = 1) -> None:
        """Increment summary field value.
        
        :param field: Key in validation report summary.
        :type field: ``str``
        :param increment: Value to increment.
        :type increment: ``int``
        :return: Updated report with incremented value.
        :rtype: ``any``
        """
        self.validation_report["summary"][field] += increment
    
    def __append_warning(self, state_id: str, action_type: str, status_var: str, body_var: str,
                         validation_type: str) -> None:
        """Append warning to validation report.
        
        :param state_id: State id in which the request action is located.
        :type state_id: ``str``
        :param action_type: Set of actions inside state.
        :type action_type: ``str``
        :param status_var: Request response status variable.
        :type status_var: ``str``
        :param body_var: Request response body variable.
        :type body_var: ``str``
        :param validation_type: Type of validation found.
        :type validation_type: ``str``
        :return: Updated report with appended warning.
        :rtype: ``any``
        """
        self.validation_report["warnings"].append({
            "state id": state_id,
            "action type": action_type,
            "status variable": status_var,
            "body variable": body_var,
            "validation": validation_type
        })
    
    def __update_report(self, next_val: str, outputs_val: str, state_id: str, action_type: str,
                        http_vars: tp.Tuple[str, str]) -> None:
        """Update validation report depending on type of validation.
        
        :param next_val: Validation of next action.
        :type next_val: ``str``
        :param outputs_val: Validation of outputs.
        :type outputs_val: ``str``
        :param state_id: State id in which the request action is located.
        :type state_id: ``str``
        :param action_type: Set of actions inside state.
        :type action_type: ``str``
        :param http_vars: Request response variables (status and body).
        :type http_vars: ``tuple`` of ``str``
        :return: Updated report.
        :rtype: ``any``
        """
        status_var, body_var = http_vars
    
        if self.__status_validation in (next_val, outputs_val):
            self.__increment_summary_field(self.__status_validation)
        elif self.__body_validation in (next_val, outputs_val):
            self.__increment_summary_field(self.__body_validation)
            self.__append_warning(state_id, action_type, status_var, body_var, self.__body_validation)
        else:
            self.__increment_summary_field(self.__no_validation)
            self.__append_warning(state_id, action_type, status_var, body_var, self.__no_validation)
    
    def validate_next_action(self, next_action: dict, http_vars: tp.Tuple[str, str]) -> str:
        """Return validation status according to action after HTTP request.
        
        :param next_action: Action after HTTP request in flow structure.
        :type next_action: ``dict``
        :param http_vars: Result variables of request (status and body).
        :type http_vars: ``tuple`` of ``str``
        :return: Type of validation found.
        :rtype: ``str``
        """
        if (not next_action) or (next_action["type"] not in self.__accepted_next_actions):
            return self.__no_validation
    
        status_var, body_var = http_vars
        next_action_str = str(next_action)
        if status_var in next_action_str:
            return self.__status_validation
        elif body_var in next_action_str:
            return self.__body_validation
        else:
            return self.__no_validation

    def validate_outputs(self, outputs: tp.List[dict], http_vars: tp.Tuple[str, str]) -> str:
        """Return validation status according to outputs of the HTTP request's state.
        
        :param outputs: Structure of redirecting to other states according to conditions.
        :type outputs: ``list`` of ``dict``
        :param http_vars: Result variables of request (status and body).
        :type http_vars: ``tuple`` of ``str``
        :return: Type of validation found.
        :rtype: ``str``
        """
        condition_variables = []
        for output in outputs:
            if "conditions" in output:
                condition_variables.extend([condition.get("variable") for condition in output["conditions"]])
    
        if not condition_variables:
            return self.__no_validation
    
        status_var, body_var = http_vars
        if status_var in condition_variables:
            return self.__status_validation
        elif body_var in condition_variables:
            return self.__body_validation
        else:
            return self.__no_validation

    @staticmethod
    def iterate_http_actions(states: tp.List[dict], action_types: tuple,
                             http_types: tuple) -> tp.List[tp.Tuple[dict, str, int, dict]]:
        """Generate list with necessary information for validation of each HTTP request.
        
        :param states: Chatbot flow states.
        :type states: ``list``
        :param action_types: Types of actions in states.
        :type action_types: ``tuple``
        :param http_types: Types of actions that execute HTTP requests.
        :type http_types: ``tuple``
        :return: List with all elements required for validation.
        :rtype: ``list`` of ``tuple`` of ``dict, str, int, dict``
        """
        http_actions = []
        for state in states:
            for action_type in action_types:
                for index, action in enumerate(state[action_type]):
                    if action["type"] in http_types:
                        http_actions.append((state, action_type, index, action))
        
        return http_actions
    
    def validate_states(self, states: list) -> None:
        """Loop over flow states and validate those that have HTTP requests.
        
        :param states: Chatbot flow states.
        :type states: ``list``
        :return: Validation report updated.
        :rtype: ``any``
        """
        for item in self.iterate_http_actions(states, self.__action_types, self.__http_types):
            state, action_type, index, http_action = item
            state_id = state["id"]
            outputs = state["outputs"]
            
            self.__increment_summary_field(self.__total)
            http_vars = (http_action["settings"].get("responseStatusVariable", ""),
                         http_action["settings"].get("responseBodyVariable", ""))
            
            next_action = dict() if index == (len(state[action_type]) - 1) else state[action_type][index + 1]

            next_action_validation = self.validate_next_action(next_action, http_vars)
            outputs_validation = self.validate_outputs(outputs, http_vars)

            self.__update_report(next_action_validation, outputs_validation, state_id, action_type, http_vars)
    
    def analyse(self, flow: Flow) -> dict:
        """Return a report with summary and warnings of HTTP requests validation.
        
        :param flow: Chatbot flow structure.
        :type flow: ``blip_flowanalysis.core.Flow``
        :return: Report of the validation process with summary and warnings.
        :rtype: ``dict``
        
        The structure of the validation report is described bellow.
        ```
        {
            "summary": overall results
            {
                "total": number of HTTP requests found,
                "status validation": number of requests with validation of status variable,
                "body validation": number of requests with validation of body variable,
                "no validation": number of requests without validation of either status or body variable
            },
            "warnings": details for warning cases ("body validation" and "no validation")
            [
                {
                    "state id": state id in which the request action is located,
                    "action type": either "inputActions" or "outputActions",
                    "status variable": status variable name,
                    "body variable": body variable name,
                    "validation": either "body validation" or "no validation"
                }
            ]
        }
        ```
        """
        self.validate_states(flow.get_states_list())
        return self.validation_report
