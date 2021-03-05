import sqlite3
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS



def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

 

  

    
    conn.execute('CREATE TABLE IF NOT EXISTS customers (id integer primary key autoincrement, name TEXT, email TEXT, password TEXT, cart TEXT)')
    print("Table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS Items (id integer primary key autoincrement, Title TEXT, Author TEXT, Genres TEXT, Originally_published TEXT, Price integer ,Images TEXT)')
    print("Table created successfully")

    
   
    conn.close()

init_sqlite_db()


app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d    

@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')

@app.route('/add-books/', methods=['POST'])  
def add_products():
    if request.method == 'POST':

        try:
            post_data = request.get_json()
            Title = post_data['title']
            Author = post_data['author']
            Genres = post_data['genres']
            Originally_published = post_data['originally_published']
            Price = post_data['price']
            Images = post_data['images']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                con.row_factory = dict_factory
                cur.execute("INSERT INTO Items (Title, Author, Genres, Originally_published, Price,Images) VALUES (?, ?, ?, ?, ?, ?)",
                 (Title, Author, Genres, Originally_published,Price, Images))
                con.commit()
                msg = "Record successfully added"
          
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            return {'msg' : msg}   

     
  
@app.route('/show-items/', methods=["GET"])
def show_items():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Items")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database." + str(e))
    finally:
        return jsonify(records)
        con.close()


@app.route('/delete-records/<int:books_id>/', methods=["GET"])
def delete_users(books_id):
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Items WHERE id=" + str(books_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg)        

   


if __name__ == '__main__':
    app.run(debug=True) 