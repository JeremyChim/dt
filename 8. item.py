def find1(content: list, item_name: str) -> int:
    for i, line in enumerate(content):
        if item_name in line:
            print(i + 1, line, end='')
            return i


def find2(content: list, no: int, item_attr: str) -> int:
    for i, line in enumerate(content[no:], no):
        if item_attr in line:
            print(i + 1, line, end='')
            return i


def change(content: list, no: int, old_val, new_val) -> list:
    new_content = content[:]
    line: str = content[no]
    new_content[no] = line.replace(old_val, new_val)
    print(no, new_content[no])
    return new_content


def change_itme(content, item_name, item_attr, old_val, new_val) -> list:
    no1 = find1(content, item_name)
    no2 = find2(content, no1, item_attr)
    new_content = change(content, no2, old_val, new_val)
    return new_content


with open("npc/items.txt") as f:
    content = f.readlines()
    new_content = change_itme(content,'"item_aghanims_shard"', '"ItemInitialStockTime"','990','0')

with open("vpk/pak01_dir/scripts/npc/items.txt", "w") as f:
    f.writelines(new_content)

input("...")

# new_lines = []
# for i, line in enumerate(lines, 1):
#     # item_aghanims_shard
#     if i == 6110:  # "ItemInitialStockTime"			"990.0"
#         line = line.replace("990.0", "0.0")
#         print(i, line, end="")
#     new_lines.append(line)
