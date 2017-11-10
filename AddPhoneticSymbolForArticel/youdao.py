from urllib.request import urlopen
from bs4 import BeautifulSoup


def CheckSymbolFromYoudao(word):
    url_template = r"http://www.youdao.com/w/eng/{0}/#keyfrom=dict2.index"
    url_word = url_template.format(word)
    symbol_dict={}
    try:
        bs_obj = BeautifulSoup(urlopen(url_word).read(),'html.parser')
    except:
        return None
    pronounce_list = bs_obj.find_all('span',class_='pronounce')
    for i in pronounce_list:
        str_pronounce = [j for j in i.stripped_strings]
        if len(str_pronounce)==2:
            symbol_dict[str_pronounce[0]] = str_pronounce[1]
            # if str_pronounce[0]=='美':
            #         return str_pronounce[1]
    if "美" in symbol_dict.keys():
        return symbol_dict["美"]
    elif "英" in symbol_dict.keys():
        return  symbol_dict["英"]
    else:
        return None