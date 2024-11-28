from flask import Flask, jsonify, request, render_template
import speech_recognition as sr
import random


app = Flask(__name__, 
    template_folder='../frontend/templates',
    static_folder='../frontend/static')

WORDS = [
    "Agriculture engineering",
    "Agriculture department",
    "Farming technology",
    "Farming method",
    "Cooking certificate"
]

@app.route('/')
def index():
    return render_template('index.html', words=WORDS)

@app.route('/check-pronunciation', methods=['POST'])
def check_pronunciation():
    data = request.get_json()
    expected_word = data.get('word')
    
    if not expected_word:
        return jsonify({
            'success': False,
            'error': 'Không tìm thấy từ cần kiểm tra'
        })
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            # Điều chỉnh nhiễu môi trường
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Đang lắng nghe...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
        print("Đang xử lý âm thanh...")
        spoken_word = recognizer.recognize_google(audio, language='en-US')
        print(f"Đã nghe: {spoken_word}")
        
        score = evaluate_pronunciation(spoken_word, expected_word)
        
        return jsonify({
            'success': True,
            'score': score,
            'spoken_word': spoken_word
        })
        
    except sr.WaitTimeoutError:
        return jsonify({
            'success': False,
            'error': 'Không nghe thấy giọng nói, vui lòng thử lại'
        })
    except sr.UnknownValueError:
        return jsonify({
            'success': False,
            'error': 'Không thể nhận diện giọng nói, vui lòng nói rõ hơn'
        })
    except sr.RequestError:
        return jsonify({
            'success': False,
            'error': 'Lỗi kết nối internet, vui lòng kiểm tra lại'
        })
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Có lỗi xảy ra, vui lòng thử lại'
        })

def evaluate_pronunciation(spoken_word, expected_word):
    if spoken_word.lower() == expected_word.lower():
        return random.randint(9, 10)
    elif is_similar(spoken_word, expected_word):
        return random.randint(6, 8)
    return random.randint(1, 3)

def is_similar(spoken_word, expected_word):
    if abs(len(spoken_word) - len(expected_word)) <= 1:
        match_count = sum(1 for a, b in zip(spoken_word.lower(), expected_word.lower()) if a == b)
        return match_count >= len(expected_word) / 2
    return False

if __name__ == '__main__':
    app.run(debug=True) 