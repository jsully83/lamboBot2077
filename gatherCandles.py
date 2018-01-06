from ccxt import bittrex
import h5py as h5
import os
from pprint import pprint
from pathlib import Path
import numpy as np

def checkForFile(path):

    try:
        wasPresent = os.stat(path)
        fh5 = h5.File (path, 'r+', libver='latest')

    except:
        fh5 = h5.File (path, 'w', libver='latest')

    fh5.swmr_mode = True
    # fh5.close
    return fh5

def createGroups(fh5, markets):
    newMarkets = []
    groups = []

    for i in range (0, len(markets)):
        groups.append(markets[i]["base"])

        if not fh5.__contains__(markets[i]["base"]):
            # print (markets[i]["base"], fh5.__contains__(markets[i]["base"]))
            fh5.create_group(markets[i]["base"])
            newMarkets.append(markets[i]["base"])

    if len(newMarkets) == 0:
        print ("No new markets were added.")

    else:
        print ("Markets added: " + ", ".join(newMarkets))

    return groups

def createDatasets(fh5, grp):
    path = grp + "/"
    dset = fh5.create_dataset(path,(1,5),dtype='i8', compression='lzf')

def parseCandles(candles):
    candlesHeader = ["Time","Open", "High", "Low", "Close", "Volume"]
    candlesArr = np.array(candles)
    floatArr = np.zeros(shape = (candlesArr.shape[0],2))

    # save significant digits and cast to int from np.float64
    priceArrTemp = np.zeros(shape=(candlesArr.shape[0],4))
    priceArr = np.zeros(shape=(candlesArr.shape[0],4))
    for i in range (1, 5):
        priceArrTemp[:,i-1] = candlesArr[:,i]*1e8
    priceArr = priceArrTemp.astype(int)

    floatArr[:,0] = candlesArr[:,0]
    floatArr[:,1] = candlesArr[:,5]

    return floatArr, priceArr

def copyToDset(floatArr, priceArr):
    print()


def main():

    bit = bittrex()
    fh5 = checkForFile("D:/Drive/atom/python/Bittrex.h5")
    markets = bit.fetch_markets()
    timeVolArr, priceArr = parseCandles(bit.fetch_ohlcv("XRP/USDT"))

    h5Groups = createGroups(fh5, markets)

    # print(fh5.__contains__(h5Groups[0]+"/"+"123"))
    # dset = fh5.create_dataset(h5Groups[0]+"/"+"123",(1,5),dtype='i8', compression='lzf')
    # dset[candles[0],"Time",candles[1],"adf"]

    # data = bit.fetch_ticker("BTC/USDT")
    # pprint(data)
    # print(len(data))
    fh5.close

if __name__ == "__main__":
    main()
