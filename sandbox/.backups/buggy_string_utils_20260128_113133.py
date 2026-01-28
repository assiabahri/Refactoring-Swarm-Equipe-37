def reverse_string(s):
    result=""
    for i in range(len(s)-1,-1,-1):
        result+=s[i]
    return result

def is_palindrome(text):
    cleaned=text.lower().replace(" ","")
    return cleaned==cleaned[::-1]

def count_vowels(string):
    vowels="aeiou"
    count=0
    for char in string.lower():
        if char in vowels:
            count+=1
    return count

def capitalize_words(sentence):
    words=sentence.split(" ")
    result=[]
    for word in words:
        result.append(word.capitalize())
    return " ".join(result)

def remove_duplicates(text):
    seen=set()
    result=[]
    for char in text:
        if char not in seen:
            seen.add(char)
            result.append(char)
    return "".join(result)

class StringProcessor:
    def __init__(self,text):
        self.text=text
    
    def length(self):
        return len(self.text)
    
    def word_count(self):
        return len(self.text.split())
    
    def to_upper(self):
        return self.text.upper()
