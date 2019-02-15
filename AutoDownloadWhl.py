import requests
from lxml import etree
import os


class AutoDownWhl():
    def __init__(self):
        # 包地址
        self.url = 'https://www.lfd.uci.edu/~gohlke/pythonlibs/'
        # 下载地址
        self.base_url = 'https://download.lfd.uci.edu/pythonlibs/r5uhg2lo/'
        # 模拟浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }

    # 获取选择器与包名
    def getLib(self):
        raw_text = requests.get(self.url, headers=self.headers).content
        seletor = etree.HTML(raw_text)
        lib_names = seletor.xpath('//ul[@class="pylibs"]//li//strong//text()')
        return seletor, lib_names

    # 输出所有包名
    def print_AllLib(self, lib_names):
        print('\n------------------共查找到' + str(len(lib_names)) + '个包------------------\n')
        for i in range(len(lib_names)):
            if i and i % 15 == 0:
                print('\n')
            print(lib_names[i], end=' ')

    # 搜索与下载
    def searchDown(self, downloadMethod='axel'):
        seletor, lib_names = self.getLib()
        print("\n\n---------------------------------------欢迎使用Whl自助搜索下载器---------------------------------------\n")
        self.print_AllLib(lib_names)
        while True:
            download_lib = input('\n\n请输入下载包的名字(英文逗号分割): ')
            download_lib = download_lib.split(',')
            for each in download_lib:
                if each in lib_names:
                    index = int(lib_names.index(each)) + 2
                    print("\n---------查找" + each + "成功,正在输出包的详细信息---------\n")
                    detail_libs = seletor.xpath('//ul[@class="pylibs"]//li[' + str(index) + ']//ul//li//text()')
                    max = 0
                    for j in range(len(detail_libs)):
                        print('(' + str(j + 1) + ')' + detail_libs[j])
                        max = j + 1

                    lib_sequence = input('\n请输入下载的包名序号： ')
                    if int(lib_sequence) <= max:
                        detail_name = detail_libs[int(lib_sequence) - 1].strip().replace('‑', '-')
                        download_url = self.base_url + detail_name
                        print('\n\n输入包名正确,下载地址：' + download_url + '\n')
                        print("---------------------------------------开始下载---------------------------------------\n")
                        if downloadMethod == 'curl':
                            cmd = 'curl -O %s' % download_url
                        else:
                            cmd = 'axel %s' % download_url
                        while True:
                            cmd_res = os.system(cmd)
                            if cmd_res == 0:
                                print('下载成功!\n')
                                break
                            else:
                                print('下载失败!\n')
                                is_try = input('是否重试下载(y|n)： ')
                                if is_try == 'y' or is_try == 'Y':
                                    continue
                                else:
                                    break
                    else:
                        print("\n \033[1;31m 输入序号不符合要求,请重新输入！ \033[0m \n")
                else:
                    print("\n \033[1;31m 输入的"+ each + "未查找到,请检查大小写与字母！ \033[0m \n")
            is_flag = input('\n是否继续下载其他库(y|n)： ')
            if is_flag == 'y' or is_flag == 'Y':
                self.print_AllLib(lib_names)
                continue
            else:
                print("\n---------------------------------------感谢使用---------------------------------------\n")
                break


dw = AutoDownWhl()
dw.searchDown(downloadMethod='axel')
