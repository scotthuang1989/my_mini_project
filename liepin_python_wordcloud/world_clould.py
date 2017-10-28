from wordcloud import WordCloud, STOPWORDS
from utilng import process_all_job
import matplotlib.pyplot as plt
import jieba
import re
import argparse

import pdb



def word_filter(word):
    filterd_re = r"经验|开发|计算机|算机|能力|职位|职责|岗位|计算|学历|本科|服务|任职|专业|熟悉|\
                  熟练|以上|上学|团队|相关|沟通|掌握|使用|以及|互联|数据库|编程|解决|优先|\
                  优先|工作|负责|责任|参与|了解|参与|技术|描述|进行|具有|考虑|良好|至少|一种|\
                  精神|精通|要求|管理|研发|具备|常用|产品|公司|项目"
    if re.search(filterd_re,word):
        return True
    else:
        return False

def get_text(filename):
    all_job_text = process_all_job.concat_jobs(filename)
    seg_list = jieba.cut(all_job_text, cut_all=False)
    # search engine mode
    # seg_list = jieba.cut_for_search(all_job_text)
    seg_list = list(seg_list)
    filterd_list = [word for word in seg_list if not word_filter(word)]
    return " ".join(filterd_list)
    # filter some unwanted word

def main():

    text = get_text("./liepinwordcloudpy/liepin_python_job.json")
    # Generate a word cloud image
    wordcloud = WordCloud(font_path="WenQuanYi Zen Hei Mono.ttf",
                          width=600, height=600).generate(text)

    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
