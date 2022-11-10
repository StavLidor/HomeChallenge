from datetime import datetime
import requests
import re

"""
    find the time according json of the block - should use when find by index
"""
def find_time_by_index(json_block):
    # the block not Exists
    if len(json_block['blocks']) == 0:
        return None
    return int(json_block['blocks'][0]['time'])


"""
    find the time according json of the block (the last block)
"""
def find_last_with_json(json_block):
    return [int(json_block['height']), int(json_block['time'])]

"""
    find by url the block and return data need according fnc
"""
def api_call_by_url(url, fnc):
    try:
        response = requests.get(url)
        if not response.ok:
            return -1
        json_block = response.json()
        res = fnc(json_block)
        return res
    except requests.ConnectionError as e:
        print("connection Error")
        return None
    except KeyError as e:
        print("not exist in block")
        return None

"""
    find the last block return index and timr
"""
def find_last():
    return api_call_by_url("https://blockchain.info/latestblock", find_last_with_json)

"""
    find the block by index and return the time
"""
def api_call_by_index(number):
    url = "https://blockchain.info/block-height/" + str(number) + "?format=json"
    return api_call_by_url(url, find_time_by_index)

"""
    class of serach the index
"""
class Search:
    def __init__(self):
        # save the api calls
        self.dic = {}
        # last and first block index and time
        self.last = find_last()
        self.first = [0, api_call_by_index(0)]
        # save in dic
        self.dic.update({self.last[0]: self.last[1]})
        self.dic.update({0: self.first[1]})
        # time of api call to last
        self.time_read_last = datetime.now()
        self.diff_min = 10

    """
    Given timestamp T S find N where tbN < T S < tbN+1 (i.e. the latest block
    prior to T S).
    return index if find , else return -1
    """

    def search(self, input):
        # convert to int the unix time
        time = int(re.findall(r'\d+', input)[0])
        # before the first block not in range of to blocks time
        if time <= self.first[1]:
            return -1
        # # the time of last block not in range of to blocks time
        # if time == self.last[1]:
        #     return -1
        # the last block time not important if the input small in exponential search
        if time >= self.last[1]:
            time_now = datetime.now()
            # if pass 10 minutes and more, find the last block
            if (time_now - self.time_read_last).total_seconds() / 60 < self.diff_min:
                return -1
            # update the time find last
            new_last = find_last()
            # if the last not the same block
            if new_last[0] != self.last[0]:
                self.time_read_last = time_now
                self.last = find_last()
                self.dic.update({self.last[0]: self.last[1]})
            # out of the range
            if time >= self.last[1]:
                return -1

        return self.exp_search(time)

    """
       Given timestamp T S find N where tbN < T S < tbN+1 (i.e. the latest block
        prior to T S). - use exponential search algo
        return index if find , else return -1
            
    """

    def exp_search(self, time):
        #  a check between 0-1
        if self.get_by_index(0) < time < self.get_by_index(1):
            return 0

        index = 1  # 2^0
        while index <= self.last[0]:
            time_index1 = self.get_by_index(index)
            time_index2 = self.get_by_index(index + 1)
            # if in range
            if time_index1 < time < time_index2:
                return index

            if time_index1 > time:
                time_index_before = self.get_by_index(index / 2)
                # binary search case
                if time_index_before <= time <= time_index1:
                    return self.bin_search(index / 2, index, time)
            index *= 2  # 2^i
        return self.bin_search(index / 2, self.last[0], time)
        # return 0

    """
       binary search
    """

    def bin_search(self, start, end, time):
        while start <= end:
            mid = int((start + end) / 2)
            time_index1 = self.get_by_index(mid)
            time_index2 = self.get_by_index(mid + 1)
            if time_index1 < time < time_index2:
                return mid
            if time_index1 > time:
                end = mid - 1
            else:
                start = mid + 1

        return -1

    """
       if its in dictionary not do api call , else do api call and insert to dictionary
       return the time according the index block
    """

    def get_by_index(self, i):
        if self.dic.get(i) is None:
            time = api_call_by_index(i)

            if time is None:
                print(i, "Problem")
                exit(-1)
            self.dic.update({i: time})

        return self.dic.get(i)
