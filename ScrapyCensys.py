from CitationRank import TargetContents
import json
import socket
import os

def domain2ip(domain):
    result = socket.getaddrinfo(domain, None)
    return result[0][4][0]


def get_black_domain_list(file_path):
    with open(file_path, mode="r") as black_list:
        lines = black_list.readlines()[10:-1]
    return [line.split("\t")[1].split("\n")[0] for line in lines]


def main():
    black_domain_list = get_black_domain_list(
        r"D:\CS\Computer Network\191205_DataSet\Reputation blacklists\From hpHosts\ad_servers.txt")
    file_count = 0
    for domain in black_domain_list:
        print(os.path.exists("C:\\Users\\11818\\Desktop\\misc\\logs\\"))
        ip = domain2ip(domain)
        url = "https://censys.io/ipv4/" + ip + "/raw"
        print(file_count, url)
        contents = TargetContents(url=url)
        parsed_html = contents.parse_html(tag="code", dict={"class": "json"})
        for parsed_text in parsed_html:
            ip_dict = json.loads(parsed_text.get_text())
            print(ip_dict)
            json.dump(ip_dict, open("C:\\Users\\11818\\Desktop\\misc\\logs\\" + ip + ".json", mode="a"))
        file_count += 1


if __name__ == '__main__':
    main()
