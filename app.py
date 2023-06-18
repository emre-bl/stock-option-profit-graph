import streamlit as st
from functions import *
import numpy as np

def main():
    st.title("Profit/Loss Graph Generator")

    min_strike_price = float('inf')
    max_strike_price = float('-inf')

    all_payoffs = []

    option_count = st.number_input("Kaç opsiyon kullanacaksınız:", min_value=1, value=1, step=1)
    stock_count = st.number_input("Kaç hisse senedi kullanacaksınız:", min_value=1, value=1, step=1)
    stock_spot_price = st.number_input("Hisse senedi Spot Fiyatı:", value=100.0, step=1.0)

    st.write("Hisse senedi Bilgileri", size="large")
    # hisse senedi alım mı satım mı bilgisi
    stocks = {}
    for i in range(1, stock_count + 1):
        stock_type = st.selectbox("Hisse Alım/Satım -" + str(i), ["Alım", "Satım"], key= 200+i)
        stocks.update({i: {"type": stock_type}})

    # find number of Alım and Satım in stocks
    stock_buy_count = 0
    stock_sell_count = 0
    for stock in stocks.values():
        if stock["type"] == "Alım":
            stock_buy_count += 1
        else:
            stock_sell_count += 1
    
    if stock_buy_count >= stock_sell_count:
        stock_type = "Alım"
        stock_count = stock_buy_count-stock_sell_count
    else:
        stock_type = "Satım"
        stock_count = stock_sell_count-stock_buy_count    

    options = {}



    for i in range(1, option_count + 1):
        st.write("-----------------------------")
        st.subheader(f"{i}. Opsiyon için bilgileri giriniz")
        option_type = st.selectbox("Call/Put", ["C", "P"], key=4*i+1)
        option_buy_sell = st.selectbox("Alım-Satım", ["Alım", "Satım"], key=4*i+2)
        option_strike_price = st.number_input("Strike Fiyatı:", value=0.0, step=1.0, key=4*i+3)
        option_price = st.number_input("Opsiyon Fiyatı:", value=0.0, step=1.0, key=4*i+4)
        
        options.update({i: {
            "type": option_type,
            "buy_sell": option_buy_sell,
            "strike_price": option_strike_price,
            "option_price": option_price
        }})
        
        if option_strike_price < min_strike_price:
            min_strike_price = option_strike_price
            
        if option_strike_price > max_strike_price:
            max_strike_price = option_strike_price

    if stock_spot_price < min_strike_price:
        min_strike_price = stock_spot_price

    if stock_spot_price > max_strike_price:
        max_strike_price = stock_spot_price


    
    stock_price_range = np.arange(min_strike_price-20, max_strike_price + 20, 1)

    for key in options.keys():
        option = options[key]
        if option.get('type') == 'C':  
            if option['strike_price'] < stock_spot_price:
                if option['option_price'] < (stock_spot_price - option['strike_price']):
                    st.write(str(key) + ". Call Opsiyonu için arbitraj fırsatı var")
            elif option['strike_price'] > stock_spot_price:
                if option['option_price'] >  (option['strike_price'] - stock_spot_price):
                    st.write(str(key) + ". Call Opsiyonu için arbitraj fırsatı var")
    
        elif option.get('type') == 'P':
            if option['strike_price'] < stock_spot_price:
                if option['option_price'] > (stock_spot_price - option['strike_price']):
                    st.write(str(key) + ". Put Opsiyonu için arbitraj fırsatı var")
            elif option['strike_price'] > stock_spot_price:
                if option['option_price'] < (option['strike_price'] - stock_spot_price):
                    st.write(str(key) + ". Put Opsiyonu için arbitraj fırsatı var")


    for key in options.keys():
        #check different call options's strike price
        if options[key]['type'] == 'C':
            for key2 in options.keys():
                if options[key2]['type'] == 'C':
                    fst = abs(options[key]['strike_price']-stock_spot_price)
                    snd = abs(options[key2]['strike_price']-stock_spot_price)
                    if fst > snd and options[key]['option_price'] < options[key2]['option_price']:
                        st.write(str(key) + ". ve " + str(key2) + ". Call Opsiyonları için arbitraj fırsatı var. Opsiyon-Fiyat dengesizliği.")
        elif options[key]['type'] == 'P':
            for key2 in options.keys():
                if options[key2]['type'] == 'P':
                    fst = abs(options[key]['strike_price']-stock_spot_price)
                    snd = abs(options[key2]['strike_price']-stock_spot_price)
                    if fst > snd and options[key]['option_price'] > options[key2]['option_price']:
                        st.write(str(key) + ". ve " + str(key2) + ". Put Opsiyonları için arbitraj fırsatı var. Opsiyon-Fiyat dengesizliği.")

    if st.button("Grafik Çizdir"):
        all_payoffs = []
        st.write("Yeşil çizgi: Stock")
        st.write("Siyah Çizgi(ler): Opsiyon ")
        st.write("Kırmızı Çizgi: Toplam")
        st.write("● : Spot Fiyat")

        ks = "Strike Fiyatları: "
        for i in range(option_count):
            ks += "K" + str(i+1) + ": $" + str(options[i+1]['strike_price']) + " "
        
        st.write(ks)

        plt.axhline(y=0, color='black', linestyle='-')

        if stock_count != 0:
            if stock_type == 'Alım':
                plot_buy_stock_payoff(stock_spot_price, stock_price_range, stock_count, all_payoffs)
            elif stock_type == 'Satım':
                plot_sell_stock_payoff(stock_spot_price, stock_price_range, stock_count ,all_payoffs)


        for _ in options.keys():
            if (options[_]['type'] == 'C') and (options[_]['buy_sell'] == 'Alım'):
                plot_call_payoff(options[_]['strike_price'], options[_]['option_price'], stock_price_range, all_payoffs)
            elif (options[_]['type'] == 'P') and (options[_]['buy_sell'] == 'Alım'):
                plot_put_payoff(options[_]['strike_price'], options[_]['option_price'], stock_price_range, all_payoffs)
            elif (options[_]['type'] == 'C') and (options[_]['buy_sell'] == 'Satım'):
                plot_sell_call_payoff(options[_]['strike_price'], options[_]['option_price'], stock_price_range, all_payoffs)
            elif (options[_]['type'] == 'P') and (options[_]['buy_sell'] == 'Satım'):
                plot_sell_put_payoff(options[_]['strike_price'], options[_]['option_price'], stock_price_range, all_payoffs)

        start_ys = [payoffs[0] for payoffs in all_payoffs]

        
        sum = 0

        for _ in range(len(start_ys)):
            sum+=start_ys[_]

        start_ys.append(0)
        start_ys.append(sum)
        start_ys.sort()

        plot_total_payoff(all_payoffs, stock_price_range, option_count, is_stock=stock_count != 0)

        y_bottom_limit = 0

        xs = [options[i+1]['strike_price'] for i in range(option_count)]
        xs.append(stock_price_range[0])
        xs.append(stock_price_range[-1])

        x0 = stock_price_range[0]

        for i in range(len(all_payoffs)):
            for j in range(len(all_payoffs[i])):
                if all_payoffs[i][j] < y_bottom_limit:
                    y_bottom_limit = all_payoffs[i][j]


        for i in range(len(all_payoffs)):
            for j in range(len(all_payoffs[i])):
                if all_payoffs[i][j] == 0:
                    xs.append(stock_price_range[j])
                    plt.plot([x0+j,x0+j], [0,y_bottom_limit], color='black', linestyle='--', linewidth=0.3)

                    if all_payoffs[i][j] < y_bottom_limit:
                        y_bottom_limit = all_payoffs[i][j]

        
        plt.scatter(stock_spot_price, 0, marker='o', color='black')

        plt.yticks(start_ys, fontsize=7)
        plt.xticks(xs , fontsize=6, rotation=90)

        

        st.pyplot(plt)
        pass

if __name__ == "__main__":
    main()
