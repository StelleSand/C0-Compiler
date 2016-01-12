#定义所有常量
class ConstDefine:
    # 运算符定义
    EQ = 1
    LE = 2
    LT = 3
    GE = 4
    GT = 5
    NE = 6
    PLUS = 7
    MINUS = 8
    STAR = 9
    SLASH = 10
    B_SLASH = 11
    # 数据类型定义
    CHAR = 12
    DIGIT = 13
    STRING = 14
    INTEGER = 15 #注意与int区别
    #保留字定义
    IF = 21
    ELSE = 22
    WHILE = 23
    CONST = 24
    INT = 25
    VOID = 26
    MAIN = 27
    RETURN = 28
    PRINTF = 29
    SCANF = 30
    #特殊符号定义
    L_PARENTHESIS = 41
    R_PARENTHESIS = 42
    L_BRACKET = 43
    R_BRACKET = 44
    L_BRACE = 45
    R_BRACE = 46
    COMMA = 47 # 逗号
    SEMICOLON = 48 # 分号
    ASSIGN = 49
    EXCLAMATION = 50
    COLON = 51
    S_QUATATION = 52
    D_QUATATION = 53
    EOF = 54
    #标识符类型定义
    ID = 61
    RESERVE = 62
    ANNOTATION = 63
    #Vn类型定义
    EMPTY = 100
    PROGRAM = 101 # <程序>
    CONST_ILLUSTRATE = 102 # <常量说明部分>
    CONST_DEFINE = 103 # <常量定义>
    DECLARE_HEAD = 104 # <声明头部>
    VAR_ILLUSTRATE = 105 # <变量说明部分>
    FUNCTION_DEFINE = 106 # <函数定义部分>
    CONPOUND_STATEMENT = 107 # <复合语句>
    PARAMETER = 108 # <参数>
    PARAMETER_LIST = 109 # <参数表>
    MAIN_FUNCTION = 110 # <主函数>
    EXPRESSION = 111 # <表达式>
    TERM = 112 # <项>
    FACTOR = 113 # <因子>
    SENTENCE = 114 # <语句>
    SENTENCE_ASSIGN = 115 # <赋值语句>
    SENTENCE_CONDITION = 116 # <条件语句>
    SENTENCE_LOOP = 117 # <循环语句>
    SENTENCE_FUNCTION_CALL = 118 # <函数调用语句>
    SENTENCE_SCANF = 119 # <读语句>
    SENTENCE_PRINTF = 120 # <写语句>
    SENTENCE_RETURN = 121 # <返回语句>
    SENTENCE_LIST = 122 # <语句序列>
    CONDITION = 123 # <条件>
    VALUE_PARAMETER_LIST = 124 # <值参数表>


const = ConstDefine

reservers = {
    'const':const.CONST,
    'int':const.INT,
    'void':const.VOID,
    'if':const.IF,
    'else':const.ELSE,
    'while':const.WHILE,
    'main':const.MAIN,
    'return':const.RETURN,
    'printf':const.PRINTF,
    'scanf':const.SCANF
}


