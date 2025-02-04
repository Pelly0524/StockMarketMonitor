import yfinance as yf
import pandas as pd
import mplfinance as mpf


def fetch_and_plot_sp500_candle_line():
    df = yf.download(
        tickers="^GSPC",
        period="5d",
        interval="5m",
        auto_adjust=False,
    )

    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index.name = "timestamp"

    market_colors = mpf.make_marketcolors(
        up="#0ecb81",  # 漲K棒 (綠)
        down="#f6465d",  # 跌K棒 (紅)
        edge="none",
        wick="inherit",
        volume="inherit",
    )

    binance_style = mpf.make_mpf_style(
        base_mpf_style="nightclouds",
        marketcolors=market_colors,
        facecolor="#181a20",
        figcolor="#181a20",
        rc={
            "figure.facecolor": "#181a20",
            "axes.facecolor": "#181a20",
            "xtick.color": "white",
            "ytick.color": "white",
            "axes.labelcolor": "white",
            "axes.titlecolor": "white",
        },
        mavcolors=["#ffda55", "#e499e6", "#8369d1"],  # 三條MA顏色: 黃, 粉, 紫
    )

    # ★ 在主圖 (panel=0) 上新增一條線圖 (df["close"])
    #   color 可自行調整
    apds = [
        mpf.make_addplot(df["close"], panel=0, type="line", color="#ffe285", width=0.7)
    ]

    mpf.plot(
        df,
        type="candle",  # K線圖
        volume=True,
        style=binance_style,
        addplot=apds,  # 額外繪製一條收盤價線
        title="S&P 500 (^GSPC) Candle + Close-Line",
        figsize=(20, 10),
        figscale=1.5,
        savefig=dict(fname="sp500_chart.png", dpi=700),
    )
    print("K線 + 收盤價線 -> sp500_chart.png")


if __name__ == "__main__":
    fetch_and_plot_sp500_candle_line()
