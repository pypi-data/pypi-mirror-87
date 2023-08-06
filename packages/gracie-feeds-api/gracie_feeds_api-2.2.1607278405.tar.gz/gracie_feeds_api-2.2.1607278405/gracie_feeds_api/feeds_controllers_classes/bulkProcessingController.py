from gracie_feeds_api import GracieBaseAPI


class bulkProcessingController(GracieBaseAPI):
    """Bulk Processing Controller"""

    _controller_name = "bulkProcessingController"

    def clearErrors(self):
        """Clear BulkProcessing errors"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/bulkProcessing/clearErrors'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, **kwargs):
        """Change BulkProcessing configuration parameters

        Args:
            chunkSize: (integer): chunkSize
            maxChunks: (integer): maxChunks
            minChunkSize: (integer): minChunkSize
            numThreads: (integer): numThreads

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'chunkSize': {'name': 'chunkSize', 'required': False, 'in': 'query'}, 'maxChunks': {'name': 'maxChunks', 'required': False, 'in': 'query'}, 'minChunkSize': {'name': 'minChunkSize', 'required': False, 'in': 'query'}, 'numThreads': {'name': 'numThreads', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def getErrors(self, **kwargs):
        """Get BulkProcessing errors

        Args:
            pageNum: (integer): pageNum
            pageSize: (integer): pageSize

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'pageNum': {'name': 'pageNum', 'required': False, 'in': 'query'}, 'pageSize': {'name': 'pageSize', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/getErrors'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def reprocessAllErrors(self):
        """Reprocess BulkProcessing errors"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/bulkProcessing/reprocessAllErrors'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def reprocessErrorList(self, taskIds):
        """Reprocess BulkProcessing errors

        Args:
            taskIds: (type, items): taskIds

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'taskIds': {'name': 'taskIds', 'required': True, 'in': 'body'}}
        parameters_names_map = {}
        api = '/bulkProcessing/reprocessErrorList'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def stats(self):
        """Get BulkProcessing stats"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/bulkProcessing/stats'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
