from quart import Quart, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

app = Quart(__name__)

# 启动 Chrome 浏览器
service = Service('/Users/xx/xx/xx/chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service=service)
driver.get('https://xx.xx.xx.xx:port/xx/xx.jsp')  # 替换为包含js的实际地址

def encrypt_password(driver, password):
    """调用页面的 encryptPwd 函数并返回结果"""
    try:
        return driver.execute_script('return encryptPwd(arguments[0]);', password)
    except Exception as e:
        print(f"Error executing script: {e}")
        return None

@app.route('/encrypt', methods=['POST'])
async def encrypt():
    data = await request.form
    # 获取用户请求的参数
    password = data.get('dataBody', '').strip()

    if not password:
        return jsonify({"error": "Password is required"}), 400

    try:
        # 使用 Selenium 执行加密
        encrypted_result = encrypt_password(driver, password)
        if encrypted_result is None:
            return jsonify({"error": "Failed to encrypt password"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 修改这里就是修改返回的数据
    response_data = (
        f"loginId={encrypted_result}&"
        "oldPassWord=679b458d243659fe83fd626f84d48b6c853c57284036f457eed31f6bfbd3125cf218f79f912be4f4cfc07062b09d8d2db461babaf0510c479229f7718577cba71b9dd99ea072eed325e50fe069b99d15fba441ff740616804ce96bc4cec2b92c3f0546868dac2e39dde6cbb89ba1cc2d80f8573354c11d113aa06e11ccee84ed&"
        "newPassWord=668480156ca536d21bb6d44928c2e7d0f794cb7a5c228a4c16b7f12e837be33b995009d889dbd08a7b3d14d404e7db8ea3735aa13e251b5c6c41c118cde432fe32964f10637221aa62703b8d4c79d4712a94de741bf35d630b598eb8f9ee8fe3295e18d45a49c2f86be8856b44bbb749736976d620ac3e1352647eaf671f2578&"
        "checkCode=76xab"
    )

    return response_data

@app.before_serving
async def startup():
    # 在服务器启动时可以添加其他初始化代码
    pass

@app.after_serving
async def cleanup():
    global driver
    try:
        if driver:
            driver.quit()
            driver = None
            print("Browser closed successfully")
    except Exception as e:
        print(f"Error closing browser: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=7001)
