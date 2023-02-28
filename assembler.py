
import os
import re

class Utils:
	def update_line_information(self,start_memory_location,lines,hold_line_info):
			# update line info: {"0":[start_addres,end_address]}
			start_addr = start_memory_location
			end_addr = 0
			# lines_to_ignnore = list(self.preprocessor_commands.values())

			# not_updated = True
			
			# while not_updated:
			for i in range(0,len(lines)):
				# to help track the new lines being modified

				end_addr = start_addr+15
				info = {"start":"0x"+f"{start_addr:02x}", "end":"0x"+f"{end_addr:02x}"}
				hold_line_info[str(i)]= info
				start_addr=end_addr+1
			
				# not_updated = False
	
	def to_binary(self,d):
		b = ''
		while True:
			if d == 0:
				break
			elif (d % 2) == 0:
				d = d // 2
				b = '0' + b
			else:
				d = d // 2
				b = '1' + b
		return b

	def from_binary(self,binary):
		binary = binary[::-1]
		d = 0
		power = 0 
		for i in binary:
			d += int(i) * (2 ** power)
			power +=1 
		return d 
	
	def addition(self,a, b):
		max_len = max(len(a), len(b))

		a = a.zfill(max_len)
		b = b.zfill(max_len)

		result = ''    
		temp = 0

		for i in range(max_len - 1, - 1, - 1):
			num = int(a[i]) + int(b[i]) + temp
			print(num)

			if num % 2 == 0:
				result = '0' + result
			else:
				result = '1' + result

			if num == 2:
				temp = 1
			else:
				temp = 0
		
		if temp !=0: 
			result = '01' + result
		
		if int(result) == 0:
			result = 0

		return result

	def subtraction(self,a, b):
		max_len = max(len(a), len(b))

		a = a.zfill(max_len)
		b = b.zfill(max_len)

		result = ''    
		temp = 0

		for i in range(max_len - 1, - 1, - 1):
			num = int(a[i]) - int(b[i]) - temp
			if num % 2 == 1:
				result = '1' + result
			else:
				result = '0' + result

			if num < 0:
				temp = 1
			else:
				temp = 0
		
		if temp !=0: 
			result = '01' + result
		
		if int(result) == 0:
			result = 0

		return result

	def multiplication(self,a, b):
		max_len = max(len(a), len(b))
		min_len = min(len(a), len(b))

		result = ''
		temp_result = ''

		temp = []
		zeroes = 0
		temp_index = 0

		for j in range(min_len - 1, - 1, - 1):
			
			temp_result = ''
			for i in range(max_len - 1, - 1, - 1):
				summ = int(a[i]) * int(b[j])
				if summ == 0:
					temp_result = '0' + temp_result
				elif summ == 1:
					temp_result = '1' + temp_result
			temp_result = temp_result + ('0' * zeroes)
			zeroes += 1
			
			temp.append(temp_result)

			if len(temp) == 2:
				result = self.addition(str(temp[0]), str(temp[1]))
			elif len(temp) > 2:
				temp_index = len(temp)
				temp_index += 1
				result = self.addition(str(result), str(temp[temp_index - 2]))
			else:
				pass
		return result


	def division(self,a, b):
		result = ''
		temp = '0'
		r = 0

		for i in range(len(a)):        
			if int(b) > int(temp):
				result += '0'
				temp += a[i]
			else:
				r = self.sunstraction(temp, b)
				if r == 0:
					temp = a[i]
					result += '1'
				else:
					r = str(r).lstrip('0')
					result += '1'
					temp = r + a[i]
		
		if temp !=int(0): 
			result = result + '0' 
					
		return result



