from const import *


class VmWriter():
    def __init__(self, filepath:str):
        self.f = open(filepath, 'w')

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.f.close()

    def write_code(self, code:str):
        self.f.write(code + '\n')

    def write_codes(self, codes:list):
        self.write_code('\n'.join(codes))

    def write_push(self, segment:str, index:str):
        self.write_code('push %s %d' % (self._get_segment_str(segment), int(index)))

    def write_pop(self, segment:str, index:str):
        self.write_code('pop %s %d' % (self._get_segment_str(segment), int(index)))

    def write_arithmetic(self, command:str):
        if command == Command.ADD:
            self.write_code('add')
        elif command == Command.SUB:
            self.write_code('sub')
        elif command == Command.NEG:
            self.write_code('neg')
        elif command == Command.EQ:
            self.write_code('eq')
        elif command == Command.GT:
            self.write_code('gt')
        elif command == Command.LT:
            self.write_code('lt')
        elif command == Command.AND:
            self.write_code('and')
        elif command == Command.OR:
            self.write_code('or')
        elif command == Command.NOT:
            self.write_code('not')

    def write_label(self, label:str):
        self.write_code('label %s' % label)

    def write_goto(self, label:str):
        self.write_code('goto %s' % label)

    def write_if(self, label:str):
        self.write_code('if-goto %s' % label)

    def write_call(self, name:str, n_args:int):
        self.write_code('call %s %d' %(name,n_args))

    def write_function(self, name:str, locals:int):
        self.write_code('function %s %d' %(name,locals))

    def write_return(self):
        self.write_code('return')

    @classmethod
    def _get_segment_str(cls, segment:int) -> str:
        if segment == Segment.ARG:
            return 'argument'
        elif segment == Segment.CONST:
            return 'constant'
        elif segment == Segment.LOCAL:
            return 'local'
        elif segment == Segment.POINTER:
            return 'pointer'
        elif segment == Segment.STATIC:
            return 'static'
        elif segment == Segment.TEMP:
            return 'temp'
        elif segment == Segment.THAT:
            return 'that'
        elif segment == Segment.THIS:
            return 'this'
        else:
            raise Exception('Unknown segment')