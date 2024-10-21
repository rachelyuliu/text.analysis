import streamlit as st
import pandas as pd
import jieba
import matplotlib.pyplot as plt

# Load the HSK, TOCFL, and IC levels data
hsk_file_path = '~/Downloads/HSK_UTF8.csv'
tocfl_file_path = '~/Downloads/TOCFL_UTF8.csv'
ic_file_path = '~/Downloads/IC_UTF8.csv'
hsk_df = pd.read_csv(hsk_file_path)
tocfl_df = pd.read_csv(tocfl_file_path)
ic_df = pd.read_csv(ic_file_path)

# Function to map words to HSK levels
def map_hsk_level(word, hsk_df):
    levels = hsk_df[hsk_df['word'] == word]['level']
    if not levels.empty:
        return levels.values[0]
    else:
        return 'N/A'

# Function to map words to TOCFL levels
def map_tocfl_level(word, tocfl_df):
    levels = tocfl_df[tocfl_df['word'] == word]['level']
    if not levels.empty:
        return levels.values[0]
    else:
        return 'N/A'

# Function to map words to IC lessons
def map_ic_lesson(word, ic_df):
    lessons = ic_df[ic_df['word'] == word]['lesson']
    if not lessons.empty:
        return lessons.values[0]
    else:
        return 'N/A'

# Title of the app
st.title("Check the quality of the text in terms of word use.")

# Step 1: User Input - Text Area
user_text = st.text_area("Paste your text here:")

# Step 2: Analyze the text when the button is clicked
if st.button("Analyze the text"):
    # Tokenize the text using jieba
    words = jieba.lcut(user_text)
    # Calculate text statistics
    text_length = len(user_text)
    unique_words = len(set(words))
    word_repetition_rate = 100 * (1 - unique_words / len(words)) if len(words) > 0 else 0
    # Display general text statistics
    st.subheader("Text General Statistics")
    st.write(f"**Length of the text:** {text_length} characters")
    st.write(f"**Words used in the text:** {len(words)} words")
    st.write(f"**Unique words used in the text:** {unique_words} words")
    st.write(f"**Word repetition rate:** {word_repetition_rate:.2f}%")
    # HSK Level Analysis
    hsk_levels = [map_hsk_level(word, hsk_df) for word in words]
    results_df_hsk = pd.DataFrame({'HSK_level': hsk_levels})
    results_df_hsk['HSK_level'] = pd.to_numeric(results_df_hsk['HSK_level'], errors='coerce')
    hsk_counts = results_df_hsk['HSK_level'].value_counts()
    hsk_results = []
    for level in [1, 2, 3, 4, 5, 6, 7, float('nan')]:
        level_str = 'N/A' if pd.isna(level) else int(level)
        count = hsk_counts.get(level, 0)
        hsk_results.append({'HSK_level': level_str, 'count': count})
    hsk_results_df = pd.DataFrame(hsk_results)
    total_count_hsk = hsk_results_df['count'].sum()
    hsk_results_df['percentage'] = (hsk_results_df['count'] / total_count_hsk) * 100
    # TOCFL Level Analysis
    tocfl_levels = [map_tocfl_level(word, tocfl_df) for word in words]
    results_df_tocfl = pd.DataFrame({'TOCFL_level': tocfl_levels})
    results_df_tocfl['TOCFL_level'] = pd.to_numeric(results_df_tocfl['TOCFL_level'], errors='coerce')
    tocfl_counts = results_df_tocfl['TOCFL_level'].value_counts()
    tocfl_results = []
    for level in [1, 2, 3, 4, 5, 6, 7, float('nan')]:
        level_str = 'N/A' if pd.isna(level) else int(level)
        count = tocfl_counts.get(level, 0)
        tocfl_results.append({'TOCFL_level': level_str, 'count': count})
    tocfl_results_df = pd.DataFrame(tocfl_results)
    total_count_tocfl = tocfl_results_df['count'].sum()
    tocfl_results_df['percentage'] = (tocfl_results_df['count'] / total_count_tocfl) * 100
    # IC Lesson Analysis
    ic_lessons = [map_ic_lesson(word, ic_df) for word in words if map_ic_lesson(word, ic_df) is not None]
    results_df_ic = pd.DataFrame({'IC_lesson': ic_lessons})
    ic_counts = results_df_ic['IC_lesson'].value_counts()
    ic_results = []
    for lesson in ic_df['lesson'].unique():
        count = ic_counts.get(lesson, 0)
        ic_results.append({'IC_lesson': lesson, 'count': count})
    ic_results_df = pd.DataFrame(ic_results)
    total_count_ic = ic_results_df['count'].sum()
    ic_results_df['percentage'] = (ic_results_df['count'] / total_count_ic) * 100
    # Display the results for HSK levels
    st.subheader("HSK Level Analysis")
    st.dataframe(hsk_results_df)
    st.subheader("HSK Level Visualization")
    fig, ax = plt.subplots()
    ax.bar(hsk_results_df['HSK_level'].astype(str), hsk_results_df['percentage'])
    ax.set_xlabel('HSK Levels')
    ax.set_ylabel('Percentage of words')
    plt.xticks(rotation=0)
    st.pyplot(fig)
    # Display the results for TOCFL levels
    st.subheader("TOCFL Level Analysis")
    st.dataframe(tocfl_results_df)
    st.subheader("TOCFL Level Visualization")
    fig, ax = plt.subplots()
    ax.bar(tocfl_results_df['TOCFL_level'].astype(str), tocfl_results_df['percentage'])
    ax.set_xlabel('TOCFL Levels')
    ax.set_ylabel('Percentage of words')
    plt.xticks(rotation=0)
    st.pyplot(fig)
    # Display the results for IC lessons
    st.subheader("Integrated Chinese Lesson Analysis")
    st.dataframe(ic_results_df)
    # Visualize only the IC lessons that actually appear in the data file
    ic_results_df_filtered = ic_results_df[ic_results_df['count'] > 0]
    st.subheader("Integrated Chinese Lesson Visualization")
    fig, ax = plt.subplots()
    ax.bar(ic_results_df_filtered['IC_lesson'].astype(str), ic_results_df_filtered['percentage'])
    ax.set_xlabel('IC Lessons')
    ax.set_ylabel('Percentage of words')
    plt.xticks(rotation=90)
    st.pyplot(fig)