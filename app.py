# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 10:59:51 2020

@author: Amritansh Vajpayee
"""

import tensorflow as tf
import cv2 as cv
import flask, werkzeug
app = flask.Flask(import_name="CaMicrosopeChallenge")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["CACHE_TYPE"] = "null"
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
def extractFeatures():
    img = flask.request.files["img"]
    img_name = img.filename
    img_secure_name = werkzeug.secure_filename(img_name)
    img.save(img_secure_name)
    classes_90 = ["background", "person", "bicycle", "car", "motorcycle",
            "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
            "unknown", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
            "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "unknown", "backpack",
            "umbrella", "unknown", "unknown", "handbag", "tie", "suitcase", "frisbee", "skis",
            "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
            "surfboard", "tennis racket", "bottle", "unknown", "wine glass", "cup", "fork", "knife",
            "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
            "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "unknown", "dining table",
            "unknown", "unknown", "toilet", "unknown", "tv", "laptop", "mouse", "remote", "keyboard",
            "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "unknown",
            "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush" ]
    with tf.gfile.FastGFile('frozen_inference_graph.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Session() as sess:
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

    # Reading and preprocessing the image.
        img = cv.imread(img_secure_name)
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

    # Running the model
        out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                    sess.graph.get_tensor_by_name('detection_scores:0'),
                    sess.graph.get_tensor_by_name('detection_boxes:0'),
                    sess.graph.get_tensor_by_name('detection_classes:0')],
                   feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})
        img_class = flask.request.form["img_class"]
        num_detections = int(out[0][0])
        count_of_matched_class = 0
        count_of_total_class = 0
        list_bounding_boxes = []
        c=0
        cropped_image_path = []
        for i in range(num_detections):
            classId = int(out[3][0][i])
            score = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if score > 0.4:
                count_of_total_class = count_of_total_class+1
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                if(classes_90[classId]==img_class):
                    count_of_matched_class = count_of_matched_class+1
                    cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
                    
                    
                    #x_up,y_up,x_down,y_down
                    #c[1]:c[3], c[0]:c[2],:]
                    #cropped_image=img[y_up:y_down,x_up:x_down]
                    cropped_image=img[int(y):int(bottom),int(x):int(right)]
                    cv.imwrite("static/cropped/"+str(c) + ".jpg", cropped_image)
                    cropped_image_path.append("static/cropped/"+str(c) + ".jpg")
                    c = c+1
                    
                    
                    list_bounding_boxes.append(bbox)
        #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'new_img.jpg')
        cv.imwrite("static/data/new_img.jpg", img)
    return flask.render_template(template_name_or_list="result.html",count_of_total_class=count_of_total_class,count_of_matched_class=count_of_matched_class,list_bounding_boxes=list_bounding_boxes,img_class=img_class,cropped_image_path=cropped_image_path)

app.add_url_rule(rule="/extract", view_func=extractFeatures,methods=["POST"], endpoint="extract")

def homepage():
    return flask.render_template(template_name_or_list="home.html")
app.add_url_rule(rule="/", view_func=homepage)
app.run(host="127.0.0.5", port=6302)


