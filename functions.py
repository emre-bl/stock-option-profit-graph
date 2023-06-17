import matplotlib.pyplot as plt
import numpy as np

min_strike_price = float('inf')
max_strike_price = float('-inf')

def get_buy_stock_payoff(strike_price, spot_price, many):
    return (spot_price - strike_price) * many

def get_sell_stock_payoff(strike_price, spot_price, many):
    return (strike_price - spot_price) * many

def plot_buy_stock_payoff(stock_spot_price, price_range, many , all_payoffs):
    payoff = []
    for price in price_range:
        payoff.append(get_buy_stock_payoff(price, stock_spot_price, many))

    all_payoffs.append(payoff)
    plt.plot(price_range, payoff, color='green')

def plot_sell_stock_payoff(stock_spot_price, price_range, many , all_payoffs):
    payoff = []
    for price in price_range:
        payoff.append(get_sell_stock_payoff(price, stock_spot_price, many))

    all_payoffs.append(payoff)
    plt.plot(price_range, payoff, color='green')



def get_sell_call_payoff(strike_price, option_price, stock_price):
    return option_price - max(stock_price - strike_price, 0)


def plot_sell_call_payoff(strike_price, option_price, stock_price_range , all_payoffs):
    payoffs = [get_sell_call_payoff(strike_price, option_price, stock) for stock in stock_price_range]
    all_payoffs.append(payoffs)
    
    plt.plot(stock_price_range, payoffs, color='black', linewidth=0.7)  # Grafik rengini siyah olarak ayarla

    

def get_sell_put_payoff(strike_price, option_price, stock_price):
    return option_price - max(strike_price - stock_price, 0)


def plot_sell_put_payoff(strike_price, option_price, stock_price_range , all_payoffs):
    payoffs = [get_sell_put_payoff(strike_price, option_price, stock) for stock in stock_price_range]
    all_payoffs.append(payoffs)
    
    plt.plot(stock_price_range, payoffs, color='black', linewidth=0.7)  # Grafik rengini siyah olarak ayarla

    


def get_call_payoff(strike_price, option_price, stock_price):
    return max(stock_price - strike_price, 0) - option_price

def plot_call_payoff(strike_price, option_price, stock_price_range , all_payoffs):
    payoffs = [get_call_payoff(strike_price, option_price, stock) for stock in stock_price_range]
    all_payoffs.append(payoffs)

    plt.plot(stock_price_range, payoffs, color='black', linewidth=0.7)  # Grafik rengini siyah olarak ayarla


    
    

def get_put_payoff(strike_price, option_price, stock_price):    
    return max(strike_price - stock_price, 0) - option_price

def plot_put_payoff(strike_price, option_price, stock_price_range , all_payoffs):
    payoffs = [get_put_payoff(strike_price, option_price, stock) for stock in stock_price_range]
    all_payoffs.append(payoffs)
    
    plt.plot(stock_price_range, payoffs, color='black', linewidth=0.7)  # Grafik rengini siyah olarak ayarla

    
def plot_total_payoff(payoffs: list, stock_price_range, option_count):
    total_payoff = []

    for i in range(len(payoffs[0])):
        sum = 0
        for _ in range(option_count+ 1):
            sum+=payoffs[_][i]
        total_payoff.append(sum)

    plt.xlabel("Hisse Senedi Fiyatı")
    plt.ylabel("Kar/Zarar")

    plt.plot(stock_price_range, total_payoff, color='red' , linewidth=1.5)  # Grafik rengini kırmızı olarak ayarla
    