# 定义V类型，作为终结符和非终结符的基类
class  V:
    def __init__(self, vtype):
        # V类型
        self.vtype = vtype
    # 判断当前实例是否是指定类型
    def isType(self, vtype):
        return self.vtype == vtype
    def isEmpty(self):
        return self.vtype == const.EMPTY
    def isVT(self):
        return self.vtype < 100
    def isVN(self):
        return self.vtype >= 100
    # 判断当前单词是否是<加法运算符>
    def isPlusOperator(self):
        return self.vtype == const.PLUS or self.vtype == const.MINUS
    # 判断当前单词是否是<乘法运算符>
    def isStarOperator(self):
        return self.vtype == const.STAR or self.vtype == const.SLASH
    # 判断当前单词是否是<关系运算符>
    def isRelationOperator(self):
        return self.vtype == const.LT or self.vtype == const.LE \
               or self.vtype == const.GT or self.vtype == const.GE \
               or self.vtype == const.NE or self.vtype == const.EQ
    # 判断当前单词是否是<（>
    def isL_Parenthesis(self):
        return self.vtype == const.L_PARENTHESIS
    # 判断当前单词是否是<)>
    def isR_Parenthesis(self):
        return self.vtype == const.R_PARENTHESIS
    # 判断当前单词是否是<{>
    def isL_Brace(self):
        return self.vtype == const.L_BRACE
    # 判断当前单词是否是<}>
    def isR_Brace(self):
        return self.vtype == const.R_BRACE
    # 判断当前单词是否是<,> 逗号
    def isComma(self):
        return self.vtype == const.COMMA
    # 判断当前单词是否是<;> 分号
    def isSemicolon(self):
        return self.vtype == const.SEMICOLON
    # 判断当前单词是否是<=> 等号
    def isAssign(self):
        return self.vtype == const.ASSIGN
    # 判断当前单词是否是<字符串>
    def isString(self):
        return self.vtype == const.STRING
    # 判断当前单词是否是<整数>
    def isInteger(self):
        return self.vtype == const.INTEGER
    # 判断当前单词是否是 EOF
    def isEOF(self):
        return self.vtype == const.EOF
    # 判断当前单词是否是<标识符>
    def isID(self):
        return self.vtype == const.ID
    # 判断当前单词是否是保留字
    def isReserve(self):
        return self.vtype >= 20 and self.vtype < 40
    # 判断当前单词是否是保留字<const>
    def isR_Const(self):
        return self.vtype == const.CONST
    # 判断当前单词是否是保留字<int>
    def isR_Int(self):
        return self.vtype == const.INT
    # 判断当前单词是否是保留字<void>
    def isR_Void(self):
        return self.vtype == const.VOID
    # 判断当前单词是否是保留字<if>
    def isR_If(self):
        return self.vtype == const.IF
    # 判断当前单词是否是保留字<else>
    def isR_Else(self):
        return self.vtype == const.ELSE
    # 判断当前单词是否是保留字<while>
    def isR_While(self):
        return self.vtype == const.WHILE
    # 判断当前单词是否是保留字<main>
    def isR_Main(self):
        return self.vtype == const.MAIN
    # 判断当前单词是否是保留字<return>
    def isR_Return(self):
        return self.vtype == const.RETURN
    # 判断当前单词是否是保留字<printf>
    def isR_Printf(self):
        return self.vtype == const.PRINTF
    # 判断当前单词是否是保留字<scanf>
    def isR_Scanf(self):
        return self.vtype == const.SCANF


# 定义VT类型，指代终结符
class VT(V):
    def __init__(self, vtype, line, text, wordNo = 0):
        V.__init__(self,vtype)
        # 终结符链表的next指针
        self.next = None
        # 终结符链表的previous指针
        self.previous = None
        # 终结符的文字，为其值的字符串形式
        self.text = text
        # 终结符所在的行数
        self.line = line
        # 终结符在一行中所处的次序
        self.wordNo = wordNo
    def printMsg(self):
        print('Vt Msg: In line ' + str(self.line) + " at " + str(self.wordNo) + ", Vt type " + str(self.vtype) + ", text is " + self.text)
    def printFormula(self):
        print(self.text, end='')
    def msg(self):
        return self.text


