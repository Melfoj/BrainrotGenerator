from moviepy.editor import VideoFileClip
import os

def splitVideo(inputPath, outputDir, segmentDuration=120):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    video = VideoFileClip(inputPath)
    videoDuration = int(video.duration)

    baseName = os.path.splitext(os.path.basename(inputPath))[0]

    for start in range(0, videoDuration, segmentDuration):
        end = min(start + segmentDuration, videoDuration)
        segment = video.subclip(start, end)
        outputPath = os.path.join(outputDir, f"{baseName}_part_{start // segmentDuration + 1}.mp4")
        print(f"Exporting {outputPath} ({start}s to {end}s)...")
        segment.write_videofile(outputPath, codec="libx264", audio_codec="aac", logger=None)

    print("Done splitting video.")

if __name__ == "__main__":
    # Example usage
    inputVideo = "Videos/SS.mp4"     # Change this to your video filename
    outputFolder = "Videos"          # Folder where segments will be saved
    splitVideo(inputVideo, outputFolder)
