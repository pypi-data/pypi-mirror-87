#!/usr/bin/env/python
from __future__ import print_function
import sys
import os
import argparse
from builtins import input
'''
 * a python implementation of
 * @author Jordan's java project
 *
 *	A class that can parse CS147DV instructions into their hexadecimal value
'''
class CS147DVError(Exception):
    pass

class MnemonicError(CS147DVError):
    pass

class RtypeError(CS147DVError):
    pass

class ItypeError(CS147DVError):
    pass

class JtypeError(CS147DVError):
    pass

class NumTypeError(CS147DVError):
    pass

class BaseError(CS147DVError):
    pass

class FieldLengthError(CS147DVError):
    pass

class RegisterError(CS147DVError):
    pass

class ShamtError(CS147DVError):
    pass

class ImmediateError(CS147DVError):
    pass

class AddressError(CS147DVError):
    pass

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

def validate_field_len(field, field_bin_value, length,field_name):
    # fields with length 5 must have a declared field_name
    # since shamt, registers both have length 5
    if not field_name:
        field_name = 'immediate' if length == 16 else 'address'
    if len(field_bin_value) > length:
        FieldLengthError_msg = field+' = '+field_bin_value
        FieldLengthError_msg += '\ntoo long! field '+field_name+' length is '
        FieldLengthError_msg += str(len(field_bin_value)) +', max length is '+str(length)
        raise FieldLengthError(FieldLengthError_msg)
    
def field_to_binary(field, base, padding, field_name=''):
    try:
        field_dec_value = int(field,base)
    except ValueError:
        BaseError_msg = "invalid base: "+str(base)
        BaseError_msg += "\nfor field: " +field_name+ '\nwith input: "' + field + '"'
        raise BaseError(BaseError_msg)

    field_bin_value = bin(field_dec_value)
    if field_bin_value.startswith('-'):
        raise RegisterError("register must contain a positive number.\nYour input: "+field)
    
    field_bin_value = field_bin_value[2:].zfill(padding)
    validate_field_len(field,field_bin_value,padding,field_name)
    return field_bin_value


def get_funct(mnemonic):
    if mnemonic in functs:
        return functs[mnemonic]
    else:
        FunctError_msg = "No Function available for mnemonc: "+mnemonic
        FunctError_msg += '\noptions are: ( '+', '.join([k for k in functs]) + ' )'
        raise MnemonicError(FunctError_msg)


def get_base(numType):
    if not numType: return ''
    elif numType in numTypes: return numTypes[numType]
    else:
        NumTypeError_msg = "invalid Number data-type: "+numType
        NumTypeError_msg += '\noptions are ( '+", ".join([k for k in numTypes])+' )'
        raise NumTypeError(NumTypeError_msg)


def get_opcode(mnemonic):
    if mnemonic in opCodes:
        return opCodes[mnemonic]
    else:
        MnemonicError_msg = "invalid Mnemonic : " + mnemonic
        MnemonicError_msg += '\noptions are ( '+', '.join([k for k in opCodes]) + ' )'
        raise MnemonicError(MnemonicError_msg)


def validate_reg_beginning(reg):
    if not reg.lower().startswith('r'):
        raise RegisterError('register must start with [rR]. Your input: '+reg)


def convert_to_bin(field,padding,field_name=''):
    num = ''
    try: # have to do binary first, all binary is also valid decimal
        num = int(field,2)
    except:
        try: # have to do decimal next. All decimal is valid hex
            num = int(field)
        except: # try converting to hexadecimal
            try:
                num = int(field,16)
            except ValueError:
                err_code = 'could not convert '+field+' to a binary|decimal|hexadecimal number'
                raise BaseError(err_code)
    
    # remove first 2 characters from bin(num), which will be '0b'
    # then pad with leading 0s to the size as requested by padding variable
    bin_str = bin(num)
    if bin_str.startswith('-'):
        if padding == 6:
            if field_name.startswith('r'):
                raise RegisterError(field_name+' cannot be negative.\nyour input: '+field)
            elif field_name == 'shamt':
                raise ShamtError('shamt cannot be a negative number.\nyour input: '+field)
        elif padding == 16:
            raise ImmediateError('immediate field cannot be negative.\nyour input: '+field)
        else:
            raise AddressError('address field cannot be negative.\nyour input: '+field)
    bin_str = bin_str[2:].zfill(padding)
    validate_field_len(field, bin_str, padding, field_name)
    return bin_str