# 定义VN类型，指代非终结符
class VN(V):
    FORMULA = {
            const.EMPTY : "<空>",
            const.PROGRAM : "<程序>",
            const.CONST_ILLUSTRATE : "<常量说明部分>",
            const.CONST_DEFINE : "<常量定义>",
            const.DECLARE_HEAD : "<声明头部>",
            const.VAR_ILLUSTRATE : "<变量说明部分>",
            const.FUNCTION_DEFINE : "<函数定义部分>",
            const.CONPOUND_STATEMENT : "<复合语句>",
            const.PARAMETER : "<参数>",
            const.PARAMETER_LIST : "<参数表>",
            const.MAIN_FUNCTION : "<主函数>",
            const.EXPRESSION : "<表达式>",
            const.TERM : "<项>",
            const.FACTOR : "<因子>",
            const.SENTENCE : "<语句>",
            const.SENTENCE_ASSIGN : "<赋值语句>",
            const.SENTENCE_CONDITION : "<条件语句>",
            const.SENTENCE_LOOP : "<循环语句>",
            const.SENTENCE_FUNCTION_CALL : "<函数调用语句>",
            const.SENTENCE_SCANF : "<读语句>",
            const.SENTENCE_PRINTF : "<写语句>",
            const.SENTENCE_RETURN : "<返回语句>",
            const.SENTENCE_LIST : "<语句序列>",
            const.CONDITION : "<条件>",
            const.VALUE_PARAMETER_LIST : "<值参数表>",
    }
    def __init__(self, vtype):
        V.__init__(self,vtype)
        # Vn的子节点数组
        self.children = []
    def empty(self):
        self.children = []
        self.vtype = const.EMPTY
        return self
    def hasVn(self):
        for child in self.children:
            if isinstance(child, VN):
                return True
        return False
    def append(self, child, forceAppend = False):
        # 传进来的child 必须是V
        assert isinstance(child, V)
        if forceAppend == True or (not self.isEmpty()):
            self.children.append(child)
        else:
            print('Warning: Trying to add child into an empty Vn!')
        return self
    def printFormula(self):
        print(self.msg(), end='')
    def printChildren(self):
        print(self.msg())
        for child in self.children:
            print("vtype.%-3d%-10s"%(child.vtype, child.msg()))
    def findChild(self, childType):
        for child in self.children:
            if child.vtype == childType:
                return child
        return None
    # 搜索子节点树，找到指定类型的所有子孙节点
    def findGrandChildren(self, childType):
        children = []
        for child in self.children:
            if child.vtype == childType:
                children.append(child)
            elif isinstance(child, VN):
                children += child.findGrandChildren(childType)
        return children
    def findChildren(self, childType):
        result = []
        for child in self.children:
            if child.vtype == childType:
                result.append(child)
        return result
    def hasChild(self, childType):
        return not self.findChild(childType) == None
    def msg(self):
        return VN.FORMULA[self.vtype]
    @staticmethod
    # 返回一个创建的空Vn对象
    def create(vtype):
        return VN(vtype)



# 数据块类，用来管理变量常量的地址空间
class DataBlock():
    def __init__(self):
        # 数据区的栈用来分配空间给变量
        # 静态栈栈底
        self.bp = 0
        # 静态栈指针, 初始化时等于栈底
        self.sp = self.bp
        # 堆指针
        self.np = 8192
    # 栈分配空间函数，参数为需要分配的字节数,默认为4
    # 返回值为分配的地址
    def stackAllocation(self, bytes = 4):
        self.sp += bytes
        return self.sp - 4
    # 堆分配空间函数，参数为需要分配的字节数,默认为4
    # 返回值为分配的地址
    def heapAllocation(self, bytes = 4):
        self.np -= bytes
        return self.np


dataBlock = DataBlock()


