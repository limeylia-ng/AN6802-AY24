from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import time, requests
import re
import os
import threading
import markdown

app = Flask(__name__)

flag = True

# Get API
api = os.getenv("makersuite")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)

telegram_api = os.getenv("telegram")
url = f"https://api.telegram.org/bot{telegram_api}/"

@app.route("/", methods=["POST", "GET"])
def index():
    return (render_template("index.html"))

@app.route("/main", methods=["POST", "GET"])
def main():
    global flag
    if flag:
        t = datetime.datetime.now()
        user_name = request.form.get("q")
        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        c.execute("insert into user (name, timestamp) values (?,?)",(user_name,t))
        conn.commit()
        c.close()
        conn.close()
        flag = False
    return (render_template("main.html"))

@app.route("/foodexp", methods=["POST", "GET"])
def foodexp():
    return (render_template("foodexp.html"))

@app.route("/foodexp_pred", methods=["POST", "GET"])
def foodexp_pred():
    q = float(request.form.get("q"))
    return (render_template("foodexp_pred.html", r=(q*0.4851)+147.4))

@app.route("/ethical_test", methods=["POST", "GET"])
def ethical_test():
    return (render_template("ethical_test.html"))

@app.route("/test_result", methods=["POST", "GET"])
def test_result():
    answer = request.form.get("answer")
    if answer == "false": 
        return (render_template("pass.html"))
    elif answer == "true":
        return (render_template("fail.html"))
    
@app.route("/FAQ", methods=["POST", "GET"])
def FAQ():
    return (render_template("FAQ.html"))
    
@app.route("/FAQ1", methods=["POST", "GET"])
def FAQ1():
    r = model.generate_content("Factors for Profit")
    r = r.candidates[0].content.parts[0].text
    return (render_template("FAQ1.html",r=r))

@app.route("/FAQinput", methods=["POST", "GET"])
def FAQinput():
    q = request.form.get("q")
    r = model.generate_content(q)
    r = markdown.markdown(r.text)
    r = re.sub(r'<.*?>', '', r)
    return (render_template("FAQinput.html",r=r))

@app.route("/telegram", methods = ['POST','GET'])
def telegram():
    return(render_template("telegram.html"))

def predict_default(salary):
    prompt = f"A person with a salary of ${salary} is likely to:"
    response = model.generate_content(prompt)
    return response.candidates[0].content.parts[0]
  
@app.route('/start_telegram', methods=['GET','POST'])
def start_telegram():
    thread = threading.Thread(target=run_telegram_bot)
    thread.daemon = True
    thread.start()
    return render_template("main.html")

def run_telegram_bot():
    flag = ""
    # chat = "7494700360"
    chat = "6466874020"
    prompt = "Please enter your salary and Gemini will judge it: (Type 'break' to exit)"
    while True:
        try:
            msg = url + f"sendMessage?chat_id={chat}&text={prompt}"
            requests.get(msg)
            time.sleep(5)
            r = requests.get(url + 'getUpdates')
            r = r.json()
            r = r['result'][-1]['message']['text']
            if r == "break":
                break
            if flag != r:
                flag = r
                if r.isnumeric():
                    # Make prediction
                    prediction = predict_default(r)
                    cleaned_text = f"{prediction}".replace('**', '')

                    # Remove the word "text:" at the beginning, if it exists
                    text = re.sub(r'^text:\s*', '', cleaned_text)

                    # Remove bullet points (* ) at the beginning of lines
                    text = re.sub(r'^\s*\*\s+', '', text, flags=re.MULTILINE)

                    # Remove extra newlines and replace them with spaces
                    text = text.replace('\\n', ' ').replace("\\n\n", "").replace("\n\n\n", "")

                    # Remove surrounding quotes (if any)
                    text = text.strip('"')

                    # Remove any remaining asterisks (*)
                    text = text.replace('*', '')

                    # Remove extra spaces caused by replacements
                    text = ' '.join(text.split())

                    # Print prediction
                    msg = url + f"sendMessage?chat_id={chat}&text={text}"
                    requests.get(msg)
                else:
                    msg = url + f"sendMessage?chat_id={chat}&text={r} is not a number"
                    requests.get(msg)
            time.sleep(8)  
        except Exception as e:
            print(f"Error in Telegram bot: {e}")
            time.sleep(10)         
    
@app.route("/userLog", methods=["POST", "GET"])
def userLog():
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute("select *  from user")
    r= ""
    for row in c:
        r = r + str(row) + "\n"
    print(r)
    c.close()
    conn.close()
    return (render_template("userLog.html", r=r))

@app.route("/deleteLog", methods=["POST", "GET"])
def deleteLog():
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return (render_template("deleteLog.html"))

if __name__ == "__main__":
    app.run(debug=True)