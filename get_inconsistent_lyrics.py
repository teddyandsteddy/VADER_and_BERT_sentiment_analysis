import sqlite3

def get_inconsistent_lyrics(db_path):
    """
    BERTではネガティブ、VADERではポジティブな歌詞を抽出します。
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query = """
        SELECT
            t1.lyrics
        FROM
            bert_sentiment_scores AS t1
        JOIN
            vader_sentiment_scores AS t2
        ON
            t1.lyrics_id = t2.lyrics_id
        WHERE
            t1.sentiment_label = 'NEGATIVE'
            AND t2.positive_word_count > t2.negative_word_count;
        """
        
        cursor.execute(query)
        inconsistent_lyrics = cursor.fetchall()
        
        conn.close()
        
        if inconsistent_lyrics:
            print("\n--- 不一致と判断された歌詞 ---")
            for i, lyrics_tuple in enumerate(inconsistent_lyrics, 1):
                print(f"--- 歌詞 {i} ---")
                print(lyrics_tuple[0])
                print("-" * 15)
        else:
            print("不一致と判断された歌詞は見つかりませんでした。")
            
    except sqlite3.OperationalError as e:
        print(f"データベースへの接続またはクエリの実行エラー: {e}")
    except sqlite3.Error as e:
        print(f"データベースエラー: {e}")

if __name__ == '__main__':
    get_inconsistent_lyrics('analyzed_spotify_data.db')