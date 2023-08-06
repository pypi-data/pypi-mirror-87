from polzybackend import db, auth
from polzybackend.utils.auth_utils import generate_id, str_id_to_bytes, bytes_id_to_str, generate_token, get_expired
from datetime import datetime, timedelta, date
from sqlalchemy import and_
import uuid
import json

# system date format
date_format = "%Y-%m-%d"

# authentication
@auth.verify_token
def verify_token(token):
    user = User.query.filter_by(access_key=token).first()
    if user and user.key_expired > datetime.utcnow():
        return user


#
# Authentication Models
#

#
# Association Models
#
class UserToCompany(db.Model):
    #
    # association object between user and company
    #
    __tablename__ = 'user_company'
    user_id = db.Column(db.LargeBinary, db.ForeignKey('users.id'), primary_key=True)
    company_id = db.Column(db.LargeBinary, db.ForeignKey('companies.id'), primary_key=True)
    role = db.Column(db.String(32), nullable=False)
    attributes = db.Column(db.String(1024), nullable=True)

    # relationships
    user = db.relationship('User', backref='companies', foreign_keys=[user_id])
    company = db.relationship('Company', backref='users', foreign_keys=[company_id])

    def to_json(self):
        # JSON-string to dict 
        load_json = lambda string: json.loads(string) if string else None
        return {
            'id': bytes_id_to_str(self.company.id),
            'name': self.company.name,
            'displayed_name': str(self.company),
            'role': self.role,
            'attributes': load_json(self.company.attributes),
            'user_attributes': load_json(self.attributes)
        }

class CompanyToCompany(db.Model):
    #
    # association object between companies
    #
    __tablename__ = 'company_company'
    parent_id = db.Column(db.LargeBinary, db.ForeignKey('companies.id'), primary_key=True)
    child_id = db.Column(db.LargeBinary, db.ForeignKey('companies.id'), primary_key=True)
    attributes = db.Column(db.String(1024), nullable=True)

    # relationships
    parent = db.relationship('Company', backref='child_companies', foreign_keys=[parent_id])
    child = db.relationship('Company', backref='parent_companies', foreign_keys=[child_id])


#
# Company Models
#
class Company(db.Model):
    __tablename__="companies"
    id = db.Column(db.LargeBinary, primary_key=True, default=generate_id)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(128), unique=True, nullable=False)
    displayed_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(32), nullable=True)
    phone = db.Column(db.String(16), nullable=True)
    country = db.Column(db.String(32), nullable=True)
    post_code = db.Column(db.String(8), nullable=True)
    city = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    attributes = db.Column(db.String(1024), nullable=True)

    def __str__(self):
        return self.displayed_name or self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.LargeBinary, primary_key=True, default=generate_id)
    email = db.Column(db.String(64), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    displayed_name = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    oauth_provider_id = db.Column(db.Integer, db.ForeignKey('oauth_providers.id'), nullable=False)
    oauth_user_id = db.Column(db.String(128), nullable=False)
    oauth_token = db.Column(db.String(128), nullable=False)
    access_key = db.Column(db.String(128), nullable=False, default=generate_token)
    key_expired = db.Column(db.DateTime, nullable=False, default=get_expired)
    # current session attributes
    stage = db.Column(db.String(8), nullable=True)
    language = db.Column(db.String(8), nullable=True)
    company_id = db.Column(db.LargeBinary, db.ForeignKey('companies.id'), nullable=True)

    # relationships
    oauth_provider = db.relationship(
        'OAuthProvider',
        foreign_keys=[oauth_provider_id],
    )
    company = db.relationship(
        'UserToCompany',
        primaryjoin=and_(
            id == UserToCompany.user_id,
            company_id == UserToCompany.company_id,
        ),
        uselist=False,
        #foreign_keys=[company_id],
    )

    def __str__(self):
        return self.displayed_name or self.first_name or self.last_name or self.email.split('@')[0]

    def set_stage(self, stage):
        self.stage = stage
        db.session.commit()

    def set_language(self, language):
        self.language = language
        db.session.commit()

    def set_company(self, company_id=None, company=None):
        # check if either company data is provided
        if company_id is None and company is None:
            raise Exception('Neither Company ID nor Company provided')

        # check if company should be fetched
        if company is None:
            company = Company.query.get(str_id_to_bytes(company_id))
        
        # check if company exists
        if company is None:
            raise Exception('Company not found')

        # get UserToCompany instance
        user_company = UserToCompany.query.filter(and_(
            UserToCompany.user_id == self.id,
            UserToCompany.company_id == company.id,
        )).first()

        # check if assocoation exests
        if user_company is None:
            raise Exception('User is not assigned to this company')

        # set company
        self.company_id = company.id
        db.session.commit()

    def to_json(self):
        return {
            'name': str(self),
            'access_key': self.access_key,
            'companies': [company.to_json() for company in self.companies],
        }

class OAuthProvider(db.Model):
    __tablename__ = 'oauth_providers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    client_id = db.Column(db.String(128), nullable=False)
    secret_key = db.Column(db.String(128), nullable=False)

    def __str__(self):
        return self.name


#
# Activity Models
#
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.LargeBinary, primary_key=True, default=generate_id)
    creator_id = db.Column(db.LargeBinary, db.ForeignKey('users.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    policy_number = db.Column(db.String(64), nullable=False)
    effective_date = db.Column(db.Date, nullable=False, default=date.today)
    #type_id = db.Column(db.Integer, db.ForeignKey('activity_types.id'), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(64), nullable=True)
    finished = db.Column(db.DateTime, nullable=True)
    attributes = db.Column(db.String, nullable=True)
    
    # relationships
    creator = db.relationship(
        'User',
        backref=db.backref('created_activities', order_by='desc(Activity.created)'),
        foreign_keys=[creator_id],
    )
    #type = db.relationship(
    #    'ActivityType',
    #    foreign_keys=[type_id],
    #)

    def __str__(self):
        return str(uuid.UUID(bytes=self.id))

    @classmethod
    def new(cls, data, policy, current_user):
        # 
        # create instance using data
        #

        instance = cls(
            policy_number=policy.number,
            effective_date=datetime.strptime(policy.effective_date, date_format).date(),
            type=data['activity'].get('name'),
            creator=current_user,
            attributes=json.dumps(data['activity'].get('fields'))
        )
        
        # store to db
        db.session.add(instance)
        db.session.commit()
        
        return instance

    @classmethod
    def read_policy(cls, policy_number, effective_date, current_user):
        #
        # create instance of reading a policy
        #

        instance = cls(
            policy_number=policy_number,
            effective_date=datetime.strptime(effective_date, date_format).date(),
            type='Read Policy',
            creator=current_user,
            finished=datetime.utcnow(),
            status='OK',
        )

        # store to db
        db.session.add(instance)
        db.session.commit()
        
        return instance


    def finish(self, status):
        #
        # sets is_finished to True 
        #
        self.status = status
        self.finished = datetime.utcnow()
        db.session.commit()

class ActivityType(db.Model):
    __tablename__ = 'activity_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=True)


