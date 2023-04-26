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
                #print("Checking bid and ask")

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
                    #print("putting bids on")

                    try:
                        if  state.position[product] > 15:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -4))
                        elif  state.position[product] < -15:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, 4))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, 4))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -4))
                            else:
                                continue

                    except:
                        if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                            
                            volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))
                            #print("BUY", str(1), "x", acceptable_price_to_buy)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                            #print("SELL", str(1) + "x", acceptable_price_to_sell)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
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

                        #print("BUY", str(-best_ask_volume) + "x", best_ask)
                        outbound_orders.append(Order(product, best_ask, -best_ask_volume))

                    elif best_ask == acceptable_price and state.position[product] < 0: #Cancel out position
                        #print("BUY", str(state.position[product]) + "x", best_bid)
                        outbound_orders.append(Order(product, best_bid, -state.position[product]))

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

                    elif best_bid == acceptable_price and state.position[product] > 0: #Cancel out position
                        print("SELL", str(state.position) + "x", best_bid)
                        outbound_orders.append(Order(product, best_bid, -state.position[product]))



                # Add all the above the orders to the result dict
                result[product] = outbound_orders

            if product == 'COCONUTS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for COCONUTS
                order_depth_coconuts: OrderDepth = state.order_depths[product]
                order_depth_pina: OrderDepth = state.order_depths['PINA_COLADAS']
                outbound_orders_coconuts: list[Order] = []
                outbound_orders_pinas: list[Order] = []
                discount_for_pina_colada = 7100

                try:
                    position = state.position[product]
                except:
                    position = 0

                #print("coconuts position: ",position)


                if (len(order_depth_coconuts.sell_orders) > 0) and (len(order_depth_pina.buy_orders) > 0):

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_bid_coconuts = max(order_depth_coconuts.buy_orders.keys())
                    best_bid_volume_coconuts = order_depth_coconuts.buy_orders[best_bid_coconuts]
                    best_ask_coconuts = min(order_depth_coconuts.sell_orders.keys())
                    best_ask_volume_coconuts = order_depth_coconuts.sell_orders[best_ask_coconuts]

                    # if len buy ordders > 0
                    best_bid_pinas = max(order_depth_pina.buy_orders.keys())
                    best_bid_volume_pinas = order_depth_pina.buy_orders[best_bid_pinas]
                    best_ask_pinas = min(order_depth_pina.sell_orders.keys())
                    best_ask_volume_pinas = order_depth_pina.sell_orders[best_ask_pinas]

                    mid_price_pinas = (best_ask_pinas + best_bid_pinas)/2

                    #mid_price_coconuts = (best_ask_coconuts + best_bid_coconuts)/2

                    #comparable_price_pinas = mid_price_pinas - discount_for_pina_colada

                    #comparable_bid_pinas = best_bid_pinas - discount_for_pina_colada

                    #comparable_ask_pinas = best_ask_pinas - discount_for_pina_colada

                    #print("pinas > coconuts: ",str(comparable_ask_pinas > best_bid_coconuts))

                    mean_coconuts = 7979
                    std_dev_coconuts = 11.169

                    mean_pinas = 14957
                    std_dev_pinas = 21.17

                    comparable_bid_coconuts = (best_bid_coconuts - mean_coconuts) / std_dev_coconuts

                    comparable_ask_pinas = (best_ask_pinas - mean_pinas) / std_dev_pinas

                    comparable_ask_coconuts = (best_ask_coconuts - mean_coconuts) / std_dev_coconuts

                    comparable_bid_pinas = (best_bid_pinas - mean_pinas) / std_dev_pinas



                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if comparable_bid_pinas > comparable_ask_coconuts + 0.2 and position < 20:
                        # In case the pina price is relatively higher than the coconut value,
                        # This presents an opportunity for us to buy coconuts and sell pinas
                        # The code below therefore sends a BUY order at the price level of the ask for coconuts,
                        # with the same quantity
                        # We expect this order to trade with the sell or
                        # we also send a SELL order at the price level of the bid for pinas,

                        volume_coconuts_ask = best_ask_volume_coconuts
                        volume_pinas_bid = best_bid_volume_pinas

                        # First check which has lower volume
                        if abs(volume_coconuts_ask) > abs(volume_pinas_bid):
                            volume_coconuts_ask = volume_coconuts_ask / abs(volume_coconuts_ask) * abs(volume_pinas_bid)
                            # translates the volume of coconuts asked into a smaller amount 
                            # makes sure I dont stuff up the sign
                        elif abs(volume_coconuts_ask) < abs(volume_pinas_bid):
                            volume_pinas_bid = volume_pinas_bid / abs(volume_pinas_bid) * abs(volume_coconuts_ask)
                            # tanslates the volume of coconuts asked into a smaller amount 
                            # makes sure I dont stuff up the sign
                        else:
                            pass

                        volume_pinas_bid = volume_pinas_bid // 2

                        # buying the coconuts
                        #print("BUY", 'COCONUTS',str(-volume_coconuts_ask) + "x", best_ask_coconuts)
                        #outbound_orders_coconuts.append(Order(product, best_ask_coconuts, -volume_coconuts_ask))

                        # selling the pinas
                        #print("SELL",'PINAS', str(-volume_pinas_bid) + "x", best_bid_pinas)
                        #outbound_orders_pinas.append(Order('PINA_COLADAS', best_bid_pinas, -volume_pinas_bid)) # could bug here

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if (len(order_depth_coconuts.buy_orders) != 0) and (len(order_depth_pina.sell_orders) > 0):

                    # Sort all the available buy orders by their price,
                    # and select only the buy order with the highest price
                    best_bid_coconuts = max(order_depth_coconuts.buy_orders.keys())
                    best_bid_volume_coconuts = order_depth_coconuts.buy_orders[best_bid_coconuts]
                    best_ask_coconuts = min(order_depth_coconuts.sell_orders.keys())
                    best_ask_volume_coconuts = order_depth_coconuts.sell_orders[best_ask_coconuts]

                    # if len buy ordders > 0
                    best_bid_pinas = max(order_depth_pina.buy_orders.keys())
                    best_bid_volume_pinas = order_depth_pina.buy_orders[best_bid_pinas]
                    best_ask_pinas = min(order_depth_pina.sell_orders.keys())
                    best_ask_volume_pinas = order_depth_pina.sell_orders[best_ask_pinas]

                    #mid_price_pinas = (best_ask_pinas + best_bid_pinas)/2

                    #mid_price_coconuts = (best_ask_coconuts + best_bid_coconuts)/2

                    #comparable_price_pinas = mid_price_pinas - discount_for_pina_colada

                    #comparable_bid_pinas = best_bid_pinas - discount_for_pina_colada

                    #comparable_ask_pinas = best_ask_pinas - discount_for_pina_colada

                    #print("pinas < coconuts: ",str(comparable_ask_pinas < best_bid_coconuts))

                    mean_coconuts = 7979
                    std_dev_coconuts = 11.169

                    mean_pinas = 14957
                    std_dev_pinas = 21.17

                    comparable_bid_coconuts = (best_bid_coconuts - mean_coconuts) / std_dev_coconuts

                    comparable_ask_pinas = (best_ask_pinas - mean_pinas) / std_dev_pinas

                    comparable_ask_coconuts = (best_ask_coconuts - mean_coconuts) / std_dev_coconuts

                    comparable_bid_pinas = (best_bid_pinas - mean_pinas) / std_dev_pinas



                    # Check if the highest bid (buy order) is higher than the above defined fair value
                    if comparable_ask_pinas + 0.2 < comparable_bid_coconuts and position > -20:
                        # In case the pina price is relatively lower than the coconut value,
                        # This presents an opportunity for us to sell coconuts and buy pinas
                        # The code below therefore sends a SELL order at the price level of the bid for coconuts,
                        # with the same quantity
                        # We expect this order to trade with the buy or
                        # we also send a BUY order at the price level of the ask for pinas,

                        volume_coconuts_bid = best_bid_volume_coconuts
                        volume_pinas_ask = best_ask_volume_pinas

                        # First check which has lower volume
                        if abs(volume_coconuts_bid) > abs(volume_pinas_ask):
                            volume_coconuts_bid = volume_coconuts_bid / abs(volume_coconuts_bid) * abs(volume_pinas_ask)
                            # tanslates the volume of coconuts bid into a smaller amount 
                            # makes sure I dont stuff up the sign
                        elif abs(volume_coconuts_bid) < abs(volume_pinas_ask):
                            volume_pinas_ask = volume_pinas_ask / abs(volume_pinas_ask) * abs(volume_coconuts_bid)
                            # tanslates the volume of coconuts bid into a smaller amount 
                            # makes sure I dont stuff up the sign
                        else:
                            pass

                        volume_pinas_ask = volume_pinas_ask // 2

                        # selling the coconuts
                        #print("SELL",'COCONUTS', str(-volume_coconuts_bid) + "x", best_bid_coconuts)
                        #outbound_orders_coconuts.append(Order(product, best_bid_coconuts, -volume_coconuts_bid)) # could bug here

                        # buying the pinas
                        #print("BUY", 'PINAS', str(-volume_pinas_ask) + "x", best_ask_pinas)
                        #outbound_orders_pinas.append(Order('PINA_COLADAS', best_ask_pinas, -volume_pinas_ask)) # removed negatives on volume pinas


                # Add all the above the orders to the result dict
                result[product] = outbound_orders_coconuts
                result['PINA_COLADAS'] = outbound_orders_pinas
            
            if product == 'BERRIES':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]
                outbound_orders: list[Order] = []
                #acceptable_price = 10000
                time = state.timestamp
                try:
                    position = state.position[product]
                except:
                    position = 0

                first_period_start = 0
                first_period_end = 20000
                second_period_start = first_period_end
                second_period_end = 100000
                third_period_start = second_period_end
                third_period_end = 75000
                fourth_period_start = third_period_end
                fourth_period_end = 100000
                fifth_period_start = fourth_period_end
                fifth_period_end = 75000 # research this
                sixth_period_start = fifth_period_end
                sixth_period_end = 90000
                seventh_period_start = sixth_period_end
                seventh_period_end = 100000

                if time > 100000:
                    first_period_start = 0
                    first_period_end = 10*first_period_end
                    second_period_start = first_period_end
                    second_period_end = 10*second_period_end
                    third_period_start = second_period_end
                    third_period_end = 10*third_period_end
                    fourth_period_start = third_period_end
                    fourth_period_end = 10*fourth_period_end
                    fifth_period_start = fourth_period_end
                    fifth_period_end = 10*fifth_period_end # research this
                    sixth_period_start = fifth_period_end
                    sixth_period_end = 10*sixth_period_end
                    seventh_period_start = sixth_period_end
                    seventh_period_end = 10*seventh_period_end

                if (first_period_start <= time < first_period_end):
                    if time == first_period_start:
                        print("position on Berries is at time: ",time," is position: ", position)
                    elif time >= (first_period_end - 100):
                        print("position on Berries is at time: ",time," is position: ", position)
                    # buy
                    max_pos = 20

                    min_pos = -20 # don't take the negative when referencing

                    time_to_next_phase = first_period_end - time

                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    acceptable_price_to_buy = best_bid + 1
                    acceptable_price_to_sell = best_ask - 1


                    if acceptable_price_to_sell <= acceptable_price_to_buy:
                        continue

                    else:

                        if  position > max_pos:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_sell))
                        elif  position < min_pos:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
                            else:
                                continue
                elif (second_period_start <= time < second_period_end):

                    if time == second_period_start:
                        print("position on Berries is at time: ",time," is position: ", position)
                    elif time >= (second_period_end - 100):
                        print("position on Berries is at time: ",time," is position: ", position)
                    # Market Make
                    max_pos = 100

                    min_pos = -10 # don't take the negative when referencing

                    time_to_next_phase = second_period_end - time

                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    acceptable_price_to_buy = best_bid + 1
                    acceptable_price_to_sell = best_ask - 1


                    if acceptable_price_to_sell <= acceptable_price_to_buy:
                        continue

                    else:
                        if  position > max_pos:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_sell))
                        elif  position < min_pos:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
                            else:
                                continue
                elif (third_period_start <= time < third_period_end):
                    if time == third_period_start:
                        print("position on Berries is at time: ",time," is position: ", position)
                    elif time >= (third_period_end - 100):
                        print("position on Berries is at time: ",time," is position: ", position)

                    # MM / get flat
                    max_pos = 30

                    min_pos = -100 # don't take the negative when referencing

                    time_to_next_phase = second_period_end - time

                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    acceptable_price_to_buy = best_bid + 1
                    acceptable_price_to_sell = best_ask - 1


                    if acceptable_price_to_sell <= acceptable_price_to_buy:
                        continue

                    else:
                        if  position > max_pos:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_sell))
                        elif  position < min_pos:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
                            else:
                                continue
                    
                elif (fourth_period_start <= time < fourth_period_end):
                    # sell like crazy
                    if time == fourth_period_start:
                        print("position on Berries is at time: ",time," is position: ", position)
                    elif time >= (fourth_period_end - 100):
                        print("position on Berries is at time: ",time," is position: ", position)

                    # MM / get flat
                    max_pos = 20

                    min_pos = -20 # don't take the negative when referencing

                    time_to_next_phase = second_period_end - time

                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    acceptable_price_to_buy = best_bid + 1
                    acceptable_price_to_sell = best_ask - 1


                    if acceptable_price_to_sell <= acceptable_price_to_buy:
                        continue

                    else:
                        if  position > max_pos:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_sell))
                        elif  position < min_pos:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
                            else:
                                continue
                elif (fifth_period_start <= time < fifth_period_end):
                    # make sure very negative
                    if time == fifth_period_start:
                        print("position on Berries is at time: ",time," is position: ", position)
                    elif time >= (fifth_period_end - 100):
                        print("position on Berries is at time: ",time," is position: ", position)

                    # MM / get flat
                    max_pos = -270

                    min_pos = -300 # don't take the negative when referencing

                    time_to_next_phase = second_period_end - time

                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    acceptable_price_to_buy = best_bid + 1
                    acceptable_price_to_sell = best_ask - 1


                    if acceptable_price_to_sell <= acceptable_price_to_buy:
                        continue

                    else:
                        if  position > max_pos:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_sell))
                        elif  position < min_pos:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
                            else:
                                continue
                    
                elif (sixth_period_start <= time < sixth_period_end):
                    # make sure negative and market make
                    if time == sixth_period_start:
                        print("position on Berries is at time: ",time," is position: ", position)
                    elif time >= (sixth_period_end - 100):
                        print("position on Berries is at time: ",time," is position: ", position)

                    max_pos = -200

                    min_pos = -300 # don't take the negative when referencing

                    time_to_next_phase = second_period_end - time

                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    acceptable_price_to_buy = best_bid + 1
                    acceptable_price_to_sell = best_ask - 1


                    if acceptable_price_to_sell <= acceptable_price_to_buy:
                        continue

                    else:
                        if  position > max_pos:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_sell))
                        elif  position < min_pos:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
                            else:
                                continue
                    
                elif (seventh_period_start <= time < seventh_period_end):
                    # get flat so buy
                    if time == seventh_period_start:
                        print("position on Berries is at time: ",time," is position: ", position)
                    elif time >= (seventh_period_end - 100):
                        print("position on Berries is at time: ",time," is position: ", position)

                    # MM / get flat
                    max_pos = 0

                    min_pos = -50 # don't take the negative when referencing

                    time_to_next_phase = second_period_end - time

                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    acceptable_price_to_buy = best_bid + 1
                    acceptable_price_to_sell = best_ask - 1


                    if acceptable_price_to_sell <= acceptable_price_to_buy:
                        continue

                    else:
                        if  position > max_pos:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_sell))
                        elif  position < min_pos:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
                            else:
                                continue
                # Add all the above the orders to the result dict
                result[product] = outbound_orders
            if product == 'DIVING_GEAR':
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
                #print("Checking bid and ask")

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
                    #print("putting bids on")

                    try:
                        if  state.position[product] > 5:
                            #print("SELL", str(10) + "x", acceptable_price_to_sell)
                            volume_to_sell = abs(best_bid_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -4))
                        elif  state.position[product] < -5:
                            #print("BUY", str(10) + "x", acceptable_price_to_buy)
                            volume_to_buy = abs(best_ask_volume)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, 4))
                        else:
                            if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                                #print("BUY", str(1), "x", acceptable_price_to_buy)
                                volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))

                                outbound_orders.append(Order(product, acceptable_price_to_buy, 4))
                                #print("SELL", str(1) + "x", acceptable_price_to_sell)
                                outbound_orders.append(Order(product, acceptable_price_to_sell, -4))
                            else:
                                continue

                    except:
                        if ((len(order_depth.sell_orders) > 0) and (len(order_depth.buy_orders) > 0)):
                            
                            volume_to_buy_and_sell = min(abs(best_ask_volume),abs(best_bid_volume))
                            #print("BUY", str(1), "x", acceptable_price_to_buy)
                            outbound_orders.append(Order(product, acceptable_price_to_buy, volume_to_buy_and_sell))
                            #print("SELL", str(1) + "x", acceptable_price_to_sell)
                            outbound_orders.append(Order(product, acceptable_price_to_sell, -volume_to_buy_and_sell))
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
            

        return result
