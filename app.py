# 必要なライブラリやモジュールをインポートします
import os
from flask import Flask, request, send_file, render_template, url_for, jsonify, session
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from image_processing import preprocess_image, encode_image
from ai_communication import extract_timecard_info
from excel_generation import write_to_excel
from config import Config

# Flaskアプリケーションを作成します
app = Flask(__name__)
# アプリケーションの設定を読み込みます
app.config.from_object(Config)
# 設定の初期化を行います（例：必要なフォルダの作成など）
Config.init_app(app)

# ルートURL ('/')へのGETとPOSTリクエストを処理するルートを定義します
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # POSTリクエストの場合、ファイルのアップロードと処理を行います
        if 'file1' not in request.files or 'file2' not in request.files or 'selected_month' not in request.form:
            # 必要なファイルや情報が不足している場合、エラーを返します
            return jsonify({"error": "前半と後半の両方の写真、および月の選択が必要です。"})
        
        # アップロードされたファイルと選択された月を取得します
        file1 = request.files['file1']
        file2 = request.files['file2']
        selected_month = request.form['selected_month']
        
        # ファイルが選択されているか確認します
        if file1.filename == '' or file2.filename == '':
            return jsonify({"error": "ファイルが選択されていません。"})
        
        if file1 and file2:
            try:
                # ファイル名をセキュアにし、保存パスを設定します
                filename1 = secure_filename(file1.filename)
                filename2 = secure_filename(file2.filename)
                filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
                filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
                # ファイルを保存します
                file1.save(filepath1)
                file2.save(filepath2)
                
                # 画像の前処理と保存を行います
                processed_image1 = preprocess_image(filepath1)
                processed_image2 = preprocess_image(filepath2)
                processed_url1 = save_processed_image(processed_image1, f"processed_{filename1}")
                processed_url2 = save_processed_image(processed_image2, f"processed_{filename2}")
                
                # AIを使用してタイムカード情報を抽出します
                timecard_data = extract_timecard_info(filepath1, filepath2, selected_month, preprocess_image, encode_image)
                
                # 抽出されたデータをセッションに保存します
                session['timecard_data'] = timecard_data
                session['selected_month'] = selected_month
                
                # 処理結果をJSON形式で返します
                return jsonify({
                    "timecard_data": timecard_data,
                    "processed_images": [processed_url1, processed_url2]
                })
            except Exception as e:
                # エラーが発生した場合、エラーメッセージを返します
                return jsonify({"error": f"エラーが発生しました: {str(e)}"})
    
    # GETリクエストの場合、またはPOST以外の場合、HTMLテンプレートを表示します
    return render_template('index.html')

# Excelファイルのダウンロードを処理するルートを定義します
@app.route('/download-excel', methods=['POST'])
def download_excel():
    try:
        # POSTリクエストからタイムカードデータを取得します
        timecard_data = request.json
        # セッションから選択された月を取得します（デフォルトは1月）
        selected_month = session.get('selected_month', '01')
        if not timecard_data:
            # データが利用できない場合、エラーを返します
            return jsonify({"error": "データが利用できません"}), 400
        
        # タイムカードデータをExcelファイルに書き込みます
        excel_file = write_to_excel(timecard_data, selected_month)
        # 生成されたExcelファイルをダウンロードとして送信します
        return send_file(excel_file, as_attachment=True, download_name="タイムカード情報.xlsx")
    except Exception as e:
        # エラーが発生した場合、ログに記録しエラーメッセージを返します
        app.logger.error(f"Excelファイルの生成中にエラーが発生しました: {str(e)}")
        return jsonify({"error": f"Excelファイルの生成中にエラーが発生しました: {str(e)}"}), 500

# アップロードされたファイルを提供するルートを定義します
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# 処理済みの画像ファイルを提供するルートを定義します
@app.route('/processed/<filename>')
def processed_file(filename):
    return send_file(os.path.join(app.config['PROCESSED_FOLDER'], filename))

# 処理済みの画像を保存し、URLを返す関数を定義します
def save_processed_image(image_data, filename):
    filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    with open(filepath, 'wb') as f:
        f.write(image_data)
    return url_for('processed_file', filename=filename)

# このスクリプトが直接実行された場合、Flaskアプリケーションを起動します
if __name__ == '__main__':
    app.run(debug=True)