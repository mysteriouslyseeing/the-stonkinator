import discord
import random
import json
import time
import math



client = discord.Client()
token = "nu uh"

@client.event
async def on_ready():
    print("Stonks are active!")

def read_users():
    with open("userlist.txt", "r") as f:
        lines = f.readlines()
        return json.loads(lines[0].strip())

def edit_users(dict):
    with open("userlist.txt") as f:
        file = f.read()
    with open("userlist.txt", "w+") as f:
        f.write(json.dumps(dict))
    return file

async def give_guild(amount, guild):
    userlist = read_users()
    if amount < len(guild.get_role(700161722824261744).members):
        edit_users(userlist)
        return amount
    for member in guild.get_role(700161722824261744).members:
        if not str(member) in userlist:
            userlist[str(member)] = {"coins": 0, "pickaxe": 1, "automine": 0, "time": time.time(), "tag": str(member)}
            edit_users(userlist)
        userlist[str(member)]["coins"]+=amount/len(guild.get_role(700161722824261744).members)
    userlist["Gurgl#7916"]["coins"] += amount%len(guild.get_role(700161722824261744).members)
    return amount
    edit_users(userlist)
            
        

@client.event
async def on_message(message):
    if 1:
        content = message.content
        guild = message.guild
        author = message.author
        channel = message.channel
        send = channel.send
        cmd = content.casefold()
        userlist = read_users()
        tag = str(author)
        userlist = read_users()
        while True:
            userlist["time"] += 10
            userlist["companies"]['pear'] += random.randint(round(0-userlist["companies"]['pear']/1000), round(userlist["companies"]['pear']/950))
            if userlist['time'] >= time.time()+10:
                break
        edit_users(userlist)
        if tag in userlist:
            print("user found")
            if userlist[tag]["automine"] != 0:
                print("autominer found")
                if userlist[tag]["time"] < time.time()+300:
                    out = 0
                    for i in range(50):
                        userlist[tag]["time"] += 300
                        userlist[tag]['coins'] += userlist[tag]["automine"]
                        if userlist[tag]["time"] >= time.time()+300:
                            out = 1
                            break
                    if out == 0:
                        userlist[tag]["time"] = time.time()
                    edit_users(userlist)
        else:
            userlist[tag] = {"coins": 0, "pickaxe": 1, "automine": 0, "time": time.time(), "tag": tag}
            edit_users(userlist)
        def check(m):
            return (m.content.casefold() == 'y' or m.content.casefold() == 'n') and m.channel == channel and m.author == author
        if guild.id != 700154056655503490:
            return
        elif channel.name != "stonks":
            return
        if cmd.startswith("!invest"):
            userlist = read_users()
            if len(cmd.strip()) == 7:
                await send("Stonk report: Pear has $" + str(userlist["companies"]["pear"]) + " and macrohard is at $" + str(userlist["companies"]["macrohard"])+".")
        if cmd.startswith("!stats"):
            userlist = read_users()
            fail = None
            if cmd.strip() == "!stats":
                target = tag
                fail = True
            try:
                if fail:
                    raise EscapeError
                if content[7:] in userlist:
                    try:
                        target = userlist[content[7:]]
                        target["coins"]
                    except:
                        await send("Sorry, that is not a user. \""+content[7:]+"\" is not in our database. Please make sure you put their tag, like exampleuser#6666")
                        return
                else:
                    await send("Sorry, the user \""+content[7:]+"\" is not in our database. Please make sure you put their tag, like exampleuser#6666")
                    return
            except:
                pass
            if cmd.strip() == "!stats":
                target = userlist[tag]
            msg = "Info: user "+str(target["tag"])+"\nStonkcoins: "+str(target["coins"])+"\nPickaxe level: "+str(target["pickaxe"])+"\nAutominer level: "+str(target["automine"])
            await send(msg)
        if cmd.startswith("!coins"):
            userlist = read_users()
            await send("You have " + str(userlist[tag]['coins']) + " stonkcoins")
        if cmd.startswith("!mine"):
            userlist = read_users()
            amount = random.randint(1, userlist[tag]["pickaxe"]**2+3)
            tax = 0
            if amount >49:
                tax = await give_guild(math.floor(amount/50), guild)
                amount -= tax
            print(tag, "mined", amount, "stonkcoins (tax:",str(tax) + ")")
            await send("You mined " + str(amount) + " stonkcoins (The Guild taxed " + str(tax) + " coins)")
            userlist[tag]["coins"] = userlist[tag]["coins"] + amount
            edit_users(userlist)
        if cmd.startswith("!buy"):
            costpick = ((userlist[tag]["pickaxe"]+1)*5)**2
            userlist = read_users()
            if cmd.strip() == "!buy":
                await send("**LIST OF ITEMS**\n-Pickaxe " + str(costpick) + " coins (!buy pickaxe)\n-Guild Membership 300 coins(!buy member)\n-autominer "+str(((userlist[tag]["automine"]+4)**3)*20)+" coins (!buy autominer)")
            elif cmd.strip() == "!buy pickaxe":
                cost = ((userlist[tag]["pickaxe"]+1)*5)**2
                if cost > userlist[tag]["coins"]:
                    await send("Unfortunately, you don't have enough stonks to buy this. You have " + str(userlist[tag]["coins"]) + " coins. You need " + str(cost) + " coins.")
                    return
                await send("Sure! That'll be "+str(cost)+" coins! Do you want to buy? y/n")
                try:
                    msg = await client.wait_for('message', timeout=30.0, check=check)
                except:
                    await send("Error: Timeout. Purchase cancelled.")
                msg = msg.content
                if msg.casefold() == 'y':
                    userlist[tag]["pickaxe"] = userlist[tag]["pickaxe"]+1
                    userlist[tag]["coins"] -= cost
                    await send("It's been bought. Your pickaxe is now level " + str(userlist[tag]["pickaxe"]) + ".")
                else:
                    await send("Purchase cancelled.")
                edit_users(userlist)
            elif cmd.strip() == "!buy member":
                if guild.get_role(700161722824261744) in author.roles:
                    await send("You are already a member! If you wish to be promoted, please contact someone higher up in the chain than you are.")
                    return
                elif 300 > userlist[tag]["coins"]:
                    await send("You don't have enough coins for that! You need 300, but you only have " + str(userlist[tag]["coins"]) + " coins.")
                    return
                await send("Sure! That'll be 300 coins! Do you want to buy? y/n")
                try:
                    msg = await client.wait_for('message', timeout=30.0, check=check)
                except:
                    await send("Error: Timeout. Purchase cancelled.")
                msg = msg.content
                if msg.casefold() == 'y':
                    await author.add_roles(guild.get_role(700161722824261744))
                else:
                    await send("Purchase cancelled.")
            elif cmd.strip() == "!buy autominer":
                cost = ((userlist[tag]["automine"]+4)**3)*20
                if cost > userlist[tag]["coins"]:
                    await send("You don't have enough coins for that! You need " + str(cost) + ", but you only have " + str(userlist[tag]["coins"]) + " coins.")
                    return
                await send("Sure! That'll be "+str(cost)+" coins! Do you want to buy? y/n")
                try:
                    msg = await client.wait_for('message', timeout=30.0, check=check)
                except:
                    await send("Error: Timeout. Purchase cancelled.")
                msg = msg.content
                print(msg)
                print(msg.casefold())
                print('y')
                print(msg.casefold() == 'y')
                if msg.casefold() == 'y':
                    userlist[tag]["automine"] += 1
                    userlist[tag]["coins"] -= cost
                    userlist[tag]["time"] = time.time()
                    edit_users(userlist)
                else:
                    await send("Purchase cancelled.")
        edit_users(userlist)
        
    #except Exception as error:
    #    print("Error:", error)
    #    await send("Oops! I encountered an error! (" +str(error)+") Please contact @mysteriouslyseeing#3832 for help!")
            

client.run(token)
