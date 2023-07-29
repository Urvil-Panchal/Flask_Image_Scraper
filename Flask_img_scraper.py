from flask import Flask , request , render_template
import urllib.parse
import requests
from bs4 import BeautifulSoup as bs
import os

app = Flask(__name__)

@app.route("/" , methods=["POST" , "GET"])
def Home():
    
    return render_template('index.html')


@app.route('/success' , methods=['POST' , "GET"])
def logic():
    if request.method=='POST':
        query=request.form['img']

    
    save_dir = "images/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    query_uncoded = urllib.parse.quote(query)
    #The reason we use query_encoded instead of query is to properly handle 
    # special characters and spaces in the search query when constructing the URL
    
    response = requests.get(f"https://www.google.com/search?sxsrf=AB5stBiKUIC4nSYOZqAmjzbziW63nF1VSQ:1690654990823&q={query_uncoded}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwj4r6nRxLSAAxVZcmwGHaKFBZ0Q0pQJegQIDRAB&biw=1536&bih=707&dpr=1.25")

    soup = bs(response.content , 'html.parser')

    img_tags = soup.find_all("img")

    del img_tags[0]

    store_img =[]

    for i in img_tags:
        img_url = i['src']
        img_data = requests.get(img_url).content
        mydict = {"index" : img_url , "image" : img_data}
        store_img.append(mydict)

        with open(os.path.join(save_dir, f"{query}_{img_tags.index(i)}.jpg") , "wb") as f:
            f.write(img_data)

    return render_template('success.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="1313")