import ccxt
import pandas as pd
import mplfinance as mpf
import matplotlib.dates as mdates


def get_binance_style():
    """
    回傳自定的 Binance 夜間風格
    """
    market_colors = mpf.make_marketcolors(
        up="#0ecb81",
        down="#f6465d",
        edge="none",
        wick="inherit",
        volume="inherit",
    )
    return mpf.make_mpf_style(
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
        mavcolors=["#ffda55", "#e499e6", "#8369d1"],
    )


def fetch_and_plot_paxg_usdt_binance():
    """
    連接 Binance，抓取 PAXG/USDT 15 分鐘K線資料，繪製圖表並在右側標註最新價格
    """
    exchange = ccxt.binance()
    try:
        bars = exchange.fetch_ohlcv("PAXG/USDT", timeframe="15m", limit=50)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    df = pd.DataFrame(
        bars, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    last_price = df["close"].iloc[-1]

    mpf_style = get_binance_style()

    fig, axes = mpf.plot(
        df,
        type="candle",
        volume=True,
        style=mpf_style,
        # mav=(7, 25),
        title="PAXG/USDT 15Minute",
        figsize=(16, 8),
        figscale=1.2,
        returnfig=True,
    )

    axes[0].axhline(y=last_price, color="white", linestyle="--", linewidth=1, alpha=0.7)

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

    output_path = "charts/paxg_15m_chart_binance.png"
    fig.savefig(output_path, dpi=300)
    print(f"Chart saved to {output_path}")


if __name__ == "__main__":
    fetch_and_plot_paxg_usdt_binance()
    print("PAXG/USDT 圖表已繪製完成！")
