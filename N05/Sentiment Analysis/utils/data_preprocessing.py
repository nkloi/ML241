import re
import string
from underthesea import text_normalize, word_tokenize
import emoji

def clean_text(text): 
    """ 
    Preprocesses a single text string by applying a series of normalization steps. 
    Steps include: 
        1. Converting text to lowercase. 
        2. Removing emojis, replacing them with spaces.
        3. Reducing repeated characters (e.g., 'chấtttt lượngg' -> 'chất lượng'). 
        4. Normalizing punctuation spacing to ensure proper separation. 
        5. Stripping leading and trailing spaces. 
        6. Removing all punctuation. 
        7. Normalizing Vietnamese text for consistent diacritics and formatting. 
        8. Tokenizing the text into words for further processing. 
    Args: 
        text (str): The input text string to preprocess. 
    Returns: 
        str: The cleaned and tokenized text string. 
    """
    # Lowercase text 
    text = text.lower() 
    
    # Remove emoji 
    text = emoji.replace_emoji(text, replace=' ') 
    
    # Reduce repeated characters (e.g., 'chấtttt lượngg' -> 'chất lượng') 
    text = re.sub(r'(.)\1+', r'\1', text)

    # Normalize punctuation spacing 
    text = re.sub(r'(\w)([' + string.punctuation + '])(\w)', r'\1 \2 \3', text) 
    text = re.sub(r'([' + string.punctuation + '])([' + string.punctuation + '])+', r'\1', text) 
    
    # Remove leading/trailing spaces 
    text = text.strip() 
    
    # Remove punctuation 
    text = text.translate(str.maketrans('', '', string.punctuation)) 
    
    # Normalize Vietnamese text 
    text = text_normalize(text) 
    
    # Tokenize 
    text = word_tokenize(text, format='text') 
    
    return text

if __name__ == '__main__':
    text = 'Chấttt lượngg sản phẩm tuyệt vời,sẽ ủng hộ shop nhiều.';
    print(clean_text(text))