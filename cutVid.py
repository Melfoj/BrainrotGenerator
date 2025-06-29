from moviepy.editor import VideoFileClip
import os

def split_video(input_path, output_dir, segment_duration=120):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = VideoFileClip(input_path)
    video_duration = int(video.duration)

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    for start in range(0, video_duration, segment_duration):
        end = min(start + segment_duration, video_duration)
        segment = video.subclip(start, end)
        output_path = os.path.join(output_dir, f"{base_name}_part_{start//segment_duration + 1}.mp4")
        print(f"Exporting {output_path} ({start}s to {end}s)...")
        segment.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

    print("Done splitting video.")

if __name__ == "__main__":
    # Example usage
    input_video = "Videos/SS.mp4"      # Change this to your video filename
    output_folder = "Videos"   # Folder where segments will be saved
    split_video(input_video, output_folder)
