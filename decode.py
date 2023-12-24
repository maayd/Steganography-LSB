import sys

from PIL import Image
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
def main():
    filepath = sys.argv[1]
    data = decode(filepath)
    file = open("decoded_secret.txt", "w")
    textdata = ''

    for i in data:
        textdata += i.decode("utf-8")
        file.write(i.decode("utf-8"))
    file.close()
    print(textdata)
    print()
    print("Encoding and decoding finished successfully!")

# Driver Code
if __name__ == '__main__':
    # Calling main function
    main()