from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
mars_data = client.mars_db

app = Flask(__name__)

@app.route('/')
def home():
	mars_info = mars_data.find_one()
	return render_template('index.html', mars=mars_info)


@app.route('/scrape')
def scrape():
	scrape_mars.scrape()

### I already added the data from the web scrape into my database in the scrape_mars.py file. 
### Not going to repeat that step here. 

if __name__ == "__main__":
    app.run(debug=True)