class MemoryUnitSim:
	'''
	Simulates the memory unit for storage
	'''
	bits = None
	rows = None
	mem_unit = []
	mem_unit_inst_start = 1664 # '0xd000'
	mem_unit_map = {}

	def __init__(self,rows= 2048, columns=32):
		self.bits = columns
		self.rows = rows
		self.mem_unit = [['x' for i in range(columns)] for i in range(rows)]
	
	def map_memory(self):
		# print memory state
		last_line_total_bits = 0
		key_to_next_line = 0
		for i in range(self.rows):
			# print(self.mem_unit[i])
			# compressed = "".join(self.mem_unit[i])
			# self.mem_unit[i] = compressed
			# compressed = self.mem_unit[i]
			# print(key_to_next_line)
			self.mem_unit_map[f"{hex(key_to_next_line)}"] = {"index":i,"start":f"{hex(key_to_next_line)}","end":f"{hex(key_to_next_line+31)}"}
			last_line_total_bits = key_to_next_line + 31
			key_to_next_line = last_line_total_bits + 1
		
		# print(self.mem_unit_map)

	def show_memory(self):
		# print memory state
		for i in range(self.rows):
			# print(self.mem_unit[i])
			compressed = "".join(self.mem_unit[i])
			# compressed = self.mem_unit[i]
			# self.mem_unit[i] = compressed
			# self.mem_unit_map[hex(last_line_total_bits+bits_to_next_line)] = i
			end_key ="end"
			print(f"{self.mem_unit_map[hex(i*32)][end_key]}: {compressed}")
			
		
	def mem_store_instruction(self,information,destination,bit_range):
		# store in memory, return location
		# print(information)
		# print(self.mem_unit[destination][bit_range[0]:bit_range[1]])
		self.mem_unit[destination][bit_range[0]:] = information
		# print(self.mem_unit[destination][0:31])
		self.mem_unit[destination] = self.mem_unit[destination][0:32]
		return {"location":destination,"bit_range":bit_range}

	def mem_read(self,destination,bit_range):
		# read from memory
		pass

utils = Utils()


