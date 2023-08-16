from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_videos(video_paths):
    """
    Merge a list of videos in the given order.
    
    Args:
    - video_paths (list): List of video file paths.
    
    Returns:
    - VideoClip object. The merged video can saved as output_file.
    """

    clips = [VideoFileClip(video) for video in video_paths]
    final_clip = concatenate_videoclips(clips)
    # final_clip.write_videofile(output_file, codec='libx264')
    return final_clip


# video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]
# final_c = merge_videos(video_files)
# print(final_c)
