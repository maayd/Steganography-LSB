import glob
import sys

from PIL import Image


#

def bitstring_to_bytes(s):
    if s == "00000000":
        return bytearray(1)
    else:
        v = int(s, 2)
        b = bytearray()
        while v:
            b.append(v & 0xff)
            v >>= 8
        return bytes(b[::-1])


# Convert from ASCII value to 8-bit binary
def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        if len(i) == 0:
            newd.append(format(32, '08b'))
        else:
            newd.append(format(ord(i), '08b'))
    return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    # print("lendata is: ", lendata)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
    return newimg


# Decode the data in the image
def decode(fileName):
    fileName = Image.open(fileName, 'r')

    data = []
    imgdata = iter(fileName.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data.append(bitstring_to_bytes(binstr))
        if (pixels[-1] % 2 != 0):
            return data


# Main Function
def main():
    secret_message = []



    # use filepath to choose the file you want to hide inside the image/images.
    filepath = "files/quiz.pdf"



    with open(filepath, "rb") as f:
        byte = f.read(1)
        while byte:
            secret_message.append(byte)
            byte = f.read(1)

    # use pics_dir to specify the folder with images to hide the data in (by default its a folder called pics in the same directory).
    pics_dir = "pics"



    pics_dir += "/*"
    pics = glob.glob(pics_dir)
    secret_images_sizes = []
    for i in pics:
        tmp = Image.open(i)
        secret_images_sizes.append(int((tmp.width * tmp.height) / 3.0))
    print("pics are: ", pics)
    print("amount of bytes each pic can hold respectively: ", secret_images_sizes)
    print("Total number of bytes available for hiding: ", sum(secret_images_sizes))
    print("size of message to be concealed (in bytes): ", len(secret_message))
    if len(secret_message) > sum(secret_images_sizes):
        print(
            "Secret message provided is larger than the available set of images. Please add more images or choose a "
            "smaller file.")
        sys.exit("Exiting code...")
    print("----------------------------------------------------------------")

    images_needed = []
    tmp = 0
    for i in range(len(pics)):
        if len(secret_message) > tmp:
            images_needed.append(pics[i])
            tmp += secret_images_sizes[i]
    print("images needed are: ", images_needed)

    encoded_images = []
    j = 0
    k = 0
    for i in range(len(images_needed)):
        img = Image.open(images_needed[i], 'r')
        if i == len(images_needed) - 1:
            k = len(secret_message)
        else:
            k = k + secret_images_sizes[i]
        print("from ", j, " to ", k)
        encoded_images.append(encode(img, secret_message[j:k]))
        j = k

    for i in range(len(encoded_images)):
        name = "secret" + str(i) + ".png"
        encoded_images[i].save(name, "png")

    datalist = []
    for i in range(len(images_needed)):
        filename = "secret" + str(i) + ".png"
        datalist.append(decode(filename))

    file = open(("decoded_secret" + filepath[-4:]), "wb")
    for data in datalist:
        for i in data:
            file.write(i)
    file.close()
    print()
    print("Encoding and decoding finished successfully!")


# Driver Code
if __name__ == '__main__':
    # Calling main function
    main()
