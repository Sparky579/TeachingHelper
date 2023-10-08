import os

import openai
import json
import ast
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
import numpy as np


# 目前需要设置代理才可以访问 api
# os.environ["HTTP_PROXY"] = "127.0.0.1:7464"
# os.environ["HTTPS_PROXY"] = "127.0.0.1:7464"


def get_api_key():
    with open('key.txt', 'r') as file:
        key_content = file.read()
    return key_content

openai.api_key = get_api_key()
openai.api_base = 'https://api.closeai-asia.com/v1'


def count_sentences(text):
    # 使用句号作为分隔符将文本拆分成句子列表
    sentences = text.split('.')

    num_sentences = len(sentences)

    return num_sentences - 1

def get_response(question, maxtoken = 120):
    rsp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "I am an AI language model tasked to analyze the structure of a given sentence."},
            {"role": "user", "content": question}
        ],
        max_tokens=maxtoken
    )
    return rsp.get("choices")[0]["message"]["content"]

if __name__ == "__main__":
    text = ("A tall tree can transport a hundred gallons of water a day from its roots deep underground to the treetop."
            " Is this movement propelled by pulling the water from above or pushing it from below? "
            "The pull mechanism has long been favored by most scientists. "
            "First proposed in the late 1800s, "
            "the theory relies on a property of water not commonly associated with fluids:"
            "its tensile strength. Instead of making a clean break, "
            "water evaporating from treetops tugs on the remaining water molecules, "
            "with that tug extending from molecule to molecule all the way down to the roots. "
            "The tree itself does not actually push or pull; "
            "all the energy for lifting water comes from the sun’s evaporative power.")
    # text= (" technical considerations has played a crucial role in mapmaking and cartographic scholarship.Since nineteenth centur"
    #        "y cartographers,for instance,understood themselves as technicians who did not care about visual effects,while others saw"
    #        " themselves as landscape painters.That dichotomy structured the discipline of the history of cartography.Until the 1980s,in"
    #        " what Blakemore and Harley called“the Old is Beautiful Paradigm,”scholars largely focused on maps made before 1800,marveling "
    #        "at their beauty and sometimes regretting the decline of the pre－technical age.Early mapmaking was considered art while modern cartography "
    #        "was located within the realm of engineering utility.Alpers,however,has argued that this boundary would have puzzled mapmakers in the seventeenth "
    #        "century,because they considered themselves to be visual engineers.")
    num = count_sentences(text)
    question = (f"Please analyze the structure of the following full sentence. "
                f"Identify the overarching functionality of the entire sentence using a concise descriptor. There are {num} sentences in my sentence, so your list should contain {num} elements."
                f"Do NOT break the sentence into segments. "
                f"Possible descriptors include: 'background information', 'connecting', 'conclusion', 'explanation', 'introduction', 'evidence', "
                f"'counterargument', 'refutation', 'emphasis', 'transition', 'elaboration', 'example', 'clarification', 'summary', 'call to action', "
                f"'question', 'quote', 'analogy', and 'hypothetical situation'. "
                f"Your response should be in a Python list format, like [a, b, c]. "
                f"Only provide this list, without any additional context or information. The text"
                f" is: {text}")
    res = get_response(question)
    # res = "['background information', 'connecting', 'explanation', 'elaboration']"
    print(res)

    descriptors = ast.literal_eval(res)
    sentences = text.split(".")
    while len(descriptors) < len(sentences):
        descriptors.append('unknown')

    unique_descriptors = list(set(descriptors))
    colors = cm.rainbow(np.linspace(0, 1, len(unique_descriptors)))
    descriptor_color_mapping = {desc: colors[i] for i, desc in enumerate(unique_descriptors)}

    # 创建图


    # 定义句子和其对应的描述符
    # 自动根据描述符数量生成颜色映射
    unique_descriptors = list(set(descriptors))
    colors = cm.rainbow(np.linspace(0, 1, len(unique_descriptors)))
    descriptor_color_mapping = {desc: colors[i] for i, desc in enumerate(unique_descriptors)}

    # 绘制带有颜色的句子
    plt.figure(figsize=(10, 8))
    for idx, sentence in enumerate(sentences):
        if idx < len(descriptors):
            plt.text(-0.1, 1 - (idx * 0.1), sentence, color=descriptor_color_mapping[descriptors[idx]], wrap=True)
    plt.axis('off')

    patches = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in
               descriptor_color_mapping.values()]
    plt.legend(patches, descriptor_color_mapping.keys(), loc='lower left')

    plt.show()



