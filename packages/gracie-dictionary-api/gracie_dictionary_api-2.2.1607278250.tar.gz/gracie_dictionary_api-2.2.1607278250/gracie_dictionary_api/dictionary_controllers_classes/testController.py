from gracie_dictionary_api import GracieBaseAPI


class testController(GracieBaseAPI):
    """Test Controller"""

    _controller_name = "testController"

    def convert(self, **kwargs):
        """

        Args:
            stringArg: (string): stringArg

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'stringArg': {'name': 'stringArg', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/test/convert'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def extractDocuments(self, files, **kwargs):
        """

        Args:
            files: (array): files
            languageId: (string): languageId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'files': {'name': 'files', 'required': True, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/test/extractDocuments'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def test(self, **kwargs):
        """

        Args:
            argDouble: (number): argDouble in range [-5,5]
            argInteger: (integer): argInteger
            argIntegerArray: (array): argIntegerArray
            argIntegerArrayOptional: (array): argIntegerArrayOptional
            argIntegerOptional: (integer): argIntegerOptional
            argString: (string): argString
            argStringArray: (array): argStringArray
            argStringArrayOptional: (array): argStringArrayOptional
            argStringOptional: (string): argStringOptional

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'argDouble': {'name': 'argDouble', 'required': False, 'in': 'query'}, 'argInteger': {'name': 'argInteger', 'required': False, 'in': 'query'}, 'argIntegerArray': {'name': 'argIntegerArray', 'required': False, 'in': 'query'}, 'argIntegerArrayOptional': {'name': 'argIntegerArrayOptional', 'required': False, 'in': 'query'}, 'argIntegerOptional': {'name': 'argIntegerOptional', 'required': False, 'in': 'query'}, 'argString': {'name': 'argString', 'required': False, 'in': 'query'}, 'argStringArray': {'name': 'argStringArray', 'required': False, 'in': 'query'}, 'argStringArrayOptional': {'name': 'argStringArrayOptional', 'required': False, 'in': 'query'}, 'argStringOptional': {'name': 'argStringOptional', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/test/test'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def testImage(self, **kwargs):
        """

        Args:
            encode: (boolean): encode
            file: (file): file
            imageUrl: (string): imageUrl
            removeImage: (boolean): removeImage

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'encode': {'name': 'encode', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': False, 'in': 'formData'}, 'imageUrl': {'name': 'imageUrl', 'required': False, 'in': 'query'}, 'removeImage': {'name': 'removeImage', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/test/testImage'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def testImageFeedback(self, imageId, **kwargs):
        """

        Args:
            addedTags: (array): addedTags
            imageId: (string): imageId
            includeOriginalTags: (boolean): includeOriginalTags
            removedTags: (array): removedTags

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'addedTags': {'name': 'addedTags', 'required': False, 'in': 'query'}, 'imageId': {'name': 'imageId', 'required': True, 'in': 'query'}, 'includeOriginalTags': {'name': 'includeOriginalTags', 'required': False, 'in': 'query'}, 'removedTags': {'name': 'removedTags', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/test/testImageFeedback'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def testRequest(self, **kwargs):
        """

        Args:
            booleanArg: (boolean): booleanArg
            doubleArg: (number): doubleArg
            intArg: (integer): intArg
            longArg: (integer): longArg
            stringArg: (string): stringArg

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'booleanArg': {'name': 'booleanArg', 'required': False, 'in': 'query'}, 'doubleArg': {'name': 'doubleArg', 'required': False, 'in': 'query'}, 'intArg': {'name': 'intArg', 'required': False, 'in': 'query'}, 'longArg': {'name': 'longArg', 'required': False, 'in': 'query'}, 'stringArg': {'name': 'stringArg', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/test/testRequest'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def testTask(self, **kwargs):
        """

        Args:
            booleanArg: (boolean): booleanArg
            doubleArg: (number): doubleArg
            intArg: (integer): intArg
            longArg: (integer): longArg
            sleepMs: (integer): sleepMs
            stringArg: (string): stringArg

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'booleanArg': {'name': 'booleanArg', 'required': False, 'in': 'query'}, 'doubleArg': {'name': 'doubleArg', 'required': False, 'in': 'query'}, 'intArg': {'name': 'intArg', 'required': False, 'in': 'query'}, 'longArg': {'name': 'longArg', 'required': False, 'in': 'query'}, 'sleepMs': {'name': 'sleepMs', 'required': False, 'in': 'query'}, 'stringArg': {'name': 'stringArg', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/test/testTask'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def testVS(self, **kwargs):
        """

        Args:
            modelId: (string): modelId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'modelId': {'name': 'modelId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/test/testVS'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
