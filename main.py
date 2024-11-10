import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import speech_recognition as sr
import random
import time
from tkinter import font
import math

class PronunciationCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cute Pronunciation Checker")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFE5E5")

        self.words = [
            "Dim light", "Lip balm", "Chapped lips", "Coloured vegetables",
            "Red spots", "Activity", "Active", "Vitamin", "Breakfast",
            "Avoid", "Affect", "Food", "Fit"
        ]

        # Tạo main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Tạo title
        title_label = ttk.Label(
            self.main_frame,
            text="✨ Chọn từ để kiểm tra phát âm ✨",
            font=("Comic Sans MS", 16, "bold"),
            foreground="#4FA1D9",
            background="#FFE5E5"
        )
        title_label.pack(pady=20)

        # Frame chứa các nút từ vựng
        self.words_frame = ttk.Frame(self.main_frame)
        self.words_frame.pack(expand=True, fill="both", padx=20)

        # Tạo grid cho các nút
        row = 0
        col = 0
        for word in self.words:
            word_button = tk.Button(
                self.words_frame,
                text=word,
                font=("Comic Sans MS", 12),
                bg="#FFB6C1",
                fg="#4FA1D9",
                relief="flat",
                padx=15,
                pady=10,
                command=lambda w=word: self.open_pronunciation_check(w)
            )
            word_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            word_button.bind('<Enter>', self.on_hover)
            word_button.bind('<Leave>', self.on_leave)
            
            col += 1
            if col > 2:  # 3 cột
                col = 0
                row += 1

        # Cân bằng các cột
        for i in range(3):
            self.words_frame.grid_columnconfigure(i, weight=1)

        # Thêm style cho ttk widgets
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#FFE5E5')
        self.style.configure('Custom.TLabel', background='#FFE5E5')
        
        # Thêm hiệu ứng pulse cho title
        self.pulse_scale = 1.0
        self.pulse_direction = 1
        self.animate_title(title_label)

    def animate_title(self, title_label):
        # Hiệu ứng nhịp đập cho title (chậm hơn)
        self.pulse_scale += 0.01 * self.pulse_direction  # Giảm từ 0.02 xuống 0.01
        if self.pulse_scale >= 1.1:
            self.pulse_direction = -1
        elif self.pulse_scale <= 0.9:
            self.pulse_direction = 1
            
        new_size = int(16 * self.pulse_scale)
        title_label.configure(font=("Comic Sans MS", new_size, "bold"))
        self.root.after(100, lambda: self.animate_title(title_label))  # Tăng từ 50 lên 100

    def on_hover(self, event):
        # Hiệu ứng hover mượt mà hơn
        widget = event.widget
        widget.hover_animation = True
        self.animate_button_hover(widget, 0)

    def animate_button_hover(self, widget, step):
        if not hasattr(widget, 'hover_animation') or not widget.hover_animation:
            return
            
        if step < 10:
            r = int(255 - (255-255) * step/10)  # From FFB6C1 to FF69B4
            g = int(182 - (182-105) * step/10)
            b = int(193 - (193-180) * step/10)
            color = f'#{r:02x}{g:02x}{b:02x}'
            widget.configure(bg=color)
            self.root.after(20, lambda: self.animate_button_hover(widget, step + 1))

    def on_leave(self, event):
        widget = event.widget
        widget.hover_animation = False
        self.animate_button_leave(widget, 0)

    def animate_button_leave(self, widget, step):
        if hasattr(widget, 'hover_animation') and widget.hover_animation:
            return
            
        if step < 10:
            r = int(255)  
            g = int(105 + (182-105) * step/10)
            b = int(180 + (193-180) * step/10)
            color = f'#{r:02x}{g:02x}{b:02x}'
            widget.configure(bg=color)
            self.root.after(20, lambda: self.animate_button_leave(widget, step + 1))

    def open_pronunciation_check(self, word):
        # Tạo cửa sổ mới để kiểm tra phát âm
        check_window = tk.Toplevel(self.root)
        check_window.title(f"Kiểm tra phát âm - {word}")
        check_window.geometry("600x400")
        check_window.configure(bg="#FFE5E5")

        # Frame chính cho cửa sổ kiểm tra
        check_frame = ttk.Frame(check_window)
        check_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Hiển thị từ đang kiểm tra
        word_label = ttk.Label(
            check_frame,
            text=word,
            font=("Comic Sans MS", 20, "bold"),
            foreground="#4FA1D9",
            background="#FFF0F5",
            padding=15
        )
        word_label.pack(pady=20)

        # Nút kiểm tra phát âm
        check_button = tk.Button(
            check_frame,
            text="🎤 Kiểm tra phát âm",
            font=("Comic Sans MS", 12),
            bg="#FFB6C1",
            fg="#4FA1D9",
            relief="flat",
            padx=15,
            pady=10,
            command=lambda: self.check_pronunciation(word, check_frame)
        )
        check_button.pack(pady=20)
        check_button.bind('<Enter>', self.on_hover)
        check_button.bind('<Leave>', self.on_leave)

        # Label kết quả
        self.result_label = ttk.Label(
            check_frame,
            text="",
            font=("Comic Sans MS", 14),
            foreground="#4FA1D9",
            background="#FFF0F5",
            padding=10
        )
        self.result_label.pack(pady=20)

        # Thêm hiệu ứng fade in cho cửa sổ mới
        check_window.attributes('-alpha', 0.0)
        self.fade_in(check_window)

    def fade_in(self, window, alpha=0.0):
        if alpha < 1.0:
            window.attributes('-alpha', alpha)
            window.after(20, lambda: self.fade_in(window, alpha + 0.1))

    def check_pronunciation(self, word, parent_frame):
        # Thêm hiệu ứng loading
        self.result_label.config(text="Đang nghe")
        self.animate_loading_text()
        parent_frame.update()
        self.record_and_evaluate(word)

    def animate_loading_text(self):
        current_text = self.result_label.cget("text")
        if current_text.startswith("Đang nghe"):
            dots = current_text.count(".")
            new_text = "Đang nghe" + "." * ((dots + 1) % 4)
            self.result_label.config(text=new_text)
            if hasattr(self, 'recording') and self.recording:
                self.root.after(500, self.animate_loading_text)

    def record_and_evaluate(self, expected_word):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            # Chuyển đổi giọng nói thành văn bản
            spoken_word = recognizer.recognize_google(audio)
            print(f"Người dùng nói: {spoken_word}")

            # Đánh giá phát âm
            score = self.evaluate_pronunciation(spoken_word, expected_word)
            self.result_label.config(text=f"Điểm phát âm của từ '{expected_word}': {score}/10")
        
        except sr.UnknownValueError:
            messagebox.showerror("Lỗi", "Không thể nhận diện giọng nói.")
            self.result_label.config(text="") 
        except sr.RequestError as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối đến dịch vụ nhận diện giọng nói: {e}")
            self.result_label.config(text="")  

    def is_similar(self, spoken_word, expected_word):
        # Kiểm tra xem hai từ có độ dài gần giống nhau và ít nhất 50% ký tự giống nhau
        if abs(len(spoken_word) - len(expected_word)) <= 1:  # Độ dài gần giống nhau
            match_count = sum(1 for a, b in zip(spoken_word.lower(), expected_word.lower()) if a == b)
            return match_count >= len(expected_word) / 2 
        return False

    def evaluate_pronunciation(self, spoken_word, expected_word):
        # So sánh từ đã nói và từ mong đợi để đánh giá
        if spoken_word.lower() == expected_word.lower():
            return random.randint(9, 10) 
        elif self.is_similar(spoken_word, expected_word):
            return random.randint(6, 8) 
        else:
            return random.randint(1, 3) 

if __name__ == "__main__":
    root = tk.Tk()
    app = PronunciationCheckerApp(root)
    root.mainloop()
