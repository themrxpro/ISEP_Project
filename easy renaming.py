import os

folder = r'F:\Desktop\New folder'
for root, dirnames, filenames in os.walk(folder):
    i=0
    for filename in filenames:
        #print('{}-{}-{}'.format(root,dirnames,filename))
        pasta = os.path.split(root)[1]
        i=i+1
        new_name ='{} {}{}'.format(pasta,i,os.path.splitext(filename)[1])
        new = os.path.join(root, new_name)
        old = os.path.join(root, filename)
        os.rename(old,new)