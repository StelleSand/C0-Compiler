from dataStruct import const
from dataStruct import reservers
from dataStruct import V
from dataStruct import VT
from dataStruct import VN
from dataStruct import InstructionStream
from dataStruct import Instruction
from dataStruct import SymbolTable
from dataStruct import SymbolTableItem
from dataStruct import Error


class grammaAnalysis:
    def __init__(self,file, start, end, symbolTable, instructionStream):
        self.file = file
        self.start = start
        self.end = end
        self.pointer = self.start
        self.errors = []
        self.program = None
        self.symbolTable = symbolTable
        self.instructionStream = instructionStream
    def emit(self, instruction):
        if not instruction:
            return
        assert isinstance(instruction,Instruction)
        self.instructionStream.append(instruction)
    # 为overlookSet添加一个元素
    def overlookSetAdd(self, overlookSet, item):
        if not item in overlookSet:
            overlookSet.append(item)
        return overlookSet
    # 跳过单词直到下一个指定符号,取出的单词是指定符号
    def overlookToMark(self, mark):
        while self.pointer.isType(mark) :
            self.getsym()
    # 跳过单词直到下一个指定符号集,取出的单词是指定符号集中任意符号
    def overlookToMarks(self, marks):
        while True:
            for mark in marks:
                if self.pointer.isType(mark) or self.isEnd():
                    return
            self.getsym()
    # 判断给定Vn是否是空节点，如果子节点为0，则返回空节点
    def checkEmpty(self, Vn):
        if len(Vn.children) == 0 :
            Vn.vtype = const.EMPTY
        return Vn
    # 获取下一个单词，即Vt
    def getsym(self):
        if not self.isEnd():
            self.pointer = self.pointer.next
        else :
            print("to End！")
        # 对于连续的空分号的处理: 直接忽略
        if (not self.pointer is None) and self.pointer.isSemicolon() and self.pointer.previous.isSemicolon():
            self.getsym()
    # 判断语法分析是否结束
    def isEnd(self):
        return self.pointer.isEOF()
    def hasError(self):
        return len(self.errors) > 0
    # 退格，还原上一个单词的状态
    def retrace(self):
        self.pointer = self.pointer.previous;
    # 设置sym状态为指定状态
    def setsymat(self, pointer):
        self.pointer = pointer;
    def addSymbol(self, name, value, itemType):
        self.symbolTable.addItem(name, value, itemType)
    def scan(self):
        # 进入程序是当前单词已经是链表的第一个单词
        print('Gramma Analysis Start!')
        self.program = self.analyze_program()
        print('Gramma Analysis Complete!')
        return self.program
    # <程序>
    # <程序> ::= (<常量说明部分>)(<变量说明部分>){<函数定义部分>}<主函数>
    def analyze_program(self):
        overlookSet = [const.CONST, const.INT, const.VOID]
        V_program = VN.create(const.PROGRAM)
        # 当没有检测到主函数时，执行此无限循环
        while True:
            # 如果是const，<常量说明>
            if self.pointer.isR_Const():
                V_program.append(self.analyze_constIllustrate(overlookSet))
            # 如果是void，进入函数分析！
            elif self.pointer.isR_Void():
                V_program.append(self.analyze_functionDefine(overlookSet))
            # 前面两种状态都不对，那就是定义变量或者定义其它函数或者定义主函数，需要多看两步再说
            elif self.pointer.isR_Int():
                # 保存下当前指针状态
                tempPointer = self.pointer
                self.getsym()
                # 识别出main函数，跳出无限循环
                if self.pointer.isR_Main():
                    self.setsymat(tempPointer)
                    break
                # 如果识别出ID,仍要再看一步
                elif self.pointer.isID():
                    self.getsym()
                    # 如果是左括号,那就是函数定义了，其它情况都交给变量定义来做
                    if self.pointer.isL_Parenthesis():
                        self.setsymat(tempPointer)
                        V_program.append(self.analyze_functionDefine(overlookSet))
                    else :
                        self.setsymat(tempPointer)
                        V_program.append(self.analyze_varIllustrate(overlookSet))
                # ID都识别不出来，那只有一个int头，交给变量定义吧
                else :
                    self.setsymat(tempPointer)
                    V_program.append(self.analyze_varIllustrate(overlookSet))
            # 因为文件终结符而结束！
            elif self.isEnd():
                break
            # 什么都识别不出来，只有报错跳过了
            else:
                self.error(Error.GA_ILLEGAL_INPUT)
                self.overlookToMarks(overlookSet)
        if not self.isEnd():
            # 跳出循环且不是读到文件结束，只有可能是因为识别出了main函数，直接进行函数识别
            V_program.append(self.analyze_functionDefine())
        return V_program
    # 常量说明部分
    # <常量说明部分> ::=  const <常量定义>｛,<常量定义>｝;
    def analyze_constIllustrate(self, overlookSet = [const.CONST, const.INT, const.VOID]):
        downoverlookSet = overlookSet[:]
        self.overlookSetAdd(downoverlookSet, const.SEMICOLON);
        V_constIllustrate = VN.create(const.CONST_ILLUSTRATE)
        # 此处为第一个常量定义处理，如果只有空const,报错！
        # 进入函数的时候已经检验了存在 const标识符,不用重复检查
        V_constIllustrate.append(self.pointer)
        self.getsym()
        V_constIllustrate.append(self.analyze_constDefine(downoverlookSet))
        while(self.pointer.isComma()):
            comma = self.pointer
            self.getsym()
            V_constIllustrate.append(comma).append(self.analyze_constDefine(downoverlookSet))
        #如果读到分号，结束返回,记得多读一个！
        if self.pointer.isSemicolon():
            V_constIllustrate.append(self.pointer)
            self.getsym()
        else:
            # 如果没有分号，报错！但是别多读一个了
            # 已经读的仍然保留
            self.error(Error.GA_MISS_SEMICOLON, self.pointer.previous)
        # 防止只有 const 保留字和/或 ; 被读入了
        if not V_constIllustrate.hasVn():
            V_constIllustrate.empty()
        self.run_constIllustration(V_constIllustrate)
        return self.checkEmpty(V_constIllustrate)
    # 常量定义部分
    # <常量定义> ::=  <标识符>＝<整数>
    def analyze_constDefine(self, overlookSet = [const.SEMICOLON, const.ID, const.CONST, const.INT, const.VOID]):
        V_constDefine = VN.create(const.CONST_DEFINE)
        if self.pointer.isID():
            V_constDefine.append(self.pointer)
            self.getsym()
            if self.pointer.isAssign():
                V_constDefine.append(self.pointer)
                self.getsym()
                if self.pointer.isInteger():
                    V_constDefine.append(self.pointer)
                    self.getsym()
                else :
                    self.error(Error.GA_MISS_INTEGER, self.pointer.previous, 'Gramma Analysis Error: A value after Assign mark is expected.')
                    self.overlookToMarks(overlookSet)
                    V_constDefine.empty()
            else :
                self.error(Error.GA_MISS_ASSIGN, self.pointer.previous, "Gramma Analysis Error: A \'=\'  is expected in const variables\' defination  .")
                self.overlookToMarks(overlookSet)
                V_constDefine.empty()
        else :
            self.error(Error.GA_MISS_IDENTIFIER)
            self.overlookToMarks(overlookSet)
            V_constDefine.empty()
        return V_constDefine
    # 变量说明部分
    # <变量说明部分>::=  <声明头部>｛,<标识符>｝;
    def analyze_varIllustrate(self, overlookSet = [const.SEMICOLON, const.ID, const.CONST, const.INT, const.VOID]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.COMMA)
        self.overlookSetAdd(downOverlookSet, const.SEMICOLON)
        V_varIllustrate = VN.create(const.VAR_ILLUSTRATE)
        # 进入函数的时候已经检验了存在 int标识符,不用重复检查,但是int这个属于<变量头部>这里不要规约
        V_varIllustrate.append(self.analyze_declareHead(downOverlookSet))
        while(self.pointer.isComma()):
            comma = self.pointer
            self.getsym()
            if(self.pointer.isID()):
                V_varIllustrate.append(comma)
                V_varIllustrate.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_IDENTIFIER)
        #如果读到分号，结束返回,记得多读一个！
        if self.pointer.isSemicolon():
            V_varIllustrate.append(self.pointer)
            self.getsym()
        # 两个连续的标识符, 报缺分号
        # elif self.pointer.isID():
        #   self.error(Error.GA_MISS_COMMA, self.pointer.previous, 'Gramma Analysis Error: A \',\' is expected between variables\' defination.')
        else:
            # 其余则报缺分号！
            self.error(Error.GA_MISS_SEMICOLON, self.pointer.previous, 'Gramma Analysis Error: a \';\' after end of sentence is Expected.')
            self.overlookToMarks(overlookSet)
        self.run_varIllustrate(V_varIllustrate)
        return self.checkEmpty(V_varIllustrate)
    # 声明头部
    # <声明头部>::=  int <标识符>
    def analyze_declareHead(self, overlookSet = [const.COMMA, const.SEMICOLON]):
        V_declareHead = VN.create(const.DECLARE_HEAD)
        V_declareHead.append(self.pointer)
        self.getsym()
        if(self.pointer.isID()):
            V_declareHead.append(self.pointer)
            self.getsym()
        else:
            self.error(Error.GA_MISS_IDENTIFIER)
            self.overlookToMarks(overlookSet)
        return self.checkEmpty(V_declareHead)
    # 参数表
    # <参数表>::=  int <标识符>｛,int <标识符>} | <空>
    def analyze_parameterList(self, overlookSet = [const.R_PARENTHESIS]):
        # downOverlookSet = overlookSet[:]
        # self.overlookSetAdd(downOverlookSet, const.R_PARENTHESIS)
        V_parameterList = VN.create(const.PARAMETER_LIST)
        parameterNum = 0
        # 确认是INT，先加入子节点
        if self.pointer.isR_Int():
            V_parameterList.append(self.pointer)
            self.getsym()
            if self.pointer.isID():
                V_parameterList.append(self.pointer)
                parameterNum += 1
                self.getsym()
                while(self.pointer.isComma()):
                    comma = self.pointer
                    self.getsym()
                    if self.pointer.isR_Int():
                        int = self.pointer
                        self.getsym()
                        if self.pointer.isID():
                            parameterNum += 1
                            V_parameterList.append(comma)
                            V_parameterList.append(int)
                            V_parameterList.append(self.pointer)
                            self.getsym()
                        else:
                            self.error(Error.GA_MISS_IDENTIFIER, self.pointer, 'Gramma Analysis Error: A identifier is expected after variables\' type.')
                            self.overlookToMarks(overlookSet)
                    else:
                        self.error(Error.GA_MISS_TYPE, self.pointer, 'Gramma Analysis Error: A variable type declaration is expected before variables.')
                        self.overlookToMarks(overlookSet)
                if self.pointer.isR_Int():
                    self.error(Error.GA_MISS_COMMA)
                    self.overlookToMarks(overlookSet)
                elif self.pointer.isID():
                    self.error(Error.GA_MISS_TYPE)
                    self.overlookToMarks(overlookSet)
            else:
                self.error(Error.GA_MISS_IDENTIFIER, self.pointer,'Gramma Analysis Error: A identifier is expected after variables\' type.')
                self.overlookToMarks(overlookSet)
                return V_parameterList.empty()
        else:
            self.overlookToMarks(overlookSet)
        if parameterNum == 0:
            V_parameterList.empty()
        return self.checkEmpty(V_parameterList)
    # 参数
    # <参数>::=  '('<参数表>')'
    def analyze_parameter(self, lookoverSet = [const.L_BRACE]):
        downLookoverSet = lookoverSet[:]
        self.overlookSetAdd(downLookoverSet, const.R_PARENTHESIS)
        #进入时已经确认是(了，直接添加！
        V_parameter = VN.create(const.PARAMETER)
        V_parameter.append(self.pointer)
        self.getsym()
        # 判断参数表是否为空,不为空则进入参数表解析
        if not self.pointer.isR_Parenthesis():
            # 添加参数表函数解析结果
            V_parameter.append(self.analyze_parameterList())
        if self.pointer.isR_Parenthesis():
            V_parameter.append(self.pointer)
            self.getsym()
        else:
            self.error(Error.GA_MISS_R_PARENTHESIS)
        return self.checkEmpty(V_parameter)
    # 因子
    # <因子>::=  <标识符>｜'（'<表达式>'）'｜<整数>｜<函数调用语句>
    def analyze_factor(self, overlookSet):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet,const.R_PARENTHESIS)
        V_factor = VN.create(const.FACTOR)
        # 进入后先判断是哪种因子
        # 如果是ID，则可能是标识符或者调用函数
        if self.pointer.isID() and (not self.pointer.next.isL_Parenthesis()):
            symbolItem = self.symbolTable.getItem(self.pointer.text)
            # 去符号表中找这个ID，找不到记得报错
            if symbolItem:
                V_factor.append(self.pointer)
                self.emit(Instruction(Instruction.LOC, symbolItem.name))
                self.getsym()
            else:
                self.error(Error.ST_UNDEFINED_ID)
                self.overlookToMarks(overlookSet)
        elif self.pointer.isID() and self.pointer.next.isL_Parenthesis():
            symbolItem = self.symbolTable.getItem(self.pointer.text)
            # 去符号表中找这个ID，找不到记得报错
            if symbolItem:
                V_factor.append(self.analyze_sentenceFunctionCall(overlookSet))
            else:
                self.error(Error.ST_UNDEFINED_ID)
                self.overlookToMarks(overlookSet)
        # 处理表达式
        elif self.pointer.isL_Parenthesis():
            l_parenthesis = self.pointer
            self.getsym()
            # 接着要进行进入表达式解析
            expression = self.analyze_expression(downOverlookSet)
            if self.pointer.isR_Parenthesis():
                V_factor.append(l_parenthesis).append(expression).append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_R_PARENTHESIS)
                self.overlookToMarks(overlookSet)
        elif self.pointer.isInteger():
            V_factor.append(self.pointer)
            self.emit(Instruction(Instruction.LOC, self.pointer.text))
            self.getsym()
        else:
            self.error(Error.GA_ILLEGAL_INPUT, self.pointer.previous, "Gramma Analysis Error: An expression, id, or integer is expeted")
            self.overlookToMarks(overlookSet)
        return self.checkEmpty(V_factor)
    # 项
    # <项>::=<因子>{<乘法运算符><因子>}
    def analyze_term(self, overlookSet):
        downOverlookSet = overlookSet[:]
        V_term = VN.create(const.TERM)
        factor = self.analyze_factor(overlookSet)
        V_term.append(factor)
        while self.pointer.isStarOperator():
            star = self.pointer
            self.getsym()
            factor = self.analyze_factor(overlookSet)
            V_term.append(star).append(factor)
            self.emit(Instruction.create(star))
        # 此处结束后没有检查！！！直接返回
        return self.checkEmpty(V_term)
    # 表达式
    # <表达式>::= (<加法运算符>)<项>｛<加法运算符><项>｝
    def analyze_expression(self, overlookSet):
        downOverlookSet = overlookSet[:]
        V_expression = VN.create(const.EXPRESSION)
        plus = False
        # 如果开头就有符号，那么肯定是 -x 或者 +x ，默认操作数为0
        if self.pointer.isPlusOperator():
            plus = self.pointer
            V_expression.append(plus)
            self.getsym()
            # 操作数 0 入栈
            self.emit(Instruction(Instruction.LOC, '0', False))
        term = self.analyze_term(overlookSet)
        # 如果有操作符，那么生成加或减指令
        self.emit(Instruction.create(plus))
        V_expression.append(term)
        while self.pointer.isPlusOperator():
            plus = self.pointer
            self.getsym()
            term = self.analyze_term(overlookSet)
            V_expression.append(plus).append(term)
            self.emit(Instruction.create(plus))
        # 此处结束后没有检查！！！直接返回
        return self.checkEmpty(V_expression)
    # 条件
    # <条件>::=  <表达式><关系运算符><表达式>｜<表达式>
    def analyze_condition(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = overlookSet[:]
        V_condition = VN.create(const.CONDITION)
        expression = self.analyze_expression(overlookSet)
        V_condition.append(expression)
        if self.pointer.isRelationOperator():
            relationOperator = self.pointer
            V_condition.append(relationOperator)
            self.getsym()
            V_condition.append(self.analyze_expression(overlookSet))
            # 结束后将逻辑运算符入栈
            self.emit(Instruction.create(relationOperator))
        # 这里结束后没有检查，直接返回
        return self.checkEmpty(V_condition)
    # 条件语句
    # <条件语句>::=  if'（'<条件>'）'<语句>(else<语句>)
    def analyze_sentenceIf(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.R_PARENTHESIS)
        self.overlookSetAdd(downOverlookSet, const.ELSE)
        ifSentenceOverlookSet = overlookSet[:]
        self.overlookSetAdd(ifSentenceOverlookSet, const.ELSE)
        V_sentenceIf = VN.create(const.SENTENCE_CONDITION)
        V_sentenceIf.append(self.pointer)
        self.getsym()
        if self.pointer.isL_Parenthesis():
            V_sentenceIf.append(self.pointer)
            self.getsym()
            V_sentenceIf.append(self.analyze_condition(downOverlookSet))
            if self.pointer.isR_Parenthesis():
                # 分析完条件，加入比较跳转指令
                headBRFInstruction = Instruction(Instruction.BRF, Instruction.generateLab())
                self.emit(headBRFInstruction)
                V_sentenceIf.append(self.pointer)
                self.getsym()
                if not self.pointer.isR_Else():
                    V_sentenceIf.append(self.analyze_sentence(ifSentenceOverlookSet))
                else:
                    self.error(Error.GA_MISS_SENTENCE, self.pointer.previous, 'Gramma Analysis Error: A sentence between IF and ELSE is expected.')
                if self.pointer.isR_Else():
                    V_sentenceIf.append(self.pointer)
                    self.getsym()
                    # 在if标记后的语句分析结束后，Else分析开始前,添加一条BR指令，
                    # 用于跳转到Else分析结束后的第一条指令
                    # 如果没有else部分，这条指令不存在
                    headBRInstruction = Instruction(Instruction.BR, Instruction.generateLab())
                    self.emit(headBRInstruction)
                    # if标记之后的语句分析结束后，加入lab标记，
                    # 使得在Else分析出的语句中的第一条语句获得lab标记
                    self.instructionStream.setLab(headBRFInstruction.operator)
                    V_sentenceIf.append(self.analyze_sentence(overlookSet))
                    # 对于存在Else分析的情况，在Else结束后的第一条语句后面添加BR标记
                    self.instructionStream.setLab(headBRInstruction.operator)
                else:
                    # if标记之后的语句分析结束后，加入lab标记，
                    # 在没有else标记的情况下，if分析后的第一条语句也要加入lab标记
                    self.instructionStream.setLab(headBRFInstruction.operator)
            else :
                self.error(Error.GA_MISS_R_PARENTHESIS)
                self.overlookToMarks(overlookSet)
        else:
            self.error(Error.GA_MISS_L_PARENTHESIS, self.pointer.previous)
            self.overlookToMarks(overlookSet)
        return V_sentenceIf
    # 循环语句
    # <循环语句>::=  while'（'<条件>'）'<语句>
    def analyze_sentenceWhile(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = [const.R_BRACE]
        self.overlookSetAdd(downOverlookSet, const.R_PARENTHESIS)
        V_sentenceWhile = VN.create(const.SENTENCE_LOOP)
        V_sentenceWhile.append(self.pointer)
        self.getsym()
        whileBRInstruction = None
        whileHeadLab = Instruction.generateLab()
        if self.pointer.isL_Parenthesis():
            V_sentenceWhile.append(self.pointer)
            self.getsym()
            # 为while头部设置lab标签
            self.instructionStream.setLab(whileHeadLab)
            V_sentenceWhile.append(self.analyze_condition(downOverlookSet))
            if self.pointer.isR_Parenthesis():
                V_sentenceWhile.append(self.pointer)
                self.getsym()
                # 条件分析结束后加入BRF指令
                whileBRInstruction = Instruction(Instruction.BRF, Instruction.generateLab())
                self.instructionStream.append(whileBRInstruction)
                V_sentenceWhile.append(self.analyze_sentence(overlookSet))
                # while中的语句分析结束后，加入BR指令，直接跳转回while头部
                self.emit(Instruction(Instruction.BR, whileHeadLab))
            else:
                self.error(Error.GA_MISS_R_PARENTHESIS)
                self.overlookToMarks(downOverlookSet)
        else:
            self.error(Error.GA_MISS_L_PARENTHESIS, self.pointer.previous)
            self.overlookToMarks(downOverlookSet)
        # while分析结束后，在其后的第一条语句添加lab标记
        if whileBRInstruction:
            self.instructionStream.setLab(whileBRInstruction.operator)
        return self.checkEmpty(V_sentenceWhile)
    # 值参数表
    # <值参数表>::=  <表达式>｛,<表达式>｝｜<空>
    def analyze_valueParameterList(self, overlookSet = [const.R_PARENTHESIS]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.COMMA)
        V_valueParameterList = VN.create(const.VALUE_PARAMETER_LIST)
        V_valueParameterList.append(self.analyze_expression(downOverlookSet))
        while self.pointer.isComma():
            V_valueParameterList.append(self.pointer)
            self.getsym()
            V_valueParameterList.append(self.analyze_expression(downOverlookSet))
        # 此处绝对不要检查！ 因为空的也要返回去！
        return V_valueParameterList
    # 函数调用语句
    # <函数调用语句>::=  <标识符>'（'<值参数表>'）'
    def analyze_sentenceFunctionCall(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.R_PARENTHESIS)
        V_sentenceFunctionCall = VN.create(const.SENTENCE_FUNCTION_CALL)
        func = self.pointer
        V_sentenceFunctionCall.append(func)
        symbolFunc = self.symbolTable.getItem(self.pointer.text)
        if not symbolFunc:
            self.error(Error.ST_UNDEFINED_ID)
            self.overlookToMarks(overlookSet)
        else:
            if not symbolFunc.isFunction():
                self.error(Error.ST_UNDEFINED_ID)
                self.overlookToMarks(overlookSet)
        self.getsym()
        if self.pointer.isL_Parenthesis():
            V_sentenceFunctionCall.append(self.pointer)
            self.getsym()
            # 下一个如果不是右括号，才进入参数表分析
            if not self.pointer.isR_Parenthesis():
                paraValue = self.analyze_valueParameterList(downOverlookSet)
                paras = paraValue.findChildren(const.EXPRESSION)
                # 这里检查参数数量是否正确，但是出错也不要 overlook
                if len(paras) > symbolFunc.paraNum:
                    self.error(Error.ST_CALL_PARANUM_EXCEED, func)
                elif len(paras) < symbolFunc.paraNum:
                    self.error(Error.ST_CALL_PARANUM_LACK, func)
                V_sentenceFunctionCall.append(paraValue)
            if self.pointer.isR_Parenthesis():
                V_sentenceFunctionCall.append(self.pointer)
                self.emit(Instruction(Instruction.JSR, func.text))
                self.getsym()
            else:
                self.error(Error.GA_MISS_R_PARENTHESIS)
                self.overlookToMarks(overlookSet)
        else:
            self.error(Error.GA_MISS_L_PARENTHESIS, self.pointer.previous)
            self.overlookToMarks(overlookSet)
        # 函数调用语句结束记得给下一条语句加上标记
        self.instructionStream.setLab('ret_addr')
        return V_sentenceFunctionCall
    # 赋值语句
    # <赋值语句>::=  <标识符>＝<表达式>
    def analyze_sentenceAssign(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = overlookSet[:]
        V_sentenceAssign = VN.create(const.SENTENCE_ASSIGN)
        symbolItem = self.symbolTable.getItem(self.pointer.text)
        if symbolItem:
            V_sentenceAssign.append(self.pointer)
            if symbolItem.isInt() or symbolItem.isParameter():
                # 此处是标识符，生成LDA指令
                self.emit(Instruction(Instruction.LDA, symbolItem.name))
                self.getsym()
            else:
                # 这里的给常量赋值错误虽然报错，但是仍然要读取下一个符号并继续分析，
                # 仅仅不再插入指令
                self.error(Error.ST_ASSIGN_CONST)
                self.getsym()
        else:
            self.error(Error.ST_UNDEFINED_ID)
            self.overlookToMarks(overlookSet)
        if self.pointer.isAssign():
            V_sentenceAssign.append(self.pointer)
            self.getsym()
            V_sentenceAssign.append(self.analyze_expression(overlookSet))
            # 表达式识别结束之后将赋值指令入栈
            self.emit(Instruction(Instruction.STN))
        else:
            self.error(Error.GA_MISS_ASSIGN)
            self.overlookToMarks(overlookSet)
        return V_sentenceAssign
    # 返回语句
    # <返回语句>::=  return [ '('<表达式>')' ]
    def analyze_sentenceReturn(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.R_PARENTHESIS)
        V_sentenceReturn = VN.create(const.SENTENCE_RETURN)
        V_sentenceReturn.append(self.pointer)
        self.getsym()
        if self.pointer.isL_Parenthesis():
            V_sentenceReturn.append(self.pointer)
            self.getsym()
            V_sentenceReturn.append(self.analyze_expression(downOverlookSet))
            if self.pointer.isR_Parenthesis():
                V_sentenceReturn.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_R_PARENTHESIS)
                self.overlookToMarks(overlookSet)
        # 也可能是直接返回一个语句
        elif not self.pointer.isSemicolon():
            V_sentenceReturn.append(self.analyze_expression(downOverlookSet))
        self.run_sentenceReturn()
        return V_sentenceReturn
    # 读语句
    # <读语句>::=  scanf'('<标识符>'）'
    def analyze_sentenceScanf(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.R_PARENTHESIS)
        V_sentenceScanf = VN.create(const.SENTENCE_SCANF)
        V_sentenceScanf.append(self.pointer)
        self.getsym()
        if self.pointer.isL_Parenthesis():
            V_sentenceScanf.append(self.pointer)
            self.getsym()
            if self.pointer.isID():
                id = self.pointer
                symbol = self.symbolTable.getItem(id.text)
                if not symbol:
                    self.error(Error.ST_UNDEFINED_ID)
                # 找到标识符，先加载
                else:
                    self.emit(Instruction(Instruction.LDA, id.text))
                V_sentenceScanf.append(self.pointer)
                self.getsym()
                if self.pointer.isR_Parenthesis():
                    V_sentenceScanf.append(self.pointer)
                    self.getsym()
                    # 添加赋值指令
                    self.emit(Instruction(Instruction.JSR, 'SCANF'))
                    self.instructionStream.setLab('ret_addr')
                else:
                    self.error(Error.GA_MISS_R_PARENTHESIS, self.pointer.previous)
                    self.overlookToMarks(overlookSet)
            else :
                self.error(Error.GA_MISS_IDENTIFIER)
                self.overlookToMarks(overlookSet)
        else :
            self.error(Error.GA_MISS_L_PARENTHESIS, self.pointer.previous)
            self.overlookToMarks(overlookSet)
        return V_sentenceScanf
    # 写语句
    # <写语句>::=  printf'('[<字符串>,][<expression >]'）'
    def analyze_sentencePrintf(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.R_PARENTHESIS)
        V_sentencePrintf = VN.create(const.SENTENCE_PRINTF)
        V_sentencePrintf.append(self.pointer)
        self.getsym()
        if self.pointer.isL_Parenthesis():
            V_sentencePrintf.append(self.pointer)
            self.getsym()
            if self.pointer.isString():
                self.emit(Instruction(Instruction.LOD, '"'+ self.pointer.text + '"'))
                V_sentencePrintf.append(self.pointer)
                self.getsym()
                if self.pointer.isComma():
                    V_sentencePrintf.append(self.pointer)
                    self.getsym()
                # 这里虽然没有逗号，但是为了后面的表达式，不要用overlook函数！
                elif not self.pointer.isR_Parenthesis() :
                    self.error(Error.GA_MISS_COMMA, self.pointer.previous)
            # 如果字符串后面不是有括号，那就解析表达式
            if not self.pointer.isR_Parenthesis():
                V_sentencePrintf.append(self.analyze_expression(downOverlookSet))
            if self.pointer.isR_Parenthesis():
                V_sentencePrintf.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_R_PARENTHESIS, self.pointer.previous)
                self.overlookToMarks(overlookSet)
        else :
            self.error(Error.GA_MISS_L_PARENTHESIS, self.pointer.previous)
            self.overlookToMarks(overlookSet)
        # 两部分都加载完成后调用printf函数
        self.emit(Instruction(Instruction.JSR, 'PRINTF'))
        self.instructionStream.setLab('ret_addr')
        return V_sentencePrintf
    # 语句
    # <语句>::=<条件语句>｜<循环语句>｜'{'<语句序列>'}'｜<函数调用语句>;｜<赋值语句>; | <返回语句>;｜<读语句>;｜<写语句>;｜<空>
    def analyze_sentence(self, overlookSet = [const.R_BRACE]):
        sentenceListOverlookSet = []
        self.overlookSetAdd(sentenceListOverlookSet, const.R_BRACE)
        self.overlookSetAdd(sentenceListOverlookSet, const.CONST)
        self.overlookSetAdd(sentenceListOverlookSet, const.INT)
        sentenceOverlookSet = [const.R_BRACE]
        self.overlookSetAdd(sentenceOverlookSet, const.SEMICOLON)
        V_sentence = VN.create(const.SENTENCE)
        if self.pointer.isR_If():
            V_sentence.append(self.analyze_sentenceIf(overlookSet))
        elif self.pointer.isR_While():
            V_sentence.append(self.analyze_sentenceWhile(overlookSet))
        # 如果是{，就是处理语句序列
        elif self.pointer.isL_Brace():
            V_sentence.append(self.pointer)
            self.getsym()
            V_sentence.append(self.analyze_sentenceList(sentenceListOverlookSet))
            if self.pointer.isR_Brace():
                V_sentence.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_R_BRACE, self.pointer.previous)
                self.overlookToMarks(overlookSet)
        elif self.pointer.isR_Return():
            V_sentence.append(self.analyze_sentenceReturn(sentenceOverlookSet))
            if self.pointer.isSemicolon():
                V_sentence.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_SEMICOLON, self.pointer.previous)
                self.overlookToMarks(overlookSet)
        elif self.pointer.isR_Scanf():
            V_sentence.append(self.analyze_sentenceScanf(sentenceOverlookSet))
            if self.pointer.isSemicolon():
                V_sentence.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_SEMICOLON, self.pointer.previous)
                self.overlookToMarks(overlookSet)
        elif self.pointer.isR_Printf():
            V_sentence.append(self.analyze_sentencePrintf(sentenceOverlookSet))
            if self.pointer.isSemicolon():
                V_sentence.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_SEMICOLON, self.pointer.previous)
                self.overlookToMarks(overlookSet)
        # 读到标识符，可能是函数调用或者赋值语句，
        elif self.pointer.isID() and self.pointer.next.isAssign():
            V_sentence.append(self.analyze_sentenceAssign(sentenceOverlookSet))
            if self.pointer.isSemicolon():
                V_sentence.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_SEMICOLON, self.pointer.previous)
                self.overlookToMarks(overlookSet)
        elif self.pointer.isID() and self.pointer.next.isL_Parenthesis():
            V_sentence.append(self.analyze_sentenceFunctionCall(sentenceOverlookSet))
            if self.pointer.isSemicolon():
                V_sentence.append(self.pointer)
                self.getsym()
            else:
                self.error(Error.GA_MISS_SEMICOLON, self.pointer.previous)
                self.overlookToMarks(overlookSet)
        # 全都不是，但是是个id，报错
        elif self.pointer.isID():
            self.getsym()
            self.error(Error.GA_ILLEGAL_INPUT)
            self.overlookToMarks(overlookSet)
        return self.checkEmpty(V_sentence)
    # 语句序列
    # <语句序列>::=  <语句>｛<语句>｝
    def analyze_sentenceList(self, overlookSet = [const.R_BRACE]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.IF) #条件语句
        self.overlookSetAdd(downOverlookSet, const.WHILE) #循环语句
        self.overlookSetAdd(downOverlookSet, const.RETURN) #返回语句
        self.overlookSetAdd(downOverlookSet, const.L_BRACE) #语句序列
        self.overlookSetAdd(downOverlookSet, const.SCANF)
        self.overlookSetAdd(downOverlookSet, const.PRINTF)

        V_sentenceList = VN.create(const.SENTENCE_LIST)
        # 对于是语句First集的单词，统统继续叠加语句
        while self.pointer.isID() or self.pointer.isR_If() \
            or self.pointer.isR_While() or self.pointer.isR_Return() \
            or self.pointer.isL_Brace() or self.pointer.isR_Scanf() \
            or self.pointer.isR_Printf():
            V_sentenceList.append(self.analyze_sentence(downOverlookSet))
        return self.checkEmpty(V_sentenceList)
    # 复合语句
    # <复合语句>::=  '{'(<常量说明部分>)(<变量说明部分>)<语句序列>'}'
    def analyze_conpoundStatement(self, overlookSet = [const.INT, const.CONST, const.ID]):
        downOverlookSet = [const.R_BRACE]
        selfOverlookSet = [const.R_BRACE]
        self.overlookSetAdd(downOverlookSet, const.R_BRACE)
        self.overlookSetAdd(downOverlookSet, const.INT) #处理变量定义
        self.overlookSetAdd(downOverlookSet, const.CONST) #常量定义
        self.overlookSetAdd(downOverlookSet, const.IF) #条件语句
        self.overlookSetAdd(downOverlookSet, const.WHILE) #循环语句
        self.overlookSetAdd(downOverlookSet, const.RETURN) #返回语句
        self.overlookSetAdd(downOverlookSet, const.L_BRACE) #语句序列
        self.overlookSetAdd(downOverlookSet, const.SCANF)
        self.overlookSetAdd(downOverlookSet, const.PRINTF)
        # 进入则表示已经识别{,直接添加
        V_conpoundStatement = VN.create(const.CONPOUND_STATEMENT)
        V_conpoundStatement.append(self.pointer)
        self.getsym()
        # 没有到函数末尾的}时，一直循环
        while not self.pointer.isR_Brace():
            # 如果读到Const,则是常量说明，
            if self.pointer.isR_Const():
                V_conpoundStatement.append(self.analyze_constIllustrate(downOverlookSet))
            # 读到int，则是变量说明
            elif self.pointer.isR_Int():
                V_conpoundStatement.append(self.analyze_varIllustrate(downOverlookSet))
            # 否则就只能是语句序列了，整！
            elif self.pointer.isID() or self.pointer.isL_Brace() \
                or self.pointer.isR_If() or self.pointer.isR_While() \
                or self.pointer.isR_Return() or self.pointer.isR_Printf() \
                or self.pointer.isR_Scanf():
                V_conpoundStatement.append(self.analyze_sentenceList(downOverlookSet))
            else:
                self.error(Error.GA_ILLEGAL_INPUT)
                self.overlookToMarks(selfOverlookSet)
                break
        # 复合语句的最后，因该是一个}，无则报错
        if self.pointer.isR_Brace():
            V_conpoundStatement.append(self.pointer)
            self.getsym()
        else:
            self.error(Error.GA_MISS_R_BRACE, self.pointer.previous)
            self.overlookToMarks(overlookSet)
        return V_conpoundStatement
    # 函数定义部分
    # <函数定义部分>::=  （<声明头部>｜void <标识符>）<参数><复合语句>
    def analyze_functionDefine(self, overlookSet = [const.CONST, const.INT, const.VOID]):
        downOverlookSet = overlookSet[:]
        self.overlookSetAdd(downOverlookSet, const.INT)
        isMain = False
        # 判断是不是主函数
        if self.pointer.next.isR_Main():
            V_functionDefine = VN.create(const.MAIN_FUNCTION)
            isMain = True
        else:
            V_functionDefine = VN.create(const.FUNCTION_DEFINE)
        if self.pointer.isR_Int() and (not isMain):
            declareHead = self.analyze_declareHead()
            V_functionDefine.append(declareHead)
            id = declareHead.findChild(const.ID)
        elif self.pointer.isR_Int() and isMain:
            V_functionDefine.append(self.pointer)
            self.getsym()
            id = self.pointer
            V_functionDefine.append(self.pointer)
            self.getsym()
        # 不是int，那就是void型咯！
        elif self.pointer.isR_Void():
            void = self.pointer
            self.getsym()
            # 还需要再来一个标识符!
            if self.pointer.isID() or self.pointer.isR_Main():
                V_functionDefine.append(void)
                id = self.pointer
                V_functionDefine.append(self.pointer)
                self.getsym()
            # 标识符都没有，直接回上层
            else:
                self.error(Error.GA_MISS_IDENTIFIER)
                self.overlookToMarks(overlookSet)
                return V_functionDefine.empty()
        # 都不是，那就报"不认识"
        else:
            self.error(Error.GA_ILLEGAL_TYPE)
            self.overlookToMarks(overlookSet)
            return V_functionDefine.empty()
        # 接着是参数解析
        # 参数解析前加上函数名的 lab 标识，表示函数入口！
        self.instructionStream.setLab(id.text)
        if self.pointer.isL_Parenthesis():
            V_functionDefine.append(self.analyze_parameter())
        else:
            self.error(Error.GA_MISS_L_PARENTHESIS, self.pointer.previous)
            self.overlookToMarks([const.L_BRACE])
        # 头部定义结束，run一次
        self.run_functionDefine(V_functionDefine)
        # 然后是复合语句解析
        if self.pointer.isL_Brace():
            V_functionDefine.append(self.analyze_conpoundStatement())
        else:
            self.error(Error.GA_MISS_L_BRACE, self.pointer.previous)
            self.overlookToMarks(overlookSet)
        # self.emit(Instruction(Instruction.RET))
        self.run_functionDefineEnd(V_functionDefine)
        return V_functionDefine
    # 语义分析
    # <常量说明部分>
    def run_constIllustration(self, Vn):
        if self.hasError() or Vn.isEmpty():
            return
        for child in Vn.children:
            if child.isType(const.CONST_DEFINE):
                name = child.findChild(const.ID).text
                value = child.findChild(const.INTEGER).text
                no = self.symbolTable.addItem(name, value, SymbolTableItem.TYPE_CONST)
                if no == -1:
                    self.error(Error.ST_REPEATED_ID, child.findChild(const.ID))
    # 语义分析
    # <变量说明部分>
    def run_varIllustrate(self, Vn):
        if self.hasError() or Vn.isEmpty():
            return
        for child in Vn.children:
            if child.isType(const.DECLARE_HEAD):
                id = child.findChild(const.ID)
                name = id.text
            elif child.isType(const.ID) :
                id = child
                name = id.text
            else :
                continue
            no = self.symbolTable.addItem(name, None, SymbolTableItem.TYPE_INT)
            if no == -1:
                self.error(Error.ST_REPEATED_ID, id)
    # 语义分析
    # <函数定义部分>
    def run_functionDefine(self, Vn):
        if self.hasError() or Vn.isEmpty():
            return
        if Vn.isType(const.MAIN_FUNCTION):
            if Vn.hasChild(const.VOID):
                returnValue = SymbolTableItem.TYPE_VOID
            else:
                returnValue = SymbolTableItem.TYPE_INT
            id = Vn.findChild(const.MAIN)
        elif Vn.hasChild(const.VOID):
            returnValue = SymbolTableItem.TYPE_VOID
            id = Vn.findChild(const.ID)
        else :
            returnValue = SymbolTableItem.TYPE_INT
            id = Vn.findChild(const.DECLARE_HEAD).findChild(const.ID)
        no = self.symbolTable.addItem(id.text, None, SymbolTableItem.TYPE_FUNCTION, returnValue)
        if no == -1:
            self.error(Error.ST_REPEATED_ID, id)
            return
        else:
            self.symbolTable.addIndex(id.text)
        # 函数开始处指令
        self.emit(Instruction(Instruction.ALC, 0))
        # 第一条指令已经确定地址，将地址传回符号表
        self.symbolTable.table[no].addr = self.instructionStream.no
        self.emit(Instruction(Instruction.STO, 'ret_addr'))
        # 如果有参数表，记得加入参数到符号表中
        parameter = Vn.findChild(const.PARAMETER)
        if parameter.hasChild(const.PARAMETER_LIST):
            parameterList = parameter.findChild(const.PARAMETER_LIST)
            ids = parameterList.findChildren(const.ID)
            # 设置函数符号的变量个数
            self.symbolTable.table[no].paraNum = len(ids)
            for id in ids:
                self.symbolTable.addItem(id.text, None, SymbolTableItem.TYPE_PARAMETER)
                self.emit(Instruction(Instruction.STO, id.text))
        else:
            return
    # 语义分析
    # 函数定义结束后的符号表收尾动作
    def run_functionDefineEnd(self, Vn):
        if self.hasError() or Vn.isEmpty():
            return
        if Vn.isType(const.MAIN_FUNCTION):
            id = Vn.findChild(const.MAIN)
        elif Vn.hasChild(const.VOID):
            id = Vn.findChild(const.ID)
        else :
            id = Vn.findChild(const.DECLARE_HEAD).findChild(const.ID)
        if Vn.findChild(const.VOID):
            returnValue = const.VOID
        else:
            returnValue = const.INT
        # 收起函数内符号
        self.symbolTable.collapseToFunction(id.text)
        # 修改函数头部 ALC 指令的分配空间大小
        funcItem = self.symbolTable.getItem(id.text)
        allocateInstru = self.instructionStream.instructions[funcItem.addr]
        allocateInstru.operator = funcItem.space
        # 检查是否有非法 return 指令
        if returnValue == const.VOID:
            rets = Vn.findGrandChildren(const.SENTENCE_RETURN)
            for ret in rets:
                if ret.hasChild(const.EXPRESSION):
                    self.error(Error.ST_ILLEGAL_RETURN, ret.findChild(const.RETURN))
        # 为没有 ret 指令的函数加入ret指令
        sentencelist = Vn.findChild(const.CONPOUND_STATEMENT).findChild(const.SENTENCE_LIST)
        if sentencelist is None:
            self.run_sentenceReturn()
        else:
            sentences = sentencelist.findChildren(const.SENTENCE)
            ret = False
            for sentence in sentences:
                if not sentence.findChild(const.SENTENCE_RETURN) is None:
                    ret = True
                    break
            if not ret:
                self.run_sentenceReturn()
    # 语义分析
    # <返回语句>结束后的语义分析
    def run_sentenceReturn(self):
        if self.hasError():
            return
        self.emit(Instruction(Instruction.LOD, "ret_addr"))
        self.emit(Instruction(Instruction.BR, "ret_addr"))
    # 错误处理函数
    def error(self,errorNo = Error.GA_UNDEFINED, Vt = None, msg = ''):
        if Vt is None:
            Vt  = self.pointer
        err = Error(self.file, errorNo, Vt.line, msg, Vt.wordNo)
        self.errors.append(err)
        return
    def printAllVn(self):
        self.printVn(self.program)
    def printVn(self, V):
        if isinstance(V, VN):
            print('Vn.Type:' + V.msg() + '')
            for child in V.children:
                self.printVn(child)
        else:
            print('Vt.No' + str(V.vtype) + ' Text:' + V.msg() )