class Instruction():
    LOD = 1 # 加载指令, 对象为D，将D中内容加载到操作数栈
    LOC = 2 # 立即加载指令，将常量入栈
    LDA = 3 # 地址加载，将变量地址入栈
    STO = 4 # 存储指令，将栈顶内容存入D
    ST = 5  # 间接存储指令，将栈顶内容存入D所指单元
    STN = 6 # 间接存储指令，将栈顶内容存入次栈顶所指单元
    ADD = 7 # 栈顶和次栈顶相加，结果留栈顶
    SUB = 8 # 次栈顶内容减栈顶内容，差留栈顶
    MUL = 9 # 次栈顶内容乘栈顶内容，积留栈顶
    DIV = 10 # 次栈顶内容除以栈顶内容，商留栈顶
    EQL = 20 # 相等 次栈顶与栈顶内容比较，结果(1或0)留栈顶
    NEQ = 21 # 不等
    GRT = 22 # 大于
    LES = 23 # 小于
    GTE = 24 # 大于等于
    LSE = 25 # 小于等于
    AND = 30 # 逻辑 与
    ORL = 31 # 逻辑 或
    NOT = 32 # 逻辑 非

    BR  = 41 # 无条件转移到lab
    BRF = 42 # 检查栈顶单元逻辑值，若为假（0）则转移到lab
    JSR = 43 # 控制转到被调用过程入口lab，并将返回地址（JSR的下一条指令地址）放入操作数栈
    RET = 51 # 返回语句
    ALC = 52 # 在运行栈上为调用过程分配一大小为M的活动记录区
    Msg = {
            LOD : 'LOD ',
            LOC : 'LOD ',
            LDA : 'LDA ',
            STO : "STO ",
            ST  : "ST ",
            STN : "STN ",
            ADD : "ADD ",
            SUB : "SUB ",
            MUL : "MUL ",
            DIV : "DIV ",
            EQL : "EQL ",
            NEQ : "NEQ ",
            GRT : "GRT ",
            LES : "LES ",
            GTE : "GTE ",
            LSE : "LSE ",
            AND : "AND ",
            ORL : "ORL ",
            NOT : "NOT ",
            BR  : "BR  ",
            BRF : "BRF ",
            JSR : "JSR ",
            RET : 'RET ',
            ALC : 'ALC ',
    }

    labNo = 0
    def __init__(self, instruction, operator = None, lab = []):
        self.instruction = instruction
        if isinstance(operator, int):
            self.operator = str(operator)
        else:
            self.operator = operator
        self.lab = lab
    def printMsg(self):
        print(Instruction.Msg[self.instruction],end='')
        if (not self.operator is None) and self.instruction != Instruction.LDA:
            print(self.operator)
        elif (not self.operator is None) and self.instruction == Instruction.LDA:
            print('(' + self.operator + ')')
        else :
            print('')
    def msg(self):
        if (not self.operator is None) and self.instruction != Instruction.LDA:
            op = self.operator
        elif (not self.operator is None) and self.instruction == Instruction.LDA:
            op = '(' + self.operator + ')'
        else :
            op = ''
        lab = ''
        if len(self.lab) > 0 :
            for i in self.lab:
                lab += i + ':'
        return [lab, Instruction.Msg[self.instruction], op]
    @staticmethod
    def generateLab():
        Instruction.labNo += 1
        return 'lab_' + str(Instruction.labNo)
    def create(Vt):
        if not Vt:
            return False
        elif Vt.isType(const.PLUS):
            return Instruction(Instruction.ADD)
        elif Vt.isType(const.MINUS):
            return Instruction(Instruction.SUB)
        elif Vt.isType(const.STAR):
            return Instruction(Instruction.MUL)
        elif Vt.isType(const.SLASH):
            return Instruction(Instruction.DIV)
        elif Vt.isType(const.EQ):
            return Instruction(Instruction.EQL)
        elif Vt.isType(const.NE):
            return Instruction(Instruction.NEQ)
        elif Vt.isType(const.GT):
            return Instruction(Instruction.GRT)
        elif Vt.isType(const.LT):
            return Instruction(Instruction.LES)
        elif Vt.isType(const.GE):
            return Instruction(Instruction.GTE)
        elif Vt.isType(const.LE):
            return Instruction(Instruction.LSE)
        else:
            return False


