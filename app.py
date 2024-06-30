import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
app = Flask(__name__)
CORS(app)
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


@app.route("/user/info", methods=['GET'])
def get_user_info():
  uid = request.args.get('token')  # 获取查询参数中的 token，这里假设是用户的 uid

  with db.cursor() as cursor:
    # 查询数据库以验证用户
    sql = "SELECT Account, Role, uid, CardID FROM Login WHERE uid=%s"
    cursor.execute(sql, (uid,))
    result = cursor.fetchone()  # 假设只查询到一个用户信息，使用 fetchone()

    if result:
      # 构造返回的 JSON 数据
      user_info = {
        "status": 200,
        "message": "登录成功",
        "username": result['Account'],  # 假设 Account 是用户的用户名
        "is_admin": True if result['Role'] == 'Admin' else False,  # 根据 Role 判断是否是管理员
        "userid": result['uid'],  # 用户的 uid
        "card_id": result['CardID']  # 用户的 CardID
      }
      return jsonify(user_info), 200  # 返回用户信息和状态码 200 表示成功
    else:
      return jsonify({"status": 404, "message": "用户不存在"}), 404  # 如果未找到用户，返回状态码 404 表示未找到用户

#获取书籍信息
@app.route('/book/info', methods=['GET'])
def get_book_info():
  is_admin = request.args.get('is_admin')
  if not is_admin:
    return jsonify({"status": "error", "message": "没有管理员权限!"}), 404
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
  is_admin = request.args.get('is_admin')
  if not is_admin:
    return jsonify({"status": "error", "message": "没有管理员权限!"}), 404
  with db.cursor() as cursor:
    # 查询数据库以获取读者信息
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
    sql = "SELECT CardID,ISBN,BorrowDate,BorrowPeriod,ReturnDate,Fine FROM BorrowInfo_ALL"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    #返回结果
    response = jsonify({'items': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200
#获取某个读者借书列表
@app.route('/reader/borrowinfoOfOne', methods=['GET'])
def get_borrowbook_info_of_one():
  card_id = request.args.get('card_id')
  print(card_id)
  if not card_id:
    return jsonify({"status": "error", "message": "缺少 card_id 参数"}), 400

  with db.cursor() as cursor:
    # 查询数据库以获取图书信息
    sql = "SELECT CardID, ISBN, BorrowDate, BorrowPeriod, ReturnDate, Fine FROM BorrowInfo WHERE CardID = %s"
    cursor.execute(sql, (card_id,))
    result = cursor.fetchall()
    print(result)

    # 返回结果
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
# 查询书本
@app.route("/reader/search", methods=["GET"])
def search_books():
  title = request.args.get('title', '')
  isbn = request.args.get('isbn', '')
  author = request.args.get('author', '')

  with db.cursor() as cursor:
    sql = """
        SELECT * FROM Bookinfo
        WHERE Title LIKE %s OR ISBN LIKE %s OR Author LIKE %s
        """
    cursor.execute(sql, ('%' + title + '%', '%' + isbn + '%', '%' + author + '%'))
    result = cursor.fetchall()
    print(result)
    response = jsonify({'items': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200
# 查询书本
@app.route("/reader/search_book", methods=["GET"])
def search_reader_books():
  name = request.args.get('name', '')
  card_id = request.args.get('card_id', '')

  with db.cursor() as cursor:
    # 根据输入的读者姓名或借书证号查询基本信息及未归还图书信息
    sql = """
            SELECT
                r.CardID,
                r.Name,
                r.Gender,
                r.Title,
                r.MaxBorrowQuantity,
                r.CurrentBorrowQuantity,
                r.Department,
                r.PhoneNumber,
                b.ISBN,
                b.Title as BookName
            FROM
                ReaderInfo r
            LEFT JOIN
                BorrowInfo bi ON r.CardID = bi.CardID
            LEFT JOIN
                BookInfo b ON bi.ISBN = b.ISBN
            WHERE
                (r.Name LIKE %s OR r.CardID LIKE %s)
                AND bi.ISBN IS NOT NULL
                AND bi.ReturnDate IS NULL
        """
    cursor.execute(sql, ('%' + name + '%', '%' + card_id + '%'))
    result = cursor.fetchall()
    print(result)
    response = jsonify({'items': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# 借书
@app.route("/reader/borrow", methods=["POST"])
def borrow_a_book():
  data = request.json
  isbn = data.get('ISBN')
  card_id = data.get('CardID')

  if not isbn or not card_id:
    return jsonify({"status": "error", "message": "ISBN and CardID are required"}), 400
  #检查书是否存在
  with db.cursor() as cursor:
    sql_book = "SELECT * FROM BookInfo WHERE ISBN = %s and IsAvailable = True"
    cursor.execute(sql_book, isbn)
    book = cursor.fetchone()
    if not book:
      return jsonify({"status": "error", "message": f"Book with ISBN {isbn} not found"}), 404
  #检查读者是否存在
  with db.cursor() as cursor:
    sql_reader = "SELECT * FROM ReaderInfo WHERE CardID = %s"
    cursor.execute(sql_reader, card_id)
    reader = cursor.fetchone()
    if not reader:
      return jsonify({"status": "error", "message": f"Reader with CardID {card_id} not found"}), 404

  borrow_date = datetime.date.today()  # Assuming today's date as borrow date
  borrow_period = 14  #  14 days borrow period
  return_date = None  # Initial return date is null
  fine = None  # Initial fine amount is null

  #向总表中插入，向当前表中插入
  with db.cursor() as cursor:
    sql_insert1 = """
        INSERT INTO BorrowInfo (CardID, ISBN, BorrowDate, BorrowPeriod, ReturnDate, Fine)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    cursor.execute(sql_insert1, (card_id, isbn, borrow_date, borrow_period, return_date, fine))
    sql_insert2 = """
        INSERT INTO BorrowInfo_ALL (CardID, ISBN, BorrowDate, BorrowPeriod, ReturnDate, Fine)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    cursor.execute(sql_insert2, (card_id, isbn, borrow_date, borrow_period, return_date, fine))
    sql_update_book="""
      UPDATE Bookinfo set AvailableQuantity=AvailableQuantity-1 where ISBN = %s
      """
    cursor.execute(sql_update_book, isbn)
    db.commit()

  return jsonify({"status": "success", "message": "Book borrowed successfully"}), 200
# 还书
@app.route("/reader/return", methods=["POST"])
def return_a_book():
  data = request.json
  isbn = data.get('ISBN')
  card_id = data.get('CardID')

  if not isbn or not card_id:
    return jsonify({"status": "error", "message": "ISBN and CardID are required"}), 400
  #检查书是否存在
  with db.cursor() as cursor:
    sql_book = "SELECT * FROM BookInfo WHERE ISBN = %s "
    cursor.execute(sql_book, isbn)
    book = cursor.fetchone()
    if not book:
      return jsonify({"status": "error", "message": f"Book with ISBN {isbn} not found"}), 404
  #检查读者是否存在
  with db.cursor() as cursor:
    sql_reader = "SELECT * FROM ReaderInfo WHERE CardID = %s"
    cursor.execute(sql_reader, card_id)
    reader = cursor.fetchone()
    if not reader:
      return jsonify({"status": "error", "message": f"Reader with CardID {card_id} not found"}), 404
  # 获取借书时间和借书期限
  with db.cursor() as cursor:
    sql_borrow_info = "SELECT BorrowDate, BorrowPeriod FROM BorrowInfo WHERE ISBN = %s AND CardID = %s"
    cursor.execute(sql_borrow_info, (isbn, card_id))
    borrow_info = cursor.fetchone()
    print(borrow_info)
    if not borrow_info:
      return jsonify({"status": "error", "message": "No borrow record found for this book and reader"}), 404

  borrow_date = borrow_info['BorrowDate']
  borrow_period = borrow_info['BorrowPeriod']
  return_date = datetime.date.today()
  overdue_days = (return_date - borrow_date).days - borrow_period
  fine = max(overdue_days, 0) * 5

  with db.cursor() as cursor:
    # 向总表中加入信息，从当前表中删除
    sql_return1 = """
        UPDATE BorrowInfo_ALL SET returndate=%s, Fine=%s WHERE ISBN = %s and CardID = %s
        """
    cursor.execute(sql_return1, (return_date, fine, isbn,card_id))
    sql_return2 = """
        DELETE FROM BorrowInfo  WHERE ISBN = %s and CardID = %s
        """
    cursor.execute(sql_return2, ( isbn,card_id))
    sql_update_book="""
      UPDATE Bookinfo set AvailableQuantity=AvailableQuantity+1 where ISBN = %s
      """
    cursor.execute(sql_update_book, isbn)
    db.commit()

  return jsonify({"status": "success", "message": "Book borrowed successfully"}), 200

#所有已借未归还图书
@app.route("/books/overdue", methods=["GET"])
def get_overdue_books():
  with db.cursor() as cursor:
    # 查询所有到期未归还的图书信息
    sql = """
            SELECT
                b.ISBN,
                b.Title,
                r.Name AS ReaderName,
                r.CardID,
                bi.BorrowDate,
                DATE_ADD(bi.BorrowDate, INTERVAL bi.BorrowPeriod DAY) AS DueDate
            FROM
                BorrowInfo bi
            JOIN
                BookInfo b ON bi.ISBN = b.ISBN
            JOIN
                ReaderInfo r ON bi.CardID = r.CardID
            WHERE
                bi.ReturnDate IS NULL
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    response = jsonify({'items': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200
#未缴纳的欠款
@app.route("/reader/debt", methods=["GET"])
def get_debt():
  card_id = request.args.get('cardid', '')
  print(card_id)
  with db.cursor() as cursor:
    # 根据输入的读者姓名或借书证号查询欠款
    sql = """
            SELECT
                r.CardID,
                r.Name,
                r.MaxBorrowQuantity,
                r.CurrentBorrowQuantity,
                r.Department,
                r.PhoneNumber,
                SUM(BorrowInfo_ALL.Fine) as Fine
            FROM
                ReaderInfo r
            LEFT JOIN
                BorrowInfo_ALL ON r.CardID = BorrowInfo_ALL.CardID
            WHERE
                r.CardID = %s
            GROUP BY
                r.CardID, r.Name, r.MaxBorrowQuantity, r.CurrentBorrowQuantity, r.Department, r.PhoneNumber
        """
    cursor.execute(sql, (card_id,))
    result = cursor.fetchall()
    print(result)
    response = jsonify({'items': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200
# 缴纳欠款
# 还书
@app.route("/reader/returnmoney", methods=["POST"])
def return_money():
  data = request.json
  card_id = data.get('CardID')

  if  not card_id:
    return jsonify({"status": "error", "message": "ISBN and CardID are required"}), 400
  #检查读者是否存在
  with db.cursor() as cursor:
    sql_reader = "SELECT * FROM ReaderInfo WHERE CardID = %s"
    cursor.execute(sql_reader, card_id)
    reader = cursor.fetchone()
    if not reader:
      return jsonify({"status": "error", "message": f"Reader with CardID {card_id} not found"}), 404
  # 把BorrowInfo_ALL中的所有该读者的欠款项改为0
  with db.cursor() as cursor:
    # 向总表中加入信息，从当前表中删除
    sql = """
        UPDATE BorrowInfo_ALL SET Fine=0 WHERE CardID = %s
        """
    cursor.execute(sql, card_id)
    db.commit()

  return jsonify({"status": "success", "message": "Book borrowed successfully"}), 200

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"


if __name__ == '__main__':
  app.run(debug=True)
