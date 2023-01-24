
import os
import re

class Assembler():
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


	def __init__(self,base_dir):
		self.BASE_DIR =base_dir
		
		
	def readLines(self,file):
        # read file input
		full_file_path = os.path.join(self.BASE_DIR,file)
		self.file_name=file.split(".")[0] # ignore file extension for now
		
		try:
			with open(full_file_path) as f:
				# read lines and store all_lines[]
				self.all_lines=f.readlines()
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
	
	def update_line_information(self,lines):
		# update line info: {"0":[start_addres,end_address]}
		start_addr = self.start_memory_location
		end_addr = 0
		# lines_to_ignnore = list(self.preprocessor_commands.values())

		# not_updated = True
		
		# while not_updated:
		for i in range(0,len(lines)):
			# to help track the new lines being modified

			end_addr = start_addr+31
			info = {"start":hex(start_addr), "end":hex(end_addr)}
			self.all_lines_info[str(i)]= info
			start_addr=end_addr+1
		
			# not_updated = False



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
		
		self.update_line_information(lines)
		
		# self.replace_labels_to_start_addresses()
		# third run: change instructions to hex, everything to 4 bytes
		
		# start with labels to  hex
		self.replace_labels_to_start_addresses()
		

	def compile(self,file2):
		'''
			change to 4 bit byte code
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
			for j in range(0,len(lines[i])):
				code = lines[i][j]
				line_compiled = line_compiled +" "+code

			# change line to half-bytes [[opcode][R1][R2][R3][PC][COND][U][L]]
			instruction = [[],[],[],[],[],[],[],[]]
			for j in range(0,len(lines[i])):
				pass
		
		print(lines)	
		with open(file2, 'w', encoding='utf-8') as f1:
			current_line=f""
			for l in range(len(lines)):
				for j in range(len(lines[l])):
					current_line = current_line+" "+str(lines[l][j])
			
				f1.write(f"{current_line}\n")
				current_line=f""