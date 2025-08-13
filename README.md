# VADER_and_BERT_sentiment_analysis
VADER vs. BERT This project analyzed hit song lyrics using two methods: VADER (lexicon-based) and BERT (context-based) to compare their results.  This analysis revealed complex emotions, such as irony and loss, in modern lyrics that simple positive/negative analysis cannot fully capture.

Project Overview
This project collected lyrics from recent hit songs and applied two different sentiment analysis methods: VADER and BERT. By combining a general word-based analysis with a context-aware, AI-based analysis, we explore the complexities of emotional expression in modern music from multiple perspectives.

Technologies Used
Python: For creating analysis scripts.

SQL (SQLite): For managing lyric data and analysis results.

VADER: A lexicon-based sentiment analysis library.

BERT: An AI-based sentiment analysis model that considers context.

Tableau: For visualizing the analysis results.

Analysis Steps
Data Collection: Used the Spotify API to retrieve lyrics from hit songs.

VADER Analysis: Counted the number of positive and negative words based on a lexicon. These results are stored in the vader_sentiment_scores table.

BERT Analysis: The AI classified the overall sentiment of the lyrics (positive or negative) by considering the context. The confidence score (sentiment_score) for each classification was also quantified. These results are stored in the bert_sentiment_scores table.

Result Comparison: Used SQL queries to extract lyrics where VADER and BERT produced different analysis results, and then examined the potential reasons for the discrepancies.

Analysis Findings
VADER Results: Across all analyzed lyrics, the total number of positive words exceeded the total number of negative words.

BERT Results: However, BERT's contextual analysis classified a higher number of lyrics as negative than positive.

This "inconsistency" suggests that modern lyrics don't just use positive words; they may use them within a negative context to convey complex emotions like irony or a sense of loss.

Future Outlook
I plan to visualize these analysis results with Tableau to create a compelling data story:

Visualizing the distribution of sentiment scores will clearly explain why VADER and BERT's results diverged.

I will leverage the sentiment_score to explore the diversity of emotional expression in songs from the perspective of sentiment intensity.

This project provided a great opportunity to apply my data analysis skills and contextual reading comprehension, honed through my experience as a translator, to uncover the "story" behind the data. 

Scripts and Database
analyze_and_save_results.py: The main script that performs VADER and BERT analysis and saves the results to analyzed_spotify_data.db.

get_inconsistent_lyrics.py: A script to extract lyrics where the VADER and BERT analysis results are inconsistent.

analyzed_spotify_data.db: The database file containing the analysis results.

