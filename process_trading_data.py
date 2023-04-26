import csv
import numpy as np
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt
import math

def main():
    cleanedFile = './first_test.csv' 
    file = open(cleanedFile)
    reader = csv.DictReader(file)
    columns = defaultdict(list)

    trades_dict = {}
    trades_dict['BANANAS'] = {}
    trades_dict['PEARLS'] = {}

    bananasCounter = 0
    pearlsCounter = 0
    tradeCounter = 0
    columns_keys = ''
    for row in reader:
        columns_keys = list(row.keys())[0]
        row_values = list(row.values())[0]
        values = row_values.split(';')
        keys = columns_keys.split(';')
        for key in keys:
            if (key != "product"):
                if (key not in trades_dict[values[2]].keys()):
                    trades_dict[values[2]][key] = np.array([], dtype=float)
                else:
                    valueToBeAdded = values[keys.index(key)]
                    # if valueToBeAdded == '':
                    #     valueToBeAdded = 0
                    trades_dict[values[2]][key] = np.append(trades_dict[values[2]][key],valueToBeAdded)
        tradeCounter += 1 

    columns_keys = keys
    print("Column keys are ", columns_keys)

    #Had to convert it to float as some rows contained '' as a value
    # for product in ["PEARLS", "BANANAS"]:
    #     for product_key in trades_dict[product].keys():
    #         print(product_key)
    #         trades_dict[product][product_key] = np.array(trades_dict[product][product_key], dtype=float)

    plt.plot(trades_dict["BANANAS"]['mid_price'])
    plt.xlabel("Trade number")
    plt.ylabel('bid_price_1')
    plt.show()


    print('Banana means')
    trades_dict["BANANAS"]['mid_price'] = np.array(trades_dict["BANANAS"]['mid_price'], dtype=float)
    print('mid_price',np.mean(trades_dict['BANANAS']['mid_price']))

    print('PEARLs means')
    trades_dict["PEARLS"]['mid_price'] = np.array(trades_dict["PEARLS"]['mid_price'], dtype=float)
    print('mid_price', np.mean(trades_dict['PEARLS']['mid_price']))

    # Was wanting to plot everything on subplots but realised this was kind of useless as we need to use different types of plots
    # for different types of data

    # for product in ['PEARLS', 'BANANAS']:
    #     subplotXCounter = 0
    #     subplotYCounter = 0
    #     fig, axs = plt.subplots(math.floor(math.sqrt(len(columns_keys))), math.floor((math.sqrt(len(columns_keys)))))
    #     for i in range(len(columns_keys)):
    #         if i == 2:
    #             continue
   
    #         column_query = columns_keys[i]
    #         print(columns_keys)
    #         trades_dict[product][column_query] = np.array(trades_dict[product][column_query], dtype=float)
    #         print(trades_dict[product][column_query])
    #         axs[subplotXCounter, subplotYCounter].plot(trades_dict[product][column_query])
    #         plt.xlabel("Trade Number")
    #         plt.ylabel(column_query)
    #         if subplotXCounter == math.floor(math.sqrt(len(columns_keys))) - 1:
    #             subplotXCounter = 0
    #             subplotYCounter += 1
    #         else:
    #             subplotXCounter += 1
    #     plt.show()
    


if __name__ == "__main__":
    main()