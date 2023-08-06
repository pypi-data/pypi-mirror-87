from gracie_dictionary_api import GracieBaseAPI


class profileClassController(GracieBaseAPI):
    """Profile Class Controller"""

    _controller_name = "profileClassController"

    def add(self, name, profileId):
        """

        Args:
            name: (string): name
            profileId: (string): profileId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addFile(self, files, profileId, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html

        Args:
            files: (array): files
            languageId: (string): languageId
            profileId: (string): profileId

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'files': {'name': 'files', 'required': True, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/addFile'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addFromSkill(self, profileId, skillId, **kwargs):
        """

        Args:
            addSkillIdToFeatures: (boolean): addSkillIdToFeatures
            profileId: (string): profileId
            skillId: (string): skillId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'addSkillIdToFeatures': {'name': 'addSkillIdToFeatures', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/addFromSkill'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addFromSkillset(self, profileId, skillsetId, **kwargs):
        """

        Args:
            addSkillIdToFeatures: (boolean): addSkillIdToFeatures
            profileId: (string): profileId
            skillsetId: (string): skillsetId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'addSkillIdToFeatures': {'name': 'addSkillIdToFeatures', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}, 'skillsetId': {'name': 'skillsetId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/addFromSkillset'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkAdd(self, profileId, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html

        Args:
            addSkillIdToFeatures: (boolean): addSkillIdToFeatures
            files: (array): files
            languageId: (string): languageId
            profileId: (string): profileId
            skillIds: (array): skillIds
            skillsetIds: (array): skillsetIds

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'addSkillIdToFeatures': {'name': 'addSkillIdToFeatures', 'required': False, 'in': 'query'}, 'files': {'name': 'files', 'required': False, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}, 'skillIds': {'name': 'skillIds', 'required': False, 'in': 'query'}, 'skillsetIds': {'name': 'skillsetIds', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/bulkAdd'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id, **kwargs):
        """

        Args:
            id: (string): id
            removeSkillIdFromFeatures: (boolean): removeSkillIdFromFeatures

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'removeSkillIdFromFeatures': {'name': 'removeSkillIdFromFeatures', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, profileId, **kwargs):
        """

        Args:
            orderAsc: (boolean): orderAsc
            orderBy: (string): orderBy
            profileId: (string): profileId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/list'
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
        api = '/profileClass/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
