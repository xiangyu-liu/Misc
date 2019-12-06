from CitationRank import TargetContents
import json
import socket
import pickle
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool


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


def main(stop_num):
    black_domain_list = get_black_ip_set(
        r"D:\CS\Computer Network\191205_DataSet\Reputation blacklists\From hpHosts\ad_servers.txt")
    file_count = -1
    ip_list = []
    for domain in black_domain_list:
        file_count += 1
        if file_count <= stop_num:
            continue
        try:
            ip = domain2ip(domain)
            if ip in ip_list:
                print("repetition")
                continue
        except:
            print(domain, ":error")
            continue

        url = "https://censys.io/ipv4/" + ip + "/raw"
        print(file_count, ip, url)
        try:
            contents = TargetContents(url=url)
        except:
            print("error")
            continue
        parsed_html = contents.soup.find_all("code")
        if len(parsed_html) == 0:
            print("begin to loop")
            file_count -= 1
            continue
        for parsed_text in parsed_html:
            ip_dict = json.loads(parsed_text.get_text())
            print(ip_dict)
            json.dump(ip_dict, open("C:\\Users\\11818\\Desktop\\misc\\logs\\" + ip + ".json", mode="w"))
            ip_list.append(ip)
            if len(ip_list) > 1000:
                ip_list = ip_list[-1000:]


def test():
    black_domain_list = get_black_ip_set(
        r"D:\CS\Computer Network\191205_DataSet\Reputation blacklists\From hpHosts\ad_servers.txt")
    file_count = -1
    error_list = []
    for domain in black_domain_list:
        file_count += 1
        try:
            domain2ip(domain)
        except:
            print(file_count, ":error")
            error_list.append(file_count)
        else:
            print(file_count, ":correct")


if __name__ == '__main__':
    ip_list = get_black_ip_set(
        r"D:\CS\Computer Network\191205_DataSet\Reputation blacklists\From hpHosts\ad_servers.txt")
    pickle.dump(ip_list, "ip_list.pkl")
    print(len(ip_list))
