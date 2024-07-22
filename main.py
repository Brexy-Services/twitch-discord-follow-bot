import  random,     threading, requests, discord, os

from    discord.ext import commands

color        = 0x71368A
token 	     = "PLACE YOUR TOKEN HERE :)"
bot_channel  = 1258184985857495132

intents     = discord.Intents.all()
bot         = commands.Bot(command_prefix=".", help_command=None, intents=intents)
threads     = 25 # Lower this if your bot does not respond while sending followers


def get_id(user):
    json = {"operationName": "ChannelShell",
            "variables": {
                "login": user
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "580ab410bcd0c1ad194224957ae2241e5d252b2c5173d8e0cce9d32d5bb14efe"
                }
            }
        }

    headers = {
        'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'
    }

    r = requests.post('https://gql.twitch.tv/gql', json=json, headers=headers)
    if 'data' in r.json() and 'userOrError' in r.json()['data']:
        user_data = r.json()['data']['userOrError']
        if 'id' in user_data:
            return user_data['id']
        
    return None


def GetFollowCount(channel):

    headers = {
        'Authorization': 'Oath 9d69epnjsu3y6yt2l3d7pb7jg2sk0z', # Change this if goes invalid / Is only returning None
        "Client-ID": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp",
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    query = '''
    query {
      user(login: "%s") {
        followers {
          totalCount
        }
      }
    }
    ''' % channel

    url = 'https://gql.twitch.tv/gql'
    payload = [{'operationName': None, 'variables': {}, 'extensions': {}, 'query': query}]

    response = requests.post(url, headers=headers, json=payload)
    try:
        
        return response.json()[0]['data']['user']['followers']['totalCount']
    
    except:
        
        return None


def follow(target_id , amount):

    for i in range(int(amount)):

        with open('Input/tokens.txt', 'r') as file:
            lines = file.readlines()

            random_line = random.choice(lines)
            token, integ = random_line.strip().split("|")


            payload = {
                    "operationName": "FollowUserMutation",
                    "variables": {
                        "targetId": target_id,
                        "disableNotifications": False
                    },
                    "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "cd112d9483ede85fa0da514a5657141c24396efbc7bac0ea3623e839206573b8"
                        }
                    }
                }
            
            proxy_list = open('Input/proxys.txt','r').read().splitlines()
            proxy = random.choice(proxy_list)
            proxies = {
                'http': f'http://{proxy}/',
            }
            
            headers = {
                "Api-Consumer-Type": "mobile; Android/1500000",
                "Authorization": f"OAuth {token}",
                "Client-ID": clientid,
                "Connection": "Keep-Alive",
                "Client-Integrity": integ,
                "Content-Type": "application/json",
                "Host": "gql.twitch.tv",
                "User-Agent": "useragent",
                "X-APOLLO-OPERATION-NAME": "FollowUserMutation",
                "X-App-Version": "15.0.0",
                    }
            
            response = requests.post('https://gql.twitch.tv/gql', json=payload, headers=headers,proxies=proxies)
            print(response.text)


@bot.command()
async def tfollow(ctx, channel):

    if ctx.channel.id == int(bot_channel):

        await ctx.message.delete()

        target_id = get_id(channel)

        if target_id is None:

            embed = discord.Embed(title=f"Failed to find channel", description=f"Bot failed to find the inputed channel -> `{channel}`", color=color)
            await ctx.send(embed=embed, delete_after=5)
            return
                
        embed = discord.Embed(title="Follow Bot", description=f"Sending Followers to `{channel}`.", color=color)
        embed.add_field(name="Follow Count", value=f"Currently has {GetFollowCount(channel)} followers.")
        embed.add_field(name="Sending", value=f"Sending 50 followers.")
        await ctx.send(embed=embed, delete_after=5)

        for _ in range(threads):
            threading.Thread(target=follow, args=[target_id, 50/threads]).start()
    else:
        await ctx.message.delete()
    

@bot.event
async def on_ready():
    os.system("cls")
    print('Bot online')
    with open("tokens.txt", 'r') as ttokens:
        token_count = len(ttokens.readlines())
        print(f"\nFollow Stock > {token_count}")

bot.run(token)
