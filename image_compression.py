import os
import time
import stat
from PIL import Image




def compress_images(directory=False):
    if directory:
        os.chdir(directory)

    # 2. Extract all of the .jpeg files:
    files = os.listdir()

    # 3. Extract all of the images:
    images = [file for file in files if file.endswith('jpg')]

    # 4. Loop over every image:
    for image in images:


        # 5. Open every image:
        img = Image.open(image)

        # 5. Compress every image and save it with a new name:
        dim = img.size

        if dim[1] < dim[0]:
            img.close()
            os.chmod(image, stat.S_IWRITE)
            os.remove(image)
            continue
        try :
            RGB_img = img.convert("RGB")
            comp_img = RGB_img.resize((350,420))
        except :
            img.close()
            os.chmod(image, stat.S_IWRITE)
            os.remove(image)
            continue
        os.chmod(image, stat.S_IWRITE)
        comp_img.save(image)



train = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\Dataset\train"
test = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\Dataset\test"
val = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\Dataset\val"
for i in [train, test, val]:
    rootdir = i
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            compress_images(d)