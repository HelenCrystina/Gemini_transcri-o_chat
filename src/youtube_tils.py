from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcription(video_id):
    try:
        # Obtém a transcrição do vídeo
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Formata a transcrição para texto simples
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        return formatted_transcript
    except Exception as e:
        return f"Erro ao obter transcrição: {str(e)}"

# Exemplo de uso
video_id = 'Ok-xpKjKp2g'  # Este é o ID do vídeo
transcript = get_transcription(video_id)
print(transcript)
