from django.shortcuts import render
from .models import user_image
from django.views.generic import CreateView
from .forms import user_image_form

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required

from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import json
from tensorflow import Graph

from pathlib import Path

img_height, img_width=224,224
""" with open('practiceF\quickstart\models\imagenet_classes.json','r') as f:
    labelInfo=f.read() """

with open(Path.joinpath(Path(__file__).resolve().parent, 'models', 'imagenet_classes.json'),'r') as f:
    labelInfo=f.read()

labelInfo=json.loads(labelInfo)

model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        p = Path.joinpath(Path(__file__).resolve().parent, 'models', 'MobileNetModelImagenet.h5')
        print(p)
        print(p)
        print(p)
        
        model=load_model(p)
        """ model=load_model('D:\PythonFiles\educationalpractice\practiceF\quickstart\models\MobileNetModelImagenet.h5') """

# Create your views here.
class user_image_create(CreateView):
    model = user_image
    form_class = user_image_form
    extra_context = {'all_user_image': user_image.objects.all()}
    template_name = 'userimagecreate.html'
    success_url = '/'

""" def download_image(request):
    if request.method == 'POST':
        form = user_image_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = user_image_form()
    return render(request, 'userimagecreate.html', {'form': form}) """


def index_page(request):

    print (request)
    print (request.POST.dict())

    

    all_user_image = user_image.objects.all()

    predictedLabel = []
    predictedLabelresult = []


    for i in all_user_image:


        testimage = 'D:\PythonFiles\educationalpractice\practiceF'+i.image_downloaded.url
        

        img = image.load_img(testimage, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x=x/255
        x=x.reshape(1,img_height, img_width,3)
        with model_graph.as_default():
            with tf_session.as_default():
                predi=model.predict(x)

        print(predi)

        import numpy as np
        predictedLabel.append(labelInfo[str(np.argmax(predi[0]))])
    
    for i in predictedLabel:
            predictedLabelresult.append(i[1])

    print(predictedLabel)
    print(predictedLabelresult)

    data = {
        'all_user_image': all_user_image
    }

    return render(request, 'index.html', {'data':data,'predictedLabelresult':predictedLabelresult})
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request,'login.html', {"form":form})

def log_out(request):
    logout(request)
    return redirect('home')


