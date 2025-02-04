import ccxt
import pandas as pd
import mplfinance as mpf
import matplotlib.dates as mdates


def get_binance_style():
    """
    回傳自定的 Binance 夜間風格
    """
    market_colors = mpf.make_marketcolors(
        up="#0ecb81",  # 上漲 K棒(綠)
        down="#f6465d",  # 下跌 K棒(紅)
        edge="none",  # 隱藏 K棒邊框
        wick="inherit",  # 影線顏色與K棒相同
        volume="inherit",  # 成交量顏色與漲跌相同
    )
    return mpf.make_mpf_style(
        base_mpf_style="nightclouds",  # 以夜間主題為基礎
        marketcolors=market_colors,
        facecolor="#181a20",  # 圖表背景
        figcolor="#181a20",  # 外框背景
        rc={
            "figure.facecolor": "#181a20",
            "axes.facecolor": "#181a20",
            "xtick.color": "white",
            "ytick.color": "white",
            "axes.labelcolor": "white",
            "axes.titlecolor": "white",
        },
        mavcolors=["#ffda55", "#e499e6", "#8369d1"],  # 移動平均線顏色(黃、粉、紫)
    )


def fetch_and_plot_btc_usdt_binance():
    """
    連接 Binance，抓取 BTC/USDT 15 分鐘K線資料，繪製圖表並在右側標註最新價格
    """
    # 1) 連接交易所並抓取資料
    exchange = ccxt.binance()
    try:
        bars = exchange.fetch_ohlcv("BTC/USDT", timeframe="15m", limit=50)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 2) 整理成 DataFrame
    df = pd.DataFrame(
        bars, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # 毫秒轉日期時間
    df.set_index("timestamp", inplace=True)  # 設為索引

    # 3) 取得最新收盤價
    last_price = df["close"].iloc[-1]

    # 4) 取得 Binance 的 K 線風格
    mpf_style = get_binance_style()

    # 5) 繪製 K 線圖並回傳 fig, axes
    fig, axes = mpf.plot(
        df,
        type="candle",  # 蠟燭圖
        volume=True,  # 顯示成交量
        style=mpf_style,
        # mav=(7, 25),  # 繪製 7,25期移動平均線
        title="BTC/USDT 15Minute",
        figsize=(16, 8),
        figscale=1.2,
        returnfig=True,  # 回傳 figure 與 axes 以便標註
    )

    # 6) 在圖上畫最新價的水平虛線
    axes[0].axhline(y=last_price, color="white", linestyle="--", linewidth=1, alpha=0.7)

    # 7) 在圖右側標註最新價格
    axes[0].annotate(
        text=f"{last_price:.2f}",
        xy=(1.0, last_price),
        xycoords=("axes fraction", "data"),
        xytext=(10, 0),
        textcoords="offset points",
        va="center",
        ha="left",
        color="white",
        bbox=dict(boxstyle="round,pad=0.3", fc="#181a20", ec="white", alpha=0.8),
    )

    # 8) 儲存圖檔
    output_path = "charts/btc_15m_chart_binance.png"
    fig.savefig(output_path, dpi=300)
    print(f"Chart saved to {output_path}")


if __name__ == "__main__":
    fetch_and_plot_btc_usdt_binance()
    print("BTC/USDT 圖表已繪製完成！")
