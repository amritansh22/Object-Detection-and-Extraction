# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 10:59:51 2020

@author: Amritansh Vajpayee
"""
#importing neccessary libraries.

import tensorflow as tf
import cv2 as cv
import flask, werkzeug

#Declaring the Flask app
app = flask.Flask(__name__)

#The following lines ensures that the browser dosen't load the cached images.
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
    
    
# In the following function we start extracting the objects and their corresponding bounding boxes 

def extractFeatures():
    img = flask.request.files["img"]      #load the uploaded img
    img_name = img.filename
    img_secure_name = werkzeug.secure_filename(img_name)
    img.save(img_secure_name)
    
    #This is the list of the supported classes of COCOCO model
    
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
    
    #We load the pretrained COCOCO model
    
    with tf.gfile.FastGFile('frozen_inference_graph.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    
    #Intializing tensorflow session.
    
    with tf.Session() as sess:
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

    # Reading and preprocessing the image.
        img = cv.imread(img_secure_name)
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  

    # Running the model
        out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                    sess.graph.get_tensor_by_name('detection_scores:0'),
                    sess.graph.get_tensor_by_name('detection_boxes:0'),
                    sess.graph.get_tensor_by_name('detection_classes:0')],
                   feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})
        img_class = flask.request.form["img_class"]
        num_detections = int(out[0][0])
        count_of_matched_class = 0      # to store the count of total objects of the given class in image
        count_of_total_class = 0        # to store the count of total objects found in image
        list_bounding_boxes = []        #list to store the bounding boxes of the objects of matched class
        c = 0                           #a counter to give unique address to extracted objects
        cropped_image_path = []         # list to store the destination address of the extracted object images.
        for i in range(num_detections):
            classId = int(out[3][0][i])     #id of the predicted class
            score = float(out[1][0][i])     #score of the object predicted
            bbox = [float(v) for v in out[2][0][i]]     #bounding box dimensions of the extracted objects.
            if score > 0.4:                                         #this is the threshold score 40%
                count_of_total_class = count_of_total_class+1
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                if(classes_90[classId]==img_class):                 #if the class of the found object is same as the given class
                    count_of_matched_class = count_of_matched_class+1
                    cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)   # here we are drawing the bounding boxes on image
                    
                    cropped_image=img[int(y):int(bottom),int(x):int(right)]             #Here we extracting the the objects from their corresponding bounding boxes.
                    cv.imwrite("static/cropped/"+str(c) + ".jpg", cropped_image)        #Storing the cropped image
                    cropped_image_path.append("static/cropped/"+str(c) + ".jpg")
                    c = c+1
                    
                    
                    list_bounding_boxes.append(bbox)
        cv.imwrite("static/data/new_img.jpg", img)                                      #Here we are storing the complete immage with their bounding boxes drawn
    return flask.render_template(template_name_or_list="result.html",count_of_total_class=count_of_total_class,count_of_matched_class=count_of_matched_class,list_bounding_boxes=list_bounding_boxes,img_class=img_class,cropped_image_path=cropped_image_path)    #Now we move to the result page

app.add_url_rule(rule="/extract", view_func=extractFeatures,methods=["POST"], endpoint="extract")

# this is the link to the main app page.
def homepage():
    return flask.render_template(template_name_or_list="home.html")
app.add_url_rule(rule="/", view_func=homepage)


# Running the app.

if __name__ == "__main__":
    app.run(debug=True)


