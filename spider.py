import os
import requests
from lxml import etree

BASE_URL = "https://ba.gamekee.com"


def get_student_url_dict():
    response = requests.get(BASE_URL)
    html = etree.HTML(response.text)

    student_list = html.xpath(
        '//*[@id="menu-23941"]/div[3]/div[2]/div[1]/div[2]//text()'
    )
    student_html = html.xpath(
        '//*[@id="menu-23941"]/div[3]/div[2]/div[1]/div[2]/a/@href'
    )
    student_url_dict = {}
    for i, student in enumerate(student_list):
        student_url_dict[student] = BASE_URL + student_html[i]

    return student_url_dict


def get_student_info(student_url):
    response = requests.get(student_url)
    html = etree.HTML(response.text)

    name = html.xpath("//h1/text()")[0]

    if not os.path.exists(name):
        os.makedirs(name)

    audio_list = html.xpath("//audio[@src]")
    audio_src_list = []
    for audio in audio_list:
        audio_src = audio.get("src")
        audio_src_list.append(audio_src)

    if not os.path.exists(name + "/voice"):
        os.makedirs(name + "/voice")

    for audio_src in audio_src_list:
        response = requests.get("https:" + audio_src)
        filename = name + "/voice/" + audio_src.split("/")[-1]
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"{filename} saved")

    image_list = html.xpath("//img[@data-width and @data-height]")
    image_src_list = []
    for image in image_list:
        image_src = image.get("src")
        image_src_list.append(image_src)

    if not os.path.exists(name + "/image"):
        os.makedirs(name + "/image")

    for image_src in image_src_list:
        if "https:" in image_src or "http:" in image_src:
            response = requests.get(image_src)
        else:
            response = requests.get("https:" + image_src)
        filename = name + "/image/" + image_src.split("/")[-1]
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"{filename} saved")


def main():
    student_url_dict = get_student_url_dict()
    for student in student_url_dict.keys():
        student_url = student_url_dict[student]
        get_student_info(student_url)


if __name__ == "__main__":
    main()
