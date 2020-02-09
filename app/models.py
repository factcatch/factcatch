from app import db
from dataclasses import dataclass,field

@dataclass
class Claim(db.Model):
    __tablename__ = 'claim'
    id:str
    origins: str
    fack_check : str
    description: str
    originally_published: str
    referred_links : str 
    example : str
    last_updated : str
    credibility : int
    url : str
    claim : str 
    tags : str
    prob_model : float
    documents : list = field(default_factory=list)

    id = db.Column(db.String,primary_key=True)
    origins = db.Column(db.String)
    fack_check = db.Column(db.String)
    description = db.Column(db.Text)
    originally_published = db.Column(db.String)
    referred_links = db.Column(db.String)
    example = db.Column(db.String)
    last_updated = db.Column(db.String)
    credibility = db.Column(db.Integer)
    url = db.Column(db.String)
    claim = db.Column(db.String)
    tags = db.Column(db.String)
    prob_model = db.Column(db.Float)
    google_results = db.relationship('GoogleResult',backref='google_result.claim_id',lazy=True)


@dataclass
class GoogleResult(db.Model):
    __tablename__ = 'google_result'
    id : int 
    claim_id : str 
    domain : str 
    link : str 
    link_type : str
    
    id = db.Column(db.Integer,primary_key=True)
    claim_id = db.Column(db.String,db.ForeignKey('claim.id'),nullable=False)
    domain = db.Column(db.String)
    link = db.Column(db.String)
    link_type = db.Column(db.String)