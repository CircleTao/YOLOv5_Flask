# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2
import base64
import shutil

from datetime import timedelta, datetime

app = Flask(__name__)
# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'MP4', 'AVI', 'mp4', 'avi'])
IMAGE_NAME = ['jpg', 'png']
VIDEO_NAME = ['mp4', 'avi']
basepath = os.path.dirname(__file__)  # 当前文件所在路径

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def showimg(filename):
    img_stream = ''
    with open(filename, 'rb') as img:
        img_stream = img.read()
        #  print(base64.b16encode(img_stream))
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

def clear_cache():
    shutil.rmtree(os.path.join(basepath, 'static', 'images'))
    os.makedirs(os.path.join(basepath, 'static', 'images'))
    shutil.rmtree(os.path.join(basepath, 'static', 'videos'))
    os.makedirs(os.path.join(basepath, 'static', 'videos'))
    # shutil.rmtree(os.path.join(basepath, 'static', 'results1'))
    # os.makedirs(os.path.join(basepath, 'static', 'results1'))
    # shutil.rmtree(os.path.join(basepath, 'static', 'results2'))
    # os.makedirs(os.path.join(basepath, 'static', 'results2'))
    return True

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        clear_cache()
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return
            # return jsonify(
            #     {"error": 1001, "msg": "请检查上传的文件类型，仅限于'png', 'jpg', 'JPG', 'PNG', 'MP4', 'AVI', 'mp4', 'avi'"})

        if f.filename.split('.')[-1] in IMAGE_NAME:
            upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            # 使用Opencv转换一下图片格式和名称
            img = cv2.imread(upload_path)
            cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
            return redirect('/uploaded_image')

        if f.filename.split('.')[-1] in VIDEO_NAME:
            upload_path = os.path.join(basepath, 'static/videos', secure_filename(f.filename))
            f.save(upload_path)
            os.rename(upload_path, os.path.join(basepath, 'static/videos', 'test.mp4'))
            return redirect('/uploaded_video')


    return render_template('upload1.html')

# 上传图片预览页面
@app.route('/uploaded_image', methods=['POST', 'GET'])
def upload_ok():
    return render_template('uploaded_image.html')

# 自训练模型识别图片展示页面
@app.route('/show_image1', methods=['POST', 'GET'])
def showimage1():
    '''
        这里要调用模型识别的代码，将本地的图片放入模型进行识别，
        然后将生成的图片保存到本地，最后再将识别结果传到前端进行展示
    '''
    # 使用获取文件的路径并显示文件
    img_path = os.path.join(basepath, 'static/results1', 'test.jpg')
    img_stream = showimg(img_path)
    return render_template('imgshow.html', image=img_stream, msg='自训练模型')

# 官方模型识别图片展示页面
@app.route('/show_image2', methods=['POST', 'GET'])
def showimage2():
    '''
        这里要调用模型识别的代码，将本地的图片放入模型进行识别，
        然后将生成的图片保存到本地，最后再将识别结果传到前端进行展示
    '''
    img_path = os.path.join(basepath, 'static/results2', 'test.jpg')
    img_stream = showimg(img_path)
    return render_template('imgshow.html', image=img_stream, msg='官方模型')

# 上传视频预览页面
@app.route('/uploaded_video')
def movie_list():
    filename = 'videos/test.mp4'
    return render_template('uploaded_video.html', data=filename)

# 自训练模型识别视频展示页面
@app.route('/show_video1')
def showvideo1():
    '''
        这里要调用模型识别的代码，将本地的视频放入模型进行识别，
        然后将生成的视频保存到本地，最后再将识别结果传到前端进行展示

        这里未来可能要加入让用户等待的提示，以解决视频识别时间过长导致浏览器假死的情况
    '''
    video_path = 'results1/test.mp4'
    return render_template('videoshow.html', video=video_path, msg='自训练模型')

# 官方模型识别视频展示页面
@app.route('/show_video2')
def showvideo2():
    '''
        这里要调用模型识别的代码，将本地的视频放入模型进行识别，
        然后将生成的视频保存到本地，最后再将识别结果传到前端进行展示

        这里未来可能要加入让用户等待的提示，以解决视频识别时间过长导致浏览器假死的情况
    '''
    video_path = 'results2/test.mp4'
    return render_template('videoshow.html', video=video_path, msg='官方模型')

if __name__ == '__main__':
    app.run(debug=True, port=81)