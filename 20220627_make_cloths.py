import os
from PIL import Image
import numpy as np
import cv2
save_base_dir = r'F:\002_data\character_cloth'
if not os.path.exists(save_base_dir) : os.mkdir(save_base_dir)
cloth_base_dir = r'F:\002_data\glitter_cloth'
clothes = os.listdir(cloth_base_dir)
pure_name_dict = {}
for cloth in clothes :
    cloth_dir = os.path.join(cloth_base_dir, cloth)
    cloth_pil = Image.open(cloth_dir)
    # -------------------------------------------------------------------
    # frame 가져 오기
    cloth_frame_base_dir = r'F:\002_data\cloth_from_model'
    characters = os.listdir(cloth_frame_base_dir)
    for n, character in enumerate(characters) :
        character_dir = os.path.join(save_base_dir, character)
        if not os.path.exists(character_dir): os.mkdir(character_dir)
        if n >= 0 :
            character_dir = os.path.join(cloth_frame_base_dir, character)
            frames = os.listdir(character_dir)
            for frame in frames :
                if frame.startswith('test') :
                    frame_dir = os.path.join(character_dir, frame)
                    frame_pil = Image.open(frame_dir)
                    frame_np = np.array(frame_pil)
                    cloth_pil = cloth_pil.resize(frame_pil.size)
                    cloth_np = np.array(cloth_pil, dtype = np.uint8)
                    # ----------------------------------------------------
                    # 이미지 합성
                    frame_cv = cv2.imread(frame_dir)
                    #cv2.imshow('frame_cv', frame_cv)
                    cloth_cv = cv2.imread(cloth_dir)
                    cloth_cv = cv2.resize(cloth_cv, (frame_cv.shape[:2][1], frame_cv.shape[:2][0]))
                    #cv2.imshow('cloth_cv', cloth_cv)
                    #                    cv2.waitKey(0)
                    sum_cv = cv2.add(cloth_cv ,frame_cv, dtype=cv2.CV_8U)
                    pure_name = character + '_' + cloth.split('.')[0]

                    try :
                        pure_name_dict[pure_name] += 1
                    except :
                        pure_name_dict[pure_name] = 1
                    new_name = pure_name + '_' + str(pure_name_dict[pure_name]) + '.png'
                    new_dir = os.path.join(character_dir,new_name)
                    cv2.imwrite(new_dir,sum_cv)










                    #sum = cloth_np + frame_np
                    #sum_np = np.uint8(sum)
                    #height, width, channel = sum.shape

                    #cubics = []
                    #for height_index, row in enumerate(sum) :
                    ##    row_pixels = []
                    #    for width_index, column in enumerate(row) :
                    #        cloth_pixel = cloth_np[height_index,width_index,:]
                    #        frame_pixel = frame_np[height_index, width_index, :]
                    #        sum_pixel   = sum_np[height_index, width_index,:]
                    #        check = np.array_equal(cloth_pixel,sum_pixel)
                    #        if check == 'True' :
                    #            pixel = cloth_pixel
                    #        else :
                    #            pixel = frame_pixel
                    #        pixel = pixel.tolist()
                    #        row_pixels.append(pixel)
                    #    cubics.append(row_pixels)
                    #cubic = np.array(cubics)
                    #cubic = Image.fromarray(np.uint8(cubic))
                    #cubic.convert('RGB').show()
                    #cloth.show()








                    #        cloth_vector = cloth_np.flatten()
                    #sum_vector   = sum.flatten()


                    #new_vector = []
                    #for c, s in zip(cloth_vector, sum_vector) :
                    #    if c == s :
                    #        value = c
                     #   else :
                      #      value = s
                       # new_vector.append(value)
                       # new_map = np.array([new_vector])
                       # new_map = np.reshape(new_map, (1,1,new_map.shape[-1]))
                       # np.reshape(new_map, (height, width, -1))


                        #new_map = np.reshape(new_map, (height, width, channel))
                        #new_map =
                        #new_map.reshape()
                   # print(sum)
                    #sum_image = Image.fromarray(sum)
                    #sum_image.show()
