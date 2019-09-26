import re
import pickle
import numpy as np
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup


class TargetContents():
    def __init__(self, url="https://medium.com/@yuxili/rl-in-icml2019-a74693cbee8"):
        self.url = url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        page = Request(self.url, headers=headers)
        self.html = urlopen(page).read().decode('utf-8')
        self.soup = BeautifulSoup(self.html, features='lxml')

    def parse_html(self, tag, dict):
        return self.soup.find_all(tag, dict)

    def get_paper_list(self):
        return [paper.get_text() for paper in self.soup.find_all("strong")[2:]]


class SearchPaper():
    def __init__(self, paper_list=None, url_base="https://x.glgoo.top/scholar?as_ylo=2017&q="):
        self.url_base = url_base
        self.paper_list = paper_list

    def get_citation(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        location_pattern = re.compile(r"/scholar.cites=.*?")
        citation_pattern = re.compile(r"\d+")
        total_citation_num = []
        new_paper_list = []
        for paper in self.paper_list:
            url = self.url_base + paper.replace(" ", "+")
            # url = "https://x.glgoo.top/scholar?q=DQN"
            page = Request(url, headers=headers)
            html = urlopen(page).read().decode('utf-8')
            soup = BeautifulSoup(html, features='lxml')
            citation = soup.find_all(name="a", attrs={"href": location_pattern})
            if len(citation) == 0:
                continue
            all_citation = citation_pattern.findall(citation[0].get_text())
            if len(all_citation) == 0:
                continue
            new_paper_list.append(paper)
            citation_num = citation_pattern.findall(citation[0].get_text())[0]
            total_citation_num.append(int(citation_num))
            print(paper, citation_num)
        citation_file = open("2018_citation.pkl", "wb")
        new_paper_file = open("2018_new_paper.pkl", "wb")
        pickle.dump(total_citation_num, citation_file)
        pickle.dump(new_paper_list, new_paper_file)
        total_citation_num = np.array(total_citation_num)
        sort_citation = np.argsort(total_citation_num)
        for index in sort_citation:
            print(new_paper_list[index], total_citation_num[index])


if __name__ == '__main__':
    read_file = open("2018_paper_list", "rb")
    paper_list = pickle.load(read_file)
    search = SearchPaper(paper_list[:-2])
    search.get_citation()
