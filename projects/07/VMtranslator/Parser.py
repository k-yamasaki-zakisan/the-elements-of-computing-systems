from VMContents import *

class Parser():
	def __init__(self,read_file_path:str):
		self._current_command = None
		self._f_vm = open(read_file_path, 'r')
	
	def __exit__(self, exception_type, exception_value, traceback):
		self._f_vm.close()

	def advance(self):
		while True:
			line = self._f_vm.readline()
			if not line:
				self._current_command = None
				return self._current_command

			line = line.strip()

			command_i = line.find('//')

			if command_i != -1:
				line = line[:command_i]

			if line != '':
				self._current_command = line
				return self._current_command

	def command_type(self):
		if self._current_command[0] == 'push':
			return C_PUSH
		elif self._current_command[0] == 'pop':
			return C_POP
		elif self._current_command[0] == 'label':
			return C_LABEL
		elif self._current_command[0] == 'goto':
			return C_GOTO
		elif self._current_command[0] == 'if':
			return C_IF
		elif self._current_command[0] == 'function':
			return C_FUNCTION
		elif self._current_command[0] == 'return':
			return C_RETURN
		elif self._current_command[0] == 'call':
			return C_CALL
		else:
			return C_ARITHMETIC

	def arg1(self):
		if self.command_type() == C_RETURN:
			pass
		elif self.command_type() == C_ARITHMETIC:
			return self._current_command[0]
		else:
			return self._current_command[1]

	def arg2(self):
		if self.command_type() in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
			return self._current_command[1]



