from flask import Flask, request, url_for, Flask,redirect
from flask_pymongo import PyMongo
from forms import LoginForm, SignupForm,Post,PostText,EditUser,ProductForm
from flask import Flask, render_template, request
from flask import request, abort, make_response
from base64 import b64encode
import os
import pymongo
import platform
import socket
import subprocess
import shlex
import re
import requests
from datetime import date
import datetime
import random, threading, webbrowser
from neo4j import GraphDatabase

class Product:
  def __init__(self, name, price,usname):
    self.name = name
    self.price = price
    self.username=usname    

g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"))
session=g.session()

app = Flask(__name__)
app.config['SECRET_KEY']='fshfhjdchbDAHC234GFGJHJ'


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    form=LoginForm()
    return render_template('login.html',form=form)

@app.route('/login',methods=['POST'])
def login_after():
    form=LoginForm()
    g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"));
    session=g.session()
    s=''
    mes="Invalid credentials"
    us=request.form['username']
    ps=request.form['password']
    q1="match(n:user) where n.username='"+us+"' and n.password='"+ps+"' return ID(n)"
    nodes=session.run(q1)
    for n in nodes:
        s=s+str(n["ID(n)"])
    if(s):
         return redirect(url_for('people',usname=us))
    else:
        return render_template('login.html',form=form,mes=mes)

@app.route('/userLogin')
def afterlogin():
    return render_template('afterlogin.html')

@app.route('/signup')
def signup():
    form=SignupForm()
    return render_template('singup.html',form=form)

@app.route('/signup',methods=['POST'])
def signup_after():
    form=SignupForm()
    g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"));
    session=g.session()
    s=''
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    us=request.form['username']
    ps=request.form['password']
    cps=request.form['cpassword']
    em=request.form['email']
    up=request.form['updates']
    bday=request.form['bday']
    value= datetime.datetime.strptime(bday, '%Y-%m-%d').date()
    today=date.today()
    if(up=='1'):
        up='Home Based seller'
    elif(up=='2'):
        up='Whole saler'
    else:
        up='Just Gonna purchase'
    q0="match(n:user) where n.username='"+us+"' return ID(n)"
    nodes=session.run(q0)
    for n in nodes:
        s=s+str(n["ID(n)"])
    if (cps!=ps):
        message="Password doesnt match"
    elif (s):
        message="Already username exists!"
    elif(bool(re.search(regex,em))==False):
        message="Invalid Email Id"
    elif today<value:
        message="Date should not be in future!"
    else:
        q1="create(u:user{username:'" + us + "',bday:'"+bday+"',password:'" + ps + "',email:'" + em + "',role:'"+up+"',date_created:date()}) return u"
        nodes=session.run(q1)
        message="Sign up successful"
    return render_template('singup.html',form=form,message=message)

##@app.route('/people')
##def people():
##    form=PostText()
##    usname=request.args.get('usname')
##    pep={}
##    l=[usname]
##    q1="match(u:user) return u.username as uname, u.role as role"
##    nodes=session.run(q1)
##    for n in nodes:
##        pep[n["uname"]]=n["role"]
##    print(pep)
##    del pep[usname]
##    with open("F:/GreenTree/money.jpg","rb") as image:
##        f=image.read()
##        b=bytearray(f)
##    image=b64encode(b).decode("utf-8")
##    return render_template('people.html',pep=pep,us=usname,image=image,form=form)


@app.route('/people')
def people():
    g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"));
    session=g.session()
    form=PostText()
    usname=request.args.get('usname')
    total={}
    follow=[]
    d={}
    p={}
    q1="match(u:user{username:'"+usname+"'})-[f:follows]->(d:user) return d.username as users"
    q2="match(n:user) return n.username as users,n.role as role"
    q3=s="match(u:user{username:'"+usname+"'})-[f:follows]->(n:user) match (n:user)-[p:posted]->(z:post) return z.value,n.username,p.ontime"
    q4="match(u:user{username:'"+usname+"'})-[p:posted]->(p1:post) return u.username,p1.value,p.ontime"
    nodes=session.run(q1)
    nodes2=session.run(q2)
    nodes3=session.run(q3)
    nodes4=session.run(q4)
    for n in nodes3:
        p.setdefault(n['n.username'], []).append([n['z.value'],n['p.ontime']])
    for n in nodes4:
        p.setdefault(n['u.username'], []).append([n['p1.value'],n['p.ontime']])
    role=0
    for n in nodes:
        follow.append(n['users'])
    for n in nodes2:
        total[n['users']]=n['role']
        role=n['role']
    print(total[usname])
    role=total[usname]
    if role=="Just Gonna purchase":
        role=0
    else:
        role=1
    del total[usname]
    for k,v in total.items():
        if k in follow:
            d[k]=1
        else:
            d[k]=0
    print(d)
    with open("F:/GreenTree/money.jpg","rb") as image:
        f=image.read()
        b=bytearray(f)
    image=b64encode(b).decode("utf-8")
    return render_template('people123.html',d=d,us=usname,image=image,role=role,form=form,p=p)

