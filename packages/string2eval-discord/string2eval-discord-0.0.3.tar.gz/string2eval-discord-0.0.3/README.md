hi arno

import `string2eval` to do the kurdish and use `string2eval.evaluate(ctx, client, body)` to do th

ctx is ctx, client is your client, and body is the code you want to evaluate

while defining client put your id in `owner_ids` to make it ONLY work when you use the eval. you can put
more than one person

**DO NOT** put `@commands.is_owner()` or  try to make the command owner only yourself.
it handles that automatically.

if someone who doesn't have access tries to use it it will raise `NoPermsToEval`

**ENABLE PRESENCE AND MEMBERS INTENT (NOT REQUIRED BUT WORKS BEST)**

funny example

```python
from discord.ext import commands
import string2eval

TOKEN = "??"

client = commands.Bot(command_prefix="!!!", owner_ids=[429935667737264139])

client.remove_command("help")

@client.command(name="eval")
async def _eval(ctx, *, body):
    try:
        await string2eval.evaluate(ctx, client, body)
    except string2eval.NoPermsToEval:
        await ctx.send("lol cant even use eval smh")

client.run(TOKEN)
```