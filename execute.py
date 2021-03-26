import os
from coms import execute
def post_repo(data):
    if data.find(repo[0]) != -1:
        print '====================='+repo[1]+'====================='
        return data.replace(repo[0],repo[1])
    else:
        print '====================='+repo[0]+'====================='
        return data.replace(repo[1],repo[0])


repo =['https://github.com/wooi/wooi.github.io','https://git.coding.net/Wooi/wooi.coding.me.git']
cwd = os.getcwd()
filename = cwd+'/_config.yml'
com_clean = 'hexo clean'
com_g = 'hexo g'
com_d = 'hexo d'


mfile = open(filename,'r')
old_data = mfile.read()
mfile.close()

new_data = post_repo(old_data) 
mfile = open(filename,'w')
mfile.write(new_data)
mfile.close()
execute(com_clean)
execute(com_g)
execute(com_d)

old_data = new_data

new_data = post_repo(old_data)
mfile = open(filename,'w')
mfile.write(new_data)
mfile.close()
execute(com_clean)
execute(com_g)
execute(com_d)









