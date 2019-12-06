from CitationRank import TargetContents
import json
import socket
import pickle
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool

black_list_path = r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/ad_servers.txt"
log_path = "/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/logs/"


def domain2ip(domain):
    result = socket.getaddrinfo(domain, None)
    return result[0][4][0]


num = 0


def get_black_ip_set(file_path):
    with open(file_path, mode="r") as black_list:
        lines = black_list.readlines()[10:-1]
    domain_list = [line.split("\t")[1].split("\n")[0] for line in lines]

    def process(domain):
        global num
        num += 1
        print(num)
        try:
            ip = domain2ip(domain)
            print(ip)
            return ip
        except:
            print("error")
            return "0"

    cores = multiprocessing.cpu_count()
    print(cores)
    pool = ThreadPool(processes=cores)
    ip_list = pool.map(process, domain_list)
    pool.close()
    pool.join()
    return list(set(ip_list))


file_count = 0


def main():
    def process(ip):
        global file_count
        file_count += 1
        url = "https://censys.io/ipv4/" + ip + "/raw"
        print(file_count, ip, url)
        def fetch_dict():
            try:
                contents = TargetContents(url=url)
                return contents.soup.find_all("code")
            except:
                print("error")
                return []
        while True:
            parsed_html = fetch_dict()
            if len(parsed_html) != 0:
                break
            else:
                print("looping")
        for parsed_text in parsed_html:
            ip_dict = json.loads(parsed_text.get_text())
            json.dump(ip_dict, open(log_path + ip + ".json", mode="w"))

    black_ip_list = get_black_ip_set(black_list_path)
    cores = multiprocessing.cpu_count()
    print(cores)
    pool = ThreadPool(processes=cores)
    pool.map(process, black_ip_list)
    pool.close()
    pool.join()


if __name__ == '__main__':
    ip_list = get_black_ip_set(black_list_path)
    pickle.dump(ip_list, "ip_list.pkl")
    print(len(ip_list))
