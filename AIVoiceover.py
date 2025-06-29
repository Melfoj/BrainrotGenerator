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
def audio_speedx(audio_clip, factor):
    new_duration = audio_clip.duration / factor
    return AudioClip(
        lambda t: audio_clip.get_frame(t * factor),
        duration=new_duration,
        fps=audio_clip.fps
    )

# Split text into n-word batches
def split_text_in_batches(text, n=6):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(0, len(words), n)]

# Generate timed text clips based on audio duration
def generate_text_clips(text, video_size, audio_duration, words_per_clip=5):
    batches = split_text_in_batches(text, words_per_clip)
    total_words = len(text.split())
    avg_word_duration = audio_duration / total_words

    clips = []
    time_pointer = 0
    for batch in batches:
        batch_word_count = len(batch.split())
        duration = avg_word_duration * batch_word_count

        txt_clip = TextClip(
            batch,
            fontsize=30,
            font="fonts/Ultra.ttf",  # Must match the installed or provided TTF font
            color="white",
            stroke_color="black",
            stroke_width=2,
            method='caption',
            size=(video_size[0] * 0.9, None)
        ).set_position(("center", "bottom")).set_start(time_pointer).set_duration(duration)

        txt_clip = txt_clip.fadein(0.05).fadeout(0.05)

        clips.append(txt_clip)
        time_pointer += duration

    return clips


def add_voiceover_and_text(video_path, text, output_path="Videos/output_video.mp4", speed=1.0):
    # Generate TTS audio
    tts = gTTS(text)
    tts_audio_path = "temp_audio.mp3"
    tts.save(tts_audio_path)

    # Load video and audio
    video = VideoFileClip(video_path)
    audio = AudioFileClip(tts_audio_path)

    # Speed up audio
    sped_up_audio = audio_speedx(audio, speed)

    # Trim video to match sped-up audio
    video = video.subclip(0, sped_up_audio.duration)

    # Set sped-up audio to video
    video = video.set_audio(sped_up_audio)

    # Generate text clips in batches
    text_clips = generate_text_clips(text, video.size, sped_up_audio.duration)

    # Final composition
    final = CompositeVideoClip([video] + text_clips)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Clean up
    audio.close()
    sped_up_audio.close()
    os.remove(tts_audio_path)

if __name__ == "__main__":
    input_video = "Videos/SS_part_1.mp4"
    narration_text = (
        "AITA for canceling my brother’s wedding gift after he uninvited me from the wedding? "
        "So, I (28F) was supposed to attend my brother’s wedding next month. We’ve always had a rocky "
        "relationship, but I still love him, and I was genuinely excited. I even got him and his fiancée "
        "a really expensive espresso machine from their registry — like, $700 expensive. A few days ago, "
        # "I got a call from him. He awkwardly said that they were making the wedding “smaller” and that "
        # "unfortunately, I didn’t make the final guest list. I was shocked. I asked why, and he said something "
        # "about “keeping the drama down” and wanting “a peaceful environment.” I asked if his fiancée’s sister "
        # "— who literally keyed my car two years ago — was still going. He said yes. So I was cut to “avoid drama,” "
        # "but she wasn’t? Anyway, I told him I understood and hung up. That night, I went online and canceled the "
        # "espresso machine order. It hadn’t shipped yet, so I got a full refund. Well, fast forward to yesterday. "
        # "He texts me a picture of the empty gift table and says, “Thanks for not even sending a card.” I replied, "
        # "“Thanks for uninviting me from the wedding.” Now my mom is blowing up my phone saying I’m being petty and "
        # "making things worse. She says “family is family” and that gifts shouldn't be conditional. But honestly? "
        # "If I'm not good enough to be at the wedding, why should my $700 be? AITA?"
    )
    add_voiceover_and_text(input_video, narration_text, speed=1.3)
