from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
from werkzeug.utils import secure_filename
import easyocr
import sikibetu

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy(app)

# 定义 User 数据模型
class User(db.Model):
    mail = db.Column(db.String(120), primary_key=True)
    phonenumber = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class UserInfo(db.Model):
    mail = db.Column(db.String(120), primary_key=True)
    gender = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)

@app.route('/aa')
def photo():
    return render_template('photo.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_action', methods=['POST'])
def register_action():
    mail = request.form['mail']
    phonenumber = request.form['phonenumber']
    password = request.form['password']

    # 检查邮箱是否已存在
    existing_user = User.query.filter_by(mail=mail).first()
    if existing_user:
        print(f"邮箱: {mail} 已存在")
        return jsonify({"message": "メールがすでに存在します。"}), 400

    new_user = User(mail=mail, phonenumber=phonenumber, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "登録情報已接收并存储"})

@app.route('/save_user_info', methods=['POST'])
def save_user_info():
    mail = request.form['mail']
    gender = request.form['gender']
    
    # 将字符串格式的birthdate转换为date对象
    birthdate_str = request.form['birthdate']
    year, month, day = map(int, birthdate_str.split('-'))
    birthdate_obj = date(year, month, day)
    
    weight = float(request.form['weight'])

    # 检查是否存在同样的用户信息，如果存在则更新，否则插入新的记录
    existing_info = UserInfo.query.get(mail)
    if existing_info:
        existing_info.gender = gender
        existing_info.birthdate = birthdate_obj   # 使用date对象而不是字符串
        existing_info.weight = weight
    else:
        user_info = UserInfo(mail=mail, gender=gender, birthdate=birthdate_obj, weight=weight)  # 使用date对象而不是字符串
        db.session.add(user_info)
    db.session.commit()
    print(f"用户信息已保存: {mail}")
    return jsonify({"message": "信息已保存"})

@app.route('/login_action', methods=['POST'])
def login_action():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(mail=username).first()
    if user and user.password == password:
        # 检查UserInfo表中是否有该用户的信息
        user_info_exists = UserInfo.query.get(username) is not None
        print(user_info_exists)
        return jsonify({"status": "success", "infoExists": user_info_exists})
    else:
        return jsonify({"status": "fail"})


@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

@app.route('/main')
def main():
    return render_template('main.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload_files', methods=['POST'])
# def upload_files():
#     # 检查文件是否存在于请求中
#     if 'file[]' not in request.files:
#         return jsonify({"message": "No file part in the request."}), 400

#     files = request.files.getlist('file[]')  # 获取所有上传的文件

#     filenames = []
#     for file in files:
#         if file.filename == '':
#             return jsonify({"message": "No selected file."}), 400
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
#             filenames.append(filename)

#     return jsonify({"message": "Files uploaded successfully!", "filenames": filenames})

@app.route('/upload_files', methods=['POST'])
def upload_files():
    if 'file[]' not in request.files:
        return jsonify({"message": "No file part in the request."}), 400

    files = request.files.getlist('file[]')
    filenames = []
    ocr_results = []

    for file in files:
        if file.filename == '' or not allowed_file(file.filename):
            continue
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        filenames.append(filename)

        # 对上传的图片执行 OCR
        result = sikibetu.recognize_image(file_path)  # 假设你的函数名为 recognize_image
        ocr_results.append(result)

    return jsonify({"message": "Files processed successfully!", "filenames": filenames, "ocr_results": ocr_results})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 在运行应用程序之前创建数据库表
    app.run(host='0.0.0.0', port=7777, debug=True)
