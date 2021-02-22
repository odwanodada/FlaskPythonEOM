from flask import Flask,render_template,request,jsonify

app = Flask(__name__)

person = [{
    'id': 1,
    'name': 'Odwa',
    'surname': 'Nodada',
    'Academy': 'LifeChoices',
    'Skills': 'Html,Css,Js'
},

{
    'id': 2,
    'name': 'Victor',
    'surname': 'Nkuna',
    'Academy': 'LifeChoices',
    'Skills': 'Html,Css,Js,Python'
},

{
    'id': 3,
    'name': 'Tabag',
    'surname': 'Duda',
    'Academy': 'CodeSpace',
    'Skills': 'Html,Css,React,js,Node'
},
]

@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')

@app.route('/index', methods=['GET'])  
def api_all():
    return jsonify(person)






if __name__ == '__main__':
    app.run(debug=True)    