@app.route('/feeds')
def view_feeds():
    us=request.args.get('us')
    post=request.args.get('usp')
    x=datetime.datetime.now()
    q1="match(u:user{username:'"+us+"'}) create (p:post{value:'"+post+"'}) create (u)-[p1:posted{ontime:'"+x.strftime("%d-%b-%Y %I:%M:%S %p")+"'}]->(p)"
    session.run(q1)
    return redirect(url_for('people',usname=us))
    

@app.route('/follow')
def follow():
    pep={}
    g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"));
    session=g.session()
    q0="match(u:user) return u.username as uname, u.role as role"
    nodes=session.run(q0)
    for n in nodes:
        pep[n["uname"]]=n["role"]
    usname  = request.args.get('usname', None)
    folname  = request.args.get('folname', None)
    value  = request.args.get('value', None)
    print(value)
    if(int(value)==0):
        l=[usname]
        q1="match(n:user{username:'"+usname+"'}),(u:user{username:'"+folname+"'}) create (n)-[f:follows{from:date()}]->(u)"
        session.run(q1)
    else:
        q2="match(u1:user{username:'"+usname+"'})-[f:follows]-(u2:user{username:'"+folname+"'}) delete f"
        session.run(q2)
    return redirect(url_for('people',usname=usname))

##@app.route('/post/<us>')
##def post(us):
##    b=""
##    l=[]
##    image=""
##    form=Post()
##    q1="match(p:post{by:'"+us+"'}) return p.value"
##    nodes=session.run(q1)
##    if(nodes.peek()):
##        for n in nodes:
##            b=bytearray(n['p.value'],'utf8')
##        image=b64encode(b).decode("utf-8")
##        return render_template("post.html",form=form,image=image)
##    else:
##        return render_template("post.html",form=form)

##@app.route('/post/<us>',methods=['POST'])
##def postafter(us):
##    form=Post()
##    files=request.form["files"]
##    with open(files,"rb") as image:
##        f=image.read()
##        b=bytearray(f)
##    image=b64encode(b).decode("utf-8")
##    session.run("CREATE (p:post {by:'"+us+"',value:'"+str(image)+"'})")
##    return render_template("post.html",form=form,image=image)

@app.route('/edit')
def edit():
    g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"));
    session=g.session()
    role=''
    date=''
    us=request.args.get('usname')
    q1="match(p:user{username:'"+us+"'}) return p.role as role, p.date_created as date"
    q2="MATCH (n:user{username:'"+us+"'})-[r]->() RETURN COUNT(r)"
    q3="MATCH (n:user{username:'"+us+"'})<-[r]-() RETURN COUNT(r)"
    nodes=session.run(q1)
    follow=session.run(q2)
    follow_by=session.run(q3)
    d1={}
    for c in follow:
        d1['Follows']=(c['COUNT(r)'])
    for f in follow_by:
        d1['Followed by']=(f['COUNT(r)'])
    for n in nodes:
        role=n['role']
        date=n['date']
    return render_template('edit_profile.html',us=us,role=role,date=date,d1=d1)
    
@app.route('/edit-us')
def edit_us():
    g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"));
    session=g.session()
    us=request.args.get('us')
    usp=request.args.get('usp')
    q1="match(n:user{username:'"+us+"'}) set n.username='"+usp+"'"
    session.run(q1)
    return redirect(url_for('edit',usname=usp))

@app.route('/edit-rs')
def edit_rs():
    g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"));
    session=g.session()
    us=request.args.get('us')
    usp=request.args.get('usp')
    q1="match(n:user{username:'"+us+"'}) set n.role='"+usp+"'"
    session.run(q1)
    return redirect(url_for('edit',usname=us))

