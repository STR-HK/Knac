import json

def jamo(args):
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    r_lst = []

    for w in list(args):

        if (w == '○'):
            r_lst.append('○')
            continue
        
        ch1 = (ord(w) - ord('가')) // 588
        ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
        ch3 = (ord(w) - ord('가')) - (588 * ch1) - (28 * ch2)

        r_lst.append(CHOSUNG_LIST[ch1])
        r_lst.append(JUNGSUNG_LIST[ch2])
        r_lst.append(JONGSUNG_LIST[ch3])
    
    return r_lst

def gyeopjamo(args):

    data = '''{
                "ㄲ" : "ㄱㄱ", "ㄸ" : "ㄷㄷ", "ㅃ" : "ㅂㅂ", "ㅆ" : "ㅅㅅ", "ㅉ" : "ㅈㅈ", 
                "ㄳ" : "ㄱㅅ", "ㄵ" : "ㄴㅈ", "ㄶ" : "ㄴㅎ", "ㄺ" : "ㄹㄱ", "ㄻ" : "ㄹㅁ", 
                "ㄼ" : "ㄹㅂ", "ㄽ" : "ㄹㅅ", "ㄾ" : "ㄹㅌ", "ㄿ" : "ㄹㅍ", "ㅀ" : "ㄹㅎ", "ㅄ" : "ㅂㅅ", 
                "ㅐ" : "ㅏㅣ", "ㅒ" : "ㅑㅣ", "ㅔ" : "ㅓㅣ", "ㅖ" : "ㅕㅣ", "ㅘ" : "ㅗㅏ", 
                "ㅙ" : "ㅗㅏㅣ", "ㅚ" : "ㅗㅣ", "ㅝ" : "ㅜㅓ", "ㅞ" : "ㅜㅓㅣ", "ㅟ" : "ㅜㅣ", "ㅢ" : "ㅡㅣ", "" : ""
            }'''

    data = json.loads(data)

    returns = []

    for s in range(len(args)):
        if args[s] not in data:
            returns.append(args[s])
        if args[s] in data:
            returns.append(data[args[s]])

    return returns

def convertonumber(args):

    data = '''{
                "ㄱ" : 2, "ㄴ" : 2, "ㄷ" : 3, "ㄹ" : 5, "ㅁ" : 4, "ㅂ" : 4, "ㅅ" : 2, 
                "ㅇ" : 1, "ㅈ" : 3, "ㅊ" : 4, "ㅋ" : 3, "ㅌ" : 4, "ㅍ" : 4, "ㅎ" : 3, 
                "ㅏ" : 2, "ㅑ" : 3, "ㅓ" : 2, "ㅕ" : 3, "ㅗ" : 2, "ㅛ" : 3, 
                "ㅜ" : 2, "ㅠ" : 3, "ㅡ" : 1, "ㅣ" : 1, "○" : 0
            }'''

    data = json.loads(data)
    returns = 0

    for v in range(len(args)):
        returns += data[args[v]]
        
    return returns