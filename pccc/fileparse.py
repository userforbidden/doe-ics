'''
Created on Feb 9, 2017

@author: Saranyan
'''
import os
import sys
import string
import struct
import filecap
import binascii
import ConfigParser
import types
from sys import stdout
from ladderDrawer import ladderDrawer

class fileparse():
    
    
    def __init__(self):
      pass
      #print "fileparse Initiated"
      
    smtplist = []
    all_config = []
    all_rungs = []
    all_instructions = []
    allRungFileList = []
    branch_instructions = []
    fileNameDir = []
    saveDir = ""
    cont_flag = ""
    cont_flag_list = []
    printoutput = ""
    #instructions Configuration stored in this file
    instruc_Settings = ConfigParser.RawConfigParser()
    instruc_Settings.read('instructionsConfig.ini')
    #details about Data files are stored in this config file
    datafile_config = ConfigParser.RawConfigParser()
    datafile_config.read('datafileconfig.ini')
    datafileCount = 1
    #ld = ""
    #test by pranita
    
    def fileFinder(self,strfile,filetype):
      #open the file in Binary read mode
      self.fileNameDir = strfile.split('/')
      #print self.fileNameDir
      dirlen = len(self.fileNameDir)
      for fol in range(1, (dirlen-1)):
	self.saveDir += '/'+str(self.fileNameDir[fol])#+'/'+str(self.fileNameDir[2])+'/'+str(self.fileNameDir[3])+'/'+str(self.fileNameDir[4])+'/'+str(self.fileNameDir[5])+'/'+str(self.fileNameDir[6])
      #print self.saveDir
      with open(strfile, 'rb') as f:
      #check for file number 04 and file  
	if (filetype == '4C'):
       
	  buffer = f.read()  
	  nb = ''.join([ buffer[x:x+2][::-1] for x in range(0, len(buffer), 2) ])
	  self.smtplist.insert(0,nb[0:15])
	  self.smtplist.insert(1,nb[16:79])
	  self.smtplist.insert(2,nb[80:143])
	  self.smtplist.insert(3,nb[144:207])
	  self.smtplist.insert(4,nb[208:271])
	  self.smtplist.insert(5,nb[272:335])
	  self.smtplist.insert(6,nb[336:399])
	  self.smtplist.insert(7,nb[400:463])
	  self.smtplist.insert(8,nb[464:527])
	  self.smtplist.insert(9,(nb[528:559] + nb[562:593]))
	  self.smtplist.insert(10,(nb[594:641] + nb[643:659]))
	  self.smtplist.insert(11,nb[660:723])
	  self.smtplist.insert(12,nb[726:789])
	  self.smtplist.insert(13,(nb[790:805] + nb[808:855]))
	  self.smtplist.insert(14,nb[856:915])
	  #print chr(smtplist[0][3])
	  if (ord(self.smtplist[0][0]) == 0 and ord(self.smtplist[0][1]) == 9 and ord(self.smtplist[0][2]) == 3 and ord(self.smtplist[0][3]) == 140):
	    print "SMTP file signature matches"
	    if ord(self.smtplist[1][1]) > 0:
		print "Email Server: " + str(self.smtplist[1][2:])
	    else:
		print "Email server Not Configured"
	    if ord(self.smtplist[2][1]) > 0:
		print "From Address: " + str(self.smtplist[2][2:])
	    else:
		print "From Address: Not Configured"
	    if ord(self.smtplist[3][1]) > 0:
		print "Username:" + str(self.smtplist[3][2:])
	    else:
		print "Username: Not Configured"
	    if ord(self.smtplist[4][1]) > 0:
		print "Password: " + str(self.smtplist[4][2:])
	    else:
		print "Password Not Configured"
	    if ord(self.smtplist[5][1]) > 0:
		print "To Address[1]: " + str(self.smtplist[5][2:])
	    else:
		print "To Address[1]: Not Configured"
	    if ord(self.smtplist[6][1]) > 0:
		print "To Address[2]: " + str(self.smtplist[6][2:])
	    else:
		print "To Address[2]: Not Configured"
	    if ord(self.smtplist[7][1]) > 0:
		print "To Address[3]: " + str(self.smtplist[7][2:])
	    else:
		print "To Address[3]: Not Configured"
	    if ord(self.smtplist[8][1]) > 0:
		print "To Address[4]: " + str(self.smtplist[8][2:])
	    else:
		print "To Address[4]: Not Configured"
	    if ord(self.smtplist[9][1]) > 0:
		print "To Address[5]: " + str(self.smtplist[9][2:])
	    else:
		print "To Address[5]: Not Configured"
	    if ord(self.smtplist[10][1]) > 0:
		print "To Address[6]: " + str(self.smtplist[10][2:])
	    else:
		print "To Address[6]: Not Configured"
	    if ord(self.smtplist[11][1]) > 0:
		print "To Address[7]: " + str(self.smtplist[11][2:])
	    else:
		print "To Address[7]: Not Configured"
	    if ord(self.smtplist[12][1]) > 0:
		print "To Address[8]: " + str(self.smtplist[12][2:])
	    else:
		print "To Address[8]: Not Configured"
	    if ord(self.smtplist[13][1]) > 0:
		print "To Address[9]: " + str(self.smtplist[13][2:])
	    else:
		print "To Address[9]: Not Configured"
	    if ord(self.smtplist[14][1]) > 0:
		print "To Address[10]: " + str(self.smtplist[14][2:])
	    else:
		print "To Address[10]: Not Configured"
	  #if not an SMTP file remove it  
	  else:
	    print "This is not smtp file"
	#tell parser is not configured to parse this file      
	elif filetype == '85':
	  if self.fileNameDir[dirlen-1][8:] != 'Type:85':
	      print "Give a Valid Binary Data file for parsing"
	      sys.exit(0)
	  buf = f.read()
	  nb = ''.join([ buf[x:x+2][::-1] for x in range(0, len(buf), 2) ])
	  hexx = binascii.hexlify(nb)
	  #print hexx
	  indi = filecap.borders(hexx,4)
	  print indi
	  print "Data present in file : " + strfile 
	  for i,j in enumerate(indi):
	    #print dir(i)
	    print "Index:" + str(i) + " =" ,
	    #y = str(struct.unpack("h",str(j)))
	    #print y
	    print bin(int(j,16))[2:].zfill(16)
	    
	elif filetype == '82':
	  if self.fileNameDir[dirlen-1][8:] != 'Type:82':
	      print "Give a Valid Output Data file for parsing"
	      sys.exit(0)
	  buf = f.read()
	  nb = ''.join([ buf[x:x+2][::-1] for x in range(0, len(buf), 2) ])
	  hexx = binascii.hexlify(nb)
	  #print hexx
	  indi = filecap.borders(hexx,4)
	  print indi
	  print "Data present in file : " + strfile 
	  for i,j in enumerate(indi):
	    #print dir(i)
	    print "Index:" + str(i) + " =" ,
	    #y = str(struct.unpack("h",str(j)))
	    #print y
	    print bin(int(j,16))[2:].zfill(16)
	elif filetype == '89':
	  if self.fileNameDir[dirlen-1][8:] != 'Type:89':
	      print "Give a Valid Integer Data file for parsing"
	      sys.exit(0)
	  buf = f.read()
	  indi = filecap.borders(buf,2)
	  print "Data present in file : " + strfile 
	  for i,j in enumerate(indi):
	    #print dir(i)
	    print "Index:" + str(i) + " =" ,
	    y = str(struct.unpack("h",str(j)))
	    print y.split('(')[1].split(',')[0]
	
	elif filetype == '86':
	  if self.fileNameDir[dirlen-1][8:] != 'Type:86':
	      print "Give a Valid Timer Data file for parsing"
	      sys.exit(0)
	  timbuf = f.read()
	  ntb = ''.join([ timbuf[x:x+2][::-1] for x in range(0, len(timbuf), 2) ])
	  thexx = binascii.hexlify(ntb)
	  indi_t = filecap.borders(thexx,12)
	  for i in range(0, len(indi_t)):
	    if indi_t[i][1:4] == "200":
	      print "T:"+ str(i)+ "/BASE:1.0" + "/PRE:"+ str(int(indi_t[i][4:8],16)) + "/ACC:"+ str(int(indi_t[i][8:],16))
	    elif indi_t[i][1:4] == "000": 
	      print "T:"+ str(i)+ "/BASE:0.01" + "/PRE:"+ str(int(indi_t[i][4:8],16)) + "/ACC:"+ str(int(indi_t[i][8:],16))
	    elif indi_t[i][1:4] == "100":
	      print "T:"+ str(i)+ "/BASE:0.001" + "/PRE:"+ str(int(indi_t[i][4:8],16)) + "/ACC:"+ str(int(indi_t[i][8:],16))
	    else:
	      print "T:"+ str(i)+ "/BASE:"+ str(indi_t[i][0:4]) + "/PRE:"+ str(int(indi_t[i][4:8],16)) + "/ACC:"+ str(int(indi_t[i][8:],16))
	    
	elif filetype == '22':
	    #print self.fileNameDir[dirlen-1][7:]
	    if self.fileNameDir[dirlen-1][8:] != 'Type:22':
	      print "Give a Valid Ladder file for parsing"
	      sys.exit(0)
	      
	    with open(self.saveDir+'/file:00-Type:03', 'rb') as sf:
		buf = sf.read()
		nb = ''.join([ buf[x:x+2][::-1] for x in range(0, len(buf), 2) ])
		hexx = binascii.hexlify(nb)
		#The Data files start from the 134th Byte 
		start_bit = int(hexx[2:4],16)
		start_bit = start_bit - 2
		self.configSpliter(hexx[(start_bit*2):])
		#print self.all_config
		self.createFileConfig(self.all_config)
		self.ladderParser(f)
		self.printReadableInstruction(self.allRungFileList)
		
		#ld = ladderDrawer()
	        #saveDir1 = str(self.saveDir) + '/ImageResults/'#+str(self.fileNameDir[5])+'/'
	        ##print saveDir1
	        #ld.setSaveDir(saveDir1)
		#ld.setFilepath(self.allRungFileList)
	      #print fl
	      #ld.combineImageHorizontally(fl,imagename)
	      #print ld.getAllFilePath()
	  
	elif filetype == '03':
	  if self.fileNameDir[dirlen-1][8:] != 'Type:03':
	      print "Give a Valid System file for parsing"
	      sys.exit(0)
	  buf = f.read()
	  nb = ''.join([ buf[x:x+2][::-1] for x in range(0, len(buf), 2) ])
	  hexx = binascii.hexlify(nb)
	  print "Processor name: " + str(buf[2:10])
	  
	  #The Data files start from the 134th Byte 
	  start_bit = int(hexx[2:4],16)
	  start_bit = start_bit - 2
	  self.configSpliter(hexx[(start_bit*2):])
	  #print self.all_config
	  self.createFileConfig(self.all_config)
	  print "Number of Data Files Configured: " + str(self.datafileCount)
       
	else:
	  print "parser is not configured to parse this filenumber and filetype combination"
	  #continue
	
    def ladderParser(self, f1):
	
	try:
	    buf = f1.read()
	    nb = ''.join([ buf[x:x+2][::-1] for x in range(0, len(buf), 2) ])
	    hexx = binascii.hexlify(nb)
	    #print hexx
	    self.rungSplitter(hexx)
	    #print self.all_rungs
	    for i in range(0,len(self.all_rungs)):
	      del self.all_instructions[:]
	      self.instructionSplitter(self.all_rungs[i][12:])
	      #imagename = "Rung:"+str(i)
	      #print i,self.all_instructions
	      TEMP = []
	      for j in range(0,len(self.all_instructions)):
		    TEMP.append(self.all_instructions[j])
	      self.allRungFileList.append(TEMP)
	    #print self.allRungFileList

	except Exception as ex:
	    print "At ladderParser"
	    template = "{0}"
	    message = template.format(type(ex).__name__, ex.args)
	    print message
	    pass
      
    def createFileConfig(self,configList):
      #Separating the Data file's configuration and storing them as fileconfig.ini config File
	fileconfig = open(self.saveDir+'/fileconfig.ini','w')
	config = ConfigParser.RawConfigParser()
	dataconfig_num = 0
	for i in range(0,len(configList)):
	  try:
	     
	     filetype_num = configList[i][0:2]
	     data_code = self.datafile_config.get(filetype_num.upper(),'filetype')
	     data_denotion = self.datafile_config.get(filetype_num.upper(),'denotion')
	     #data_filenum = self.datafile_config.get(configList[i][2:4].upper(),'filenum')
	     stadd = int(configList[i][8:12],16)
	     dtsize = int(configList[i][6:8],16)
	     
	     #print data_code, stadd, dtsize
	     for i in range(0,dtsize):
		  nwsecaddress = stadd + i
		  sectionName = str(format(nwsecaddress,'02x').upper())
		  config.add_section(sectionName)
		  config.set(sectionName,'filetype',data_code)
		  config.set(sectionName,'filetypenumber',filetype_num)
		  config.set(sectionName,'dataconfignum',dataconfig_num)
		  config.set(sectionName,'denotion',data_denotion)
		  config.set(sectionName,'wordaddress',i)
		  #self.datafileCount += 1
	     
	     self.datafileCount = self.datafileCount + 1
	     
	     if self.datafile_config.has_section(filetype_num):
	       #print "I'm here"
	       dataconfig_num = dataconfig_num + 1
	       #self.datafileCount = dataconfig_num + 1
	       #print self.datafileCount
	  except Exception as ex:
	      template = "{0}"
	      message = template.format(type(ex).__name__, ex.args)
	      if message == "NoSectionError":
		pass#print "Data File is not configured in Configuration File"
	      else:
		print message
		pass
	config.write(fileconfig)
	fileconfig.close()
	#print "configfile created at " + self.saveDir+'/fileconfig.ini'
      
    def configSpliter(self,strn):
	try:
	    config = strn[0:20]
	    self.all_config.append(config)
	    rem = strn[20:]
	    if rem != "":
	      self.configSpliter(rem)    
	    
	except Exception as ex:
	    print "At config splitter"
	    template = "{0}"
	    message = template.format(type(ex).__name__, ex.args)
	    print message
	    pass
	    
    def rungSplitter(self,strn):
        try:
            sz_limit = int(strn[10:12],16)
            rung = strn[0:sz_limit*2]
            self.all_rungs.append(rung)
            rem = strn[sz_limit*2:]
            if rem != "":
	      self.rungSplitter(rem)
        except Exception as ex:
	    print " At Rung Splitter"
	    template = "{0}"
	    message = template.format(type(ex).__name__, ex.args)
	    print message
	    pass

    def instructionSplitter(self, strn):
	if strn[0:4].upper() == '0008':
	  self.branchedInstructionSplitter(strn[4:])
	  
	else:
	    try:
	      ins_inscode = self.instruc_Settings.get(strn[0:4].upper(),'inscode')
	      ins_size = self.instruc_Settings.getint(strn[0:4].upper(),'size')
	      instruc = strn[0:(ins_size*2)].upper()
	      #print strn,
	      self.all_instructions.append(instruc)
	      rem = strn[(ins_size*2):]
	      if rem != "":
		  self.instructionSplitter(rem)
	    except Exception as ex:
	      template = "{0}"
	      message = template.format(type(ex).__name__, ex.args)
	      if message == "NoSectionError":
		print strn,
		print " - This Instruction not configured in Configuration File -",
		print "length of this non-configured instruction = " + str(len(strn)/2)
	      elif message == "NoOptionError": 
		pass
	      elif message == "ValueError":
		instruc = strn[0:(ins_size*2)].upper()
		#instruc = str(ins_inscode)
		self.all_instructions.append(instruc)
	      else:
		print message
		pass
    def branchedInstructionSplitter(self,strn):
	#branch_instructions = []
	#print strn
	if strn[0:4].upper() == '0008':
	  self.cont_flag = 'F'
	  self.branchedInstructionSplitter(strn[4:])
	  
	  #print strn
	elif strn[0:4].upper() == "02D4":
	  #print "branch start" 
	  #print strn
	  self.cont_flag = 'F'
	  self.branchedInstructionSplitter(strn[4:])
	  
	elif strn[0:8].upper() == "02D00010":
	  #print "branch continues" 
	  #print strn
	  self.cont_flag = 'F'
	  self.branchedInstructionSplitter(strn[8:])
	  
	elif strn[0:8].upper() == "00140010":
	  #print "branch Continues"
	  self.cont_flag = 'F'
	  self.branchedInstructionSplitter(strn[8:])  
	  
	elif strn[0:8].upper() == "0014000C":
	  #print "branch end" 
	  #print strn
	  self.cont_flag = 'F'
	  if strn[8:16].upper() == "00140010":
	    #print " sub branch Continues"
	    self.branchedInstructionSplitter(strn[16:])
	  else:
	    #print self.branch_instructions
	    TEMP2 = []
	    for k in range(0,len(self.branch_instructions)):
		#print self.cont_flag_list[k]
		TEMP2.append(self.branch_instructions[k])
	    self.all_instructions.append(TEMP2)
	    #print self.all_instructions
	    del self.branch_instructions[:]
	    self.instructionSplitter(strn[8:])
  
	else:
	    try:
	      ins_inscode = self.instruc_Settings.get(strn[0:4].upper(),'inscode')
	      ins_size = self.instruc_Settings.getint(strn[0:4].upper(),'size')
	      #print "flag:" + self.cont_flag
	      b_instruc = str(self.cont_flag) + str(strn[0:(ins_size*2)].upper())
	      #b_instruc = str(strn[0:(ins_size*2)].upper())
	      self.cont_flag_list.append(self.cont_flag)
	      #print b_instruc
	      self.branch_instructions.append(b_instruc)
	      rem = strn[(ins_size*2):]
	      if rem != "":
		  self.cont_flag = 'T'
		  self.branchedInstructionSplitter(rem)
	      
		
	    except Exception as ex:
	      print "at branchedInstructionSplitter"
	      template = "{0}"
	      message = template.format(type(ex).__name__, ex.args)
	      if message == "NoSectionError":
		print strn
		print "Branched Instruction not configured in Configuration File",
	      elif message == "NoOptionError": 
		pass
	      elif message == "ValueError":
		instruc = strn[0:(ins_size*2)].upper()
		#instruc = str(ins_inscode)
		self.all_instructions.append(instruc)
	      else:
		print message
		pass  
    
    
    def printReadableInstruction(self,allrunglist):
	#print " at printReadableInstruction"
	  #print allrunglist
	#self.printoutput = ""
	#try:
	for i in range(0,len(allrunglist)):
	    #print allrunglist[i]
	    #print "(",
	    print "Rung-" + str(i) + ":",
	    if i == (len(allrunglist))-1:
	      self.printoutput = self.getConfigPrintSections(allrunglist[i][0])
	      print self.printoutput,
	    else:
	      for j in range(0, len(allrunglist[i])):
		#islist = isinstance(allrunglist[i][j], types.StringTypes)
		#print j, 
		if isinstance(allrunglist[i][j], types.StringTypes):
		  if j == (len(allrunglist[i])) - 1:
		    self.printoutput = self.getConfigPrintSections(allrunglist[i][j])
		    print "--> " + "("+str(self.printoutput)+")"
		  else:  
		    try:
		      self.printoutput = self.getConfigPrintSections(allrunglist[i][j])
		      if allrunglist[i][j+2] != '':
			print "("+str(self.printoutput)+")" + ' AND ',
		    except Exception as ex:
		      template = "{0}"
		      message = template.format(type(ex).__name__, ex.args)
		      #print " at printReadableInstruction" + message
		      if message == "IndexError":
			print "(" + str(self.printoutput) + ")",
			pass
		
		else:
		  print "(",
		  try:
		    if allrunglist[i][j+2] != '':
		      for k in range(0, len(allrunglist[i][j])):
			self.printoutput = self.getConfigPrintSections(allrunglist[i][j][k][1:])
			#print "(",
			if k == (len(allrunglist[i][j])) - 1:
			  if allrunglist[i][j][k][0] == 'T':
			    print self.printoutput + ")",
			  else:
			    print "(",
			    print self.printoutput + ")",
			else:
			  try:
			    #print "(",
			    if allrunglist[i][j][k+1][0] == 'T':
			      print "("+self.printoutput+ " AND",
			    else:
			      if allrunglist[i][j][k][0] == 'T':
				print self.printoutput + ")" + " OR",
			      else:
				print "(",
				print self.printoutput+")" + " OR",
			  except:
			    template = "{0}"
			    message = template.format(type(ex).__name__, ex.args)
			    #print " at printReadableInstruction" + message
			    if message == "IndexError":
			      print self.printoutput,
			      pass
		      print ")" + " AND",
		  except Exception as ex:
		      template = "{0}"
		      message = template.format(type(ex).__name__, ex.args)
		      #print " at printReadableInstruction" + message
		      if message == "IndexError":
			for k in range(0, len(allrunglist[i][j])):
			    self.printoutput = self.getConfigPrintSections(allrunglist[i][j][k][1:])
			    #print self.printoutput,
			    #print "(",
			    if k == (len(allrunglist[i][j])) - 1:
			      if allrunglist[i][j][k][0] == 'T':
				print self.printoutput + ")",
			      else:
				print "(",
				print self.printoutput + ")",
			    else:
			      try:
				#print "(",
				if allrunglist[i][j][k+1][0] == 'T':
				  print "("+self.printoutput+ " AND",
				else:
				  if allrunglist[i][j][k][0] == 'T':
				    print self.printoutput + ")" + " OR",
				  else:
				    print "(",
				    print self.printoutput+")" + " OR",
			      except:
				template = "{0}"
				message = template.format(type(ex).__name__, ex.args)
				#print " at printReadableInstruction" + message
				if message == "IndexError":
				  print self.printoutput,
				pass
			print ")",
			pass     
 
		    
    def getConfigPrintSections(self,strn):
      	#print self.instruc_Settings.sections()  
      	ins_inscode = ''
      	ins_size = ''
      	ins_opcode = ''
      	ins_instype = ''
      	ins_fe = 0 
      	ins_fs = 0
      	ins_be = 0 
      	ins_bs = 0
      	ins_timebase = ''
	file_config_path = self.saveDir +'/fileconfig.ini'
	#print file_config_path
	file_Settings = ConfigParser.RawConfigParser()
	file_Settings.read(file_config_path)
	#print file_Settings
	try:
	  #print strn[0:4]
	  #ins_name = self.instruc_Settings.get(strn[0:4].upper(),'name')
	  for (each_key, each_val) in self.instruc_Settings.items(strn[0:4]):
	      if each_key == 'inscode':
		ins_inscode = each_val
	      elif each_key == 'size':
		ins_size = each_val
	      elif each_key == 'opcode':
		ins_opcode = each_val
	      elif each_key == 'filestart':
		ins_fs = int(each_val)
	      elif each_key == 'fileend':
		ins_fe = int(each_val)
	      elif each_key == 'bitstart':
		ins_bs = int(each_val)
	      elif each_key == 'bitend':
		ins_be = int(each_val)
	      elif each_key == 'instype':
		ins_instype = each_val
	      elif each_key == 'timebase':
		ins_timebase = each_val
	      elif each_key == 'fsstart':
		ins_sf_start = int(each_val) 	#Source file addresss start point
	      elif each_key == 'fsend':
		ins_sf_end = int(each_val)   	#Source file address end point 
	      elif each_key == 'fsbstart':
		ins_sfb_start = int(each_val)	#Source file bitaddress start point
	      elif each_key == 'fsbend':
		ins_sfb_end = int(each_val)	#Source file bitaddress end point
	      elif each_key == 'fostart':
		ins_of_start = int(each_val)	#Output file address start point
	      elif each_key == 'foend':
		ins_of_end = int(each_val)	#Output file address start point
	      elif each_key == 'fobstart':
		ins_ofb_start = int(each_val)	#Output file bitaddress start point
	      elif each_key == 'fobend':
		ins_ofb_end = int(each_val)	#Output file bit address end point
	      elif each_key == '1_var_start':
		ins_1var_start = int(each_val) 
	      elif each_key == '1_var_end':
		ins_1var_end = int(each_val)
	      elif each_key == '2_var_start':
		ins_2var_start = int(each_val) 
	      elif each_key == '2_var_end':
		ins_2var_end = int(each_val)
	      elif each_key == '3_var_start':
		ins_3var_start = int(each_val) 
	      elif each_key == '3_var_end':
		ins_3var_end = int(each_val)
	      else:
		continue
	  #print ins_instype
	  if ins_instype == 'bit':
	    ins_address = str(strn[(ins_fs*2):(ins_fe*2)]).upper()
	    bit_address = int(strn[(ins_bs*2):(ins_be*2)],16)
	    output = str(ins_inscode)+ "/" + self.getAddressOfDatafileinIns(ins_address, bit_address, 'TRUE')
	  elif ins_instype == 'longbit':
	    sf_address = str(strn[(ins_sf_start*2):(ins_sf_end*2)]).upper()
	    sf_bit_address = int(strn[(ins_sfb_start*2):(ins_sfb_end*2)],16)
	    of_address = str(strn[(ins_of_start*2):(ins_of_end*2)]).upper()
	    of_bit_address = int(strn[(ins_ofb_start*2):(ins_ofb_end*2)],16)
	    if ins_inscode == 'RHC':
	      output = str(ins_inscode) + "/" + self.getAddressOfDatafileinIns(sf_address, sf_bit_address, 'FALSE')
	    else:
	      output = str(ins_inscode) + "/" + self.getAddressOfDatafileinIns(sf_address, sf_bit_address, 'TRUE') + "/" + self.getAddressOfDatafileinIns(of_address, of_bit_address, 'TRUE')
	    	    
	  elif ins_instype == 'end':
	     output = str(ins_inscode)
	  elif ins_instype == 'timer':
	    ins_address = str(strn[(ins_fs*2):(ins_fe*2)]).upper()
	    #print ins_address,
	    bit_address = int(strn[(ins_bs*2):(ins_be*2)],16)
	    ins_filetype = file_Settings.get(ins_address,'filetype')
	    ins_filetype_num = file_Settings.get(ins_address, 'filetypenumber')
	    ins_denotion = file_Settings.get(ins_address,'denotion')
	    ins_file_number = file_Settings.get(ins_address,'dataconfignum')
	    ins_wordaddress = file_Settings.getint(ins_address,'wordaddress')
	    
	    timedatafilename = self.saveDir + "/file:" + str(ins_file_number).zfill(2) + "-Type:" + ins_filetype_num
	    with open(timedatafilename, 'rb') as tf:
	      timbuf = tf.read()
	      ntb = ''.join([ timbuf[x:x+2][::-1] for x in range(0, len(timbuf), 2) ])
	      thexx = binascii.hexlify(ntb)
	      indi_t = filecap.borders(thexx,12)
	      #print indi_t[bit_address]
	      
	      if ins_inscode == 'RES':
		output = str(ins_inscode) + "/[" + str(ins_denotion)+str(ins_file_number)+":"+ str(bit_address)+"]"
	      elif ins_denotion == 'T':
		output = str(ins_inscode)+"/["+str(ins_denotion)+str(ins_file_number)+":"+ str(bit_address)+"/"+str(ins_timebase)+"/"+str(int(indi_t[bit_address][5:8],16))+"/"+str(int(indi_t[bit_address][10:12],16))+"]"  
	      else: 
		output = str(ins_inscode)+"/["+str(ins_denotion)+str(ins_file_number)+":"+ str(bit_address)+"/"+str(int(indi_t[bit_address][5:8],16))+"/"+str(int(indi_t[bit_address][10:12],16))+"]"
	      
	  elif ins_instype == 'compare1':
	    first_address = str(strn[(ins_1var_start*2):(ins_1var_end*2)]).upper()
	    second_address = str(strn[(ins_2var_start*2):(ins_2var_end*2)]).upper()
	    third_address = str(strn[(ins_3var_start*2):(ins_3var_end*2)]).upper()
	    
	    if ins_inscode == 'LIM':
	      output = str(ins_inscode) + "/" + self.getAddressOfDatafileinIns(third_address[0:4], int(third_address[4:],16), 'FALSE') + "/" + self.getAddressOfDatafileinIns(first_address[0:4], int(first_address[4:],16), 'FALSE') + "/" + self.getAddressOfDatafileinIns(second_address[0:4], int(second_address[4:],16), 'FALSE')
	    elif ins_inscode == 'MEQ':
	      output = str(ins_inscode) + "/" + self.getAddressOfDatafileinIns(first_address[0:4], int(first_address[4:],16), 'FALSE') + "/" + self.getAddressOfDatafileinIns(second_address[0:4], int(second_address[4:],16), 'FALSE') + "/" + self.getAddressOfDatafileinIns(third_address[0:4], int(third_address[4:],16), 'FALSE')
	    else:
	      output = str(ins_inscode) + "/" + self.getAddressOfDatafileinIns(third_address[0:4], int(third_address[4:],16), 'FALSE') + "/" + self.getAddressOfDatafileinIns(first_address[0:4], int(first_address[4:],16), 'FALSE') + "/" + self.getAddressOfDatafileinIns(second_address[0:4], int(second_address[4:],16), 'FALSE')
	  else:
	     output = str(ins_inscode) + "/" + strn 
	  return output


	except Exception as ex:
	  template = "{0}"
	  message = template.format(type(ex).__name__, ex.args)
	  print "At getConfigPrintSections:" + message
	  if message == "NoSectionError":
		print strn
		print "Instruction not configured in Configuration File",
	  elif message == "NoOptionError": 
		pass
	  elif message == "ValueError":
		instruc = strn[0:(ins_size*2)].upper()
		#instruc = str(ins_inscode)
		self.all_instructions.append(instruc)
	  else:
		print message
		pass  
    
    
    def getAddressOfDatafileinIns(self, ins_address, bitaddress, bitflag):
	#print ins_address, bitaddress
	dec_value = 0
	file_config_path = self.saveDir +'/fileconfig.ini'
	file_Settings = ConfigParser.RawConfigParser()
	file_Settings.read(file_config_path)
	try:
	  denotion = file_Settings.get(ins_address,'denotion')
	  file_number = file_Settings.get(ins_address,'dataconfignum')
	  wordaddress = file_Settings.getint(ins_address,'wordaddress')
	  if denotion == 'T':
	      #print ins_wordaddress
	      b = wordaddress/6
	      bit = (wordaddress*8) + bitaddress
	      c,d = divmod(bit,3)
	      #print b,c
	      gg = self.datafile_config.get('TIMERCONFIG',str(d))
	      fileaddress = "["+str(denotion)+str(file_number)+":"+str(b)+"/"+gg+"]"#+strn
	  elif denotion == 'C':
	      #print ins_wordaddress
	      b = wordaddress/8
	      bit = (wordaddress*8) + bitaddress
	      c,d = divmod(bit,6)
	      #print b,c
	      gg = self.datafile_config.get('COUNTERCONFIG',str(d))
	      fileaddress = "["+str(denotion)+str(file_number)+":"+str(b)+"/"+gg+"]"#+strn
	  elif denotion == 'R':
	      #print ins_wordaddress
	      b = wordaddress/10
	      bit = (wordaddress*8) + bitaddress
	      c,d = divmod(bit,10)
	      #print b,c
	      gg = self.datafile_config.get('CONTROLCONFIG',str(d))
	      fileaddress = "["+str(denotion)+str(file_number)+":"+str(b)+"/"+gg+"]"#+strn
	  else:
	      #print denotion, bitaddress, wordaddress, file_number, inscode
	      bit = (wordaddress*8) + bitaddress
	      b,c = divmod(bit,16)
	      if bitflag == 'TRUE':
		fileaddress =  "["+str(denotion)+str(file_number)+":"+str(b)+"/"+str(c)+"]"#+strn
	      else:
		fileaddress =  "["+str(denotion)+str(file_number)+":"+str(b)+"]"#+strn
	
	  return fileaddress
	except Exception as ex:
	  template = "{0}"
	  message = template.format(type(ex).__name__, ex.args)
	  #print "At getAddressOfDatafileinIns:" + message
	  if message == "NoSectionError":
		return str(int(str(ins_address) + str(bitaddress)))
	  elif message == "NoOptionError": 
		pass
	  elif message == "ValueError":
		instruc = strn[0:(ins_size*2)].upper()
		#instruc = str(ins_inscode)
		self.all_instructions.append(instruc)
	  else:
		print message
		pass
      
    def setAllFilePath(self, strn):
        print self.imagePathForVerticalMerging
        self.imagePathForVerticalMerging.append(strn)
        print self.imagePathForVerticalMerging
    
    def getAllFilePath(self):
        #del self.imagePathForHorizontalMerging[:]
        return self.imagePathForVerticalMerging
        #del self.imagePathForVerticalMerging[:]
    
   
def main():
    #check for command line arguments
    if len(sys.argv) < 3 :
	print "Usage python fileparse.py filetype filepath "
	#print " FileNumber can be 00 to 254"
	print " FileType can be 00 to 254"
	print " Storage path is where the PLC file dumps are stored"
	sys.exit()
    else:
	#filenumber = (str(sys.argv[1])).upper()
	filetype = (str(sys.argv[1])).upper()
	strfile = str(os.path.abspath(sys.argv[2]))
	dial = fileparse()
	dial.fileFinder(strfile,filetype)
if __name__ == '__main__': 
    main()    
