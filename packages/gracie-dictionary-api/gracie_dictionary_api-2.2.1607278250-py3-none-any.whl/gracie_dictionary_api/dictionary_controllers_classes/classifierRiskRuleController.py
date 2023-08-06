from gracie_dictionary_api import GracieBaseAPI


class classifierRiskRuleController(GracieBaseAPI):
    """Classifier Risk Rule Controller"""

    _controller_name = "classifierRiskRuleController"

    def addLabel(self, id, label):
        """

        Args:
            id: (string): id
            label: (string): label

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classifierRiskRules/addLabel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def create(self, classifierType, excludeRefs, includeRefs, minRelevance, numInclude, orderBy, riskLabel):
        """

        Args:
            classifierType: (string): classifierType
            excludeRefs: (array): excludeRefs
            includeRefs: (array): includeRefs
            minRelevance: (number): minRelevance
            numInclude: (integer): numInclude
            orderBy: (string): orderBy
            riskLabel: (string): riskLabel

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'classifierType': {'name': 'classifierType', 'required': True, 'in': 'query'}, 'excludeRefs': {'name': 'excludeRefs', 'required': True, 'in': 'query'}, 'includeRefs': {'name': 'includeRefs', 'required': True, 'in': 'query'}, 'minRelevance': {'name': 'minRelevance', 'required': True, 'in': 'query'}, 'numInclude': {'name': 'numInclude', 'required': True, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': True, 'in': 'query'}, 'riskLabel': {'name': 'riskLabel', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classifierRiskRules/create'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            excludeRefs: (array): excludeRefs
            id: (string): id
            includeRefs: (array): includeRefs
            minRelevance: (number): minRelevance
            numInclude: (integer): numInclude
            orderBy: (string): orderBy
            riskLabel: (string): riskLabel

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'excludeRefs': {'name': 'excludeRefs', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'includeRefs': {'name': 'includeRefs', 'required': False, 'in': 'query'}, 'minRelevance': {'name': 'minRelevance', 'required': False, 'in': 'query'}, 'numInclude': {'name': 'numInclude', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'riskLabel': {'name': 'riskLabel', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classifierRiskRules/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            label: (string): label

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'label': {'name': 'label', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classifierRiskRules/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def listLabels(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/classifierRiskRules/listLabels'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classifierRiskRules/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeLabel(self, id, label):
        """

        Args:
            id: (string): id
            label: (string): label

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classifierRiskRules/removeLabel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classifierRiskRules/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
