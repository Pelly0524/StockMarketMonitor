import yfinance as yf
import pandas as pd
import mplfinance as mpf


def fetch_and_plot_gold_daily():
    """
    使用 yfinance 從 Yahoo Finance 下載黃金期貨 (GC=F) 的日線資料，並繪製成暗色風格的K線圖。
    """
    # === 1. 下載 GC=F 日線資料，抓最近 1 個月 (期間可改)
    df = yf.download(
        tickers="GC=F",
        period="5d",  # 1個月資料
        interval="5m",  # 1小時頻率
        auto_adjust=False,
    )

    if df.empty:
        print("無法從Yahoo Finance 取得 GC=F 日線資料，請稍後再試或換別的參數。")
        return

    # === 2. 整理欄位，mplfinance 需要 open, high, low, close, volume
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index.name = "timestamp"  # 時間索引

    # === 3. 設定暗色 Binance 風格
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

    # === 4. 繪製 K 線圖
    mpf.plot(
        df,
        type="candle",
        volume=True,  # 顯示成交量
        style=binance_style,
        addplot=apds,  # 額外繪製一條收盤價線
        title="Gold Futures (GC=F) Chart",
        figsize=(20, 10),
        figscale=1.5,
        savefig=dict(fname="gold_chart.png", dpi=700),
    )
    print("黃金(GC=F) 日線K線圖已產出 -> gold_chart.png")


if __name__ == "__main__":
    fetch_and_plot_gold_daily()
