import dataStruct
from dataStruct import const
from dataStruct import VT
from dataStruct import InstructionStream
from dataStruct import SymbolTable
from wordsAnalysis import wordAnalysis
from grammaAnalysis import grammaAnalysis
import sys

if(len(sys.argv) >= 2):
    debug = False
else:
    debug = True

if not debug:
    if len(sys.argv) >= 2 :
        inFileName = sys.argv[1]
    else:
        inFileName = 'test.c'
    file = open(inFileName, 'r')
    if len(sys.argv) >= 3:
        outFileName = sys.argv[2]
    else:
        outFileName = 'out.txt'
    outFile = open(outFileName, 'w')
else:
    # 以下为调试时的设置
    fileName = 'test.c'
    file = open(fileName, 'r');

# 词法分析相关调用
WA = wordAnalysis(file)
WA.scan()
# 加上这个语句可以查看词法分析结果
# WA.printAllVt()
for error in WA.errors:
    if debug:
        error.printMsg()
    else:
        error.fileOutMsg(outFile)

symbolTable = SymbolTable()
instructionStream = InstructionStream()
GA = grammaAnalysis(file,WA.head,WA.pointer, symbolTable, instructionStream)
GA.scan()
# 加上这个语句可以查看语法分析结果
# GA.printAllVn()
# 以下这个for循环打印所有Error信息
for error in GA.errors:
    if debug:
        error.printMsg()
    else:
        error.fileOutMsg(outFile)
# 以下语句打印符号表
GA.symbolTable.printTable()

# GA.symbolTable.fileOutTable(outFile)
# 以下语句打印最终生成的指令
if debug:
    instructionStream.printAllInstructions()
else:
    instructionStream.fileOutAllInstructions(outFile)