document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('checkModal');
    const wordButtons = document.querySelectorAll('.word-button');
    const closeBtn = document.querySelector('.close');
    const recordButton = document.getElementById('recordButton');
    const selectedWordElement = document.getElementById('selectedWord');
    const resultElement = document.getElementById('result');

    wordButtons.forEach(button => {
        button.addEventListener('click', () => {
            const word = button.dataset.word;
            selectedWordElement.textContent = word;
            resultElement.textContent = '';
            modal.style.display = 'block';
        });
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        resultElement.textContent = '';
    });

    recordButton.addEventListener('click', async () => {
        const word = selectedWordElement.textContent;
        resultElement.textContent = 'Đang nghe...';
        
        try {
            const response = await fetch('/check-pronunciation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ word: word })
            });
            
            const data = await response.json();
            
            if (data.success) {
                resultElement.textContent = `Điểm phát âm của từ '${word}': ${data.score}/10`;
            } else {
                resultElement.textContent = 'Có lỗi xảy ra khi kiểm tra phát âm';
            }
        } catch (error) {
            resultElement.textContent = 'Không thể kết nối đến máy chủ';
        }
    });
}); 