# 指令流类，用来存放最终生成的指令流
class InstructionStream():
    def __init__(self):
        self.instructions = []
        self.no = -1
        self.lab = []
    def setLab(self, lab):
        self.lab.append(lab)
    def append(self, instruction):
        assert isinstance(instruction, Instruction)
        self.no += 1
        instruction.lab = self.lab
        self.lab = []
        self.instructions.append(instruction)
    def printAllInstructions(self):
        print('P-Code Instructions for this program are followed as :')
        print('%-5s%-20s%-12s%-10s'%('No.','Lab.','Instruction','Operator.'))
        no = 0
        for instruction in self.instructions:
            arr = tuple([no]+ instruction.msg())
            print("%-5d%-20s%-12s%-10s"%arr)
            # instruction.printMsg()
            no += 1
    def fileOutAllInstructions(self, file):
        file.write('%-5s%-20s%-12s%-10s'%('No.','Lab.','Instruction','Operator.\n'))
        no = 0
        for instruction in self.instructions:
            arr = tuple([no]+ instruction.msg())
            file.write("%-5d%-20s%-12s%-10s\n"%arr)
            no += 1



class SymbolTableIndex:
    def __init__(self, name, level, itemNo):
        self.name = name
        self.level = level
        self.itemNo = itemNo


class SymbolTableItem:
    TYPE_CONST = 1
    TYPE_INT = 2
    TYPE_FUNCTION = 3
    TYPE_PARAMETER = 4
    TYPE_VOID = 5
    TYPE_STRING = 6
    String = {
        TYPE_CONST:"Const",
        TYPE_INT:"Int",
        TYPE_FUNCTION:"Function",
        TYPE_PARAMETER:"Parameter",
        TYPE_VOID:"Void",
        TYPE_STRING:"String",
    }

    def __init__(self, name, value, level, itemType, no, returnValue = None, paraNum = 0, space = 0):
        self.name = name
        # value对于普通变量就是值，对于函数指针就是代码段下标，
        self.value = value
        self.level = level
        self.itemType = itemType
        self.no = no
        # 函数类型需要的参数数量
        self.paraNum = paraNum
        # 函数类型需要的定长空间
        self.space = space
        # returnType对于普通变量等于itemType,对于函数变量等于返回值类型
        if self.itemType != SymbolTableItem.TYPE_FUNCTION:
            self.returnType = itemType
        else:
            self.returnType = returnValue
        # 为变量分配地址
        self.allocation()
    def allocation(self):
        if self.itemType == SymbolTableItem.TYPE_CONST:
            self.addr = hex(dataBlock.heapAllocation())
        elif self.itemType == SymbolTableItem.TYPE_INT:
            self.addr = hex(dataBlock.stackAllocation())
        elif self.itemType == SymbolTableItem.TYPE_FUNCTION:
            self.addr = 0
        elif self.itemType == SymbolTableItem.TYPE_PARAMETER:
            self.addr = 0
    def isConst(self):
        return self.itemType == SymbolTableItem.TYPE_CONST
    def isInt(self):
        return self.itemType == SymbolTableItem.TYPE_INT
    def isParameter(self):
        return self.itemType == SymbolTableItem.TYPE_PARAMETER
    def isFunction(self):
        return self.itemType == SymbolTableItem.TYPE_FUNCTION
    def setValue(self, value):
        self.value = value


