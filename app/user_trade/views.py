from flask import Blueprint, flash
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask_login import login_required
from app.user_trade.operation import *
from app.user_trade.form import *
from datetime import *

import base64

user_trade_ = Blueprint('utrade', __name__)

@user_trade_.route("/bids/")
#@login_required
def bid_list_all():
	containing = ['bidlist']
	#bid_list = bid_list_by_user(current_user.UserID)
	bid_list = bid_list_by_user(1)
	display_list = list()

	if('status' in request.form):
		print "bidlist with status"
		status = request.form['status'];
		for bid in bid_list:
			if(bid.DSState == status):
				display_list.append(bid)
	else:
		display_list = bid_list

	print bid_list

	#return render_template('index.html')
	return render_template('bid_list.html', usertype = 'comsumer', ct = containing, type = 'user', blist = display_list)

@user_trade_.route("/decorations/", methods=['GET', 'POST'])
@login_required
def decorations_list():
	dclist = get_dcform_list(current_user.UserID)
	display_list = list()

	if('status' in request.form):
		print "dclist with status"
		status = request.form['status'];
		for deco in dclist:
			if(deco.DcFormState == status):
				display_list.append(deco)
	else:
		display_list = dclist

	return render_template('decoration_list.html', dlist = display_list)

@user_trade_.route("/bids/<int:bid>/<operation>")
@login_required
def bid_operation(bid, operation):
	dcid = bid / 65537
	schid = bid % 65537

	if operation == '' or operation == 'info':
		bidInfo = bid_info(dcid, schid)
		return render_template('bid_info.html', source = 'user', bid = bidInfo)

	if operation == 'choose':
		bid_choose(dcid, schid)
		flash("Successfully choose bid", "success")
		redirect(url_for(bid_list_deco(dcid)))

	if operation == "reject":
		bid_reject(dcid, schid)
		flash("Successfully rejected bid", "success")
		redirect(url_for(bid_list_deco(dcid)))

	now_path = "/user_trade/bids/" + str(bid) + "/" + operation
	return render_template('404.html', path = now_path, reason = "Wrong Operation")

@user_trade_.route("/decorations/new", methods=['GET', 'POST'])
@login_required
def new_decoration():
	form = DecorationForm(request.form)
	if form.validate_on_submit():
		dcform_create(current_user.UserID, form.description.data, today())
		flash('The decoration has been submitted.', 'success')
		redirect(url_for(decorations_list))

	return render_template('new_decoration.html')

@user_trade_.route("/decorations/<int:dcid>", methods=['GET', 'POST'])
@login_required
def decoration_detail(dcid):
	containing = ['dcinfo', 'bidlist', 'comments']
	dcinfo = get_dcform_by_ID(dcid)
	bid_list = bid_list_by_dcform(dcid)
	display_list = list()
	comments = read_comments_by_decoration(dcid)

	if('status' in request.form):
		print "dclist with status"
		status = request.form['status'];
		for bid in bid_list:
			if(bid.DSState == status):
				display_list.append(bid)
	else:
		display_list = bid_list

	return render_template('bid_list.html', usertype = 'comsumer', ct = containing, type = 'deco', blist = display_list, dcinfo = dcinfo, comments = comments)

@user_trade_.route("/decorations/<int:dcid>/new_comment", methods=['GET', 'POST'])
@login_required
def new_comment(dcid):
	form = DecorationForm(request.form)
	if form.validate_on_submit():
		add_comment(form.rank.data, form.contents.data, dcid, None);
		redirect(decoration_detail(dcid))

	now_path = "/user_trade/decorations/" + str(dcid) + "/new_comment"
	return render_template('404.html', path = now_path, reason = "Empty Form")


