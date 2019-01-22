def getpass():

  with open('pwsf.txt', 'r') as myfile:
      data=myfile.read().replace('\n', '')
  password = "TC" + str(data[4:10]) + "9000"
  return password  
