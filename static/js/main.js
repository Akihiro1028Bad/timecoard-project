document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const loadingIndicator = document.getElementById('loading');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        loadingIndicator.style.display = 'block';

        var formData = new FormData(this);
        var selectedMonth = document.getElementById('month').value;
        formData.append('selected_month', selectedMonth);
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = 'none';

            if (data.error) {
                alert(data.error);
            } else {
                displayResults(data.timecard_data, selectedMonth);
                displayProcessedImages(data.processed_images);
            }
        })
        .catch(error => {
            loadingIndicator.style.display = 'none';
            console.error('Error:', error);
            alert('エラーが発生しました: ' + error);
        });
    });

    document.getElementById('download-excel').addEventListener('click', function() {
        var updatedData = {};
        var rows = document.querySelectorAll('#timecard-table tbody tr');
        rows.forEach(function(row) {
            var date = row.cells[0].textContent;
            var inputs = row.querySelectorAll('input');
            updatedData[date] = {
                出勤時間: inputs[0] ? inputs[0].value : '',
                退勤時間: inputs[1] ? inputs[1].value : '',
                備考: inputs[2] ? inputs[2].value : ''
            };
        });

        fetch('/download-excel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Unknown error occurred') });
            }
            return response.blob();
        })
        .then(blob => {
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'タイムカード情報.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('エラーが発生しました: ' + error.message);
        });
    });
});

function displayResults(data, selectedMonth) {
    var tbody = document.querySelector('#timecard-table tbody');
    tbody.innerHTML = '';
    for (var date in data) {
        var row = tbody.insertRow();
        var displayDate = `2024-${selectedMonth}-${date.split('-')[2]}`;
        row.insertCell().textContent = displayDate;
        row.insertCell().innerHTML = `<input type="text" value="${data[date].出勤時間 || ''}" class="time-input">`;
        row.insertCell().innerHTML = `<input type="text" value="${data[date].退勤時間 || ''}" class="time-input">`;
        row.insertCell().innerHTML = `<input type="text" value="${data[date].備考 || ''}" class="remark-input">`;
    }
    document.getElementById('result-container').style.display = 'flex';
}

function displayProcessedImages(images) {
    document.getElementById('processed-image1').src = images[0];
    document.getElementById('processed-image2').src = images[1];
}