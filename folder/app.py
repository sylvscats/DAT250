import functools
from flask import Flask, render_template, url_for, request, session, flash, g, redirect
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
connection = sqlite3.connect('user_database.db')
def get_db_connection():
    conn = sqlite3.connect('user_database.db')
    conn.row_factory = sqlite3.Row
    return conn
app = Flask(__name__)
app.secret_key = "abbas"

@app.route('/')
def index():
    return render_template('hjemmeside.html')
@app.route("/view")
def view():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('view.html', users=users)

@app.route("/login", methods=["GET", "POST"])
def login():
                 if request.method == 'POST':
                     personnum = request.form['personnumber'] 
                     passw = request.form['password']
                     if not personnum:
                         error = 'personnumber is required.'
                     elif not passw:
                             error = 'Password is required.'
                     else:        
                       conn = get_db_connection()
                       found_user = conn.execute('SELECT * FROM users WHERE personnumber = ?;',[personnum]).fetchall()
                       conn.commit()
                       conn.close() 
                       if not found_user:
                                error = "you dont have account, join us now" 
                                return redirect(url_for('signup'))
                       else:
                           password = found_user[0]['password']
                           result=check_password_hash(password,passw)
                           if result == True: 
                               user_id = found_user[0]['id']
                               print(user_id)
                               return redirect( url_for('user',usr=user_id))                             
                           else:
                              error = 'wrong password !!'
                     flash(error)
                 return render_template("login.html")

@app.route('/signup', methods=('GET', 'POST'))
def signup():
              if request.method == 'POST':
                 name = request.form['name']
                 personnumber = request.form['personnumber']
                 email = request.form['email']
                 address = request.form['address']
                 password = request.form['password']
                 if not name:
                         error = 'name is required.'
                 elif not personnumber:
                         error = 'personnumber is required.'
                 elif not email:
                         error = 'email is required.'
                 elif not address:
                         error = 'address is required.'
                 elif not password:
                         error = 'Password is required.'
                
                 else:  
                         hashed_pass=generate_password_hash(password)
                         conn = get_db_connection()
                         conn.execute('INSERT INTO users (name, personnumber, email, address, password, AvailableBalance) VALUES (?, ?, ?, ?, ?, ?)',
                          (name, personnumber, email, address, hashed_pass, 100))
                         conn.commit()
                         conn.close() 
                         return redirect(url_for('login'))

                 flash(error)
              return render_template('signup.html')
@app.route("/user/<usr>", methods=('GET', 'POST'))
def user(usr): 
    conn = get_db_connection()                                          
    sender_user_val = conn.execute('SELECT AvailableBalance FROM users WHERE id = ' + usr + ';').fetchone()
    conn.commit()
    conn.close()
    if request.method == 'POST': 
                            reciver = request.form['reciver']
                            val = request.form['val']
                            if not reciver:
                                    flash(f"we nedd the personnumber.", "info")
                            elif not val:
                                        flash(f"How much do you want to send.", "info") 
                                
                            else:  
                                        
                                conn = get_db_connection()            
                                reciver_user= conn.execute('SELECT * FROM users WHERE personnumber = ' + reciver + ';').fetchone()
                                reciver_user_val= conn.execute('SELECT AvailableBalance FROM users WHERE  personnumber= ' + reciver +';').fetchone()
                                conn.commit()
                                conn.close()
                                if not reciver_user:
                                        flash(f"not avaliabel konto", "info")
                                else:
                                        converted_val = int(val) 
                                        if converted_val > sender_user_val[0]:

                                             flash(f"sorry you dont have enogh mony", "info")
                                        else:
                                              conn = get_db_connection()                                    
                                              print(reciver_user_val[0])
                                              new_sender_val= sender_user_val[0]-converted_val                       
                                              new_reciver_val= reciver_user_val[0]+converted_val
                                              converted_new_sender_val=str(new_sender_val)
                                              converted_new_reciver_val=str(new_reciver_val)
                                              conn.execute('UPDATE users SET AvailableBalance = ' +converted_new_sender_val+' WHERE id =' + usr + ';').fetchone() 
                                              conn.execute('UPDATE users SET AvailableBalance = '+ converted_new_reciver_val+' WHERE personnumber =' + reciver + ';').fetchone()                                        
                                              conn.commit()
                                              conn.close()
                                              flash(f"ok", "info")
                                       

    return render_template('user.html', users=sender_user_val)
@app.route("/logout")
def logout():
    flash(f"you are now logged out", "info")
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)