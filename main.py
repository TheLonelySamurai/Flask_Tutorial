from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text
from password import hash_password, decrypt_password
app = Flask(__name__)
# mysql://<username>:<password>@<host>/<database_name>
conn_str = "mysql://root:74CLpyrola!@localhost/bankdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


# render a file
@app.route('/')
def index():
    users = conn.execute(text("SELECT * FROM Accounts ORDER BY AccountID")).all()
    admins = conn.execute(text("SELECT * FROM Accounts")).all()
    conn.execute(text("TRUNCATE TABLE Login"))
    login = conn.execute(text("SELECT * FROM Login")).first()
    return render_template('index.html', users=users, admins=admins, login=login)

@app.route('/users')
def get_users():
    users = conn.execute(text(f"SELECT * FROM Accounts ORDER BY AccountID")).all()
    login = conn.execute(text("SELECT * FROM Login")).first()
    print(users)
    return render_template('users.html', users=users, login=login)
@app.route('/profile', methods=['GET'])
def get_profile_get_request():
    login = conn.execute(text("SELECT * FROM Login")).first()
    return render_template('logging.html', success=False, login=login)
@app.route('/profile', methods=['POST'])
def get_profile_from_login():
    #logic for login
    username = request.form['username']
    password = request.form['password']
    # Check if the username and password are correct
    user = conn.execute(text("SELECT * FROM Accounts WHERE Username = :username"), {'username': username}).first()
    admin = conn.execute(text("SELECT * FROM Admins WHERE Username = :username"), {'username': username}).first()
    login = conn.execute(text("SELECT * FROM Login")).first()
    if user:
        success = False
        # Check if the password matches the hashed password
        if decrypt_password(user.Password_hash, password):
            # Update the Login table to store the login information
            if user.approved == False:
                return render_template('logging.html', success=False, username=username, approved = False, admin=False)
            conn.execute(
                text("TRUNCATE TABLE Login")
            )
            conn.execute(
                text("INSERT INTO Login (Username, Password_hash, AdminAccount) VALUES (:username, :password, False)"),
                {'username': username, 'password': user.Password_hash}
            )
            login = conn.execute(text("SELECT * FROM Login")).first()
            print(login)
            # Password is correct, redirect to profile page
            success = True
        return render_template('logging.html', success=success, username=username, approved=True, admin=False, login=login)
    elif admin:
        if decrypt_password(admin.Password_hash, password):
            # Update the Login table to store the login information
            conn.execute(
                text("TRUNCATE TABLE Login")
            )
            conn.execute(
                text("INSERT INTO Login (Username, Password_hash, AdminAccount) VALUES (:username, :password, True)"),
                {'username': username, 'password': admin.Password_hash}
            )
            login = conn.execute(text("SELECT * FROM Login")).first()
            # Password is correct, redirect to profile page
            return render_template('logging.html', success=True, username=username, approved=True, admin=True, login=login)
        else:
            return render_template('logging.html', success=False, username=username, approved=True, admin=False, login=login)
@app.route('/profile/<username>', methods=['GET'])
def get_profile(username=None):
    login = conn.execute(text("SELECT * FROM Login")).first()
    admins = conn.execute(text("SELECT * FROM Admins")).all()
    if id != None:
        users = conn.execute(text("SELECT * FROM Accounts WHERE Username = :username"), {'username': username}).first()
        return render_template('profile.html', users=users, failure=False, login=login)
    else: 
        users = conn.execute(text(f"SELECT * FROM Accounts ORDER BY AccountID")).all()
        print(users)
        return render_template('index.html', users=users, failure=True, login=login, admins=admins)

@app.route('/admin', methods=['GET'])
def admin_get_request():
    login = conn.execute(text("SELECT * FROM Login")).first()
    users = conn.execute(text(f"SELECT * FROM Accounts ORDER BY AccountID")).all()
    admins = conn.execute(text("SELECT * FROM Admins")).all()
    return render_template('admin.html', users=users, admins=admins, login=login, success = None)
@app.route('/admin', methods=['POST'])
def admin_post_request():
    login = conn.execute(text("SELECT * FROM Login")).first()
    admins = conn.execute(text("SELECT * FROM Admins")).all()
    admin = conn.execute(text("SELECT * FROM Admins WHERE Username = :username"), {'username': login.Username}).first()
    if request.form['approved'] == '1':
        # Approve user
        # Save previus value of approved
        previous_approved = conn.execute(
            text("SELECT approved FROM Accounts WHERE AccountID = :id"),
            request.form
        ).first()
        conn.execute(
            text("UPDATE Accounts SET approved = True WHERE AccountID = :id"),
            request.form
        )
        new_approved = conn.execute(
            text("SELECT approved FROM Accounts WHERE AccountID = :id"),
            request.form
        ).first()
        #update the admin transcript table
        conn.execute(
            text(f"INSERT INTO AdminTranscript (AdminUsername, actionDate, accountID, rowChange, previousValue, newValue) VALUES ('{str(admin.Username)}', NOW(), :account_id, 'approved','{str(previous_approved)}', '{str(new_approved)}')"),
            {'account_id': request.form['id']}
        )
    elif request.form['approved'] == '0':
        # Reject user
        # Save previus value of approved
        previous_approved = conn.execute(
            text("SELECT approved FROM Accounts WHERE AccountID = :id"),
            request.form
        ).first()
        conn.execute(
            text("UPDATE Accounts SET approved = False WHERE AccountID = :id"),
            request.form
        )
        new_approved = conn.execute(
            text("SELECT approved FROM Accounts WHERE AccountID = :id"),
            request.form
        ).first()
        #update the admin transcript table
        conn.execute(
            text(f"INSERT INTO AdminTranscript (AdminUsername, actionDate, accountID, rowChange, previousValue, newValue) VALUES ('{str(admin.Username)}', NOW(), :account_id, 'approved','{str(previous_approved)}', '{str(new_approved)}')"),
            {'account_id': request.form['id']}
        ) 
    users = conn.execute(text(f"SELECT * FROM Accounts ORDER BY AccountID")).all()
    return render_template('admin.html', users=users, admins=admins, login=login, success="Updated successfully!")
@app.route('/admin/transcript', methods=['GET'])
def transcript_get_request():
    login = conn.execute(text("SELECT * FROM Login")).first()
    admins = conn.execute(text("SELECT * FROM Admins")).all()
    transcripts = conn.execute(text("SELECT * FROM AdminTranscript")).all()
    return render_template('admin_transcript.html', transcript=transcripts, login=login, admins=admins)
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
