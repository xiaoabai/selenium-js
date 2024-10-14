from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def encrypt_password(driver, password):
    """调用页面的encryptPwd函数并返回结果"""
    try:
        #这里是修改加密函数以及参数的地方，多个参数修改函数的形参
        return driver.execute_script('return encryptPwd(arguments[0]);', password)
    except Exception as e:
        print(f"Error executing script: {e}")
        return None

# 将映射关系打印到终端
def mapping(passwords,encrypted_passwords):
    for original, encrypted in zip(passwords, encrypted_passwords):
        print(f"{original} -> {encrypted}")

if __name__ == '__main__':
    # 启动Chrome浏览器
    service = Service('/Users/xx/xx/xx/chromedriver-mac-x64/chromedriver')
    # 配置无头浏览器选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 启用无头模式
    chrome_options.add_argument('--no-sandbox')  # 针对某些环境的配置
    chrome_options.add_argument('--disable-dev-shm-usage')  # 解决共享内存不足

    # 启动Chrome浏览器
    driver = webdriver.Chrome(service=service,options=chrome_options)

    # 替换为实际的网站地址
    driver.get('https://xx.xx.xx.xx:port/xx/login.jsp')

    # 示例批量处理
    passwords = [123456, 654321, 111111, 'abcdef']
    encrypted_passwords = []

    for pwd in passwords:
        encrypted = encrypt_password(driver, pwd)
        if encrypted is not None:
            encrypted_passwords.append(encrypted)

    mapping(passwords,encrypted_passwords)

    # 关闭浏览器
    driver.quit()
