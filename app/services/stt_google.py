from google.cloud import speech

def STT(audio_file_path: str) -> str:
  client=speech.SpeechClient()

  with open(audio_file_path, "rb") as f:
    audio_bytes=f.read()
  
  audio=speech.RecognitionAudio(content=audio_bytes)
  config=speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="ko-KR",
  )

  response=client.recognize(
    config=config,
    audio=audio
  )

  if not response.results:
    return ""
  
  return response.results[0].alternatives[0].transcript