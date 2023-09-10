import discord
import requests
from bs4 import BeautifulSoup


TOKEN = 'seu token'
PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True

# Inicializa o bot
client = discord.Client(intents=intents)

# Função para buscar promoções da Steam
def get_steam_sales():
    url = 'https://store.steampowered.com/specials#tab=TopSellers'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sales = []

    for sale in soup.find_all('a', class_='search_result_row'):
        title = sale.find('span', class_='title').text.strip()
        price = sale.find('div', class_='discount_final_price').text.strip()
        sales.append(f'{title} - {price}')

    return sales

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f'{PREFIX}promo'):
        sales = get_steam_sales()
        if sales:
            sales_text = '\n'.join(sales)
            await message.channel.send(f'Promoções na Steam:\n```\n{sales_text}```')
        else:
            await message.channel.send('Não foi possível encontrar as promoções da Steam.')

    if message.content.startswith('!perry'):
        await message.channel.send('Olá!')


client.run(TOKEN)
