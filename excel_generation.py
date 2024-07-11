# excel_generation.py
import pandas as pd
from datetime import datetime

def write_to_excel(timecard_data, selected_month):
    current_year = datetime.now().year

    # JSONデータをDataFrameに変換
    df = pd.DataFrame.from_dict(timecard_data, orient='index', columns=['出勤時間', '退勤時間', '備考'])
    df.index.name = '日付'
    df.reset_index(inplace=True)

    # 日付を適切に処理
    df['日付'] = pd.to_datetime(df['日付'], format='%Y-%m-%d', errors='coerce')

    # 出勤時間、退勤時間、日付を適切に処理
    for col in ['出勤時間', '退勤時間', '日付']:
        df[col] = df[col].replace({'不明': pd.NaT, '': pd.NaT})  # '不明'と空文字をNaTに置換

    # 日付をM/D形式に変更（不明の場合は空白に）
    df['日付'] = df['日付'].apply(lambda x: f"{x.month}/{x.day}" if pd.notnull(x) else '')

    # Excelファイルに書き込み
    excel_file = 'タイムカード情報.xlsx'
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # NaN値を空文字列に置換
        df = df.fillna('')
        
        df.to_excel(writer, sheet_name='タイムカード', index=False)

    return excel_file