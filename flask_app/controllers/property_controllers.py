from flask_app.models.property_model import Property
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user_model
#--- STEPS TO START USING APU IN PYTHON ---#
# 1. install request ----> python3 -m pip install requests 
# 2. import requests

import requests

# ***** this doesnt let me go the dashboard- checks the cond first ******
@app.route("/properties")
def dashboard():
    if not 'uid' in session:
        flash("access denied")
        return redirect("/")
    results = user_model.User.all_properties_with_users()
    print(results)
    print(session['uid'])
    return render_template('dashboard.html', results=results)

@app.route("/view/all")
def view_all():

    api_key = "JHTwQThtR9M_Mkmsw37NTw_Kwc_nJ8QU1otFK8lNbXRQKoXmmy7E1ZkiBsMruWdKKR8Do0QrxwlI8yl5HPk4-UsM_-L3b88rPat64JXezzvhas7s1MMno-7dPaekY3Yx"
    our_headers = {f'Authorization' : f'Bearer {api_key}' }
#     headers = {
#     "accept": "application/json",
#     "Authorization": "JHTwQThtR9M_Mkmsw37NTw_Kwc_nJ8QU1otFK8lNbXRQKoXmmy7E1ZkiBsMruWdKKR8Do0QrxwlI8yl5HPk4-UsM_-L3b88rPat64JXezzvhas7s1MMno-7dPaekY3Yx"
# }
    # api_url = 'http://api.yelp.com/v3//businesses/search'
    api_url = "https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit=20"
    our_params = {'term':'coffee',
                # 'limit': 50,
                'radius': 10000,
                'location':''
            }
    response = requests.get(api_url, headers=our_headers, params= our_params)
    print("THIS IS MY RESPONSE FROM YELP------------------->", response.text)

    # url = "https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit=20"

    # headers = {
    #     "accept": "application/json",
    #     "Authorization": "bearer XDg0tJz7SYlTaBT6cAGoUEZXXNlkLZSixHLPbs3OTtpMiebt2wwNVpKDv44V3PVS2TQ0BPApH_Lq6TacE1UUsH2-SwYiOFKDvDdIQyA1SCXcyqAyCQilbhKP7I2iY3Yx"
    # }

    # response = requests.get(url, headers=headers)

    print(response.text)
    return render_template('view_all.html', all_properties=Property.get_all())



@app.route("/show/all")
def all_shows():
    return render_template('create_property.html', all_properties=Property.get_all())


@app.route('/properties/destroy/<int:id>')
def distroy_properties(id):
    data = {
        "id": id
    }
    Property.destroy(data)
    return redirect("/properties")

@app.route('/properties/display/<int:id>')
def display_properties(id):
    data = {
        "id": id
    }
    properties = Property.get_one(data)
    return render_template('show_property.html', properties = properties)

@app.route('/properties/edit/<int:id>')
def edit_properties(id):

    data = {
        "id": id
    }
    result = Property.get_property_by_id(data)
    return render_template('edit_property.html', result = result)


@app.route("/create_property", methods=["POST"])
def new_property():

    if not Property.validates_property_creation_updates(request.form):
        return redirect("/property/all")

    data={
        **request.form,
        "user_id": session['uid']
    }
    Property.save(data)
    return redirect("/properties")

@app.route("/edit_property/<int:id>", methods=["POST"])
def updated_show(id):

    if not Property.validates_property_creation_updates(request.form):
        return redirect("/view/all/edit/"+str(id))

    data={
        **request.form,
        "id": id
    }
    Property.update(data)
    return redirect("/properties")