from . import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class OAuthClient(db.Model):

    __tablename__ = 'oauth_client'
    client_id = db.Column(db.Unicode, primary_key=True)
    client_secret = db.Column(db.Unicode, nullable=False)
    user_id = db.Column(UUID, db.ForeignKey('user.id'))
    name = db.Column(db.Unicode, nullable=False)
    desc = db.Column(db.Unicode, nullable=False)
    website = db.Column(db.Unicode, nullable=False)
    redirect_uri = db.Column(db.UnicodeText, nullable=False)
    scopes = db.Column(db.UnicodeText, default=u'user publication')

    user = db.relationship('User')

    allowed_includes = []

    def get_scopes(self):
        if hasattr(self, '_scopes') is False:
            self._scopes = self.scopes.split()
        return self._scopes

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self, includes=[]):
        response = dict(client_id=self.client_id,
            client_secret=self.client_secret,
            user_id=self.user_id,
            name=self.name,
            desc=self.desc,
            website=self.website,
            redirect_uri=self.redirect_uri,
            scopes=self.scopes)
        return response

        
class OAuthGrant(db.Model):

    __tablename__ = 'oauth_grant'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Unicode, index=True, nullable=False)
    client_id = db.Column(db.Unicode, db.ForeignKey('oauth_client.client_id', 
        onupdate='CASCADE'), nullable=False)
    user_id = db.Column(UUID, db.ForeignKey('user.id'), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    redirect_uri = db.Column(db.UnicodeText, nullable=False)
    scopes = db.Column(db.UnicodeText)

    client = db.relationship('OAuthClient')
    user = db.relationship('User')

    def get_scopes(self):
        if hasattr(self, '_scopes') is False:
            self._scopes = self.scopes.split()
        return self._scopes

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
        
class OAuthToken(db.Model):

    __tablename__ = 'oauth_token'
    
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.Unicode, unique=True, nullable=False)
    refresh_token = db.Column(db.Unicode, unique=True, nullable=False)
    client_id = db.Column(db.Unicode, db.ForeignKey('oauth_client.client_id', 
        onupdate='CASCADE'), nullable=False)
    user_id = db.Column(UUID, db.ForeignKey('user.id'), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    scopes = db.Column(db.UnicodeText)

    client = db.relationship('OAuthClient')
    user = db.relationship('User')

    def get_scopes(self):
        if hasattr(self, '_scopes') is False:
            self._scopes = self.scopes.split()
        return self._scopes

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
