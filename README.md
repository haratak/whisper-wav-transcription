# Whisper Wav Transcription

Whisper Wav Transcription は、OpenAI の API を使用して、Wavファイルを自動文字起こしするPythonスクリプトです。

## 必要なもの

Python 3.6 以降
OpenAI API キー
pydub ライブラリ
インストール

```bash

pip install pydub
pip install openai

```

## 使い方

```bash

python whisper_wav_transcription.py [-h] wav_source_path transcription_file_name
wav_source_path: 自動文字起こしする Wav ファイルのパス
transcription_file_name: 出力する自動文字起こし結果のファイル名

```

## 例

```bash
python whisper_wav_transcription.py example.wav transcription.txt
```

上記例では、example.wav ファイルの自動文字起こしを行い、transcription.txt ファイルに結果を出力します。

