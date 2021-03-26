#coding=utf-8
from coms import execute
from coms import call_com
file_path = 'C:\\Users\Administrator\\MK\\'

print u"1.反编译文件，输入APK文件名（不包含数字和后缀名）:"
apk_name = raw_input()
apk_name = file_path + apk_name

com = file_path + 'apktool d '+ apk_name+'.apk -o '+apk_name
execute(com)
print u'完成反编译任务\n'

print u'2.输入渠道号（去除a和b）:'
channel_id = raw_input()

marz_filepath = apk_name+"/assets/marz"
open(marz_filepath,'w').close()
with open(marz_filepath,'a') as myfile:
    myfile.write('b'+channel_id)
print u'成功修改敏坤Id为b'+channel_id

mainfest_file = open(apk_name+"/AndroidManifest.xml",'r')
mainfest_data = mainfest_file.read()
mainfest_file.close()

mainfest_new_id = mainfest_data.replace("com.zolamobi.Umeng",'a'+channel_id)
mainfest_file = open(apk_name+"/AndroidManifest.xml",'w')
mainfest_file.write(mainfest_new_id)
mainfest_file.close()
print u'成功修改友盟Id为a'+channel_id

com = file_path + 'apktool b '+ apk_name+' -o '+apk_name+'_out.apk'
execute(com)
print u'3.编译成功，开始签名\n'

com2 =  'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1  -keystore '+file_path+'bxp.keystore -signedjar '+apk_name+'_'+channel_id+'_sign.apk '+apk_name+'_out.apk '+file_path+'bxp.keystore'
print u'4.输入密码123456'
execute(com)




