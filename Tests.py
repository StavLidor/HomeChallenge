# This is a sample Python script.
import requests

from Search import Search
import time


def find_last():
    try:
        response = requests.get("https://blockchain.info/latestblock")
        if not response.ok:
            return None
        json_block = response.json()
        return [int(json_block['height']), int(json_block['time'])]

        # try:
        #
        # except KeyError:
        #     print("ID doesn't exist")

    except requests.ConnectionError as e:
        print("connection Error")
        return None
    except KeyError as e:
        print("not exist in block")
        return None

if __name__ == '__main__':
    s = Search()
    # # edge case
    # #  start 1231006505
    # # TODO : if its equal to one of the limit what should to do ?

    # start time -not in some range
    print("start time -not in some range- ",s.search("1231006505")) # -1
    # before start -not in some range
    print("before start -not in some range- ",s.search("1231006504")) # -1
    # after start - in range
    print("after start - in range - ",s.search("1231006506"))  # 0
    last1 = find_last()
    if last1 is not None:
        # after end time -not in some range
        print("after end time -not in some range ",s.search(str(last1[1] +1)))  # -1
        #  end time -not in some range
        print("end time -not in some range ",s.search(str(last1[1])))  # -1
    print("start sleep 10 m")
    time.sleep(600)
    print("finsh to  sleep 10 m")
    last2 = find_last()
    if last2 is not None and last2[0] > last1[0]:
        print("the block before the last now if add new block ",s.search(str(last1[1])))  # the block before the last now if add new block
    elif last2[0] == last1[0]:
        print("equal after 10 m")

    print("example  ",s.search("R1637430034"))  # 710592
    print("example  ", s.search("R1637430034"))  # 710592
    print("example  ",s.search("1232103989")) #693

