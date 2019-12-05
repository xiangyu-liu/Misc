from CitationRank import TargetContents
import ast
import json

if __name__ == '__main__':
    file_count = 0
    for i in range(255):
        if i == 0:
            continue
        for j in range(255):
            if j == 0:
                continue
            url = "https://censys.io/ipv4/22.222." + str(i) + "." + str(j) + "/raw"
            print(file_count, url)
            contents = TargetContents(url=url)
            parsed_html = contents.parse_html(tag="code", dict={"class": "json"})
            for parsed_text in parsed_html:
                print(json.loads(parsed_text.get_text()))
            file_count += 1
