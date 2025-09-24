# 创建队友列表
friend = ["friend2", "friend3", "friend4", "friend5"]
# 创建敌人列表
enemy = ["enemy1", "enemy2", "enemy3", "enemy4", "enemy5"]

# 读取文件
with open("lua/general.lua", encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
x = 0
y = 0
for i, line in enumerate(lines, 1):
    if 49 <= i <= 52:  # 4个队友行号
        val = line.split("'")[1]
        new_val = friend[x] # 获取队友名字
        line = line.replace(val, new_val)  # 替换队友名字
        x += 1
        print(line, end="")
    if 57 <= i <= 61:  # 5个敌人行号
        val = line.split("'")[1]
        new_val = enemy[y] # 获取敌人名字
        line = line.replace(val, new_val)  # 替换敌人名字
        y += 1
        print(line, end="")
    new_lines.append(line)

# 写入文件
with open("general.lua", "w", encoding='utf-8') as f:
    f.writelines(new_lines)
