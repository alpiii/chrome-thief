import os
import sys
import sqlite3
import win32crypt

def getFilePath():
    """
    If the running operating system is Windows, returns the local path of the database file
    :return: Path of the database file
    """
    if os.name == "nt":
        # windows path
        path = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
        if os.path.isdir(path) == False: # if directory doesn't exist, Chrome is not installed on the machine
            print "Chrome isn't installed on this machine!"
            sys.exit(0)
        else:
            return path
    else:
        print "Supporting only Windows Operating System!"
        sys.exit(0)

def readData(dbPath):
    """
    Fetches the datas from database file.
    :param dbPath: Local path of the database file
    :return: Database table records
    """
    try:
        cn = sqlite3.connect(dbPath + "Login Data") # Login Data is the database file name
        cursor = cn.cursor()
        r = cursor.execute('select action_url, username_value, password_value from logins')
        rows = r.fetchall()
        cn.close()
        return rows
    except sqlite3.OperationalError, err:
        err = str(err)
        if err == 'database is locked':
            print "Can't get datas while Google Chrome is running!"
        else:
            print 'Error : ' + err
        sys.exit(0)

def printList(authList):
    """
    Prints the username-password list to the console
    :param authList: List that contains username, password and url informations
    """
    print '*' * 15 + str(len(authList)) + ' passwords found!' + '*' * 15
    for authInfo in authList:
        print 'Link : ' + authInfo['link']
        print 'User name : ' + authInfo['username']
        print 'Password : ' + authInfo['password']
        print '*' * 30

def main():
    dataList = readData(getFilePath())
    authList = [] # result list
    for data in dataList:
        password = win32crypt.CryptUnprotectData(data[2], None, None, None, 0)[1]  # decrypting the password
        if password:
            authList.append({'link': data[0], 'username': data[1], 'password': password})
    if len(authList)>0:
        printList(authList)
    else:
        print "Couldn't find a stored password on Google Chrome"

if __name__ == '__main__':
    main()
