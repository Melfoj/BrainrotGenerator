from moviepy.config import change_settings
from moviepy.editor import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip
)
from moviepy.audio.AudioClip import AudioClip
from gtts import gTTS
import os

change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# Custom audio speed-up function (compatible with older MoviePy)
def audioSpeedx(audioClip, factor):
    newDuration = audioClip.duration / factor
    return AudioClip(
        lambda t: audioClip.get_frame(t * factor),
        duration=newDuration,
        fps=audioClip.fps
    )

# Split text into n-word batches
def splitTextInBatches(text, n=6):
    words = text.split()
    return [' '.join(words[i:i + n]) for i in range(0, len(words), n)]

# Generate timed text clips based on audio duration
def generateTextClips(text, videoSize, audioDuration, wordsPerClip=5):
    batches = splitTextInBatches(text, wordsPerClip)
    totalWords = len(text.split())
    avgWordDuration = audioDuration / totalWords

    clips = []
    timePointer = 0
    for batch in batches:
        batchWordCount = len(batch.split())
        duration = avgWordDuration * batchWordCount

        txtClip = TextClip(
            batch,
            fontsize=30,
            font="fonts/Ultra.ttf",  # Must match the installed or provided TTF font
            color="white",
            stroke_color="black",
            stroke_width=2,
            method='caption',
            size=(videoSize[0] * 0.9, None)
        ).set_position(("center", "bottom")).set_start(timePointer).set_duration(duration)

        txtClip = txtClip.fadein(0.05).fadeout(0.05)

        clips.append(txtClip)
        timePointer += duration

    return clips

def addVoiceoverAndText(videoPath, text, outputPath="Videos/output_video.mp4", speed=1.0):
    # Generate TTS audio
    tts = gTTS(text)
    ttsAudioPath = "temp_audio.mp3"
    tts.save(ttsAudioPath)

    # Load video and audio
    video = VideoFileClip(videoPath)
    audio = AudioFileClip(ttsAudioPath)

    # Speed up audio
    spedUpAudio = audioSpeedx(audio, speed)

    # Trim video to match sped-up audio
    video = video.subclip(0, spedUpAudio.duration)

    # Set sped-up audio to video
    video = video.set_audio(spedUpAudio)

    # Generate text clips in batches
    textClips = generateTextClips(text, video.size, spedUpAudio.duration)

    # Final composition
    final = CompositeVideoClip([video] + textClips)
    final.write_videofile(outputPath, codec='libx264', audio_codec='aac')

    # Clean up
    audio.close()
    spedUpAudio.close()
    os.remove(ttsAudioPath)

if __name__ == "__main__":
    inputVideo = "Videos/SS_part_1.mp4"
    narrationText = (
        "AITA for canceling my brother’s wedding gift after he uninvited me from the wedding? "
        "So, I (28F) was supposed to attend my brother’s wedding next month. We’ve always had a rocky "
        "relationship, but I still love him, and I was genuinely excited. I even got him and his fiancée "
        "a really expensive espresso machine from their registry — like, $700 expensive. A few days ago, "
        "I got a call from him. He awkwardly said that they were making the wedding “smaller” and that "
        "unfortunately, I didn’t make the final guest list. I was shocked. I asked why, and he said something "
        "about “keeping the drama down” and wanting “a peaceful environment.” I asked if his fiancée’s sister "
        "— who literally keyed my car two years ago — was still going. He said yes. So I was cut to “avoid drama,” "
        "but she wasn’t? Anyway, I told him I understood and hung up. That night, I went online and canceled the "
        "espresso machine order. It hadn’t shipped yet, so I got a full refund. Well, fast forward to yesterday. "
        "He texts me a picture of the empty gift table and says, “Thanks for not even sending a card.” I replied, "
        "“Thanks for uninviting me from the wedding.” Now my mom is blowing up my phone saying I’m being petty and "
        "making things worse. She says “family is family” and that gifts shouldn't be conditional. But honestly? "
        "If I'm not good enough to be at the wedding, why should my $700 be? AITA?"
    )
    addVoiceoverAndText(inputVideo, narrationText, speed=1.3)
