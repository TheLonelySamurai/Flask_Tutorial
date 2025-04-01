from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:74CLpyrola!@localhost/boatdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


# render a file
@app.route('/')
def index():
    return render_template('index.html')

# remember how to take user inputs?
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# get all boats
# this is done to handle requests for two routes -
@app.route('/boats/')
@app.route('/boats/<page>', methods=['POST'])
def get_boats(page=1):
    page = int(page)  # request params always come as strings. So type conversion is necessary.
    per_page = 12  # records to show per page
    if page == 0:
        page = 1
    search = request.form.get('search', None)  # get the search value from the form
    if search:
        boats = conn.execute(text(f"SELECT * FROM boats WHERE name LIKE '%{search}%' ORDER BY id LIMIT {per_page} OFFSET {(page - 1) * per_page}")).all()
    else:
        boats = conn.execute(text(f"SELECT * FROM boats ORDER BY id LIMIT {per_page} OFFSET {(page - 1) * per_page}")).all()
    print(boats)
    return render_template('boats.html', boats=boats, page=page, per_page=per_page, search=search)
@app.route('/boats/<page>/<search>')
def get_boats_search_with_page(page=1, search=None):
    page = int(page)  # request params always come as strings. So type conversion is necessary.
    if page == 0:
        page = 1
    if search == 'MihAKpC5ZaIMXK+APl4CfQ==':
        search = None
    per_page = 12  # records to show per page
    if search:
        boats = conn.execute(text(f"SELECT * FROM boats WHERE name LIKE '%{search}%' ORDER BY id LIMIT {per_page} OFFSET {(page - 1) * per_page}")).all()
    else:
        boats = conn.execute(text(f"SELECT * FROM boats ORDER BY id LIMIT {per_page} OFFSET {(page - 1) * per_page}")).all()
    print(boats)
    return render_template('boats.html', boats=boats, page=page, per_page=per_page, search=search)
@app.route('/boat/<id>', methods=['GET'])
def get_boat(id):
    boat = conn.execute(text("SELECT * FROM boats WHERE id = :id"), {'id': id}).first()
    return render_template('boat.html', boat=boat)

@app.route('/create', methods=['GET'])
def create_get_request():
    return render_template('boats_create.html')


@app.route('/create', methods=['POST'])
def create_boat():
    # you can access the values with request.from.name
    # this name is the value of the name attribute in HTML form's input element
    # ex: print(request.form['id'])
    try:
        conn.execute(
            text("INSERT INTO boats (id, name, type, owner_id, rental_price) values (:id, :name, :type, :owner_id, :rental_price)"),
            request.form
        )
        return render_template('boats_create.html', error=None, success="Data inserted successfully!")
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('boats_create.html', error=error, success=None)
    
@app.route('/update', methods=['GET'])
def update_get_request():
    return render_template('boats_update.html')

@app.route('/update', methods=['POST'])
def update_boat():
    try:
        conn.execute(
            text("UPDATE boats SET name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price WHERE id = :id"),
            request.form
        )
        return render_template('boats_update.html', error=None, success="Data updated successfully!")
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('boats_update.html', error=error, success=None)

@app.route('/delete', methods=['GET'])
def delete_get_request():
    return render_template('boats_delete.html')


@app.route('/delete', methods=['POST'])
def delete_boat():
    try:
        conn.execute(
            text("DELETE FROM boats WHERE id = :id"),
            request.form
        )
        return render_template('boats_delete.html', error=None, success="Data deleted successfully!")
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('boats_delete.html', error=error, success=None)


if __name__ == '__main__':
    app.run(debug=True)
