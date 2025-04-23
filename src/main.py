import streamlit as st
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

import gemini_utils  # Certifique-se de que este módulo está correto e configurado

def get_transcription(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except TranscriptsDisabled:
        return "❌ Este vídeo não possui legendas ativadas."
    except NoTranscriptFound:
        return "❌ Nenhuma transcrição encontrada para este vídeo."
    except Exception as e:
        return f"⚠️ Erro ao obter transcrição: {str(e)}"

def main():
    st.title("📺 YouTube Summarizer com Gemini")

    video_url = st.text_input("🔗 Insira a URL do vídeo do YouTube:")
    if video_url:
        try:
            yt = YouTube(video_url)
            video_id = yt.video_id
            video_title = yt.title

            st.subheader(f"🎬 Título do Vídeo: {video_title}")
            transcript = get_transcription(video_id)

            if transcript.startswith("❌") or transcript.startswith("⚠️"):
                st.warning(transcript)
            else:
                st.subheader("📝 Transcrição:")
                st.write(transcript)

                if st.button("✨ Gerar Resumo com Gemini"):
                    gemini_utils.configure_gemini()
                    summary = gemini_utils.generate_summary(transcript)

                    if summary:
                        st.subheader("📄 Resumo Gerado:")
                        st.write(summary)
                    else:
                        st.error("Erro ao gerar o resumo com Gemini.")

        except Exception as e:
            st.error(f"💥 Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
