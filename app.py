from flask import Flask,render_template,request
from model import get_rec
from byFeatureModel import recommendByFeature
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predicte/title',methods=['POST'])
def recommend():
    if request.method == 'POST' and request.form['movie']!= '' :
        movies=get_rec(request.form['movie'])
        return render_template('index.html',movies=movies,name=request.form['movie'])
    else :
        return render_template('index.html')

@app.route('/predicte/features',methods=['POST'])
def recommendByTags():
     if request.method == 'POST' :
        print(request.form)
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
