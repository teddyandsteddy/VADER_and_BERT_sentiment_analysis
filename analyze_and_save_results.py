import sqlite3
from transformers import pipeline, AutoTokenizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_and_save_results(source_db_path, output_db_path):
    """
    元のDBから歌詞を抽出し、VADERとBERTで分析、新しいDBに結果を保存します。
    """
    # VADERとBERTのツールを準備
    vader_analyzer = SentimentIntensityAnalyzer()
    
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    bert_classifier = pipeline('sentiment-analysis', model=model_name)
    
    # 元のDBからデータを抽出
    source_conn = sqlite3.connect(source_db_path)
    source_cursor = source_conn.cursor()
    
    try:
        source_cursor.execute("SELECT id, lyrics FROM tracks WHERE lyrics IS NOT NULL")
        lyrics_data = source_cursor.fetchall()
    except sqlite3.OperationalError:
        print("エラー: 'tracks'テーブルまたは'lyrics'カラムが見つかりませんでした。")
        source_conn.close()
        return
    
    source_conn.close()
    
    if not lyrics_data:
        print("歌詞データが見つかりませんでした。")
        return

    # 新しいDBファイルを作成
    output_conn = sqlite3.connect(output_db_path)
    output_cursor = output_conn.cursor()
    
    # VADER分析結果用のテーブルを作成
    output_cursor.execute("""
        CREATE TABLE vader_sentiment_scores (
            lyrics_id INTEGER PRIMARY KEY,
            positive_word_count INTEGER,
            negative_word_count INTEGER
        )
    """)
    
    # BERT分析結果用のテーブルを作成
    output_cursor.execute("""
        CREATE TABLE bert_sentiment_scores (
            lyrics_id INTEGER PRIMARY KEY,
            sentiment_label TEXT NOT NULL,
            sentiment_score REAL NOT NULL,
            lyrics TEXT NOT NULL
        )
    """)
    output_conn.commit()

    print("分析を開始します...")
    print(f"分析対象の歌詞件数: {len(lyrics_data)}")

    for track_id, lyrics in lyrics_data:
        # VADER分析
        positive_count = 0
        negative_count = 0
        for word in lyrics.split():
            sentiment = vader_analyzer.polarity_scores(word)
            if sentiment['compound'] >= 0.05:
                positive_count += 1
            elif sentiment['compound'] <= -0.05:
                negative_count += 1
        output_cursor.execute("INSERT INTO vader_sentiment_scores VALUES (?, ?, ?)", 
                             (track_id, positive_count, negative_count))
        
        # BERT分析
        try:
            bert_result = bert_classifier(lyrics, truncation=True, max_length=512)[0]
            output_cursor.execute("INSERT INTO bert_sentiment_scores VALUES (?, ?, ?, ?)", 
                                 (track_id, bert_result['label'], float(bert_result['score']), lyrics))
        except Exception as e:
            print(f"警告: 歌詞 (ID: {track_id}) のBERT分析中にエラーが発生しました - {e}")
            
    output_conn.commit()
    output_conn.close()
    
    print("\n--- 処理完了 ---")
    print(f"分析結果は新しいデータベースファイル '{output_db_path}' に保存されました。")

if __name__ == '__main__':
    analyze_and_save_results('spotify_data.db', 'analyzed_spotify_data.db')