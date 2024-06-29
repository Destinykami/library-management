from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# 配置 JWT 密钥
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 更换为你自己的密钥
jwt = JWTManager(app)

# 连接到数据库
db = pymysql.connect(
  host="localhost",
  user="root",
  password="kami1234",
  database="library-manager",
  cursorclass=pymysql.cursors.DictCursor
)


@app.route("/user/login", methods=['POST'])
def user_login():
  post_data = request.get_json()
  login_username = post_data.get('username')
  login_password = post_data.get('password')

  print(login_username, login_password)

  if login_username is not None and login_password is not None:
    try:
      with db.cursor() as cursor:
        # 查询数据库以验证用户
        sql = "SELECT * FROM Login WHERE Account=%s AND Password=%s"
        cursor.execute(sql, (login_username, login_password))
        userinfo = cursor.fetchone()
        uid = userinfo['uid']
        if userinfo:
          return jsonify({"status": 200, "message": "登录成功", "token": uid}), 200
        else:
          return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
      return jsonify({"message": str(e)}), 500
  else:
    return jsonify({"message": "Username and password are required"}), 400


#获取用户信息
@app.route("/user/info", methods=['GET'])
def get_user_info():
  print("try to get user info")
  #post_data = request.get_json()
  #token=post_data.get('token')
  #print(token)
  user = 0
  return jsonify({"status": 200, "message": "登录成功", "username": "adminkami", "is_admin": 1, "userid": 0}), 200


#获取书籍信息
@app.route('/book/info', methods=['GET'])
def get_book_info():
  with db.cursor() as cursor:
    # 查询数据库以获取图书信息
    sql = "SELECT ISBN, Title, Publisher, Author, TotalQuantity, AvailableQuantity, IsAvailable FROM BookInfo"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    #返回结果
    response = jsonify({'items': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


#获取读者信息
@app.route('/reader/info', methods=['GET'])
def get_reader_info():
  with db.cursor() as cursor:
    # 查询数据库以获取图书信息
    sql = "SELECT CardID,Name,Gender,Title,MaxBorrowQuantity,CurrentBorrowQuantity,Department,PhoneNumber FROM ReaderInfo"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    #返回结果
    response = jsonify({'items': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


#新增读者信息
@app.route("/reader/add", methods=["POST"])
def add_user():
  data = request.json
  with db.cursor() as cursor:
    sql = """
        INSERT INTO ReaderInfo (CardID, Name, Gender, Title, MaxBorrowQuantity, CurrentBorrowQuantity, Department, PhoneNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(sql, (
      data["CardID"], data["Name"], data["Gender"], data["Title"],
      data["MaxBorrowQuantity"], data["CurrentBorrowQuantity"],
      data["Department"], data["PhoneNumber"]
    ))
    db.commit()
  return jsonify({"status": "success"}), 200


#新增图书
@app.route("/book/add", methods=["POST"])
def add_book():
  data = request.json
  with db.cursor() as cursor:
    sql = """
        INSERT INTO BookInfo (ISBN, Title, Publisher, Author, TotalQuantity, AvailableQuantity, IsAvailable)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(sql, (
      data["ISBN"], data["Title"], data["Publisher"], data["Author"],
      data["TotalQuantity"], data["AvailableQuantity"], data["IsAvailable"]
    ))
    db.commit()
  return jsonify({"status": "success"}), 200


#获取借书列表
@app.route('/book/borrowinfo', methods=['GET'])
def get_borrowbook_info():
  with db.cursor() as cursor:
    # 查询数据库以获取图书信息
    sql = "SELECT CardID,ISBN,BorrowDate,BorrowPeriod,ReturnDate,Fine FROM BorrowInfo"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    #返回结果
    response = jsonify({'items': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


#删除图书
@app.route("/book/delete", methods=["POST"])
def delete_book():
  data = request.json
  with db.cursor() as cursor:
    sql = "DELETE FROM bookinfo WHERE ISBN = %s"
    cursor.execute(sql, str(data))
    db.commit()
  return jsonify({"status": "success"}), 200


# 修改图书
@app.route("/book/update", methods=["POST"])
def update_book():
  data = request.json
  if not data or 'ISBN' not in data:
    return jsonify({"status": "error", "message": "Invalid request data"}), 400

  isbn = data['ISBN']
  title = data.get('Title')
  publisher = data.get('Publisher')
  author = data.get('Author')
  total_quantity = data.get('TotalQuantity')
  available_quantity = data.get('AvailableQuantity')
  is_available = data.get('IsAvailable')

  with db.cursor() as cursor:
    sql = """
        UPDATE Bookinfo
        SET Title = %s, Publisher = %s, Author = %s, TotalQuantity = %s, AvailableQuantity = %s, IsAvailable = %s
        WHERE ISBN = %s
        """
    cursor.execute(sql, (title, publisher, author, total_quantity, available_quantity, is_available, isbn))
    db.commit()

  return jsonify({"status": "success"}), 200

# 修改读者
@app.route("/reader/update", methods=["POST"])
def update_reader():
  data = request.json
  if not data or 'CardID' not in data:
    return jsonify({"status": "error", "message": "Invalid request data"}), 400
  card_id = data['CardID']
  name = data.get('Name')
  gender = data.get('Gender')
  title = data.get('Title')
  max_borrow_quantity = data.get('MaxBorrowQuantity')
  department = data.get('Department')
  phone_number = data.get('PhoneNumber')
  with db.cursor() as cursor:
    sql = """
        UPDATE ReaderInfo
        SET Name = %s, Gender = %s, Title = %s, MaxBorrowQuantity = %s, Department = %s, PhoneNumber = %s
        WHERE CardID = %s
        """
    cursor.execute(sql, (name, gender, title, max_borrow_quantity, department, phone_number, card_id))
    db.commit()
  return jsonify({"status": "success"}), 200

# 删除读者
@app.route("/reader/delete", methods=["POST"])
def delete_reader():
  data = request.json
  with db.cursor() as cursor:
    sql = "DELETE FROM ReaderInfo WHERE CardID = %s"
    cursor.execute(sql, str(data))
    db.commit()
  return jsonify({"status": "success"}), 200

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"


if __name__ == '__main__':
  app.run(debug=True)
