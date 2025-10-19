import pyperclip

expand_per = '+50%'

def update_value(old_ability):
    sap = ('[tab]"[ab_name]"\t\t\t\t\t\t"[ab_val]"\n'
           f'[tab]"special_bonus_shard"\t\t"{expand_per}"\n'
           f'[tab]"special_bonus_scepter"\t\t"{expand_per}"\n')
    ability_list = old_ability.split('"')
    new_ability = (sap.replace('[tab]', ability_list[0])
                   .replace('[ab_name]', ability_list[1])
                   .replace('[ab_val]', ability_list[3]))
    return new_ability


def update_value_more(old_ability):
    sap = ('[tab]"[ab_name]"\n'
           '[tab]{\n'
           '[tab]\t"value"\t\t\t\t\t\t"[ab_val]"\n'
           f'[tab]\t"special_bonus_shard"\t\t"{expand_per}"\n'
           f'[tab]\t"special_bonus_scepter"\t\t"{expand_per}"\n'
           '[tab]}\n')
    ability_list = old_ability.split('"')
    new_ability = (sap.replace('[tab]', ability_list[0])
                   .replace('[ab_name]', ability_list[1])
                   .replace('[ab_val]', ability_list[3]))
    return new_ability


# def fun3(a):
#     sap = ('[tab]"[ab_name]"\n'
#            '[tab]{\n'
#            '[tab]\t"value"\t\t\t\t\t\t"0"\n'
#            '[tab]}\n'
#            '[tab]"AbilityChargeRestoreTime"\n'
#            '[tab]{\n'
#            '[tab]\t"value"\t\t\t\t\t\t"[ab_val]"\n'
#            '[tab]\t"special_bonus_shard"\t\t"-25%"\n'
#            '[tab]\t"special_bonus_scepter"\t\t"-25%"\n'
#            '[tab]}\n'
#            '[tab]"AbilityCharges"\n'
#            '[tab]{\n'
#            '[tab]\t"value"\t\t\t\t\t\t"0"\n'
#            '[tab]\t"special_bonus_shard"\t\t"+1"\n'
#            '[tab]\t"special_bonus_scepter"\t\t"+1"\n'
#            '[tab]}\n'
#            )
#     b = a.split('"')
#     c = sap.replace('[tab]', b[0]).replace('[ab_name]', b[1]).replace('[ab_val]', b[3])
#     return c

def update_charge_restore(old_cooldown):
    sap = ('[tab]"AbilityCharges"\n'
           '[tab]{\n'
           '[tab]\t"value"\t\t\t\t\t\t"1"\n'
           '[tab]\t"special_bonus_shard"\t\t"+1"\n'
           '[tab]\t"special_bonus_scepter"\t\t"+1"\n'
           '[tab]}\n'
           '[tab]"AbilityChargeRestoreTime"\n'
           '[tab]{\n'
           '[tab]\t"value"\t\t\t\t\t\t"[ab_val]"\n'
           '[tab]\t"special_bonus_shard"\t\t"-25%"\n'
           '[tab]\t"special_bonus_scepter"\t\t"-25%"\n'
           '[tab]}\n'
           '[tab]"[ab_name]"\t\t\t\t\t\t"0"\n'
           )
    cooldown_list = old_cooldown.split('"')
    new_cooldown = (sap.replace('[tab]', cooldown_list[0])
                    .replace('[ab_name]', cooldown_list[1])
                    .replace('[ab_val]', cooldown_list[3]))
    return new_cooldown


if __name__ == '__main__':
    # x = '\t\t\t\t"haha"\t\t\t\t"100 200 300 400"'
    # print(fun1(x))
    # print(fun2(x))
    print('"special_bonus_shard"		"+50%"')
    print('"special_bonus_scepter"		"+50%"')
    print('"AbilityCharges"                 "1"')
    print('"AbilityChargeRestoreTime"       "10"')
    print('')

    while True:
        ability_data = input('输入技能数据：')
        if '--ch' in ability_data:
            ability_data = update_charge_restore(ability_data)
        else:
            if 'value' in ability_data:
                ability_data = update_value(ability_data)
            else:
                ability_data = update_value_more(ability_data)

            if ('--cd' in ability_data
                    or 'Cooldown' in ability_data
                    or 'ManaCost' in ability_data
                    or 'CastPoint' in ability_data
                    or 'RestoreTime' in ability_data):
                ability_data = ability_data.replace('+50%', '-25%').replace('--cd', '')

        print(ability_data)
        pyperclip.copy(ability_data)
