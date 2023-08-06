from gracie_feeds_api import GracieBaseAPI


class processReviewTasksController(GracieBaseAPI):
    """Process Review Tasks Controller"""

    _controller_name = "processReviewTasksController"

    def submit(self, privacyMode, productId, productName, projectId, review, reviewTypeId, **kwargs):
        """

        Args:
            author: (string): Person who created the review.
            businessCategories: (array): Business categories.
            businessCoordinatesLatitude: (number): Business coordinates latitude.
            businessCoordinatesLongitude: (number): Business coordinates longitude.
            businessId: (string): Business id.
            businessLocationAddress1: (string): Business location address1.
            businessLocationAddress2: (string): Business location address2.
            businessLocationAddress3: (string): Business location address3.
            businessLocationCity: (string): Business location city.
            businessLocationCountry: (string): Business location country.
            businessLocationState: (string): Business location state.
            businessLocationZipCode: (string): Business location ZIP code.
            businessName: (string): Business name.
            businessPhone: (string): Business phone.
            businessPrice: (integer): Business price.
            businessRating: (number): Business rating.
            businessTransactions: (array): Business transactions.
            businessUrl: (string): Business url.
            checkinCount: (integer): Check-in count.
            coolCount: (integer): Cool count.
            date: (integer): Date the review was posted. The number of seconds since January 1, 1970, 00:00:00 GMT.
            funnyCount: (integer): Funny count.
            helpfulCount: (integer): The number of people that indicated this review was helpful.
            languageId: (string): empty - AutoDetect.
            logging: (boolean): logging
            notHelpfulCount: (integer): The number of people that indicated this review was not helpful.
            options: (array): List of possible options.
            privacyMode: (boolean): In this mode the processed text not saved.
            productId: (string): The product id of the item being reviews.
            productName: (string): The product name.
            projectId: (string): API id of project.
            rating: (number): The review star rating.
            recommended: (boolean): Recommended.
            review: (string): Text of the review.
            reviewTypeId: (string): Amazon, Home depot, Walmart, etc...
            reviewVotesCount: (integer): Review votes count.
            stopAfterChunkNum: (integer): Only process the first N number text chunks when the document requires chunking.
            url: (string): Review url.
            verifiedUser: (boolean): Verified user.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'author': {'name': 'author', 'required': False, 'in': 'query'}, 'businessCategories': {'name': 'businessCategories', 'required': False, 'in': 'query'}, 'businessCoordinatesLatitude': {'name': 'businessCoordinatesLatitude', 'required': False, 'in': 'query'}, 'businessCoordinatesLongitude': {'name': 'businessCoordinatesLongitude', 'required': False, 'in': 'query'}, 'businessId': {'name': 'businessId', 'required': False, 'in': 'query'}, 'businessLocationAddress1': {'name': 'businessLocationAddress1', 'required': False, 'in': 'query'}, 'businessLocationAddress2': {'name': 'businessLocationAddress2', 'required': False, 'in': 'query'}, 'businessLocationAddress3': {'name': 'businessLocationAddress3', 'required': False, 'in': 'query'}, 'businessLocationCity': {'name': 'businessLocationCity', 'required': False, 'in': 'query'}, 'businessLocationCountry': {'name': 'businessLocationCountry', 'required': False, 'in': 'query'}, 'businessLocationState': {'name': 'businessLocationState', 'required': False, 'in': 'query'}, 'businessLocationZipCode': {'name': 'businessLocationZipCode', 'required': False, 'in': 'query'}, 'businessName': {'name': 'businessName', 'required': False, 'in': 'query'}, 'businessPhone': {'name': 'businessPhone', 'required': False, 'in': 'query'}, 'businessPrice': {'name': 'businessPrice', 'required': False, 'in': 'query'}, 'businessRating': {'name': 'businessRating', 'required': False, 'in': 'query'}, 'businessTransactions': {'name': 'businessTransactions', 'required': False, 'in': 'query'}, 'businessUrl': {'name': 'businessUrl', 'required': False, 'in': 'query'}, 'checkinCount': {'name': 'checkinCount', 'required': False, 'in': 'query'}, 'coolCount': {'name': 'coolCount', 'required': False, 'in': 'query'}, 'date': {'name': 'date', 'required': False, 'in': 'query'}, 'funnyCount': {'name': 'funnyCount', 'required': False, 'in': 'query'}, 'helpfulCount': {'name': 'helpfulCount', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'notHelpfulCount': {'name': 'notHelpfulCount', 'required': False, 'in': 'query'}, 'options': {'name': 'options', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': True, 'in': 'query'}, 'productId': {'name': 'productId', 'required': True, 'in': 'query'}, 'productName': {'name': 'productName', 'required': True, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'rating': {'name': 'rating', 'required': False, 'in': 'query'}, 'recommended': {'name': 'recommended', 'required': False, 'in': 'query'}, 'review': {'name': 'review', 'required': True, 'in': 'query'}, 'reviewTypeId': {'name': 'reviewTypeId', 'required': True, 'in': 'query'}, 'reviewVotesCount': {'name': 'reviewVotesCount', 'required': False, 'in': 'query'}, 'stopAfterChunkNum': {'name': 'stopAfterChunkNum', 'required': False, 'in': 'query'}, 'url': {'name': 'url', 'required': False, 'in': 'query'}, 'verifiedUser': {'name': 'verifiedUser', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/process-review-tasks/submit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
