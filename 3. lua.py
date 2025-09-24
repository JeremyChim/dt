path = r"E:\GAME\steamapps\common\dota 2 beta\game\dota\scripts\vscripts\game\Customize\general.lua"
reset = False
friend = ["nevermore", "earthshaker", "shadow_demon", "pugna"]  # 队友列表
enemy = ["medusa", "pangolier", "magnataur", "disruptor", "naga_siren"]  # 敌人列表

# 读取文件
with open("lua/general.lua", encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
x = 0
y = 0
for i, line in enumerate(lines, 1):
    if 49 <= i <= 52:  # 4个队友行号
        val = line.split("'")[1]
        if reset:
            new_val = "Random"
        else:
            new_val = "npc_dota_hero_" + friend[x]  # 获取队友名字
        line = line.replace(val, new_val)  # 替换队友名字
        x += 1
        print(line, end="")
    if 57 <= i <= 61:  # 5个敌人行号
        val = line.split("'")[1]
        if reset:
            new_val = "Random"
        else:
            new_val = "npc_dota_hero_" + enemy[y]  # 获取敌人名字
        line = line.replace(val, new_val)  # 替换敌人名字
        y += 1
        print(line, end="")
    new_lines.append(line)

# 写入文件
with open(path, "w", encoding='utf-8') as f:
    f.writelines(new_lines)

input("...")
