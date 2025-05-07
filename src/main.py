import os
import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# ========== YOUTUBE UTILITIES ==========

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def get_video_title(video_url):
    try:
        response = requests.get(video_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        return title.replace(" - YouTube", "") if title else "Título não encontrado"
    except Exception as e:
        return f"Erro ao obter título: {e}"

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        return ' '.join([x['text'] for x in transcript_list])
    except TranscriptsDisabled:
        raise Exception("❌ A transcrição está desativada para este vídeo.")
    except NoTranscriptFound:
        raise Exception("⚠️ Nenhuma transcrição foi encontrada para este vídeo.")
    except VideoUnavailable:
        raise Exception("🚫 O vídeo está indisponível.")
    except Exception as e:
        raise Exception(f"Erro inesperado ao obter transcrição: {e}")

# ========== GEMINI UTILITIES ==========

def configure_gemini():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(text):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Resuma em português: {text}")
        return response.text
    except Exception as e:
        raise Exception(f"Erro ao gerar resumo: {e}")

# ========== STREAMLIT APP ==========

def main():
    st.set_page_config(page_title="YouTube + Gemini", layout="centered")
    st.title("📺 YouTube Transcript Summarizer com Gemini")

    video_url = st.text_input("🔗 Insira a URL do vídeo do YouTube:", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    if video_url:
        try:
            video_id = extract_video_id(video_url)
            if not video_id:
                st.error("❌ URL inválida. Não foi possível extrair o ID do vídeo.")
                return

            st.write(f"🎯 ID do vídeo: `{video_id}`")

            video_title = get_video_title(video_url)
            st.subheader(f"🎬 Título do Vídeo: {video_title}")

            transcript = get_transcript(video_id)
            st.subheader("📝 Transcrição:")
            st.write(transcript)

            if st.button("✨ Gerar Resumo com Gemini"):
                configure_gemini()
                summary = generate_summary(transcript)
                if summary:
                    st.subheader("🧠 Resumo Gerado por Gemini:")
                    st.write(summary)
                else:
                    st.error("❌ Não foi possível gerar o resumo.")
        except Exception as e:
            st.error(f"💥 Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
