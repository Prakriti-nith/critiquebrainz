from flask import request, redirect, jsonify
from app import app

class CritiqueBrainzError(Exception):
    """ Parent class for app exceptions. """
    pass

class AbortError(CritiqueBrainzError):
    """ Exception raised when app cannot complete the request. """

    status_code = 400
    
    def __init__(self, message, status_code=None):
        super(AbortError, self).__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
            
    def to_dict(self):
        resp = dict(message=self.message)
        return resp
        
class RequestError(CritiqueBrainzError):
    """ Parent class for request-related exceptions. """
    pass
    
class RequestBodyNotValidJSONError(RequestError):
    """ Exception raised when request body is not a valid JSON object. """
    pass
        
class ParameterError(RequestError):
    """ Exception for errors related to request data. """
        
    def __init__(self, entity):
        super(ParameterError, self).__init__(self)
        self.entity = entity
        
class MissingDataError(ParameterError):
    """ Exception raised when request is missing required data. """
    pass
    
class NotValidDataError(ParameterError):
    """ Exception raised when request data is not valid. """
    pass

class AuthorizationError(CritiqueBrainzError):
    """ Exception raised when authentication process fails. """
    _description = {'server_error': 'The authorization server encountered an '\
                        'unexpected condition that prevented it from '\
                        'fulfilling the request.',
                    'invalid_scope': 'The requested scope is invalid, unknown, '\
                        'or malformed.',
                    'access_denied': 'The resource owner or authorization '\
                        'server denied the request.',
                    'invalid_client_id': 'Invalid client id.',
                    'mismatching_redirect_uri': 'Mismatching redirect uri.',
                    'missing_redirect_uri': 'Missing redirect uri.',
                    'invalid_redirect_uri': 'Invalid redirect uri.'}

    def __init__(self, error='server_error', redirect_uri=None):
        self.error = error
        self.description = self._description[error]
        self.redirect_uri = redirect_uri
