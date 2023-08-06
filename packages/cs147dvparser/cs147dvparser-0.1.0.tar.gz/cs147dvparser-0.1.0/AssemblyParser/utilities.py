'''
A collection of associated data used by the Parser
'''

rtype_mnemonics = ["add", "sub", "mul", "and", "or", "nor", "slt", "sll", "srl","jr"]
itype_mnemonics = ["addi", "muli", "andi", "ori", "lui", "slti", "beq", "bne", "lw", "sw"]
jtype_mnemonics = ["jmp" ,"jal" ,"push" ,"pop"]
numTypes = {
    'bin':2,
    'binary':2,
    'hex': 16,
    'hexadecimal':16,
    'hexidecimal':16,
    'decimal':10,
    'decamal':10
}
functs = {
    "add": "100000",
    "sub": "100010",
    "mul": '101100',
    "and": '100100',
    "or" : '100101',
    "nor": '100111',
    "slt": '101010',
    "sll": "000001",
    "srl": "000010",
    "jr" : "001000",
    
}
opCodes = {
    # r-type
    "add" : "000000",
    "sub" : "000000",
    "mul" : "000000",
    "and" : "000000",
    "or"  : "000000",
    "nor" : "000000",
    "slt" : "000000",
    "sll" : "000000",
    "srl" : "000000",
    "jr"  : "000000",
    # i-type
    "addi": '001000',
    "muli": '011101',
    "andi": '001100',
    "ori" : "001101",
    "lui" : "001111",
    "slti": '001010',
    "beq" : "000100",
    "bne" : "000101",
    "lw"  : "100011",
    "sw"  : "101011",
    # J-type
    "jmp" : "000010",
    "jal" : "000011",
    "push": "011011",
    "pop" : "011100"
}