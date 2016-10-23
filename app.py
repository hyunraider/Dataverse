from flask import Flask, url_for, render_template, jsonify, request, json
from flask.ext.mysql import MySQL
from wikimarkup import parse

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cs411fa2016'
app.config['MYSQL_DATABASE_DB'] = 'wiki'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

html = ""
db = []

@app.route('/')
def hello_world():
	return render_template("index.html", dbs=db)

@app.route('/query', methods=['POST'])
def testquery():
	cursor = mysql.connect().cursor()
	print "starting mysql"
    	keyword = request.form.get('keyword')
    	print "query successful"
	print keyword
	substr = "SELECT * from page where page_title='"
    	fullquery = substr + keyword + "'";
    	result = cursor.execute(fullquery)
	
	print "query done"
	print result

	data = cursor.fetchone()
	print data
	
	db.append(data);
	#old_id = data[6]
	#substr = "SELECT old_text from text where old_id='"
	#fullquery = substr + str(old_id) + "'"
	#result = cursor.execute(fullquery)
	#print "second query done"
	#print result

	#data = cursor.fetchone()
	#print data
	#db.append(data)
	#db.append(parse(data))
	return json.dumps(data)

app.run(host='0.0.0.0')
