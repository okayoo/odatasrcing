#!/usr/bin/python

import threading
import time
from dcab_datasrc import stockdata
from us_all_list import stocks

TOTAL_PROCESS_NUM = 60

cn_list = []

def save_historical_one_to_file(symb, start_date, end_date):
    rd = stockdata(symb)
    rd.save_historical_file(start_date, end_date)

#    print('save ' + symb + ' done')
    cn_list.append(symb)


def save_historical_all_to_file(start_date, end_date):
    '''
    frequently used
    '''
    count = 0
    length = len(stocks)
    for stk in stocks:
        if (count % 50 == 0):
            print(str(count) + ' / ' + str(length) + ' done')
        count = count + 1
        save_historical_one_to_file(stk, start_date, end_date)

    print(str(count) + ' / ' + str(length) + ' done')


def save_historical_parts_to_file(start_date, end_date, part_idx):
    '''
    frequently used
    part_idx : int
        part index, based on 0
    '''
    count = 0
    plen = len(stocks) // TOTAL_PROCESS_NUM
    start_idx = part_idx * plen
    end_idx = (part_idx + 1) * plen
#    print("len", plen, part_idx, start_idx, end_idx)

    # get part stocks
    if (part_idx == TOTAL_PROCESS_NUM - 1):
        # last part, to the end
        pstocks = stocks[start_idx : ]
    else:
        pstocks = stocks[start_idx : end_idx]

    pslen = len(pstocks)
    for stk in pstocks:
        #if (count % 50 == 0):
        #    print(str(part_idx) + ' thread : ' + str(count) + ' / ' + str(plen) + ' done')
        count = count + 1
        save_historical_one_to_file(stk, start_date, end_date)
#        print("stk", part_idx, count, stk)

    print(str(part_idx) + ' thread : ' + str(count) + ' / ' + str(plen) + ' done')

def save_historical_all_to_file_thread(start_date, end_date):
    '''
    frequently used
    part_idx : int
        part index, based on 0
    '''
    print("all " + str(TOTAL_PROCESS_NUM) + " threads start")

    threads = []
    time_start = time.time()

    for thrd_idx in range(TOTAL_PROCESS_NUM):
#        print("thrd_idx", thrd_idx, type(thrd_idx))
        thrd = threading.Thread(target=save_historical_parts_to_file, args=(start_date, end_date, thrd_idx))
        threads.append(thrd)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    time_end = time.time()
    time_total_in_second = int(time_end - time_start)
    time_min = time_total_in_second // 60
    time_sec = time_total_in_second % 60
    print("all " + str(TOTAL_PROCESS_NUM) + " threads over, time spent: " + str(time_min) + " min " + str(time_sec) + " second")

#
# get stock data of CN
# 600xxx.SS
# 601xxx.SS
# 603xxx.SS
# 000xxx.SZ
# 002xxx.SZ
# 300xxx.SZ
#
def cn_save_historical_parts_to_file(start_date, end_date, part_idx):
    '''
    frequently used
    part_idx : int
        part index, based on 0
    '''
    cn_stk_type = [
                "600xxx.SS",
                "601xxx.SS",
                "603xxx.SS",
                "000xxx.SZ",
                "002xxx.SZ",
                "300xxx.SZ"
                ]

    count = 0

    # list and append ss or sz
    type_len = len(cn_stk_type)
    total_len = type_len * 1000

    part_len = total_len // TOTAL_PROCESS_NUM
    start_idx = part_idx * part_len
    end_idx = (part_idx + 1) * part_len
#    print("len", part_len, part_idx, start_idx, end_idx)

    # file
    #file_name = './data/%d.txt' % part_idx
    #fhandle = open(file_name, 'w')

    for i in range(type_len):
        for j in range(1000):
            cur_idx = i * 1000 + j
            if (start_idx <= cur_idx < end_idx):
                stki = cn_stk_type[i]
                stk_symbol = stki.replace('xxx', "%03d" % j)
                #print(stk_symbol)
                #fhandle.write(stk_symbol + '\n')

                #if (count % 50 == 0):
                #    print(str(part_idx) + ' thread : ' + str(count) + ' / ' + str(part_len) + ' done')
                count = count + 1
                save_historical_one_to_file(stk_symbol, start_date, end_date)

    #fhandle.close()
    print(str(part_idx) + ' thread : ' + str(count) + ' / ' + str(part_len) + ' done')

def cn_save_historical_all_to_file_thread(start_date, end_date):
    '''
    frequently used
    part_idx : int
        part index, based on 0
    '''

    print("all " + str(TOTAL_PROCESS_NUM) + " threads start")

    threads = []
    time_start = time.time()

    for thrd_idx in range(TOTAL_PROCESS_NUM):
#        print("thrd_idx", thrd_idx, type(thrd_idx))
        thrd = threading.Thread(target=cn_save_historical_parts_to_file, args=(start_date, end_date, thrd_idx))
        threads.append(thrd)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    time_end = time.time()
    time_total_in_second = int(time_end - time_start)
    time_min = time_total_in_second // 60
    time_sec = time_total_in_second % 60
    print("all " + str(TOTAL_PROCESS_NUM) + " threads over, time spent: " + str(time_min) + " min " + str(time_sec) + " second")

def save_cn_stk(fname):
    f = open(fname, "w")
    # write string
    for item in cn_list:
        f.write("'" + item + "',\n")
    f.close

def test():
    start_date = '2017-04-01'
    #end_date = '2017-04-09'

    end_date = time.strftime("%Y-%m-%d", time.localtime())
#    save_historical_one_to_file('600000.SS', start_date, end_date)

    save_historical_one_to_file('BABA', start_date, end_date)
#    save_historical_all_to_file(start_date, end_date)

    #save_historical_all_to_file_thread(start_date, end_date)
    #cn_save_historical_all_to_file_thread(start_date, end_date)

def test_save():
    cn_list.append("60000.SH")
    cn_list.append("60001.SH")
    cn_list.append("60003.SH")
    save_cn_stk("cn_stk.txt")

def main_save():
    start_date = '2017-03-01'
    end_date = time.strftime("%Y-%m-%d", time.localtime())

    #save_historical_all_to_file_thread(start_date, end_date)
    cn_save_historical_all_to_file_thread(start_date, end_date)

def main():
    test()
    save_cn_stk("cn_stk2.txt")




if __name__ == '__main__':
    main()