def form_err_msg(mnemonic,fields, inst,restriction):
    err_msg = inst+' requires '+restriction
    err_msg += '\nyour input: "'+mnemonic+' '+' '.join(fields)+'" '
    err_msg += '('+str(len(fields))+' field' + (')' if len(fields)==1 else 's)')
    return err_msg

def parse_rtype(mnemonic,fields):
    # ensure correct number of instructions passed in for each instruction type
    if not fields:
        RtypeError_msg = form_err_msg(mnemonic,fields,inst='Every R-Type instruction',restriction='at least one field')
        raise RtypeError(RtypeError_msg)
    elif mnemonic == 'jr' and len(fields) != 1:
        RtypeError_msg = form_err_msg(mnemonic, fields,inst=mnemonic,restriction='exactly 1 field')
        raise RtypeError(RtypeError_msg)
    # sll|srl can take an optional data type declaration
    elif mnemonic in ('sll','srl') and not(3 <= len(fields) <= 4):
        RtypeError_msg = form_err_msg(mnemonic,fields,inst=mnemonic, restriction='3 fields and an optional number data-type')
        raise RtypeError(RtypeError_msg)
    elif mnemonic not in ('jr','sll','srl') and len(fields) != 3:
        RtypeError_msg = form_err_msg(mnemonic,fields,inst=mnemonic, restriction='exactly 3 fields')
        raise RtypeError(RtypeError_msg)
    
    numType = ''
    # set field values for each instruction type
    if mnemonic == 'jr':
        rs = fields[0]
        registers = [rs]
        rd = rt = shamt = '00000'
    elif mnemonic in ('srl','sll'):
        # [fields] must contain 3 or 4 values
        try:
            rd, rs, shamt, numType = fields
        except:
            rd, rs, shamt  = fields
        registers = [rd,rs]
        rt = '00000'    
    else:
        rd, rs, rt = fields
        registers = [rd,rs,rt]
        shamt = '00000'

    # make sure registers start with [rR]
    for r in registers:
        validate_reg_beginning(r)

    # if shamt starts with an r, error
    if shamt.startswith('r'):
        registerError_msg = mnemonic+' operation requires a shft amount, not a register'
        registerError_msg += '\n your input: '+shamt
        raise RegisterError(registerError_msg)

    # if data type of shamt is declared, convert to numerical base value
    # get_base() returns '' if not numType declared
    base = get_base(numType)
    return rd, rs, rt, shamt, base


def parse_itype(mnemonic, fields):
    # all itype instructions take at least 2 arguments
    if not (2<=len(fields)<=3):
        ItypeError_msg = form_err_msg(mnemonic,fields,inst='Every I-type instruction',restriction='at least 2 arguments')
    if mnemonic == 'lui' and not(2<=len(fields)<=3):
        ItypeError_msg = form_err_msg(mnemonic,fields,inst=mnemonic, restriction="2 fields and an optional number data-type")
        raise ItypeError(ItypeError_msg)    
    elif mnemonic != 'lui' and not(3<=len(fields)<=4):
        ItypeError_msg = form_err_msg(mnemonic,fields,inst=mnemonic, restriction="3 fields and an optional number data-type")
        raise ItypeError(ItypeError_msg)    

    numType = ''    
    if mnemonic == 'lui':
        try: #check if user gave a number type
            rt, immediate, numType = fields
        except :
            rt, immediate = fields
            rs = '00000'
        registers = [rt]
    else:
        try: 
            rt, rs, immediate, numType = fields
        except:
            rt,rs, immediate = fields
        registers = [rt,rs]

    for r in registers:
        validate_reg_beginning(r)
    
    base = get_base(numType)
    return rt,rs,immediate,base

def parse_jtype(mnemonic, fields):
    if mnemonic in ('push','pop') and fields:
        JtypeError_msg = form_err_msg(mnemonic,fields,inst=mnemonic,restriction='exactly 0 fields')
        raise JtypeError(JtypeError_msg)
    elif mnemonic in ('jmp','jal') and not(1<=len(fields)<=2):
        JtypeError_msg = form_err_msg(mnemonic,fields,inst=mnemonic,restriction='exactly 1 field and an optional number data type')
        raise JtypeError(JtypeError_msg)

    numType = ''
    if mnemonic in ('jmp','jal'):
        try:
            address, numType = fields
        except:
            address  = fields[0]
    else:
        address = '0x00'
        base = 16
    
    base = get_base(numType)
    return address, base

