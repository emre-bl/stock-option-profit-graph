import streamlit as st
from functions import *
import numpy as np

def main():
    st.title("Finans Uygulaması")

    min_strike_price = float('inf')
    max_strike_price = float('-inf')

    all_payoffs = []

    option_count = st.number_input("Kaç opsiyon kullanacaksınız:", min_value=1, value=1, step=1)
    stock_count = st.number_input("Kaç hisse senedi kullanacaksınız:", min_value=1, value=1, step=1)
    stock_spot_price = st.number_input("Hisse senedi Spot Fiyatı:", value=0.0, step=1.0)

    st.write("Hisse senedi Bilgileri")
    # hisse senedi alım mı satım mı bilgisi
    stock_type = st.selectbox("Alım/Satım", ["Alım", "Satım"])

    options = {}



    for i in range(1, option_count + 1):
        st.subheader(f"{i}. Opsiyon için bilgileri giriniz")
        st.write("-----------------------------")
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


    
    stock_price_range = np.arange(min_strike_price-30, max_strike_price + 30, 1)

            
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

        plot_total_payoff(all_payoffs, stock_price_range, option_count)

        y_bottom_limit = 0

        xs = [options[i+1]['strike_price'] for i in range(option_count)]

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
        plt.xticks(xs , fontsize=7)

        

        st.pyplot(plt)
        pass

if __name__ == "__main__":
    main()
