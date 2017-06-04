from app import db
from app.sql_operation.mysql import *


def next_dcformID():
	maxID = db.session.execute("select max(DecorationForm.DcFormID) from DecorationForm")
	if maxID is not None:
		return maxID[0][0] + 1
	else:
		return 1

def next_commentID():
	maxID = db.session.execute("select max(Comments.CommentsID) from Comments")
	if maxID is not None:
		return maxID[0][0] + 1
	else:
		return 1

'''
def order_create(UserID, furnitures, createtime):
	assert UserID is not None, "Order Create: UserID is empty!"

	OrderFormID = next_orderformID

	new_order = OrderForm(OrderFormID, UserID, 'Waiting', createtime)
	db.session.add(new_invation)
	db.session.commit()

	for fur in furnitures:
		OrderItemID = next_orderitemID
		new_item = OrderItem(OrderItemID, OrderFormID, fur['furData'].FurnitureID, fur['furNum'])
		db.session.add(new_item)

	db.session.commit()

def get_order_list(UID):
	res = db.session.query(OrderForm).filter_by(UserID = UID).all()
	return res

def get_order_furnitures(OID):
	res = db.session.query(OrderItem).\
			join(Furniture, OrderItem.FurnitureID == Furniture.FurnitureID).\
			filter(OrderItem.OrderFormID == OID).all()
	return res

def order_change_state(OID, state):
	db.session.query(OrderForm).filter(OrderForm.OrderFormID == OID).update({'OrderFormState' : state})
	db.session.commit()

'''
def dcform_create(ConsumerID, description, createtime):
	assert ConsumerID is not None, "DecorationForm Create: ConsumerID is empty!"
	assert createtime is not None, "DecorationForm Create: No Createtime!"
	assert len(description) <= 200, "DecorationForm Create: Description too long!"

	dcformID = next_dcformID();
	new_form = DecorationForm(dcformID, ConsumerID, description, "Waiting", createtime)
	db.session.add(new_form)
	db.session.commit()

def get_dcform_list(UID):
	res = db.session.query(DecorationForm).filter_by(ConsumerID = UID).all()
	return res

def get_dcform_by_ID(dcID):
	res = db.session.query(DecorationForm).filter_by(DcFormID = dcID).first()
	return res

def bid_list_by_user(UID):
	res = db.session.query(DecorationForm).\
			join(CompetitiveBid, DecorationForm.DcFormID == CompetitiveBid.DcFormID).\
			filter(DecorationForm.ConsumerID == UID).all()
	return res

def bid_list_by_dcform(dcformID):
	res = db.session.query(CompetitiveBid).filter_by(DcFormID = dcformID).all()
	return res

def bid_info(dcformID, schID):
	res = db.session.query(CompetitiveBid).filter(CompetitiveBid.DcFormID == dcformID).filter(CompetitiveBid.SchemeID == schID).first()
	return res;

def bid_choose(dcformID, schID):
	dcform = db.session.query(DecorationForm).filter_by(DcFormID = dcformID).first()
	assert dcform is not None, "Bid Choose: DecorationForm does not exist!"

	cbids = db.session.query(CompetitiveBid).filter_by(DcFormID = dcformID).all();
	for cbid in cbids:
		assert cbids.DSState == 'Waiting', "Bid Choose: BidState is not right!"

	db.session.query(DecorationForm).filter(DecorationForm.DcFormID == dcformID).update({'DcFormState' : 'Success'})
	db.session.query(CompetitiveBid).filter(CompetitiveBid.DcFormID == dcformID).filter(CompetitiveBid.SchemeID == schID).update({'DSState' : "Accept"})
	db.session.query(CompetitiveBid).filter(CompetitiveBid.DcFormID == dcformID).filter(CompetitiveBid.SchemeID != schID).update({'DSState' : "Reject"})
	db.session.commit()

def bid_reject(dcformID, schID):
	dcform = db.session.query(DecorationForm).filter_by(DcFormID = dcformID).first()
	assert dcform is not None, "Bid Choose: DecorationForm does not exist!"

	cbids = db.session.query(CompetitiveBid).filter_by(DcFormID = dcformID).all();
	for cbid in cbids:
		assert cbids.DSState == 'Waiting', "Bid Choose: BidState is not right!"

	db.session.query(CompetitiveBid).filter(CompetitiveBid.DcFormID == dcformID).filter(CompetitiveBid.SchemeID == schID).update({'DSState' : "Reject"})
	db.session.commit()

def dcform_change_state(state):
	db.session.query(DecorationForm).filter(DecorationForm.DcFormID == dcformID).update({'DcFormState' : state})
	db.session.commit()

def add_comment(rank, contents, dcformID, OID):
	CommentsID = next_commentID()
	new_comment = Comments(CommentsID, contents, rank, OID, dcformID)
	db.session.add(new_comment)
	db.session.commit()

def read_comments_by_scheme(schID):
	res = db.session.query(Comments).\
			join(CompetitiveBid, Comments.DcFormID == CompetitiveBid.DcFormID).\
			filter(CompetitiveBid.SchemeID == schID).all()
	return res

def read_comments_by_order(OID):
	res = db.session.query(Comments).filter_by(OrderFormID = OID).all()
	return res

def read_comments_by_decoration(DcFormID):
	res = db.session.query(Comments).filter_by(DcFormID = DcFormID).all()
	return res

def order_not_commented(UID):
	orders = db.session.query(OrderForm).filter_by(UserID = UID).all()
	res = list()

	for order in orders:
		missing = db.session.query(Comments).filter_by(OrderFormID = order.OrderFormID).first()
		if missing is None:
			res.append(order)
	return res

def decoration_not_commented(consumerID):
	decorations = db.session.query(DecorationForm).filter_by(ConsumerID = consumerID).all()
	res = list()

	for dc in decorations:
		missing = db.session.query(Comments).filter_by(DcFormID = dc.DcFormID).first()
		if missing is None:
			res.append(dc)
	return res