class SymbolTable():
    def __init__(self):
        self.level = 0
        self.index = []
        self.table = []
        self.no = -1
        # 加入“program”索引
        self.index.append(SymbolTableIndex('program', self.level, 0))
    def addIndex(self, name):
        self.level += 1
        self.index.append(SymbolTableIndex(name, self.level, self.no + 1))
    def addItem(self, name, value, itemType, returnValue = None):
        aSameItem = self.getItem(name)
        # 如果未找到同层变量，定义！
        if aSameItem is None or aSameItem.level != self.level:
            self.no += 1
            self.table.append(SymbolTableItem(name, value, self.level, itemType, self.no, returnValue))
            return self.no
        # 否则即为找到同层定义，返回-1报错！
        elif aSameItem.level == self.level:
            return -1
    def getItem(self, name):
        present = self.no
        while present >= 0:
            if self.table[present].name == name:
                return self.table[present]
            present -= 1
        return None
    # 收起指定函数下的符号，同时设置函数项 space 字段，此后level - 1
    # 同时index弹出一项
    def collapseToFunction(self, funcName):
        funcItem = self.getItem(funcName)
        if not funcItem.isFunction():
            return
        start = funcItem.no
        for i in range(0, self.no - start):
            self.table.pop()
        # 设置space字段，因为有返回地址，所以要 + 1
        funcItem.space = self.no - start + 1;
        self.no = start
        self.level -= 1
        self.index.pop()
    def printTable(self):
        print("Index%5sNo.%3sName.%10sValue.%10sKind.%10sLevel.%5sAddr.%5s"%('','','','','','',''))
        j = 0
        for i in range(0, self.no + 1):
            if j < len(self.index) and self.index[j].itemNo == i:
                print("%-10s"%(self.index[j].name),end='')
                j += 1
            else:
                print("%-10s"%(''),end='')
            item = self.table[i]
            print("%-6d%-15s%-16s%-15s%-11d%-10s"%(i, item.name, item.value, SymbolTableItem.String[item.itemType], item.level, item.addr))
    def fileOutTable(self, file):
        file.write("Index%5sNo.%3sName.%10sValue.%10sKind.%10sLevel.%5sAddr.%5s\n"%('','','','','','',''))
        j = 0
        for i in range(0, self.no + 1):
            if j < len(self.index) and self.index[j].itemNo == i:
                file.write("%-10s"%(self.index[j].name))
                j += 1
            else:
                file.write("%-10s"%(''))
            item = self.table[i]
            file.write("%-6d%-15s%-16s%-15s%-11d%-10s\n"%(i, item.name, item.value, SymbolTableItem.String[item.itemType], item.level, item.addr))



