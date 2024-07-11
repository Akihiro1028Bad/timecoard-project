# ai_communication.py
# このファイルは、AI（Anthropic社のClaude）とのコミュニケーションを管理します

# 必要なライブラリをインポートします
import anthropic  # Anthropic社のAIを使用するためのライブラリ
import json  # JSONデータを扱うためのライブラリ
from datetime import datetime  # 日付と時間を扱うためのライブラリ
from config import Config  # アプリケーションの設定を読み込むためのモジュール

# AnthropicのAPIクライアントを初期化します
client = anthropic.Client(api_key=Config.ANTHROPIC_API_KEY)

# タイムカード情報を抽出する主要な関数
def extract_timecard_info(image_path1, image_path2, selected_month, preprocess_image, encode_image):
    # 1枚の画像を処理する内部関数
    def process_single_image(image_path, is_first_half):
        # 画像を前処理し、エンコードします
        image_data = preprocess_image(image_path)
        encoded_image = encode_image(image_data)
        
        # 画像が前半か後半かを決定します
        half = "前半" if is_first_half else "後半"
        
        # AIに与える指示（プロンプト）を設定します
        system = f"""
        この画像はタイムカードの{half}の写真です。{selected_month}月の情報を抽出してください。人間が目視で確認するように、注意深く画像を観察し、以下の指示に従って情報を抽出してください：

        1. タイムカードの各行を順に見ていき、以下の情報を抽出してください：
           - 日付: 左端に記載されています。YYYY-MM-DD形式で記録してください。
           - 出勤時間: "IN"または similar_text欄に記載されています。HH:MM形式で記録してください。
           - 退勤時間: "OUT"または similar_text欄に記載されています。HH:MM形式で記録してください。
           - 備考: テレワークの場合は "テレ" と記載されている可能性があります。見つけた場合は記録してください。

        2. 全休の日も含めてください。空欄や「全休」と書かれている行も含めてください。「空欄」や「記載なし」としてください。

        3. 1日から31日すべての日付を表示してください。日付が明確でない場合は、前後の日付から推測してください。ただし、推測した場合は備考に「日付推測」と追記してください。

        4. 時間が不明確な場合や記載がない場合は、"不明"と記載してください。

        5. 手書きの文字や印字が不鮮明な場合は、最善の推測を行い、備考に「手書き」や「不鮮明」と追記してください。

        6. その他気づいた特徴（例：修正痕、特殊な記号など）があれば、備考に追記してください。

        7. 結果は以下のJSONフォーマットで出力してください：
        {{
            "YYYY-MM-DD": {{"出勤時間": "HH:MM", "退勤時間": "HH:MM", "備考": "テレ,日付推測"}},
            "YYYY-MM-DD": {{"出勤時間": "HH:MM", "退勤時間": "HH:MM", "備考": "手書き,不鮮明"}}
        }}

        8. JSONデータのみを出力し、説明や追加のコメントは含めないでください。
        """

        try:
            # AIにメッセージを送信し、応答を受け取ります
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                temperature=0.0,
                system=system,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": encoded_image
                                }
                            }
                        ]
                    }
                ]
            )
            
            # AIからの応答を処理します
            content = message.content
            print(content)
            if isinstance(content, list):
                json_data = next((item.text for item in content if item.type == 'text'), None)
            else:
                json_data = content

            if json_data:
                print("JSON data before parsing:", json_data)  # デバッグ用プリント
                parsed_data = json.loads(json_data)
                print("Parsed JSON data:", json.dumps(parsed_data, indent=2))  # デバッグ用プリント
                return post_process_data(parsed_data)
            else:
                print(f"Error: No valid JSON data found in the {half} image response")
                return {}
        except Exception as e:
            print(f"Error processing {half} image: {str(e)}")
            return {}

    # 抽出されたデータを後処理する内部関数
    def post_process_data(data):
        processed_data = {}
        for date, info in data.items():
            # 日付の形式を確認し、必要に応じて修正
            try:
                correct_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print(f"Invalid date format: {date}")
                continue

            # 時間の形式を確認し、必要に応じて修正
            for time_key in ['出勤時間', '退勤時間']:
                time = info.get(time_key, '')
                if time and time != '不明':
                    try:
                        correct_time = datetime.strptime(time, "%H:%M").strftime("%H:%M")
                        info[time_key] = correct_time
                    except ValueError:
                        info[time_key] = '不明'

            processed_data[correct_date] = info

        return processed_data

    # 両方の画像を処理します
    data1 = process_single_image(image_path1, True)
    data2 = process_single_image(image_path2, False)

    # 両方の画像から得たデータを結合します
    combined_data = {**data1, **data2}
    
    # 日付順にソートします
    sorted_data = dict(sorted(combined_data.items()))
    
    # 選択された月に基づいて日付をフィルタリングします（年は無視）
    filtered_data = {date: info for date, info in sorted_data.items() if date.split('-')[1] == selected_month}
    
    # 最終的なデータを出力します
    print("Filtered data:", json.dumps(filtered_data, indent=2, ensure_ascii=False))
    return filtered_data