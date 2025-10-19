def tab_up(old_text):
    old_list = old_text.split('\n')
    new_list = []
    for row in old_list:
        row = '\t' + row
        new_list.append(row)
    new_text = '\n'.join(new_list)
    return new_text

def tab_down(old_text):
    old_list = old_text.split('\n')
    new_list = []
    for row in old_list:
        if len(row) != 0 and row[0] == '\t':
            new_list.append(row[1:])
        else:
            new_list.append(row)
    new_text = '\n'.join(new_list)
    return new_text

if __name__ == '__main__':
    test_text = '\t123\t456\n\t123\t456'
    print(test_text)
    print(tab_up(test_text))
    print(tab_down(test_text))