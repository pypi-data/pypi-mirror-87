from gracie_dictionary_api import GracieBaseAPI


class databasesController(GracieBaseAPI):
    """Databases Controller"""

    _controller_name = "databasesController"

    def archive(self, classifierId, **kwargs):
        """

        Args:
            classifierId: (string): classifierId
            languageId: (string): languageId

        Consumes:
            application/json

        Returns:
            application/json
        """

        all_api_parameters = {'classifierId': {'name': 'classifierId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/archive'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def backup(self, **kwargs):
        """

        Args:
            incremental: (boolean): incremental
            removeFolder: (boolean): removeFolder
            zip: (boolean): zip

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'incremental': {'name': 'incremental', 'required': False, 'in': 'query'}, 'removeFolder': {'name': 'removeFolder', 'required': False, 'in': 'query'}, 'zip': {'name': 'zip', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/backup'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportDatabases(self, **kwargs):
        """

        Args:
            databaseId: (string): Id is some of { country, topic, skillSet, skill, clusterSet, clusterGroup, cluster, profile }. Or some of { "COUNTRIES", "TOPICS", "SKILLSETS", "CLUSTERSETS", "PROFILES" }. If empty then export all databases.
            password: (string): password

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'databaseId': {'name': 'databaseId', 'required': False, 'in': 'query'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/exportDatabases'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def importDatabases(self, file, **kwargs):
        """

        Args:
            conflictsResolving: (string): conflictsResolving
            databaseId: (string): Id is some of { country, topic, skillSet, skill, clusterSet, clusterGroup, cluster, profile }. Or some of { "COUNTRIES", "TOPICS", "SKILLSETS", "CLUSTERSETS", "PROFILES" }. If empty then import all databases.
            file: (file): file
            password: (string): password

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'conflictsResolving': {'name': 'conflictsResolving', 'required': False, 'in': 'query'}, 'databaseId': {'name': 'databaseId', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/importDatabases'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateBinaries(self, **kwargs):
        """

        Args:
            forceUpdateUnchanged: (boolean): forceUpdateUnchanged

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'forceUpdateUnchanged': {'name': 'forceUpdateUnchanged', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateBinaries'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateDictionaries(self, **kwargs):
        """

        Args:
            dictionaryId: (string): dictionaryId
            recalculateDocumentsVectors: (boolean): recalculateDocumentsVectors
            testSubclasses: (boolean): testSubclasses

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'dictionaryId': {'name': 'dictionaryId', 'required': False, 'in': 'query'}, 'recalculateDocumentsVectors': {'name': 'recalculateDocumentsVectors', 'required': False, 'in': 'query'}, 'testSubclasses': {'name': 'testSubclasses', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateDictionaries'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateLanguage(self, **kwargs):
        """

        Args:
            customCorpusFileName: (string): customCorpusFileName
            languageId: (string): languageId
            updateDoc2vec: (boolean): updateDoc2vec
            updateIdfModel: (boolean): updateIdfModel

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'customCorpusFileName': {'name': 'customCorpusFileName', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'updateDoc2vec': {'name': 'updateDoc2vec', 'required': False, 'in': 'query'}, 'updateIdfModel': {'name': 'updateIdfModel', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateLanguage'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateProfiles(self, **kwargs):
        """

        Args:
            id: (string): id
            updateDocuments: (boolean): updateDocuments

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'updateDocuments': {'name': 'updateDocuments', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateProfiles'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateSkillsets(self, **kwargs):
        """

        Args:
            enabledContextSensitiveKeywords: (boolean): enabledContextSensitiveKeywords
            recalculateDocumentsVectors: (boolean): recalculateDocumentsVectors
            skillId: (string): skillId
            testSubclasses: (boolean): testSubclasses

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabledContextSensitiveKeywords': {'name': 'enabledContextSensitiveKeywords', 'required': False, 'in': 'query'}, 'recalculateDocumentsVectors': {'name': 'recalculateDocumentsVectors', 'required': False, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': False, 'in': 'query'}, 'testSubclasses': {'name': 'testSubclasses', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateSkillsets'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
