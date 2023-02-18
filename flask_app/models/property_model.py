from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash

class Property:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.location = data['location']
        self.description = data['description']
        self.availability = data['availability']
        self.cash_flow = data['cash_flow']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users = []

# *******- view all proporties and add in dashboard -*
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM properties;"
        results = connectToMySQL(DATABASE).query_db(query)
        properties = []
        for r in results:
            print(r)
            properties.append(cls(r))
        return properties

# *******- creates/inserts one show 
    @classmethod
    def save(cls, data):
        query = "INSERT INTO properties (price, location, description, availability, cash_flow, user_id) VALUES (%(price)s, %(location)s, %(description)s,%(availability)s, %(cash_flow)s,%(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

# *******- gets the one show from the one user -**
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM properties left join users on properties.user_id = users.id where properties.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        one_property = cls(result[0])

        user_data = {
                "id" : result[0]["users.id"],
                "first_name": result[0]['first_name'],
                "last_name": result[0]['last_name'],
                "email": result[0]['email'],
                "password": result[0]['password'],
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at']
        }

        one_property.owner = user_model.User(user_data)
        return one_property

# *******- Updates/edits the properties  -
    @classmethod
    def update(cls, data):
        query = "UPDATE properties SET price=%(price)s, location = %(location)s, description = %(description)s, availability = %(availability)s, cash_flow = %(cash_flow)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- deletes the properties -*
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM properties WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# *******- allows the show selected to be displayed -*  
    @classmethod
    def get_property_by_id(cls, data):
        query = "SELECT * FROM properties WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validates_property_creation_updates(data):
        is_valid = True
# *******- validates property price 
        if len(data['price']) == 0:
            flash("Please provide a property's price!")
            is_valid = False
        elif len(data["price"]) < 3:
            flash("Price name must be big numbers dollars ")
            is_valid = False

# *******- validates propertys -***
        if len(data['location']) == 0:
            flash("Please provide a location!")
            is_valid = False
        elif len(data["location"]) < 3:
            flash("You must write the city or states name")
            is_valid = False

# *******- validates availability that was seen -
        if  len(data['availability']) == 0:
            flash("Availability is required!")
            is_valid = False

# *******- validates property describtion *            
        if len(data['description']) == 0:
            flash("Please provide property's description!")
            is_valid = False
        elif len(data["description"]) < 3:
            flash("Description must be at least three characters")
            is_valid = False

        # *******- validates propertys cash flow-***
        if len(data['cash_flow']) == 0:
            flash("Please provide the rent!")
            is_valid = False
        elif len(data["cash_flow"]) < 3:
            flash("Cash flow must be in numbers")
            is_valid = False

        return is_valid

# *******- get_user_with_properties holds the user and its shows *
    @classmethod
    def get_user_with_properties( cls , data ):
        query = "SELECT * FROM users LEFT JOIN properties ON users.id = properties.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )

        user = cls( results[0] )
        for row in results:

            show_data = {
                "id" : row['id'],
                "price" : row['price'],
                "location" : row['location'],
                "description" : row['description'],
                "availability" : row['availability'],
                "cash_flow" : row['cash_flow'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : row['user_id']
            }
            user.users.append(Property(show_data))
        return user
