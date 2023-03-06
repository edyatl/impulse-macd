## Python porting of Impulse MACD [LazyBear]

<https://www.tradingview.com/script/qt6xLfLi-Impulse-MACD-LazyBear/>

>Developed by [@edyatl](https://github.com/edyatl) March 2023 <edyatl@yandex.ru>

### Using [Python wrapper](https://github.com/TA-Lib/ta-lib-python) for [TA-LIB](http://ta-lib.org/) based on Cython instead of SWIG.

### Original Indicator code

```python
//
// @author LazyBear 
// 
// List of my public indicators: http://bit.ly/1LQaPK8 
// List of my app-store indicators: http://blog.tradingview.com/?p=970 
//
//
study("Impulse MACD [LazyBear]", shorttitle="IMACD_LB", overlay=false)
lengthMA = input(34)
lengthSignal = input(9)
calc_smma(src, len) =>
    smma=na(smma[1]) ? sma(src, len) : (smma[1] * (len - 1) + src) / len
    smma

calc_zlema(src, length) =>
    ema1=ema(src, length)
    ema2=ema(ema1, length)
    d=ema1-ema2
    ema1+d

src=hlc3
hi=calc_smma(high, lengthMA)
lo=calc_smma(low, lengthMA)
mi=calc_zlema(src, lengthMA) 

md=(mi>hi)? (mi-hi) : (mi<lo) ? (mi - lo) : 0
sb=sma(md, lengthSignal)
sh=md-sb
mdc=src>mi?src>hi?lime:green:src<lo?red:orange
plot(0, color=gray, linewidth=1, title="MidLine")
plot(md, color=mdc, linewidth=2, title="ImpulseMACD", style=histogram)
plot(sh, color=blue, linewidth=2, title="ImpulseHisto", style=histogram)
plot(sb, color=maroon, linewidth=2, title="ImpulseMACDCDSignal")

ebc=input(false, title="Enable bar colors")
barcolor(ebc?mdc:na)
```
### Original Indicator Overview
Impulse MACD [LazyBear] is a technical indicator for TradingView developed by the user LazyBear. It is based on the Moving Average Convergence Divergence (MACD) indicator and is designed to identify potential trade opportunities based on changes in momentum.

The indicator is designed to identify when momentum is shifting from one direction to another. A bullish signal is generated when the MACD line crosses above the signal line and the histogram bars turn green. A bearish signal is generated when the MACD line crosses below the signal line and the histogram bars turn red.

In addition to the traditional MACD signals, the Impulse MACD [LazyBear] indicator also generates signals based on the slope of the MACD line. A bullish slope is identified when the MACD line is rising and a bearish slope is identified when the MACD line is falling.

Overall, the Impulse MACD [LazyBear] indicator is a versatile tool that can be used to identify potential trade opportunities in a variety of market conditions. It can be used as part of a broader trading strategy, or as a standalone indicator.



