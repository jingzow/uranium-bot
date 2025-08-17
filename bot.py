import os
import discord
from discord.ext import commands
from datetime import datetime

from news_core.fetcher import fetch_articles
from news_core.analyzer import summarize_and_analyze

# ====== 設定 ======
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
model = "gpt-5"

# ====== Discord コマンド ======
@bot.command(name="news")
async def news(ctx):
    await ctx.send("Fetching uranium news... 🔎")

    articles = fetch_articles()
    articles = sorted(articles, key=lambda x: datetime(*x["published_parsed"][:6]), reverse=True)

    if not articles:
        await ctx.send("No articles found.")
        return

    for i, art in articles:
        dt = datetime(*art["published_parsed"][:6])
        date_str = dt.strftime("%Y-%m-%d")

        main_msg = await ctx.send(f"📰 **{art['title']}**\n🔗 {art['link']}\nDate: {date_str}")
        if i < 3:
            thread_name = f"{art['title'][:30]}... | {date_str}"
            thread = await main_msg.create_thread(name=thread_name)

            summary = summarize_and_analyze(art["content"], model)
            await thread.send(summary)

# ====== 実行 ======
if __name__ == "__main__":
    bot.run(TOKEN)