class Error:
    # Error类型定义
    WA_UNDEFINED = 1
    WA_EOF = 2
    WA_ILLEGAL_INPUT = 3

    GA_UNDEFINED = 31
    GA_MISS_SEMICOLON = 32
    GA_MISS_IDENTIFIER = 33
    GA_MISS_ASSIGN = 34
    GA_MISS_INTEGER = 35
    GA_ILLEGAL_CONST_ILLUSTRATE = 36
    GA_MISS_CONST_ILLUSTRATE = 37
    GA_MISS_VAR_ILLUSTRATE = 38
    GA_MISS_COMMA = 39
    GA_ILLEGAL_INPUT = 40
    GA_ILLEGAL_TYPE = 41
    GA_ILLEGAL_EOF = 42
    GA_MISS_L_PARENTHESIS = 43
    GA_MISS_R_PARENTHESIS = 44
    GA_MISS_L_BRACE = 45
    GA_MISS_R_BRACE = 46
    GA_MISS_TYPE = 47
    GA_MISS_EXPRESSION = 48
    GA_MISS_SENTENCE = 49

    ST_REPEATED_ID = 70
    ST_UNDEFINED_ID = 71
    ST_ASSIGN_CONST = 72
    ST_UNDEFINED_FUNCTION = 73
    ST_CALL_PARANUM_EXCEED = 74
    ST_CALL_PARANUM_LACK = 75
    ST_ILLEGAL_RETURN = 76
    ERROR_MSG = {
        WA_UNDEFINED : "Word Analysis Error: Undefined Error.",
        WA_EOF : "Word Analysis Error: Illegal EOF.",
        WA_ILLEGAL_INPUT : "Word Analysis Error: Illegal Input.",
        GA_UNDEFINED : "Gramma Analysis Error: Undefined Error.",
        GA_MISS_SEMICOLON : "Gramma Analysis Error: A \';\' is expected.",
        GA_MISS_IDENTIFIER : "Gramma Analysis Error: A identifier is expected.",
        GA_MISS_ASSIGN : "Gramma Analysis Error: \'=\' is expected.",
        GA_MISS_INTEGER : "Gramma Analysis Error: An integer is expected.",
        GA_ILLEGAL_CONST_ILLUSTRATE : "Gramma Analysis Error: Illegal const illustrate block.",
        GA_MISS_CONST_ILLUSTRATE : "Gramma Analysis Error: A const illustate block is expected.",
        GA_MISS_VAR_ILLUSTRATE : "Gramma Analysis Error: A const illustate block is expected.",
        GA_MISS_COMMA : "Gramma Analysis Error: A \',\' is expected.",
        GA_ILLEGAL_INPUT : "Gramma Analysis Error: Illegal input..",
        GA_ILLEGAL_TYPE : "Gramma Analysis Error: Undefined Variable Type.",
        GA_ILLEGAL_EOF : "Gramma Analysis Error: Illegal EOF.",
        GA_MISS_L_PARENTHESIS : "Gramma Analysis Error: A \'(\' is expected.",
        GA_MISS_R_PARENTHESIS : "Gramma Analysis Error: A \')\' is expected.",
        GA_MISS_L_BRACE : "Gramma Analysis Error: A \'{\' is expected.",
        GA_MISS_R_BRACE : "Gramma Analysis Error: A \'}\' is expected.",
        GA_MISS_TYPE : "Gramma Analysis Error: A variable type declaration is expected.",
        GA_MISS_EXPRESSION : "Gramma Analysis Error: An expression is expected.",
        GA_MISS_SENTENCE : "Gramma Analysis Error: A sentence is expected.",
        ST_REPEATED_ID : "Symbol Table Error: Try to redefine a identifier in the same level.",
        ST_UNDEFINED_ID : "Symbol Table Error: Try to use a undefined identifier.",
        ST_ASSIGN_CONST : "Symbol Table Error: Trying to assign to a const.",
        ST_UNDEFINED_FUNCTION : "Symbol Table Error: Trying to call a undefined function.",
        ST_CALL_PARANUM_EXCEED : "Symbol Table Error: Function Call failed, parameters exceed, expect less parameters.",
        ST_CALL_PARANUM_LACK : "Symbol Table Error: Function Call failed, parameters lacked, expect more parameters.",
        ST_ILLEGAL_RETURN : "Symbol Table Error: Trying to return an illegal value which not match function define.",
    }
    def __init__(self, file, errornumber, linenum, msg, wordNo = 0):
        self.file = file
        self.line = linenum
        self.no = errornumber
        self.msg = msg
        if self.msg == '':
            self.msg = Error.ERROR_MSG[self.no]
        self.wordNo = wordNo
    # 恢复file指针
    def restoreFile(self):
        self.file.seek(0,0)
    def getErrorLine(self):
        lineNum = 1
        line = self.file.readline()
        while lineNum < self.line:
            # print("line." + str(lineNum) + line)
            line = self.file.readline()
            lineNum += 1
        return line
    def printAllLine(self):
        self.restoreFile()
        lineNum = 1
        line = self.file.readline()
        while line:
            print("Line."+str(lineNum)+":"+line)
            line = self.file.readline()
            lineNum += 1
        return
    def printMsg(self):
        print("Error No." + str(self.no) + "\tIn line " + str(self.line) + " at " + str(self.wordNo) + ",\t" + self.msg)
        self.restoreFile()
        errorLine = self.getErrorLine()
        # 排除\n影响
        if len(errorLine) > 1 and errorLine[-1] == '\n':
            errorLine = errorLine[0:-1]
        # 输出原错误行
        print('\t' + errorLine)
        # 输出错误地点指示
        print('\t',end='')
        ws = 0
        while ws < self.wordNo:
            print(' ',end='')
            ws += 1
        print('^')
    def fileOutMsg(self, file):
        file.write("Error No." + str(self.no) + "\tIn line " + str(self.line) + " at " + str(self.wordNo) + ",\t" + self.msg + '\n')
        self.restoreFile()
        errorLine = self.getErrorLine()
        # 排除\n影响
        if len(errorLine) > 1 and errorLine[-1] == '\n':
            errorLine = errorLine[0:-1]
        # 输出原错误行
        file.write('\t' + errorLine + '\n')
        # 输出错误地点指示
        file.write('\t')
        ws = 0
        while ws < self.wordNo:
            file.write(' ')
            ws += 1
        file.write('^' + '\n')