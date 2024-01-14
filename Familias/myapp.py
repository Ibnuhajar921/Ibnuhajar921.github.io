from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Alamat Databasenya
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "familias"

mysql = MySQL(app)

app.secret_key = "Ini-sangat-rahasia"

def save_checkout_to_database(user_id, checkout_data):
    cur = mysql.connection.cursor()

    # Pastikan untuk mengganti nama tabel dan kolom sesuai dengan skema Anda
    cur.execute("""
        UPDATE user
        SET full_name = %s, street_name = %s, province = %s, district = %s,
            sub_district = %s, postal_code = %s, phone_number = %s, email = %s
        WHERE id = %s
    """, (
        checkout_data['full_name'], checkout_data['street_name'],
        checkout_data['province'], checkout_data['district'],
        checkout_data['sub_district'], checkout_data['postal_code'],
        checkout_data['phone_number'], checkout_data['email'],
        user_id
    ))

    mysql.connection.commit()
    cur.close()


@app.route("/")
def home():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user")
        users = cur.fetchall()
        cur.close()
        return render_template("home.html", data=users, username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/product')
def product():
    if 'is_logged_in' in session:
        return render_template("product.html")
    else:
        return redirect(url_for('login'))


@app.route('/season')
def season():
    if 'is_logged_in' in session:
        return render_template("season.html")
    else:
        return redirect(url_for('login'))


@app.route('/cart')
def shopping_cart():
    if 'is_logged_in' in session:
        return render_template("cart.html")
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['inpEmail']
        password = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id_user, username FROM user WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        if user:
            # Session
            session['is_logged_in'] = True
            session['id_user'] = user[0]  # Simpan user_id pada sesi
            session['username'] = user[1]
            # Redirect
            return redirect(url_for('home'))
        else:
            pesanError = "Cek email dan password kamu"
            return render_template("login.html", msg=pesanError)
    else:
        return render_template('login.html')


@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form['inpNama']
        email = request.form['inpEmail']
        password = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)",
                    (nama, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    else:
        return render_template('registration.html')


@app.route('/aboutus')
def aboutus():
    if 'is_logged_in' in session:
        return render_template("aboutus.html")
    else:
        return redirect(url_for('login'))


@app.route('/faqs')
def faqs():
    if 'is_logged_in' in session:
        return render_template("faqs.html")
    else:
        return redirect(url_for('login'))
    
@app.route('/location')
def location():
    if 'is_logged_in' in session:
        return render_template("location.html")
    else:
        return redirect(url_for('login'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Inisialisasi checkout_data jika belum ada
        session['checkout_data'] = session.get('checkout_data', {})

        # Proses pengisian checkout_data
        session['checkout_data']['full_name'] = request.form['inpFullName']
        session['checkout_data']['street_name'] = request.form['inpStreet']
        session['checkout_data']['province'] = request.form['inpProvince']
        session['checkout_data']['district'] = request.form['inpDistrict']
        session['checkout_data']['sub_district'] = request.form['inpSubDistrict']
        session['checkout_data']['postal_code'] = request.form['inpPostalCode']
        session['checkout_data']['phone_number'] = request.form['inpPhoneNumber']
        session['checkout_data']['email'] = request.form['inpEmail']

        # Simpan data checkout ke dalam database
        user_id = session['user_id']  # Gantilah dengan cara yang sesuai untuk mendapatkan user_id
        save_checkout_to_database(user_id, session['checkout_data'])

        # Bersihkan session checkout_data setelah disimpan
        session.pop('checkout_data', None)

        return redirect(url_for('product'))
    else:
        return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)