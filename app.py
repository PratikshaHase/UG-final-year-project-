import tkinter as tk
from tkinter import scrolledtext, messagebox
from translate import Translator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
import nltk 
nltk.download('punkt')
nltk.download('stopwords')

def summarize_transcript(transcript):
    sentences = sent_tokenize(transcript)
    words = [word for sentence in sentences for word in sentence.split()]
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stopwords.words('english')]
    fdist = FreqDist(words)
    keywords = fdist.most_common(5)

    keyword_sentences = []
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword, _ in keywords):
            keyword_sentences.append(sentence)

    summarized_text = TreebankWordDetokenizer().detokenize(keyword_sentences)
    return summarized_text

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join([entry['text'] for entry in transcript])
        summarized_transcript = summarize_transcript(full_transcript)
        return summarized_transcript
    except:
        return "Error fetching transcript."

def get_summary():
    video_id = video_id_entry.get()
    summarized_text = fetch_transcript(video_id)
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summarized_text)
    generate_summary(summarized_text)

    


def generate_summary(summarized_text):
    user_paragraph = summarized_text

    if user_paragraph:
        summary = summarize_text(user_paragraph, max_characters=500)
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, summary)
        result_text.config(state=tk.DISABLED)

        text_to_translate = summary
        target_language = "mr"  
        translated_text = translate_text(text_to_translate, target_language)

        result_text_mr.config(state=tk.NORMAL)
        result_text_mr.delete("1.0", tk.END)
        result_text_mr.insert(tk.END, translated_text)
        result_text_mr.config(state=tk.DISABLED)

        text_to_translate_hi = summary
        target_language_hi = "hi"  
        translated_text_hi = translate_text(text_to_translate_hi, target_language_hi)

        result_text_hi.config(state=tk.NORMAL)
        result_text_hi.delete("1.0", tk.END)
        result_text_hi.insert(tk.END, translated_text_hi)
        result_text_hi.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("Error", "Please enter a paragraph.")


def translate_text(text, target_language):
    translator= Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation


def summarize_text(text, max_characters=500):
    if len(text) <= max_characters:
        return text

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=3)
    summary_text = ' '.join(str(sentence) for sentence in summary)

    if len(summary_text) <= max_characters:
        return summary_text
    else:
        return summary_text[:max_characters]

# Create the main window
window = tk.Tk()
window.title("YouTube Transcript Summarizer")

video_id_label = tk.Label(window, text="Enter YouTube Video ID:")
video_id_label.pack()

video_id_entry = tk.Entry(window)
video_id_entry.pack()

summarize_button = tk.Button(window, text="Summarize", command=get_summary)
summarize_button.pack()

summary_text = tk.Text(window, height=15, width=100)
summary_text.pack()

result_text = scrolledtext.ScrolledText(wrap=tk.WORD, width=70, height=7, state=tk.DISABLED)
result_text.pack(pady=10)

result_text_mr = scrolledtext.ScrolledText(wrap=tk.WORD, width=70, height=7, state=tk.DISABLED)
result_text_mr.pack(pady=10)

result_text_hi = scrolledtext.ScrolledText(wrap=tk.WORD, width=70, height=7, state=tk.DISABLED)
result_text_hi.pack(pady=10)


window.mainloop()
