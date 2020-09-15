from parser import *
from symbol_table import SymbolTable
import code
import re
import argparse
import os.path

symbol_pattern = re.compile(r'([0-9]+)|([0-9a-zA-Z_\.\$:]+)')

def main():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('asm_file', type=str, help='asm file')
	print('111111111')
	args = parser.parse_args()
	print('222222222')
	asm_file = args.asm_file
	print('3333333')
	save_file = os.path.splitext(asm_file)[0]+".hack"

	st = SymbolTable()

	#一回目
	with HackParser(asm_file) as hp:
		op_address = 0

		while hp.advance() != None:
			cmd_type = hp.command_type()
			if cmd_type == A_COMMAND or cmd_type == C_COMMNAD:
				op_address += 1
			elif cmd_type == L_COMMAND:
				st.add_entry(hp.symbol(), op_address)

	#二回目
	with HackParser(asm_file) as hp:
		with open(save_file, 'w') as wf:
			while hp.advance() != None:
				cmd_type = hp.command_type()

				if cmd_type == A_COMMAND:
					symbol = hp.symbol()
					m = symbol_pattern.match(symbol)

					if m.group(1):
						bincode = "0" + int2bin(int(m.group(1)), 15)
					elif m.group(2):
						symbol = m.group(2)
						if st.contains(symbol):
							address = st.get_address(symbol)
							bincode = "0" + int2bin(address, 15)
						else:
							st.add_variable(symbol)
							address = st.get_address(symbol)
							bincode = "0" + int2bin(address, 15)
				elif cmd_type == C_COMMNAD:
					bincode = '111' + code.comp(hp.comp()) + code.dest(hp.dest()) + code.jump(hp.jump())

				if cmd_type != L_COMMAND:
					wf.write(bincode+'\n')

def int2bin(value:int, bitnum:int) -> str:
	bin_value = bin(value)[2:]
	if len(bin_value) > bitnum:
		raise Exception('Over binary size')
	return "0"*(bitnum - len(bin_value)) + bin_value

if __name__ == '__main__':
	main()


