# CaMicrosopeChallenge

This is the code to caMicroscope code challenge.

To run this app 

Head over to https://object-detection-nd-extraction.herokuapp.com/

### or

clone the repositry.



```
git clone https://github.com/amritansh22/CaMicrosopeChallenge.git
```
Head over to the folder
```
cd CaMicrosopeChallenge
```
Run the app by the command
``` python
python flaskApp.py
```
Open a web browser and paste the following address in the search bar  

http://127.0.0.5:6302/

Now upload the image on which the object detection is to be performed.

Now enter the class of the objects that are to be dedcted and press submit(All possible classes are given at the bottom of the page).

Now an image is shown with bounding boxes having objects of given class.
The total number of objects in the image is given along with the total number of objects of specified class.
And then the bounding box dimensions are given.


## Working demo
When you head over the link above(http://127.0.0.5:6302/) you should see a page like this:
![Screenshot (91)](https://user-images.githubusercontent.com/29978031/76889456-9fec9600-68ab-11ea-8935-60eabfc6bea6.png)

We now upload an image, having two dogs.
![example](https://user-images.githubusercontent.com/29978031/76889680-070a4a80-68ac-11ea-97c3-d7fe855acb91.jpg)

Select class of dog and press the button.
We recevie the output image as
![dog](https://user-images.githubusercontent.com/29978031/76889730-2608dc80-68ac-11ea-8497-5814f60003ce.jpg)

The output webpage look like this.
![Screenshot (90)](https://user-images.githubusercontent.com/29978031/76889845-56507b00-68ac-11ea-82de-4882f9ea8d4f.png)

And the extracted objects are shown as

You can see that all the extracted objects are shown as diffrent images.
![Screenshot (92)](https://user-images.githubusercontent.com/29978031/76990027-4e0c4480-696d-11ea-940c-e1c79188159e.png)


Had we selected a any other class we would see nothing.
Say we choose class person.
The output would look like
![dogno](https://user-images.githubusercontent.com/29978031/76889976-8566ec80-68ac-11ea-9d38-a538474d4bd6.jpg)
and the ouput page looks like:
![Screenshot (87)](https://user-images.githubusercontent.com/29978031/76890048-a596ab80-68ac-11ea-943f-372b13b13165.png)

You could see there are no bounding boxes ouput here as there are no persons in the image.



### Working example 2

This is the image on which we will perform object detection. We will choose the class of person in the image.

![test](https://user-images.githubusercontent.com/29978031/76990431-f3bfb380-696d-11ea-8ae8-86da10c4ad6c.jpg)

We will get an output page like this 

![Screenshot (93)](https://user-images.githubusercontent.com/29978031/76990678-5ca72b80-696e-11ea-8b93-2d5b3410251d.png)

and the bounding box dimensions like this

![Screenshot (95)](https://user-images.githubusercontent.com/29978031/76990776-87917f80-696e-11ea-8287-ecb558a7a1ae.png)

The images of the extracted objects looks like this

![Screenshot (94)](https://user-images.githubusercontent.com/29978031/76990898-b3ad0080-696e-11ea-904d-df2e83a513f4.png)


