import os
base_dir = r'C:\Users\dream\OneDrive\바탕 화면\pinterest_3'
files = os.listdir(base_dir)
files = sorted(files)
net_dict = {}
for file in files :
	if 'size_3' in file :
		split_file = file.split('_')
		new_file_name = '_'.join(split_file[:-2])

		file_dir = os.path.join(base_dir, file)
		images = sorted(os.listdir(file_dir))
		nets = sorted([image.split('_')[-1] for image in images])
		net_dict[new_file_name] = nets

for file in files :
	if 'size_3' not in file:
		# -------------------------------------------------------------------
		file_dir = os.path.join(base_dir, file)
		real_images = os.listdir(file_dir)

		split_file = file.split('_')
		if 'png' not in file :
			new_file_name = '_'.join(split_file[:-2])
		else :
			new_file_name = '_'.join(split_file[:-3])
		valid_images = net_dict[new_file_name]

		for real_image in real_images :
			check_name = real_image.split('_')[-1]
			if check_name not in  valid_images :
				real_image_dir = os.path.join(file_dir, real_image)
				os.remove(real_image_dir)