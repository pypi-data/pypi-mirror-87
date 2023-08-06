
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls)\
                .__call__(*args, **kwargs)
        return cls._instances[cls]

class API(metaclass=Singleton):
    def __init__(self, client_id, client_secret, url, origin, customer_id, domain):
        self.client_id = client_id
        self.client_secret = client_secret
        self.customer_id = customer_id
        self.domain = domain
        self.url = url
        self.origin = origin

    
    def __build_session(self, token=None):
        if not token:
            token = self.get_token()
        origin = self.origin
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Origin': origin,
            'Authorization': 'Bearer ' + str(token),
        })
        return session

    
    def get_token(self):
        """
        Request a token from YOM API to realize and authentication.
        """
        origin, url = self.origin, self.url
        path = url + '/api/v2/auth/tokens/grant'
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Origin': origin
        })
        try:
            response = session.post(path, json.dumps(body))
            response = json.loads(response.content.decode('utf-8'))
            if 'accessToken' in response:
                return response['accessToken']
            return None
        except Exception as e:
            return None


    def bulk_importer(self, model, batch, token):
        """
        Send data to importer, data must be a dictionary.
        """
        # Upload data
        path = f'{self.url}/api/v2/import/{model}/bulk'
        session = self.__build_session(token)
        response = session.post(path, json.dumps(batch))
        return response


    # Commerce:

    def get_commerces_mapping(self, token):
        """
        Return all commerces from API
        """
        current_page = 0
        total_pages = float('inf')
        commerces = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_commerces_mapping_page(page=current_page, limit=10000, token=token)
            commerces += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending commerce mapping query for page {}/{}'.format(current_page, total_pages))
        return commerces


    def __get_commerces_mapping_page(self, page, limit, token):
        path = self.url + '/api/v2/commerces/mapping'
        session = self.__build_session(token)
        params = {
            'page': page,
            'limit': limit,
            'field': 'contact.externalId'
        }
        response = session.get(path, params=params)
        return (response.status_code, response.json())


    def update_bulk_commerces(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/commerces/bulk'
        session = self.__build_session(token)
        body = {
            'data': batch,
            'fieldsNotToBeUpdated': fields_not_to_be_updated
        }
        response = session.put(path, json.dumps(body))
        return response


    def create_bulk_commerces(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/commerces/bulk'
        session = self.__build_session(token)
        body = {
            'data': batch,
        }
        response = session.post(path, json.dumps(body))
        return response


    # Overrides:

    def update_bulk_overrides(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/segments/overrides/bulk'
        session = self.__build_session(token)
        body = {
            'data': batch,
            'fieldsNotToBeUpdated': fields_not_to_be_updated
        }
        response = session.put(path, json.dumps(body))
        return response


    def update_bulk_overrides_by_segment(self, segment_id, batch, fields_not_to_be_updated, token):
        path = self.url + f'/api/v2/segments/{segment_id}/overrides/bulk'
        session = self.__build_session(token)
        body = {
            'data': batch,
            'fieldsNotToBeUpdated': fields_not_to_be_updated
        }
        response = session.put(path, json.dumps(body))
        return response


    def bulk_clean_overrides(self, job_id, token):
        path = self.url + f'/api/v2/segments/overrides/delete-not-by-sync-job/{job_id}'

        self.logger.info('Sending overrides delete for job id {}'.format(job_id))

        session = self.__build_session(token)
        response = session.delete(path, headers=headers)

        self.logger.info((response.status_code, response.json()))

        return response


    # Segments:

    def get_segments_mapping(self, token, fields='name'):
        current_page = 0
        total_pages = float('inf')
        segments = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_segments_mapping_page(page=current_page, limit=10000, fields=fields, token=token)
            segments += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending segments mapping query for page {}/{}'.format(currentPage, total_pages))
        return segments


    def __get_segments_mapping_page(page=current_page, limit=10000, fields, token):
        path = self.url + '/api/v2/segments/mapping'
        session = self.__build_session(token)
        params = {
            'page': page,
            'limit': limit,
            'field': fields
        }
        response = session.get(path, params=params)
        return (response.status_code, response.json())


    def update_bulk_segments(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/segments/bulk'
        session = self.__build_session(token)

        body = {
            'data': batch,
            'fieldsNotToBeUpdated': fields_not_to_be_updated
        }
        response = session.put(path, json.dumps(body))
        return response

    
    # UserSegments:

    def get_user_segments_mapping(self, token, fields='segmentId commerceId'):
        current_page = 0
        total_pages = float('inf')
        segments = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_user_segments_mapping_page(
                page=current_page,
                limit=10000,
                fields=fields,
                token=token
            )
            segments += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending segments mapping query for page {}/{}'.format(currentPage, total_pages))
        return segments


    def __get_user_segments_mapping_page(page=current_page, limit=10000, fields, token):
        path = self.url + '/api/v2/segments/user_segments/mapping'
        session = self.__build_session(token)
        params = {
            'page': page,
            'limit': limit,
            'field': fields
        }
        response = session.get(path, params=params)
        return (response.status_code, response.json())


    def update_bulk_user_segments(self, batch, fields_not_to_be_updated):
        path = self.url + '/api/v2/segments/user-segments/bulk'
        session = self.__build_session(token)

        body = {
            'data': batch,
            'fieldsNotToBeUpdated': fields_not_to_be_updated
        }
        response = session.put(path, json.dumps(body))
        return response

    # Products:

    def get_products(self):
        current_page = 0
        total_pages = float('inf')
        products = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_products_page(page=current_page, limit=100)
            products += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending products query for page {}/{}'.format(current_page, total_pages))
        return products


    def __get_products_page(self, page, limit, token):
        path = self.url + '/api/v2/products'
        session = self.__build_session(token)
        params = {
            'page': page,
            'limit': limit
        }
        response = session.get(path, params=params)
        return (response.status_code, response.json())


    def update_bulk_products(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/products/bulk'
        session = self.__build_session()
        body = {
            'data': batch,
            'fieldsNotToBeUpdated': fields_not_to_be_updated
        }
        response = session.put(path, json=body, headers=headers)
        return response

