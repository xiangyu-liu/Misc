from CitationRank import TargetContents
import json
import socket
import pickle
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool

log_path = "/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/logs/"
ip_path = "/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/ip/"
black_list_path = [r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/wrz.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/ad_servers.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/emd.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/exp.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/fsa.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/grm.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/hfs.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/hjk.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/mmt.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/pha.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/psh.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/psh.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/psh.txt",
                   r"/newNAS/Workspaces/DRLGroup/xiangyuliu/Misc/verified_online.json"]


def domain2ip(domain):
    result = socket.getaddrinfo(domain, None)
    return result[0][4][0]


num = 0


def get_black_ip_set(file_path):
    if "json" in file_path:
        json_dict = json.load(open(file_path))
        domain_list = [per_dict["url"] for per_dict in json_dict]
    else:
        with open(file_path, mode="r") as black_list:
            lines = black_list.readlines()[10: -1]
            domain_list = [line.split("\t")[1].split("\n")[0] for line in lines]

    def process(domain):
        global num
        num += 1
        print(num)
        try:
            ip = domain2ip(domain)
            return ip
        except:
            print("ip error", domain)
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
    i = 0
    for file_path in black_list_path:
        ip_list = get_black_ip_set(black_list_path)
        pickle.dump(ip_list, open(ip_path + str(i) + ".pkl", mode='w'))
        print(len(ip_list), file_path, "finish:" + str(i))
        i += 1
