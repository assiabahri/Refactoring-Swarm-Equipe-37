"""
This module provides various string utility functions.
"""

def reverse_string(s: str) -> str:
    """
    Returns the input string reversed.
    
    Args:
        s (str): The input string.
    
    Returns:
        str: The reversed input string.
    """
    return s[::-1]

def is_palindrome(text: str) -> bool:
    """
    Checks if the input text is a palindrome.
    
    Args:
        text (str): The input text.
    
    Returns:
        bool: True if the input text is a palindrome, False otherwise.
    """
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

def count_vowels(string: str) -> int:
    """
    Returns the number of vowels in the input string.
    
    Args:
        string (str): The input string.
    
    Returns:
        int: The number of vowels in the input string.
    """
    vowels = "aeiou"
    return sum(1 for char in string.lower() if char in vowels)

def capitalize_words(sentence: str) -> str:
    """
    Returns the input sentence with each word capitalized.
    
    Args:
        sentence (str): The input sentence.
    
    Returns:
        str: The input sentence with each word capitalized.
    """
    return " ".join(word.capitalize() for word in sentence.split())

def remove_duplicates(text: str) -> str:
    """
    Returns the input text with duplicate characters removed, preserving order.
    
    Args:
        text (str): The input text.
    
    Returns:
        str: The input text with duplicate characters removed.
    """
    seen = set()
    return "".join(char for char in text if not (char in seen or seen.add(char)))

from dataclasses import dataclass

@dataclass
class StringProcessor:
    """
    A class to process strings.
    
    Attributes:
        text (str): The input string.
    """
    text: str
    
    def length(self) -> int:
        """
        Returns the length of the input string.
        
        Returns:
            int: The length of the input string.
        """
        return len(self.text)
    
    def word_count(self) -> int:
        """
        Returns the number of words in the input string.
        
        Returns:
            int: The number of words in the input string.
        """
        return len(self.text.split())
    
    def to_upper(self) -> str:
        """
        Returns the input string in uppercase.
        
        Returns:
            str: The input string in uppercase.
        """
        return self.text.upper()