from flask import Flask,render_template,request,redirect

app=Flask(__name__)
 
@app.route('/hello/<who>')
def hello_world(who):

    return render_template('pozdrav.html',kto=who) 

@app.route('/factorial')
def factorial():

    fact=[]
    n=1
    for i in range(1,10):
        n=n*i
        fact.append((i,n))

    return render_template('tabulate.html',data=fact,function='faktoriál',headerx='n',headery='n!')

@app.route('/form',methods=['GET','POST'])
def reg():
    if request.method=='GET':
        return render_template("form.html")
    else: # POST
        print(request.form['meno'])
        print(request.form['priezvisko'])
        return redirect('/hello/'+request.form['meno'])