@app.route('/edit-ps')
def edit_ps():
    g=GraphDatabase.driver(uri='bolt://localhost:7687',auth=("neo4j","hema13"));
    session=g.session()
    us=request.args.get('us')
    usp=request.args.get('usp')
    q1="match(n:user{username:'"+us+"'}) set n.password='"+usp+"'"
    session.run(q1)
    return redirect(url_for('edit',usname=us))

@app.route('/addProduct')
def addProduct():
    form=ProductForm()
    return render_template('addProduct.html',form=form)

@app.route('/addProduct',methods=['POST'])
def addProduct1():
    loc=[]
    usname=request.args.get('usname')
    form=ProductForm()
    name=request.form['name']
    category=request.form['category']
    if(category=='1'):
        c="Indoor"
    if(category=='2'):
        c="Outdoor"
    if(category=='3'):
        c="Decorative"
    price=request.form['price']
    file=request.form['file']
    q2="create(p:product{name:'"+name+"',price:'"+str(price)+"',category:'"+c+"',postedBy:'"+usname+"',imageUrl:'"+file+"'}) return ID(p)"
    q3="match(p:product{name:'"+name+"'}),(n:user{username:'"+usname+"'}) create (n)-[o:owns]->(p)"
    print(q2)
    print(q3)
    nodes=session.run(q2)
    nodes1=session.run(q3)
    location=request.form.getlist('location')
    for l in location:
        if(l=='1'):
            session.run("match(p:product{name:'"+name+"'}),(l:location{name:'Vellore'}) create (p)-[a:available_in]->(l)")
        if(l=='2'):
            session.run("match(p:product{name:'"+name+"'}),(l:location{name:'Chennai'}) create (p)-[a:available_in]->(l)")
        if(l=='3'):
            session.run("match(p:product{name:'"+name+"'}),(l:location{name:'Bangalore'}) create (p)-[a:available_in]->(l)")
        if(l=='4'):
            session.run("match(p:product{name:'"+name+"'}),(l:location{name:'Hyderabad'}) create (p)-[a:available_in]->(l)")
    print(name,price,c,loc,file,usname)
    return render_template('addProduct.html',form=form)

@app.route('/purchase')
def purchase():
    l=[]
    usname=request.args.get('usname')
    mes=request.args.get('mes')
    q5="match(u:user{username:'"+usname+"'})-[f:follows]->(n:user) match(n:user)-[o:owns]->(p:product) return n.username,p.price,p.name"
    nodes=session.run(q5)
    for n in nodes:
        p=Product(n['p.name'],n['p.price'],n['n.username'])
        l.append(p)
    return render_template('purchase.html',l=l,us=usname,mes=mes)


def checkCart(usname):
  q4="match(n:user{username:'"+usname+"'})-[h:has]->(c:cart) return ID(c)"
  nodes=session.run(q4)
  if(nodes.peek()):
    for n in nodes:
      var=n['ID(c)']
  else:
    var="None"
  return var
  

@app.route('/cart')
def cart():
    usname=request.args.get('usname')
    product=request.args.get('product')
    cart_id=checkCart(usname)
    if cart_id!="None":
      q3="match (u:user{username:'"+usname+"'})-[h:has]->(c:cart), (p:product{name:'"+product+"'}) create (c)-[c1:contains]->(p)"
      session.run(q3)
    else:
      #create cart
      q5="match(u:user{username:'"+usname+"'}) create (u)-[h:has]->(c:cart)"
      q3="match (u:user{username:'"+usname+"'})-[h:has]->(c:cart), (p:product{name:'"+product+"'}) create (c)-[c1:contains]->(p)"
      session.run(q5)
      session.run(q3)
    mes="product "+product+" added to cart!"
    print(mes)
    return redirect(url_for('purchase',usname=usname,mes=mes))

@app.route('/showCart')
def showCart():
  l=[]
  total=0
  usname=request.args.get('usname')
  q6="match(u:user{username:'"+usname+"'})-[h:has]-(c:cart)-[c1:contains]-(p:product) return p.name,p.price"
  nodes=session.run(q6)
  for n in nodes:
    total=total+int(n['p.price'])
    p=Product(n['p.name'],n['p.price'],usname)
    l.append(p)
  return render_template('showCart.html',l=l,total=total,usname=usname)

@app.route('/Emptycart')
def emptycart():
  usname=request.args.get('usname')
  q7="match(u:user{username:'"+usname+"'})-[h:has]-(c:cart)-[c1:contains]-(p:product) delete c1"
  session.run(q7)
  return redirect(url_for('showCart',usname=usname))
  

  
    
if __name__=='__main__':
    app.run(debug=True,port=9999)
    
