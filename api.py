import sqlite3
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d    

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS person (id integer primary key autoincrement, name TEXT, surname TEXT, academy TEXT, skills TEXT, gender TEXT)')
    print("Table created successfully")


    conn.execute('CREATE TABLE IF NOT EXISTS books (id integer primary key autoincrement, Title TEXT, Author TEXT, Genres TEXT, Originally_published TEXT, Price TEXT)')
    print("Table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS customers (id integer primary key autoincrement, name TEXT, email TEXT, password TEXT, cart TEXT)')
    print("Table created successfully")

   
    conn.close()

init_sqlite_db()


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')

@app.route('/add-books/', methods=['POST'])  
def add_products():
    if request.method == 'POST':

        try:
            Title = request.form['title']
            Author = request.form['author']
            Genres = request.form['genres']
            Originally_published = request.form['op']
            Price = request.form = request.form['price']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO books (Title, Author, Genres, Originally_published, Price) VALUES (?, ?, ?, ?, ?)",
                 (Title, Author, Genres, Originally_published,Price))
                con.commit()
                msg = "Record successfully added"
          
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)   

     
  
@app.route('/show-items/', methods=["GET"])
def show_items():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM books")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)



if __name__ == '__main__':
    app.run(debug=True)    