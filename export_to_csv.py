import sqlite3
import pandas as pd

def export_to_csv(db_path, table_name, output_csv):
    """
    Exports the contents of the specified SQLite table to a CSV file.
    """
    try:
        conn = sqlite3.connect(db_path)
        
        # Read data from the SQL query into a pandas DataFrame
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)
        
        # Save as a CSV file
        df.to_csv(output_csv, index=False, encoding='utf-8')
        
        conn.close()
        
        print(f"Data from the '{table_name}' table has been exported to '{output_csv}'.")
        
    except sqlite3.OperationalError as e:
        print(f"Error connecting to the database or executing the query: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # Export the bert_sentiment_scores table
    export_to_csv('analyzed_spotify_data.db', 'bert_sentiment_scores', 'bert_scores.csv')
    
    # Export the vader_sentiment_scores table
    export_to_csv('analyzed_spotify_data.db', 'vader_sentiment_scores', 'vader_scores.csv')
