from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from analysis import predict


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Sentiment_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweets = db.Column(db.String(200), nullable=False)
    sentiment = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/",methods=['GET','POST'])
def index():
    if request.method == "POST":
        tweet_content = request.form["tweet"]

        tweet_content = predict(tweet_content)
        print(tweet_content["text"])
        print(tweet_content["label"])
        print(tweet_content["score"])
        

        if tweet_content != "":
            new_sentiment = Sentiment_db(tweets=tweet_content["text"],sentiment=tweet_content["label"],score="%.3f" % tweet_content["score"])
            

        try:
            db.session.add(new_sentiment)
            db.session.commit()
            return redirect("/")
        
        except:
            return "There was an issue adding your tweet!"
        
    else:
        sentiments = Sentiment_db.query.order_by(Sentiment_db.id.desc()).all()
        return render_template("index.html",sentiments=sentiments)

@app.route("/delete/<int:id>")
def delete(id):
    sentiment_to_delete = Sentiment_db.query.get_or_404(id)

    try:
        db.session.delete(sentiment_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task!"
    



if __name__ == "__main__": 
    with app.app_context():
        db.create_all()
        print("Database and tables created.")

    app.run(debug=True)
