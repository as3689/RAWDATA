import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# 데이터베이스 설정
DB_PATH = 'growth_survey.db'

def init_db():
    """DB 초기화"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS growth_survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT UNIQUE,
            date TEXT,
            crop TEXT,
            sowing_date TEXT,
            leaf_length REAL,
            leaf_width REAL,
            fresh_weight REAL,
            cultivation_days INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/register', methods=['POST'])
def register_growth():
    """생육 조사 등록"""
    data = request.json
    image_name = data['imageName']

    # 데이터 가져오기
    date = data['date']
    crop = data['crop']
    sowing_date = data['sowingDate']
    leaf_length = data['leafLength']
    leaf_width = data['leafWidth']
    fresh_weight = data['freshWeight']
    cultivation_days = data['cultivationDays']

    try:
        # DB 연결 및 데이터 삽입
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO growth_survey (
                image_name, date, crop, sowing_date,
                leaf_length, leaf_width, fresh_weight, cultivation_days
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (image_name, date, crop, sowing_date, leaf_length, leaf_width, fresh_weight, cultivation_days))
        conn.commit()
        conn.close()

        return jsonify({
            'message': f'이미지 이름 "{image_name}"이(가) 성공적으로 등록되었습니다.'
        })
    except sqlite3.IntegrityError:
        # 중복된 이미지 이름 처리
        return jsonify({
            'message': f'이미지 이름 "{image_name}"은(는) 이미 등록된 데이터입니다.'
        }), 400
    except Exception as e:
        # 일반적인 에러 처리
        return jsonify({
            'message': f'등록 중 오류가 발생했습니다: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
