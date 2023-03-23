# -*- coding: utf-8 -*-
import argparse
import openai
import os
import math
import concurrent.futures
from pydub import AudioSegment

# APIキーを設定
openai.api_key = os.environ["OPENAI_API_KEY"]


def transcribe_audio_file(file_path, start_time, end_time):
    # 音声ファイルを読み込む
    audio = AudioSegment.from_file(file_path)

    # 開始時刻と終了時刻で音声ファイルを切り取る
    sliced_audio = audio[start_time:end_time]
    sliced_file_name = f"sliced_{start_time}_{end_time}.wav"
    sliced_audio.export(sliced_file_name, format="wav")

    with open(sliced_file_name, "rb") as f:
        response = openai.Audio.transcribe(
            "whisper-1",
            file=f,
            response_format="text"
        )
    os.remove(sliced_file_name)
    return response


def parallel_transcription(file_path, segment_duration=60000, output_file="transcription.txt"):
    audio = AudioSegment.from_file(file_path)
    audio_duration = len(audio)
    num_segments = math.ceil(audio_duration / segment_duration)

    start_times = [i * segment_duration for i in range(num_segments)]
    end_times = [(i + 1) * segment_duration for i in range(num_segments)]
    end_times[-1] = audio_duration

    with concurrent.futures.ThreadPoolExecutor() as executor:
        transcriptions = list(executor.map(transcribe_audio_file, [
                              file_path] * num_segments, start_times, end_times))

    with open(output_file, "w", encoding="utf-8") as f:
        for transcription in transcriptions:
            f.write(transcription + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wav_source_path", help="path to wav file source")
    parser.add_argument("transcription_file_name",
                        help="path to transcription file name")
    args = parser.parse_args()

    input_file = args.wav_source_path
    output_file = args.transcription_file_name

    parallel_transcription(input_file, output_file=output_file)
