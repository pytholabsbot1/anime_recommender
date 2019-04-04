#!/usr/bin/env python
from flask import Flask, render_template, Response,request,jsonify
import lightfm,pickle,os,requests as req
from recsys import *
from generic_sys import *

model= pickle.load(open( "model.pickle", "rb" ))   

anime_dict =  pickle.load(open('dict.pickle','rb'))

# print(rec_list)
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

def download_images(anime_list):

    l = []

    for anime_name in anime_list:
        try:
            res = req.get('https://www.bing.com/images/search?q='+anime_name+" anime poster")
            img_link = res.text.split('<a class="thumb" target="_blank" href="')[1].split('"')[0]
            l.append(img_link)
        except:
            l.append("0")

    return(l)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/recommend')
def recommend():
    r = request.args.get('queryId')

    rec_list = item_item_recommendation(item_emdedding_distance_matrix = model,
                                    item_id = int(r),
                                    item_dict = anime_dict,
                                    n_items = 10)


    q = anime_dict[int(r)]
    res = [anime_dict[i] for i in rec_list]
    img_links = download_images(res)

    imgs = {res[i]:img_links[i] for i in range(len(res))}
    print('done recommending')       
    return render_template('recomnd.html',users=imgs,q=q)

@app.route('/message')
def message():
    """Video streaming home page."""
    
    r = request.args.get('query')
    
    print(r)

    # res = {}
    # if(c==0):
    res = {str(i):anime_dict[i] for i in anime_dict if(r in anime_dict[i].lower())}
    #print(res)

    print('done')       
    return jsonify(res)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,threaded=True)


