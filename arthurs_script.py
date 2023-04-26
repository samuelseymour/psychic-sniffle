from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:

    def get_weighted_average(self, state, product):

        # We want to get the mid point between trades
        #
        # We then want to work out the weighted mid point
        #
        # And we
        # We also just want to calculate quality trades / glitches in other peoples script if there are any
        # Basically just edge cases for really cheap stonks or easy expensive sells.
        buy_orders = state.order_depths[product].buy_orders
        buy_prices_descending = list(buy_orders.keys())
        buy_prices_descending.sort(reverse=True)
        sell_orders = state.order_depths[product].sell_orders
        sell_prices_ascending = list(sell_orders.keys())
        sell_prices_ascending.sort()

        bid_weighted_average = 0
        ask_weighted_average = 0

        wmpb_sum = 0
        wmpb_quantity = 0
        wmpa_sum = 0
        wmpa_quantity = 0
        orderIndex = 0
        if (len(buy_prices_descending) > 0):
            for vol_Index in range(len(buy_prices_descending)):
                order_price = buy_prices_descending[vol_Index]
                order_quantity = buy_orders[buy_prices_descending[vol_Index]]
                wmpb_sum += order_quantity
                wmpb_quantity += order_quantity
            bid_weighted_average = wmpb_sum / wmpb_quantity
        if (len(sell_prices_ascending) > 0):
            for vol_Index in range(len(sell_prices_ascending)):
                order_price = sell_prices_ascending[vol_Index]
                order_quantity = sell_orders[sell_prices_ascending[vol_Index]]
                wmpa_sum += order_price
                wmpa_quantity += order_quantity
            ask_weighted_average = wmpa_sum / wmpa_quantity
        weight_average_mid = (ask_weighted_average + bid_weighted_average) / 2
        return bid_weighted_average, ask_weighted_average, weight_average_mid


    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

            if product == 'BANANAS':
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]
                outbound_orders: list[Order] = []
                #bwa, awa, wam = self.get_weighted_average(state, 'PEARLS')

                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]

                acceptable_price_to_buy = best_bid + 1
                acceptable_price_to_sell = best_ask - 1
                print("Checking bid and ask")

                #if acceptable_price_to_buy > 4900 and time < 95000:
                    #send all sells
                #elif acceptable_price_to_sell < 4900 and time < 95000:
                    #send all buys
                 #else if time > 950000 and time < 100000 - 30:
                    #get position flat
                #else if time > 950000:
                    #send all sells


                if acceptable_price_to_sell <= acceptable_price_to_buy:
                    continue

                else:
                    print("putting bids on")

                    try:
                        if  state.position[product] > 10:
                            print("SELL", str(10) + "x", acceptable_price_to_sell)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -2))
                        elif  state.position[product] < -10:
                            print("BUY", str(10) + "x", acceptable_price_to_buy)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, 2))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                print("BUY", str(1), "x", acceptable_price_to_buy)
                                outbound_orders.append(Order(product, acceptable_price_to_buy, 1))
                                print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -1))
                            else:
                                continue

                    except:
                        if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                            print("BUY", str(1), "x", acceptable_price_to_buy)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, 1))
                            print("SELL", str(1) + "x", acceptable_price_to_sell)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -1))
                        else:
                            continue

                # if best_bid * 1.02 < best_ask and best_ask * 0.98 > best_bid:
                #     print("BUY", str(best_bid_volume) + "x", best_bid * 1.02)
                #     outbound_orders.append(Order(product, best_bid * 1.02, 20))
                #     print("SELL", str(best_bid_volume) + "x", best_ask * 0.98)
                #     outbound_orders.append(Order(product, best_ask * 0.98, -20))
                # else
                #     if best_bid > acceptable_price_to_buy:
                #         print("SELL", str(best_bid_volume) + "x", -best_bid_volume)
                #         outbound_orders.append(Order(product, best_bid, -best_bid_volume))
                #     if best_ask < acceptable_price_to_sell:
                #         print("BUY", str(best_ask_volume) + "x", -best_ask_volume)
                #         outbound_orders.append(Order(product, best_ask, -best_ask_volume))
                # Add all the above the orders to the result dict
                result[product] = outbound_orders
            #     order_depth: OrderDepth = state.order_depths[product]
            #     outbound_orders: list[Order] = []


            #     best_bid = max(order_depth.buy_orders.keys())
            #     best_bid_volume = order_depth.buy_orders[best_bid]
            #     best_ask = min(order_depth.sell_orders.keys())
            #     best_ask_volume = order_depth.sell_orders[best_ask]

            #     # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
            #     order_depth: OrderDepth = state.order_depths[product]
            #     outbound_orders: list[Order] = []
            #     bwa, awa, wam = self.get_weighted_average(state, 'PEARLS')

            #     reg_m = (best_ask + best_bid) / 2

            #     if best_ask == 0:
            #         reg_m = best_bid
            #     elif best_bid == 0:
            #         reg_m = best_ask

            #     if awa == 0:
            #         awa = reg_m
            #     if bwa == 0:
            #         bwa = reg_m

            #     acceptable_price_to_buy = reg_m - (awa - 5 - reg_m)
            #     acceptable_price_to_sell = reg_m + (reg_m + 5 - bwa)

            #     if len(order_depth.sell_orders) > 0:
            #         if best_ask < acceptable_price_to_buy:
            #             print("BUY", str(-best_ask_volume) + "x", best_ask)
            #             outbound_orders.append(Order(product, best_ask, 20))

            #     if len(order_depth.buy_orders) != 0:

            #         if best_bid > acceptable_price_to_sell:
            #             print("SELL", str(best_bid_volume) + "x", best_bid)
            #             outbound_orders.append(Order(product, best_bid, 20))

            #     # Add all the above the orders to the result dict
            #     result[product] = outbound_orders


            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]
                outbound_orders: list[Order] = []
                acceptable_price = 10000

                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask < acceptable_price:
                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell or

                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        outbound_orders.append(Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > acceptable_price:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        outbound_orders.append(Order(product, best_bid, -best_bid_volume))
                try:
                    if best_bid == acceptable_price and state.position[product] > 0: #Cancel out position
                        print("SELL", str(state.position) + "x", best_bid)
                        outbound_orders.append(Order(product, best_bid, -state.position))

                    if best_ask == acceptable_price and state.position[product] < 0: #Cancel out position
                        print("BUY", str(state.position) + "x", best_bid)
                        outbound_orders.append(Order(product, best_bid, -state.position))
                except:
                    pass



                # Add all the above the orders to the result dict
                result[product] = outbound_orders
        return result
