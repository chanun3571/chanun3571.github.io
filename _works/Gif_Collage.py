from PIL import Image, ImageSequence
import os

# Function to load an image and return its frames
def load_image(image_path, target_height, gif_duration=None):
    with Image.open(image_path) as image:
        aspect_ratio = target_height / image.height
        new_width = int(image.width * aspect_ratio)
        resized_frames = []

        if gif_duration is None:
            gif_duration = image.info.get("duration", 100)  # Default duration for still images

        for frame in ImageSequence.Iterator(image):
            resized_frame = frame.copy().resize((new_width, target_height))
            resized_frame.info["duration"] = gif_duration  # Set the frame duration
            resized_frames.append(resized_frame)

    return resized_frames

# Function to create an animated GIF from frames
def create_animated_gif(frames, output_path, loop=0):
    if not frames:
        return

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        loop=loop,
        duration=frames[0].info.get("duration", 100),  # Get the frame duration
        disposal=2,  # Set disposal to 2 (Background) for proper animation
    )

# Function to create a still image from a single frame
def create_still_image(frame, output_path):
    frame.save(output_path)

# Load your input images and resize them to a target height of 480 pixels
input_image1 = "output_image.gif"
input_image2 = "5b.jpg"

# Determine if at least one input image is a .gif
input_image1_is_gif = input_image1.lower().endswith(".gif")
input_image2_is_gif = input_image2.lower().endswith(".gif")

# Determine the GIF duration for the still image
gif_duration = None
if input_image1_is_gif or input_image2_is_gif:
    if input_image1_is_gif:
        gif_duration = Image.open(input_image1).info.get("duration", 100)
    if input_image2_is_gif:
        gif_duration = Image.open(input_image2).info.get("duration", 100)

image1_frames = load_image(input_image1, target_height=480, gif_duration=gif_duration)
image2_frames = load_image(input_image2, target_height=480, gif_duration=gif_duration)

# Determine the number of frames in the input images
num_frames = max(len(image1_frames), len(image2_frames))

# If one image has fewer frames, repeat its frames or duplicate the last frame to match the number of frames in the other image
if len(image1_frames) < num_frames:
    image1_frames += [image1_frames[-1]] * (num_frames - len(image1_frames))
if len(image2_frames) < num_frames:
    image2_frames += [image2_frames[-1]] * (num_frames - len(image2_frames))

# Create a list to store the merged frames
merged_frames = []

# Combine frames from both images side by side with a 20-pixel white gap in the middle
for i in range(num_frames):
    new_width = image1_frames[i].width + 20 + image2_frames[i].width
    new_height = max(image1_frames[i].height, image2_frames[i].height)

    new_frame = Image.new("RGB", (new_width, new_height), (255, 255, 255))
    new_frame.paste(image1_frames[i], (0, (new_height - image1_frames[i].height) // 2))
    new_frame.paste(image2_frames[i], (image1_frames[i].width + 20, (new_height - image2_frames[i].height) // 2))
    merged_frames.append(new_frame)

# Determine the output file extension based on the inputs
if input_image1_is_gif or input_image2_is_gif:
    output_extension = ".gif"
else:
    output_extension = ".jpg"

if output_extension == ".gif":
    # Create an animated GIF from the merged frames with a specified loop count (e.g., 0 for infinite looping)
    create_animated_gif(merged_frames, "output_image" + output_extension, loop=0)
else:
    # Create a still image
    create_still_image(merged_frames[0], "output_image" + output_extension)

# Close the input images
for frames in [image1_frames, image2_frames]:
    for frame in frames:
        frame.close()