def convert_bin_to_hex(bin_s, length):
    # no need to do length checking because 
    # all fields have already undergone length check 
    #  by this point
    return hex(int(bin_s,2))[2:].zfill(length)


def parse_instruction(instruction, vprint='os.devnull'):
    if not instruction: raise CS147DVError("No instruction provided")
    
    if vprint == 'verbose':
        vprint = sys.stderr
    elif vprint == 'os.devnull':
        vprint = open(os.devnull, 'w')

    # remove trailing comments if applicable
    comment_starters = ['//','#','/*']
    for comment_starter in comment_starters:
        comment_index = instruction.find(comment_starter)
        if comment_index != -1:
            instruction = instruction[:comment_index]
    
    opcode = ''
    rd = ''
    rs = ''
    rt = ''
    shamt = ''
    funct = ''
    immediate = ''
    address = ''

    components = instruction.lower().replace(',',' ').split()
    mnemonic, fields = components[0], components[1:]
    opcode = get_opcode(mnemonic)
    if mnemonic in rtype_mnemonics:
        vprint.write('\n R-Type detected\n')
        vprint.write(' <mnemonic> <rd> <rs> <rt|shamt> [base]\n\n')
        rd, rs, rt, shamt, base = parse_rtype(mnemonic,fields)
        funct = get_funct(mnemonic)
        vprint.write(' input: '+instruction+'\n')
        vprint.write('  _____________________________________\n')
        vprint.write(' |opcode| rs  | rt  | rd  |shamt| funct|\n')
        vprint.write(' |______|_____|_____|_____|_____|______|\n\n')
        if base:
            shamt = field_to_binary(shamt,base,5,field_name="shamt")
        else:
            shamt = convert_to_bin(shamt,5,field_name="shamt")

    elif mnemonic in itype_mnemonics:
        vprint.write('\n I-Type detected\n')
        vprint.write(' <mnemonic> <rt> <rs> <imm> [base]\n\n')
        rt, rs, immediate, base = parse_itype(mnemonic,fields)
        vprint.write(' input: '+instruction+'\n')
        vprint.write('  ___________________________________\n')
        vprint.write(' |opcode| rs  | rt  |   immediate    |\n')
        vprint.write(' |______|_____|_____|________________|\n\n')
        immediate = field_to_binary(immediate,base,16) if base else convert_to_bin(immediate,16)
    else: #J-type instruction
        vprint.write('\n J=Type detected\n')
        vprint.write(' <mnemonic> <address> [base]\n')
        address, base = parse_jtype(mnemonic, fields)
        vprint.write(' input: '+instruction+'\n')
        vprint.write('  _________________________________\n')
        vprint.write(' |opcode|          address         |\n')
        vprint.write(' |______|__________________________|\n\n')
        address = field_to_binary(address,base,26) if base else convert_to_bin(address,26)
    
    if rd: rd = field_to_binary(rd[1:],10,5, field_name='rd')
    if rt: rt = field_to_binary(rt[1:],10,5, field_name='rt')
    if rs: rs = field_to_binary(rs[1:],10,5, field_name='rt')

    to_print = []
    vprint.write(' ')
    for val, name in [[opcode, 'opcode'],[address,'address'],[rs,'rs'],[rt, 'rt'],
                 [immediate, 'imm'],[rd, 'rd'],[shamt,'shamt'],[funct,'funct']]:
        if val:
            vprint.write(name+'\t')
            to_print.append(val)

    vprint.write('\n ')
    vprint.write('\t'.join(to_print)+'\n\n')
    bin_instruction = opcode+address+rs+rt+immediate+rd+shamt+funct
    # probably unnecessary. leaving it anyways as a precaution
    assert len(bin_instruction) <= 32, " binary string too long!\n" +bin_instruction
    vprint.write(' binary_string:\n ')
    for i in range(len(bin_instruction)):
        if (i == 0) or (i%4 > 0):
            vprint.write(bin_instruction[i])
        else:
            vprint.write(' '+bin_instruction[i])
    vprint.write('\n')
    hex_instruction = convert_bin_to_hex(bin_instruction,8)
    return hex_instruction


