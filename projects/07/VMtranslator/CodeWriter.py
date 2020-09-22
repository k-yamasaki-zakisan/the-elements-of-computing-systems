import os, os.path
from VMContents import *

class CodeWriter():
    def __init__(self,write_file_path:str):
        self._out_file = open(write_file_path, 'w')
        self.label_num  = 0
        self._current_translated_file_name = ''
    
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._out_file.close()
    
    def write_arithmetic(self,command:str):
        if command in ['add', 'sub', 'and', 'or']:
            self.write_binary_operation(command)
        elif command in ['ng', 'not']:
            self.write_unary_operation(command)
        elif command in ['eq', 'gt', 'lt']:
            self.write_comp_operation(command)
    
    def write_push_pop(self,command:str,seg:str,index:int):
        if command == C_PUSH:
            if seg == 'contant':
                self.write_codes([
                    '@%d'%index,
                    'D-A' 
                ])
                self.write_push_from_d_register()
            elif seg in ['local', 'argument', 'this', 'that']:
                self.write_push_from_virtual_segment(seg, index)
            elif seg in ['temp', 'pointer']:
                self.write_push_from_static_segment(seg, index)
            if seg == 'static':
                self.write_codes([
                    "@%s.%d"+self._current_translated_file_name+str(index),
                ])
                self.write_code('D=M')
                self.write_push_from_d_register()
            
            elif command == C_POP:
                if seg in ['local', 'argument', 'this', 'that']:
                    self.write_pop_from_virtual_segment(seg, index)
                elif seg in ['temp', 'pointer']:
                    self.write_pop_from_static_segment(seg, index)
                if seg == 'static':
                    self.write_pop_to_m_register()
                    self.write_codes([
                        'D=M',
                        '@%s.%d'+self._current_translated_file_name+str(index),
                    ])
                    self.write_code('M=D')
    
    def set_current_translated_file_name(self,file_name:str):
        self._current_translated_file_name = file_name

    def write_binary_operation(self,command:str):
        self.write_pop_to_m_register()
        self.write_code('D=M')
        self.write_pop_to_m_register()
        if command == 'add':
            self.write_code('D=D+M')
        elif command == 'sub':
            self.write_code('D=M-D')
        elif command == 'and':
            self.write_code('D=D&M')
        elif command == 'or':
            self.write_code('D=D|M')
        self.write_push_from_d_register()
    
    def write_unary_operation(self,command:str):
        self.write_codes([
            '@SP',
            'A=M-1',
        ])
        if command == 'neg':
            self.write_code('M-=M')
        elif command == 'not':
            self.write_code('M=!M')
    
    def write_comp_operation(self, command:str):
        self.write_pop_to_m_register()
        self.write_code('D=M')
        self.write_pop_to_m_register()
        l1 = self.get_new_label()
        l2 = self.get_new_label()
        if command == 'eq':
            comp_type = 'JEQ'
        elif command == 'gt':
            comp_type = 'JGT'
        elif command == 'lt':
            comp_type = 'JLT'
        self.write_codes([
            'D=M-D',
            '@%s' % l1,
            'D;%s' % comp_type,
            'D=0',
            '@%s' % l2,
            '0;JMP',
            '(%s)' % l1,
            'D=-1',
            '(%s)' % l2,
        ])
        self.write_pop_to_m_register()
    
    def write_push_from_virtual_segment(self,seg:str,index):
        if seg == 'local':
            register_name = 'LCL'
        elif seg == 'argument':
            register_name = 'ARG'
        elif seg == 'this':
            register_name = 'THIS'
        elif seg == 'that':
            register_name = 'THAT'
        self.write_codes([
            '@%s' % register_name,
            'A=M'
        ])
        for _ in range(int(index)):
            self.write_code('A=A+1')
        self.write_code('D=M')
        self.write_push_from_d_register()
    
    def write_pop_from_virtual_segment(self,seg:str,index):
        if seg == 'local':
            register_name = 'LCL'
        elif seg == 'argument':
            register_name = 'ARG'
        elif seg == 'this':
            register_name = 'THIS'
        elif seg == 'that':
            register_name = 'THAT'
        self.write_codes([
            '@%s' % register_name,
            'A=M',
        ])
        for _ in range(int(index)):
            self.write_code('A=A+1')
        self.write_code('M=D')
    
    def write_push_from_static_segment(self,seg:str,index):
        if seg == 'temp':
            base_address = TEMP_BASE_ADDRESS
        elif seg == 'pointer':
            base_address = POINTER_BASE_ADDRESS
        self.write_codes([
            '@%d' % base_address,
        ])
        for _ in range(int(index)):
            self.write_code('A=A+1')
        self.write_code('D=M')
        self.write_push_from_d_register()
    
    def write_pop_from_static_segment(self,seg:str,index):
        if seg == 'temp':
            base_address = TEMP_BASE_ADDRESS
        elif seg == 'pointer':
            base_address = POINTER_BASE_ADDRESS
        self.write_pop_to_m_register()
        self.write_codes([
            'D=M',
            '@%d' % base_address,
        ])
        for _ in range(int(index)):
            self.write_code('A=A+1')
        self.write_code('M=D')
    
    def write_push_from_d_register(self):
        self.write_codes([
            '@SP',
            'A=M',
            '@SP',
            'M=M+1',
        ])
    
    def write_pop_to_m_register(self):
        self.write_codes([
            '@SP',
            'M=M-1',
            'A=M',
        ])
    def write_code(self,code:str):
        self._out_file.write(code + '\n')
    
    def write_codes(self,codes:list):
        self.write_code('\n'.join(codes))
    
    def get_new_label(self):
        self.label_num += 1
        return 'LABEL' + str(self.label_num)



