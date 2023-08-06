from base import db


# 
# Attributes Values
#

class PolicyValue(db.Model):
    __tablename__ = 'policies'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    effective_date = db.Column(db.Date)
    status = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('policy', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class PolicyAttributes(db.Model):
    __tablename__ = 'policy_attributes'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))
    attribute_3 = db.Column(db.String(32))
    attribute_4 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('policy_attributes', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class PartnerValues(db.Model):
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    is_person = db.Column(db.Boolean, nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    birth_date = db.Column(db.Date)
    company_name = db.Column(db.String(64))
    address = db.Column(db.String(128))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    postal_code = db.Column(db.String(16))
    primary_email = db.Column(db.String(64))
    secondary_email = db.Column(db.String(64))
    primary_phone = db.Column(db.String(16))
    secondary_phone = db.Column(db.String(16))
    risk_group = db.Column(db.String(64))
    current_occupation = db.Column(db.String(64))
    current_occupation_from = db.Column(db.Date)
    previous_ocupation = db.Column(db.String(64))
    sports = db.Column(db.String(64))
    health_conditions = db.Column(db.String(256))
    
    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('partner', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class InsuredPersonAttributes(db.Model):
    __tablename__ = 'insured_person_attributes'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))
    attribute_3 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('person_attributes', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class InsuredObjectAttributes(db.Model):
    __tablename__ = 'insured_object_attributes'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    object_type = db.Column(db.String(32))
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))
    attribute_3 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('object_attributes', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class ImplementationAttributes(db.Model):
    __tablename__ = 'implementation_attributes'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('implementation_attributes', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )


#
# Product Line Attributes
#

class ProductLineLife(db.Model):
    __tablename__ = 'product_line_life'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))
    attribute_3 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('productline_attributes_life', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class ProductLineHealth(db.Model):
    __tablename__ = 'product_line_health'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))
    attribute_3 = db.Column(db.String(32))
    attribute_4 = db.Column(db.String(32))
    attribute_5 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('productline_attributes_health', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class ProductLinePnC(db.Model):
    __tablename__ = 'product_line_pnc'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('productline_attributes_pnc', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class ProductLineCar(db.Model):
    __tablename__ = 'product_line_car'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('productline_attributes_car', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

#
# Insured Object Type Attributes
#

class ObjectHouse(db.Model):
    __tablename__ = 'object_house'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('object_attributes_house', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class ObjectCar(db.Model):
    __tablename__ = 'object_car'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('object_attributes_car', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class ObjectFactory(db.Model):
    __tablename__ = 'object_factory'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))
    attribute_3 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('object_attributes_factory', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class ObjectField(db.Model):
    __tablename__ = 'object_field'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))
    attribute_2 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('object_attributes_field', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )

class ObjectForest(db.Model):
    __tablename__ = 'object_forest'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.LargeBinary, db.ForeignKey('activities.id'), nullable=False)
    attribute_1 = db.Column(db.String(32))

    # relationships
    activity = db.relationship(
        'Activity',
        backref=db.backref('object_attributes_forest', uselist=False),
        foreign_keys=[activity_id],
        uselist=False,
    )