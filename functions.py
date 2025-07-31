import aiohttp

def formatPrice(v):
    try:
        v = float(v)
    except (ValueError, TypeError):
        return "0"

    limits = [(1_000, ""), (1_000_000, "K"), (1_000_000_000, "M"), (1_000_000_000_000, "B")]
    limit, suffix = next(((l, s) for l, s in limits if v < l), (1_000_000_000_000_000, "T"))
    val = v / (1 if suffix == "" else limit / 1_000)
    s = f"{val:.2f}".rstrip('0').rstrip('.')
    return f"{s}{suffix}"

def formatPlaytime(ms):
    seconds = int(ms) // 1000
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or not parts:
        parts.append(f"{minutes}m")
    return ' '.join(parts)

async def getOnlineStatus(key, playername):
    url = f"https://api.donutsmp.net/v1/lookup/{playername}"
    headers = {
        "Authorization": key,
        "accept": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            try:
                data = await resp.json(content_type=None)
            except Exception as e:
                print(f"JSON decode error: {e}")
                return
    status = data.get("status", 0)
    if status == 500:
        return False
    else:
        return True