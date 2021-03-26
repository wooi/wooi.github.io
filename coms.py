#coding=utf-8
import commands

def execute(com):
	print com
	state,result = commands.getstatusoutput(com)
        print result
        return state , result
def test():
	print 'hello'
