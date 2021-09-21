import string
alphabet_string = string.ascii_lowercase
alphabet = list(alphabet_string)
#print(alphabet)

alphabet_numbers = list(range(1,27))
#print(alphabet_numbers)

alphabet_numbered = {alphabet : alphabet_numbers for alphabet, alphabet_numbers
in zip(alphabet, alphabet_numbers)}
#print(numbered_alphabet)

numbered_alphabet = {alphabet_numbers : alphabet for alphabet_numbers, alphabet
in zip(alphabet_numbers, alphabet)}
#print(numbered_alphabet)

def decoder(message, offset):
    letter_number = ()
    offset_number = ()
    for letter in message:
        letter_number = alphabet_numbered.get(letter)
        offset_number = letter_number + offset
        if offset_number > 26:
            offset_number = offset_number - 26
    return numbered_alphabet.get(offset_number)