def get_instruction(vprint, first_time):
    if first_time:
        vprint.write('\n WELCOME TO CS147DV INTERACTIVE INSTRUCTION PARSER!\n')
        vprint.write(' ENTER IN YOUR INSTRUCTIONS ONE AT A TIME\n')
        vprint.write(' THE RESULT WILL BE PRINTED TO THE SCREEN\n')
        vprint.write(' INPUT SHOULD BE OF THE TYPE:\n')
        vprint.write('   R-Type:  <mnemonic> <rd>,<rs>,<rt|shamt>\n')
        vprint.write('   I-Type:  <mnemonic> <rt>,<rs>, <imm>\n')
        vprint.write('   J-Type:  <mnemonic> <address>\n')
        vprint.write(' OUTPUT WILL BE A 32 BIT HEXADECIMAL NUMBER\n')
        vprint.write(' PRESS ctrl-c TO EXIT AT ANY TIME\n\n')
    instruction = input("\n enter your intruction: ")
    return instruction 

if __name__ == "__main__":
    info = 'input: an instruction or set of instructions\n'
    info += '       passed in via the command line, as a file, or interactively.\n\n'
    info += 'instruction types: R-type: <mnemonic> <rd> <rs> <rt|shamt>\n'
    info += '                   I-type: <mnemonic> <rt> <rs> <immediate>\n'
    info += '                   J-type: <mnemonic> <address>\n\n'
    info += 'output: instruction will be parsed into its component parts.\n'
    info += '        By default the:\n'
    info += '        \t- instruction type\n'
    info += '        \t- bit values of each component\n'
    info += '        \t- result in the form of a 32-bit binary string\n'
    info += '        will be output to stderr\n\n'
    info += '        the resulting hexadecimal string will be output to stdout.\n'
    
    parser = argparse.ArgumentParser(description="Program to parse CS147DV instructions into hexadecimal",
                            prog = 'CS147DVInstructionParser',
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            epilog = info)
    parser.add_argument('instructions',nargs='*', default=[], help = 'CS147DV instructions wrapped in "quotes"')
    parser.add_argument('-f','--file', nargs='?',type=argparse.FileType('r'), help='file of CS147DV instructions, one per line')
    parser.add_argument_group()
    parser.add_argument('-o','--outfile', nargs='?',
                        default=sys.stdout, help='File to save results to.')
    parser.add_argument('-a','--append', action='store_true',help='append results to outfile, instead of writing over the outfile.')
    parser.add_argument('-i','--interactive',action='store_true', help='evoke interactive mode.')
    parser.add_argument('-q','--quiet', action='store_true', help='suppress meta-info about each instruction')
    args = parser.parse_args()

    # create a list of instructions to parse that 
    # are passed in from command line and/or file
    instructions = args.instructions
    if args.file:
        with args.file as f:
            instructions += [i.strip() for i in f]
    
    outfile = args.outfile
    if args.append:
        assert outfile != sys.stdout, "outfile must be a real file and not stdout if you want to append to it."
    
    if outfile != sys.stdout: 
        mode = 'a' if args.append else 'w'
        outfile = open(args.outfile, mode)
    
    interactive = args.interactive
    # if they don't provide any input, automatically set interactive to True
    if not interactive:
        interactive = not instructions

    # set file to print meta information to stdout
    # or to devnull for 'quiet' mode
    vprint = open(os.devnull,'w') if args.quiet else sys.stdout
    
    for i in instructions:
        # hex_result = parse_instruction(i,vprint)
        # print(hex_result)
        try:
            hex_result = parse_instruction(i,vprint)
        except Exception as e:
            print(e,file=sys.stderr)
            print('\n',file=sys.stderr)
        else:
            vprint.write('\n hexadecimal_string result: \n')
            outfile.write(' '+hex_result+'\n')
    
    first_time=True
    while interactive:
        try:
            i = get_instruction(vprint, first_time)
            hex_result = parse_instruction(i,vprint)
        except Exception as e:
            sys.stderr.write(' '+str(e))
            sys.stderr.write('\n try again\n\n')
        except KeyboardInterrupt:
            # these could both possibly be sys.stdout, however its
            # safe to close sys.stdout here since immediately exiting
            sys.stderr.write('\n')
            outfile.close()
            vprint.close()
            sys.exit(0)
        else:
            vprint.write('\n hexadecimal_string result:\n')
            outfile.write(' '+hex_result+'\n\n')
        first_time = False
    
    outfile.close()
    vprint.close()       
