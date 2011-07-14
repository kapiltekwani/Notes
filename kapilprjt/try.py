from pymongo.connection import Connection
from flask import Flask , redirect , url_for, request
connection = Connection("localhost")

app = Flask(__name__)

db = connection.foo
 
@app.route("/")
def view():
    cursor = db.foo.find({"state":"0"})
    #cursor =foo.cappedcol.find({}).sort({'$natural':-1})
    str1="<html><body><div><h3>TaSk MaNaGeR,</h3><form name=\"add\" action=\"addnote\" method=\"POST\">Title<input type=\"text\" name=\"title\" />"
    str1=str1+"<br>task<input type=\"text\" name=\"task\" /><input type=\"submit\" name=\"press\" value=\"Save\"/></form>"
    str1=str1+ "<form name=\"update\" action=\"update_state\" method=\"POST\"><table><tr><td></td><td><h3>TaSk LeFt</h3></td></tr><tr><td>Check</td><td>Title</td><td>Task</td></tr>"
    for d in cursor:
        str1=str1+"<tr><td><input type=\"checkbox\" name=\"state[]\" "
        if d["state"]==str(1) :
            str1=str1+"value=\""+str(d["index"])+"\" checked=\"yes\""
        else:
            str1=str1+"value=\""+str(d["index"])+"\" "
        str1=str1+"\></td><td>"+str(d["title"])+"</td><td>"+str(d["task"])+"</td></tr>"
    cursor = db.foo.find({"state":"1"})
    str1=str1+"<tr></tr><tr><td></td><td><h3>TaSk DoNe</h3></td></tr>"
    for d in cursor:
        str1=str1+"<tr><td><input type=\"checkbox\" name=\"state[]\" "
        if d["state"]==str(1) :
            str1=str1+"value=\""+str(d["index"])+"\" checked=\"yes\""
        else:
            str1=str1+"value=\""+str(d["index"])+"\" "
        str1=str1+"\></td><td>"+str(d["title"])+"</td><td>"+str(d["task"])+"</td></tr>"
    str1=str1 +"<input type=\"submit\" value=\"Done\" /> </form>"
    str1=str1+"</table></div></body></html>"
    return str1

@app.route("/addnote", methods=['POST'])
def addnote():
    new=db.foo.count()
       # if len(request.form['title']==0 || len(request.form['task']==0     #validation for empty text boxes.
    if len(request.form['title'])!=0 and len(request.form['task'])!=0:
        doc3={"index":int(new+1), "title":request.form['title'], "task":request.form['task'], "state":"0"}
        db.foo.save(doc3)
       
    return redirect(url_for('view'))

@app.route("/update_state", methods=['POST'])
def update_state():
    arr=[]
    arr=request.form.getlist('state[]')
    i=1
    while i<db.foo.count():
        db.foo.update({"index": int(i)}, {"$set":{"state":"0"}})
        i=i+1
    i=0    
    for i in arr:
        db.foo.update({"index":int(i)}, {"$set":{"state":"1"}})
        
    #return i
    #db.foo.find().sort({"state":"0"});
    return redirect(url_for('view'))

    

if __name__ == "__main__":
	app.debug = True
	app.run()
