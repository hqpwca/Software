from app import db
from app.sql_operation.mysql import *

def new_scheme_id():
	maxID = db.session.execute("select max(DesignerScheme.SchemeID) from DesignerScheme")
	if maxID is not None:
		return maxID[0][0] + 1
	else:
		return 1

def scheme_create(desID, description, image, price):
	SchemeID = new_scheme_id()
	designer = db.session.query(Designer).filter_by(DesignerID = desID).first();
	assert designer is not None, "Scheme Create: Designer does not exist!"

	new_scheme = DesignerScheme(SchemeID, desID, designer.CompanyID, description, image, price)
	db.session.add(new_scheme)
	db.session.commit()

def get_scheme_by_designer(desID):
	res = db.session.query(DesignerScheme).filter_by(DesignerID = desID).all()
	return res

def get_scheme_by_schid(schID):
	res = db.session.query(DesignerScheme).filter_by(SchemeID = schID).first()
	return res

def get_dcforms_waiting():
	res = db.session.query(DecorationForm).filter_by(DcFormState = 'Waiting').all();
	return res;

def get_dcforms_compete():
	res = db.session.query(DecorationForm).filter_by(DcFormState = 'Compete').all();
	return res;

def bid_participation(desID, schID, dcformID, desc, discount, time):
	designer = db.session.query(Designer).filter_by(DesignerID = desID).first();
	assert designer is not None, "Bid Participation: Designer does not exist!"

	scheme = db.session.query(DesignerScheme).filter_by(SchemeID = schID).first();
	assert scheme is not None, "Bid Participation: Scheme does not exist!"
	assert scheme.DesignerID == desID, "Bid Participation: Scheme does not belong to the Designer!"

	dcform = db.session.query(DecorationForm).filter_by(DcFormID = dcformID).first()
	assert dcform is not None, "Bid Participation: DecorationForm does not exist!"
	assert (dcform.DcFormState == 'Compete' or dcform.DcFormState == 'Waiting'),\
		 "Bid Participation: DecorationFormState is not right!"

	new_bid = CompetitiveBid(dcformID, schID, desc, time, 'Waiting', scheme.SchemePrice * discount)
	db.session.add(new_bid)
	db.session.query(DecorationForm).filter(DecorationForm.DcFormID == dcformID).update({'DcFormState' : 'Compete'})
	db.session.commit()

def bid_update(desID, schID, dcformID, desc, discount, time):
	designer = db.session.query(Designer).filter_by(DesignerID = desID).first();
	assert designer is not None, "Bid Participation: Designer does not exist!"

	scheme = db.session.query(DesignerScheme).filter_by(SchemeID = schID).first();
	assert scheme is not None, "Bid Participation: Scheme does not exist!"
	assert scheme.DesignerID == desID, "Bid Participation: Scheme does not belong to the Designer!"

	dcform = db.session.query(DecorationForm).filter_by(DcFormID = dcformID).first()
	assert dcform is not None, "Bid Participation: DecorationForm does not exist!"
	assert (dcform.DcFormState == 'Compete' or dcform.DcFormState == 'Waiting'),\
		 "Bid Participation: DecorationFormState is not right!"

	db.session.query(CompetitiveBid).filter_by(DcFormID = dcformID).filter_by(SchemeID = schID).\
			update({'DSDESC' : desc, 'DSPrice' : scheme.SchemePrice * discount, 'SubmitTime' : time})
	db.session.commit()

def get_bids_by_scheme(schID):
	res = db.session.query(CompetitiveBid).filter_by(SchemeID = schID).all();
	return res;

def get_bids_by_designer(desID):
	schemes = db.session.query(DesignerScheme).filter_by(DesignerID = desID).all();
	res = list()

	for scheme in schemes:
		res += get_bids_by_scheme(scheme.SchemeID);
	return res;

def read_comments_by_scheme(desID, schID):
	designer = db.session.query(Designer).filter_by(DesignerID = desID).first();
	assert designer is not None, "Bid Participation: Designer does not exist!"

	scheme = db.session.query(DesignerScheme).filter_by(SchemeID = schID).first();
	assert scheme is not None, "Bid Participation: Scheme does not exist!"
	assert scheme.DesignerID == desID, "Bid Participation: Scheme does not belong to the Designer!"

	res = db.session.query(CompetitiveBid).filter_by(SchemeID = schID).\
			join(Comments, CompetitiveBid.DcFormID == Comments.DcFormID).all();
	return res

def read_comments_by_designer(desID):
	designer = db.session.query(Designer).filter_by(DesignerID = desID).first();
	assert designer is not None, "Bid Participation: Designer does not exist!"

	schemes = db.session.query(DesignerScheme).filter_by(DesignerID = desID).all();
	res = list()

	for scheme in schemes:
		res += read_comments_by_scheme(desID, scheme.SchemeID);
	return res;
