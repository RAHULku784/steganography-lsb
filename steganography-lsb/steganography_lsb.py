from PIL import Image

# ✅ Use your uploaded file
input_img_path = 'stegno.png.jpg'
img = Image.open(input_img_path).convert('RGB')

# Message helpers
def message_to_binary(message):
    return ''.join([format(ord(char), '08b') for char in message])

def binary_to_message(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

# Encode function
def encode_image(img, message, out_path):
    binary_msg = message_to_binary(message) + '1111111111111110'
    data = iter(img.getdata())
    new_pixels = []

    for i in range(0, len(binary_msg), 3):
        pixel = list(next(data))
        for j in range(3):
            if i + j < len(binary_msg):
                pixel[j] = pixel[j] & ~1 | int(binary_msg[i + j])
        new_pixels.append(tuple(pixel))

    new_pixels += list(data)
    encoded = Image.new(img.mode, img.size)
    encoded.putdata(new_pixels)
    encoded.save(out_path)
    return out_path

# Decode function
def decode_image(img):
    binary_data = ''
    for pixel in img.getdata():
        for value in pixel[:3]:
            binary_data += str(value & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded = ''
    for byte in all_bytes:
        if byte == '11111110':
            break
        decoded += chr(int(byte, 2))
    return decoded

# ✅ Your message here
secret = "Rahul is doing a Cyber Security project on Steganography"
encoded_path = encode_image(img, secret, 'output.png')
decoded_msg = decode_image(Image.open(encoded_path))

print("✅ Message encoded and saved as output.png")
print("🔍 Decoded Message:", decoded_msg)