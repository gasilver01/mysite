# 프레임워크 로드 
from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from invest import Quant
import database

mydb = database.MyDB()
# Flask class 생성 
# 생성자 함수 필요한 인자 : 파일의 이름 
app = Flask(__name__)

# 네비게이터 -> 특정한 주소로 요청이 들어왔을때 함수와 연결
# route()함수에 인자가 의미하는것은? 
# root url + 주소(route함수에 인자) 
@app.route('/')
def index():

    return render_template('login.html')

@app.route('/main', methods=['post'])
def main():
    _id = request.form['input_id']
    _pass = request.form['input_pass']
    login_query = """
        select 
        * 
        from 
        user 
        where 
        id = %s 
        and 
        password = %s
    """

    # 함수 호출
    db_result = mydb.sql_query(login_query, _id, _pass)
    # 로그인의 성공 여부 (조건식?? db_result가 존재하는가?)
    if db_result:
        return render_template('index.html')
    else:
        # 로그인이 실패하는 경우 -> 로그인화면('/')으로 되돌아간다.
        return redirect('/')
        # return "login fail"

@app.route('/invest')
def invest():
    input_code = request.args['code']
    input_start_time = f"{request.args['s_year']}-{request.args['s_month']}-{request.args['s_day']}"
    input_end_time = f"{request.args['e_year']}-{request.args['e_month']}-{request.args['e_day']}"
    input_kind = request.args['kind']
    print(
        f"""
            {input_code}
            {input_start_time}
            {input_end_time}
            {input_kind}
        """
    )
    # input_code를 이용해서 csv 파일을 로드 
    df = pd.read_csv(f"csv/{input_code}.csv")
    quant = Quant(df, _start = input_start_time, _end=input_end_time, _col='Close')
    if input_kind == 'bnh':
        result, rtn = quant.buyandhold()
    elif input_kind == 'boll':
        result, rtn = quant.bollinger()
    elif input_kind == 'hall':
        result, rtn = quant.halloween()
    elif input_kind == 'mmt':
        result, rtn = quant.momentum()
    result.reset_index(inplace=True)
    result = result.loc[ result['rtn'] != 1,  ]
    cols = list(result.columns)
    value = result.to_dict('records')
    x = list(result['Date'])
    y = list(result['acc_rtn'])
    res_data = {
        "columns" : cols,
        'values' : value, 
        'axis_x' : x, 
        'axis_y' : y
    }
    return res_data

# 웹서버를 실행 
app.run(debug=True)