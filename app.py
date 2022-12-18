from flask import Flask,render_template,request
from model import get_rec
from byFeatureModel import recommendByFeature
from utils.formating import collapse,deleteSpaces,toLower
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict/title',methods=['POST','GET'])
def recommend():
    if request.method == 'POST' and request.form['movie']!= '' :
        movies=get_rec(request.form['movie'])
        return render_template('byTitle.html',movies=movies,name=request.form['movie'])
    elif request.method=='GET':
        return render_template('byTitle.html')
    else :
        return render_template('byTitle.html',movies=movies,name=request.form['movie'])

@app.route('/predict/features',methods=['POST','GET'])
def recommendByTags():
     if request.method == 'POST' :
        movie=request.form['movie']
        if movie!='':
            movie=deleteSpaces(movie)
        else:
            movie=' '

        gernes=request.form['genres']
        if gernes!='':
            gernes=gernes.lower()
        else : 
            gernes=' '
        star=request.form['star']
        if star!='':
            star=deleteSpaces(star)
        else :
            star=' '

        director=request.form['director']
        if director!='':
            director=deleteSpaces(director)
        else :
            director=' '

        list=[movie,gernes,star,director]
        print(list)
        ans=recommendByFeature(list)
        print(ans)
        return render_template('byFeatures.html',moviesByf=ans)
     elif request.method=='GET':
        return render_template('byFeatures.html')
if __name__=="__main__":
    app.run(debug=True)
