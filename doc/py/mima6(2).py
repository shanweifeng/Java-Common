class PasswordTool:
    def __init__(self,password):
        #类的属性
        self.password = password
        self.password_strength=0
    def process_password(self):
        if len(self.password)>=8:
            self.password_strength += 1
        else:
            print("您输入的密码不够8位")
        if self.shu_zi():
            self.password_strength +=1
        else:
            print("请输入带有数字的密码")
        if self.zi_mu():
            self.password_strength +=1
        else:
            print("您输入的密码没有字母")
    #类的方法
    def shu_zi(self):
        has_shuzi = False
        for i in self.password:
            if i.isnumeric():
                has_shuzi = True
                break
        return has_shuzi

    def zi_mu(self):
        has_zimu = False
        for i in self.password:
            if i.isalpha():
                has_zimu = True
                break
        return has_zimu

class FileTool:
    def __init__(self,filepath):
        self.filepath=filepath
    def write_to(self):
        f=open(self.filepath,'a')
        f.write(line)
        f.close()
    def write_to(self):
        f=open(self.filepath,'r')
        lines=f.readlines()
        f.close()
        return lines
def main():
    try_times=5
    filepath="mans6.txt"
    file_tool = FileTool(filepath)
    while try_times>0:
        password=input("请输入密码：")
        password_tool = PasswordTool(password)
        password_tool.process_password()

        line="您输入的密码为{}，密码强度为{}".format(password,password_tool.password_strength) + "\n"
        file_tool.write_to(line)

        if password_tool.password_strength>=3:
            print('您输入的密码正确')
            break
        else:
            print("您输入的账号密码不符合规定")
            try_times -= 1

    if try_times<=0:
        print("输入次数过多，过会再试")
    lines= file_tool.write_to()
    print(lines)
if __name__ == '__main__':
    main()
