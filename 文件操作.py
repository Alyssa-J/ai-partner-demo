
f = open("./resource/望庐山瀑布.txt","r",encoding="utf-8")

# content = f.read()
# print(content)
# f.close()

content_list =f.readlines()
for line in content_list:
    print(line.strip())

f.close()

# try:写入文件
# finally：f.close