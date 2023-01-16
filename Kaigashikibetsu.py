import os
from flask import Flask, request, redirect, render_template, flash,url_for
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
import numpy as np
#import cv2

classes = ["Gohh","Kandinsky"]
image_size = 100

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
#ここの意味がわからない
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model('./model.h5')#学習済みモデルをロード


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)


            #受け取った画像を読み込み、np形式に変換
            img = image.load_img(filepath, grayscale=False, color_mode = 'rgb',target_size=(100,100))
            uploaded = image.load_img(filepath, grayscale=False, color_mode = 'rgb',target_size=(100,100))
            img = image.img_to_array(img)

            def pred_art(img):
                #img = cv2.resize(img, (100, 100))
                pred = np.argmax(model.predict(np.array([img])))
                if pred == 0:
                    return 'Gogh'
                else:
                    return 'Kandinskiy'

            pred_answer = "あなたのアップロードした絵は " + pred_art(img) + " です"

            return render_template("index.html",answer=pred_answer, filepath=filepath)
    return render_template("index.html", answer="")


'''if __name__ == "__main__":
    app.run()'''
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)