class Assembler:
	BASE_DIR = "" # base directory
	all_lines=[]
	all_lines_info={}
	labels={}
	preprocessor_commands={}
	char_comment=";" # character used for comment
	start_memory_location=0
	last_offset = None
	file_name ="" # file containing assembly code
	offset_list = {}
	opcode_table = {
	'halt':['0x00'],
	'nop': ['0x01'],
	'li' : ['0x02'],
	'lw' : ['0x03'],
	'sw' : ['0x04'],
	'add': ['0x05'],
	'sub': ['0x06'],
	'mult': ['0x07'],
	'div':['0x08'],
	'j': ['0x09'],
	'jr':['0x0A'],
	'beq':['0x0B'],
	'bne':['0x0C'],
	'inc':['0x0D'],
	'dec':['0x0E']
	} # operation code table
	compiled_lines =[]
	register_names = {'R1':'0x00','R2':'0x01','R3':'0x02','PC':'0x03','COND':'0x04'}
	app_memory_obj =None

	def __init__(self,base_dir,mem):
		self.BASE_DIR =base_dir
		self.app_memory_obj = mem
		
		
	def readLines(self,file):
        # read file input
		full_file_path = os.path.join(self.BASE_DIR,file)
		self.file_name=file.split(".")[0] # ignore file extension for now
		
		try:
			with open(full_file_path) as f:
				# read lines and store all_lines[]
				self.all_lines=f.readlines()
		except FileNotFoundError:
			info = f"No such file as {file} was found"
			print(info)
		except:
			raise


	def printLines(self,lines):
		for i in range(0,len(lines)):
			print(f"{i+1}:{lines[i]}")
		# print(self.all_lines_info)
		# print(self.all_lines)
		for i in range(0,len(lines)):   
			start_val = self.all_lines_info[str(i)]["start"]
			line_val = f"{start_val}: "
			for j in range(0,len(lines[i])):
				seg = lines[i][j]
				line_val = line_val + f" {seg}"
				
			self.all_lines[i] = line_val
			
		with open('preprocessed.txt', 'w', encoding='utf-8') as f:
			f.writelines(f"{l}\n" for l in lines)    
			
		print("ASSEMBLY FILE INFORMATION")
		
		print("Labels: ")
		print(self.labels)
		print("")
		print("Pre_processor commands: ")
		print(self.preprocessor_commands)
		print("")
		print("Offsetlist:" )
		print(self.offset_list)
		print("")
		print("Line info: " )
		print(self.all_lines_info)
		print("")   


	def get_preprocessor_directives(self,lines):
		# get preprocessor directives
		for i in range(0,len(lines)):
			line = lines[i].find(".")
			if (line != -1):
				self.preprocessor_commands[lines[i].strip()]=i
                # lines.remove(lines[i])
	
	def get_labels(self,lines):
		# get labels
		for i in range(0,len(lines)):
			line = lines[i].find(":")
			if (line != -1):
				sp = lines[i].split(":")
				label_part = sp[0].strip() # label
				x = sp[1] # rest of insructions
				self.labels[label_part]=i 
				if len(x)!= 0:
                   # maintain rest of instructions remain
					lines[i] = x.strip()  
				else:
					# no rest of instructions  
					lines[i] = label_part
    
	def remove_comments(self,lines):
		'''comments are two types
		   after code line: li,R1, R2 ;type1
		   line comment: 

		   ; this comment above source code, type2
		   li,R1, R2
		'''
		# removing comments from source code
		for i in range(0,len(lines)):
			lines[i].strip()
			line = lines[i].find(self.char_comment)
			if (line != -1):
				line_splt=lines[i].split(self.char_comment)
				lines[i]=line_splt[0].strip() # maintain part before comment character
		
		has_line_comment = True
		while has_line_comment:
			line_sizes =[]
			for i in range(0,len(lines)):
				line_sizes.append(len(lines[i]))
			# print("line sizes: ",line_sizes)
			try:
				indx =line_sizes.index(0) # since the initial part will have length 0
				del lines[indx]
			except:
				has_line_comment = False
				break
		
		

	def remove_commas(self,lines):
		# remove commas from source code
		for i in range(0,len(lines)):
			line = lines[i].find(",")
			if (line != -1):
				lines[i]=lines[i].replace(","," ")
		
	def remove_spaces(self,lines):
		# remove spaces from source code
		for i in range(0,len(lines)):
			lines[i]=lines[i].split()	
	
	
	def replace_labels_to_start_addresses(self):
		# replace labels start address of the next line
		# print(self.all_lines_info)
		for i,key in enumerate(self.labels):
			# print(self.labels)
			# print("key: ",key)
			label = key
			label_value = self.labels[label]

			self.labels[key]=self.all_lines_info[str(self.labels[key])]["start"]
			# print(self.labels)

			# delete the lable line at i
			del self.all_lines[label_value]
			

	def process_string(self,lines):
		# change string data values to hex
		for i in range(0,len(lines)):
			line = lines[i].find('"') or lines[i].find("'") # double qute string priority, single string prioty : change order for preference
			if(line != -1):
					my_string_list = re.findall(r'"([^"]*)"', lines[i]) or re.findall(r"'([^']*)'", lines[i])
					
					for j in range(0,len(my_string_list)):
							replace_with = ""
							my_string= my_string_list[j]
							for k in range(0,len(my_string)):
								replace_with= replace_with +" "+ str(hex(ord(my_string[k])))[2:]
							lines[i] = replace_with
							return replace_with

	def process_line(self,lines):
		# replace string values with hex 
		self.process_string(lines)

	def process_string_segment(self,i,j,seg):
             
		replace_with = ""
		if(len(seg) == 1):
			replace_with = hex(ord(seg)) 
		else:   
			for j in range(0,len(seg)+1):
					
					replace_with += hex(ord(seg[j]))
		self.all_lines[i][j] = replace_with           
		return replace_with


	def preprocess(self,lines):
		# first run: comments, 
		# self.get_preprocessor_directives(lines)
		self.remove_comments(lines)
		
		# second run: string to hex, commas, remove spaces, get labels and line numbers store in dictionary, labels{}
		
		self.get_labels(lines)
		self.remove_commas(lines)
		self.remove_spaces(lines)
		
		utils.update_line_information(self.start_memory_location,lines,self.all_lines_info)
		
		# self.replace_labels_to_start_addresses()
		# third run: change instructions to hex, everything to 4 bytes
		
		# start with labels to  hex
		self.replace_labels_to_start_addresses()
		

	def compile(self,file2,interm):
		'''
			change to 4 bit byte code
			opcode register = 0x00
			R1 = 0x01
			R2 = 0x02
			R3 = 0x03
			PC = 0x04
			COND = 0x05
		'''
		
		lines = self.all_lines
		for i in range(0,len(lines)):   
			start_val = self.all_lines_info[str(i)]["start"]
			line_compiled = f"{start_val}"
			# replace label with label memory address
			for j in range(0,len(lines[i])):
				seg = lines[i][j]
				if seg in self.labels.keys():
					lines[i][j] = self.labels[seg]
				
			# replace label with label memory address
			for j in range(0,len(lines[i])):
				code = lines[i][j]
				if code in self.opcode_table.keys():
					lines[i][j] = self.opcode_table[code][0]

			# replace registers with hex values		
			for j in range(0,len(lines[i])):
				reg = lines[i][j]
				line_compiled = line_compiled +" "+code
				if reg in self.register_names.keys():
					lines[i][j] = self.register_names[reg]

		
			# if interm:
			with open("intermidiate.s", 'w', encoding='utf-8') as f1:
				current_line=f""
				for l in range(len(lines)):
					for j in range(len(lines[l])):
						current_line = current_line+" "+str(lines[l][j])
				
					f1.write(f"{current_line}\n")
					current_line=f""

			
			inst=self.compiled_to_instruction(lines[i])
			# with open(file2, 'w', encoding='utf-8') as f:
			current_line=f""
			vals =[]
			for j in range(len(inst)):
				vals=vals+inst[j]
			for k in range(0,len(vals)):
				current_line = current_line+str(vals[k])
				# current_line = current_line+" "+str(vals[k])

			self.compiled_lines.append(current_line)
			current_line=f""
			vals =[]

		with open(file2, 'w', encoding='utf-8') as f:
			f.writelines(f"{l}\n" for l in self.compiled_lines) 		



	def compiled_to_instruction(self,compiled_line):
		instruction = [[],[],[],[]]
		
		if len(compiled_line)==4:
			for i in range(0,len(compiled_line)):
				# 0x0C 0x00 0x01 0x02
				#to
				# 1100 0010 0001 0001
				instruction[i][:] = f"{eval(compiled_line[i]):04b}"
			
		elif len(compiled_line)==3:
			for i in range(0,len(compiled_line)):
				if i == 2:
					third = f"{eval(compiled_line[i]):04b}"

					if len(third)>4:
						third = f"{eval(compiled_line[i]):08b}"
						# also upper higher bits have a value
						instruction[3][:] = third[-4:]
						instruction[2][:] = third[-8:-4]
					else:
						# also upper higher bits have no value
						instruction[3][:] = f"{0:04b}"
						instruction[2][:] = third

				else:
					# 0x0C 0x01 
					#to
					# 1100 0001 0000 0000
					instruction[i][:] = f"{eval(compiled_line[i]):04b}"
				

		elif len(compiled_line)==2:
			for i in range(0,len(compiled_line)):
				# 0x0C 0x01 
				#to
				# 1100 0001 0000 0000
				instruction[i][:] = f"{eval(compiled_line[i]):04b}"
			instruction[2][:] = f"{0:04b}"
			instruction[3][:] = f"{0:04b}"
			

		elif len(compiled_line)==1:
			for i in range(0,len(compiled_line)):
				# 0x0C 
				#to
				# 1100 0000 0000 0000
				instruction[i][:] = f"{eval(compiled_line[i]):04b}"

			instruction[1][:] = f"{0:04b}"
			instruction[2][:] = f"{0:04b}"
			instruction[3][:] = f"{0:04b}"

		# print(instruction)
		return instruction

		