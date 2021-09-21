# Decoding a message:

import string
alphabet_string = string.ascii_lowercase
alphabet = alphabet_string
#print(alphabet)
punctuation = ".,?! "
#print(punctuation)

def decoder(message, offset):
    decoded_message = ""
    for letter in message:
        if letter not in punctuation:
            letter_value = alphabet.find(letter)
            decoded_message += alphabet[(letter_value + offset) % 26]
        else:
            decoded_message += letter
    return decoded_message

#print(decoder("xuo jxuhu! jxyi yi qd unqcfbu ev q squiqh syfxuh. muhu oek qrbu \
#je tusetu yj? y xefu ie! iudt cu q cuiiqwu rqsa myjx jxu iqcu evviuj!", 10))
#print(decoder("xy lyixqb, cuiiqwu husyulut bekt qdt sbuqh!", 10))

# Sending a coded message:

def encoder(message, offset):
    coded_message = ""
    for letter in message:
        if letter not in punctuation:
            letter_value = alphabet.find(letter)
            coded_message += alphabet[(letter_value - offset) % 26]
        else:
            coded_message += letter
    return coded_message

#print(encoder("hi vishal, message recieved loud and clear!", 10))
