from flask import Flask, url_for, render_template, jsonify, request, json
from flask.ext.mysql import MySQL
import wikipedia

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def det_exc(category):
  if "Articles" in category:
    return True
  elif "articles" in category:
    return True
  elif "introduction" in category:
    return True
  elif "Introduction" in category:
    return True
  elif "NPOV" in category:
    return True
  elif "Webarchive" in category:
    return True
  elif "pages" in category:
    return True
  elif "Pages" in category:
    return True
  elif "EngvarB" in category:
    return True
  elif "EngvarA" in category:
    return True
  elif "Wikipedia" in category:
    return True
  elif "Wikidata" in category:
    return True
  elif "Accuracy" in category:
    return True
  elif "accuracy" in category:
    return True
  elif "Interlanguage" in category:
    return True
  elif any(x in category for x in months):
    return True
  elif category[0:4] == "Use ":
    return True
  elif category[0:3] == "CS1":
    return True
  elif category[0:8] == "Commons ":
    return True
  elif category[0:6] == "Vague ":
    return True
  else:
    return False

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cs411fa2016'
app.config['MYSQL_DATABASE_DB'] = 'wiki'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def hello_world():
	return render_template("index.html")

@app.route('/insert', methods=['POST'])
def insertword():
    conn = mysql.connect()
    cursor = conn.cursor()
    keyword = request.form.get('keyword')
    insertword = request.form.get('insert')
    catword = request.form.get('cat')
    summary = request.form.get('summary')
    imageURL = request.form.get('imageURL')

    print summary

    sql_query = "INSERT INTO `TABLE 2` VALUES ('" + keyword + "', '" + catword + "')"
    cursor.execute(sql_query)
    conn.commit()
    sql_query = "INSERT INTO `TABLE 2` VALUES ('" + insertword + "', '" + catword + "')"
    cursor.execute(sql_query)
    conn.commit()
    sql_query = "SELECT * FROM `TABLE 1` WHERE title='" + insertword + "'"
    cursor.execute(sql_query)
    data = cursor.fetchall()
    if len(data) == 0:
        sql_query = "INSERT INTO `TABLE 1` VALUES ('" + str(insertword) + "', 'KEK', '" + str(summary) + "', '" + str(imageURL)+ "')"
        cursor.execute(sql_query)
        conn.commit()
        print "inserted"

    return json.dumps([])

@app.route('/autoinsert', methods=['POST'])
def insertdefault():
    conn = mysql.connect()
    cursor = conn.cursor()
    keyword = request.form.get('keyword')

    page = wikipedia.page(keyword)

    myCat = page.categories

    exclude_these = []
    for category in myCat:
        if (det_exc(category) == True):
            exclude_these.append(category)
            continue

    insertCat = [cat for cat in myCat if cat not in exclude_these]

    summary = page.content.split('\n')[0].encode('ascii', 'replace')
    images = page.images

    if (images):
        imageUrl = images[0]
    else:
        imageUrl = ''

    cursor.execute("INSERT INTO `TABLE 1` VALUES ('" + page.title + "', '" + page.url + "', '" + summary + "', '" + imageUrl + "')")
    conn.commit()

    for cat in insertCat:
        cursor.execute("INSERT INTO `TABLE 2` VALUES ('" + page.title + "', '" + cat + "')");
        conn.commit()


    print insertCat
    return json.dumps([])


@app.route('/query', methods=['POST'])
def testquery():
    keyword = request.form.get('keyword')

    cursor = mysql.connect().cursor()
    print "starting mysql"

    cursor.execute("SELECT * FROM `TABLE 1` WHERE title='" + keyword + "'")
    if not cursor.rowcount:
        return json.dumps(["NULL"]);

    myData = cursor.fetchone()

    print myData;
    myObj = {}
    myObj["title"]=myData[0]
    myObj["url"]=myData[1]
    myObj["summary"]=myData[2]
    myObj["images"]=myData[3]

    sql_query = "SELECT title FROM (SELECT title FROM (SELECT * FROM (SELECT t1.category AS cat1 FROM `TABLE 2` AS t1 WHERE t1.title = '" + keyword  + "') AS A CROSS JOIN (SELECT t2.category AS cat2, t2.title AS title FROM `TABLE 2` AS t2 WHERE t2.title<>'" + keyword + "') AS B) AS C WHERE cat1=cat2) AS D GROUP BY title HAVING COUNT(title)>0"
    print sql_query
    cursor.execute(sql_query)
    data = cursor.fetchall()
    myList = []
    print str(data)
    for z in data:
        myList.append(z[0]);
    print myList

    returnList = []
    returnList.append(myObj);

    for x in myList:
        temp_sql_query = "SELECT * FROM `TABLE 1` WHERE title='" + x + "'"
        print temp_sql_query
        cursor.execute(temp_sql_query)
        newData = cursor.fetchone()
        someList = []
        for y in newData:
            someList.append(y)

        returnList.append(someList)


    return json.dumps(returnList)

    """
    currData = {}
    currData["title"] = curr.title
    currData["summary"] = curr.summary.split('.')[0]
    currData["categories"] = curr.categories
    currData["pictures"] = curr.images
    return json.dumps(currData)
    """
    """
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
	"""
app.run(host='0.0.0.0')
