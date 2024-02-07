from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    #utils.NotImplemented()
    not_exist = [0] * 26
    deciphered = [""] * 26
    hash_table = {item: True for item in dictionary}
    for i in range(26):
        for char in ciphered:
            if(char != ' '):
                decrypted_char = ord(char) - i
                decrypted_char = (decrypted_char - 97) % 26 + 97
                deciphered[i] += chr(decrypted_char)
            else:
                deciphered[i] += char
        words = deciphered[i].split()
        for word in words:
            if (word not in hash_table):
                not_exist[i]+=1
    min_non_exist= min(not_exist)
    idx = not_exist.index(min_non_exist)
    return (deciphered[idx],idx,min_non_exist)