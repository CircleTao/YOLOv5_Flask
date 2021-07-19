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

'''判断上传的文件后缀是否合法'''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        shutil.rmtree(os.path.join(basepath, 'static', 'images'))
        os.makedirs(os.path.join(basepath, 'static', 'images'))
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify(
                {"error": 1001, "msg": "请检查上传的文件类型，仅限于'png', 'jpg', 'JPG', 'PNG', 'MP4', 'AVI', 'mp4', 'avi'"})

        user_input = request.form.get("name")



        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        return redirect('/upload_ok')
        # return render_template('upload_ok.html', userinput=user_input, val1=time.time())

    return render_template('upload1.html')


@app.route('/upload_ok', methods=['POST', 'GET'])
def upload_ok():
    return render_template('upload_ok.html')


@app.route('/show', methods=['POST', 'GET'])
def show():
    '''
        这里要调用模型识别的代码，将本地的图片放入模型进行识别，
        然后将生成的图片保存到本地，最后再将识别结果传到前端进行展示
    '''
    '''结果存放于/static/results下'''
    # filename = 'static/results/1.jpg'
    # request_begin_time = datetime.today()
    # print("request_begin_time", request_begin_time)
    # if request.method == 'GET':
    #     if filename is None:
    #         print('None result!')
    #     else:
    #         return send_file(filename)
    # else:
    #     pass
    # return "error"

    # 使用获取文件的路径并显示文件
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    # 下面两行为results文件夹的清除与建立（清理缓存功能），与识别模型结合再取消注释
    # shutil.rmtree(os.path.join(basepath, 'static', 'images'))
    # os.makedirs(os.path.join(basepath, 'static', 'images'))
    img_path = os.path.join(basepath, 'static/results', 'test.jpg')
    img_stream = showimg(img_path)
    return render_template('imgshow.html', image=img_stream)

def showimg(filename):

    img_stream = ''
    with open(filename, 'rb') as img:
        img_stream = img.read()
        #  print(base64.b16encode(img_stream))
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream



if __name__ == '__main__':
    app.run(debug=True, port=81)
    #show()
    #test()
