import json
import os

# Read the original JSON file
input_file = "dataset/Math/selected/Math.json"
with open(input_file, 'r') as f:
    data = json.load(f)

# Update image URLs
for item in data:
    index = item['index']
    # If there are multiple images, handle them separately
    if isinstance(item['image_url'], list):
        # Count number of images
        num_images = len(item['image_url'])
        if num_images == 1:
            item['image_url'] = [f"/mnt/zeli/LRM_Benchmark/dataset/Math/selected/images/Math_{index}.png"]
        else:
            # For multiple images, append _0, _1, etc.
            item['image_url'] = [f"/mnt/zeli/LRM_Benchmark/dataset/Math/selected/images/Math_{index}_{i}.png" for i in range(num_images)]

# Write the modified JSON back to file
output_file = "dataset/Math/selected/Math_updated.json"
with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Updated JSON has been saved to {output_file}") 