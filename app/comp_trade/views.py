from flask import Blueprint, flash
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask_login import login_required
from app.comp_trade.operation import *
from app.comp_trade.form import *
from datetime import *

comp_trade_ = Blueprint('ctrade', __name__)

@comp_trade_.route("/comments/", methods=['GET', 'POST'])
@login_required
def view_all_comments():
	comments = read_comments_by_designer(current_user.UserID)

	return render_template("comments.html", type = 'all', comments = comments)

@comp_trade_.route("/schemes/<int:schid>/comments")
@login_required
def view_comments_by_scheme(schid):
	comments = read_comments_by_scheme(current_user.UserID, schid)

	return render_template("comments.html", type = 'scheme', comments = comments)

@comp_trade_.route("/schemes/new", methods=['GET', 'POST'])
@login_required
def new_scheme():
	form = SchemeForm(request.form)
	if form.validate_on_submit():
		if form.image.data:
			image_data = request.FILES[form.image.name].read()
        else:
        	return render_template("new_scheme.html", error = True, reason = ['Image Error'])

       	scheme_create(current_user.UserID, form.description.data, image_data, form.price.data)
       	redirect(url_for(scheme_list))

	return render_template("new_scheme.html", error = False, reason = [])

@comp_trade_.route("/schemes/")
@login_required
def scheme_list():
	schemes = get_scheme_by_designer(current_user.UserID)

	return render_template("list_scheme.html", uid = current_user.UserID, schemes = schemes)

@comp_trade_.route("/bids/")
@login_required
def list_bids_of_designer():
	bid_list = get_bids_by_designer(current_user.UserID)
	display_list = list()
	containing = ['bidlist']

	if('status' in request.form):
		print "bidlist with status"
		status = request.form['status'];
		for bid in bid_list:
			if(bid.DSState == status):
				display_list.append(bid)
	else:
		display_list = bid_list

	return render_template("bid_list.html", usertype = 'designer', ct = containing, type = 'user', blist = display_list)

@comp_trade_.route("/schemes/<int:schid>/bids")
@login_required
def scheme_detail(schid):
	bid_list = get_bids_by_scheme(schid)
	scinfo = get_scheme_by_schid(schid)
	display_list = list()
	containing = ['scinfo', 'bidlist']

	if('status' in request.form):
		print "dclist with status"
		status = request.form['status'];
		for bid in bid_list:
			if(bid.DSState == status):
				display_list.append(bid)
	else:
		display_list = bid_list

	return render_template("bid_list.html", usertype = 'designer', ct = containing, type = 'user', blist = display_list, scinfo = scinfo)

@comp_trade_.route("/bids/new", methods=['GET', 'POST'])
@login_required
def create_new_bid():
	form = BidForm(request.form)
	initData = getInitData(request.form)

	if form.validate_on_submit():
		bid_participation(current_user.UserID, form.schID.data, form.dcID.data,\
		 form.description.data, form.discount.data, today())
		redirect(url_for(view_bid_info))

	return render_template("bid_data.html", type = 'create', initdata = initData)

@comp_trade_.route("/bids/change")
@login_required
def change_bid_info():
	# TODO: add code

	return render_template("bid_data.html", type = 'change', data = initData)

@comp_trade_.route("/bids/view")
@login_required
def view_bid_info():
	# TODO: add code

	return render_template("bid_data.html", type = 'view', initdata = initData)

def getInitData(form):
	res = dict()
	if 'initschID' in form:
		res['schID'] = form['initschID']
	if 'initdcID' in form:
		res['dcID'] = form['initdcID']
	# TODO: add other initdata

	return res
