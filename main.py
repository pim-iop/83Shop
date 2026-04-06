from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# 📁 File path (you can keep Desktop path)
FILE_PATH = "C:/Users/p_pha/Desktop/shared_data/room_data.txt"

# 🔥 AUTO CREATE FOLDER + FILE (THIS FIXES YOUR ERROR)
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

if not os.path.exists(FILE_PATH):
    open(FILE_PATH, "w", encoding="utf-8").close()


# 🏠 Room page
@app.route("/")
def home():
    return render_template("index.html")


# 📤 Handle form
@app.route("/send", methods=["POST"])
def send():
    room = request.form.get("room")
    message = request.form.get("message")

    with open(FILE_PATH, "a", encoding="utf-8") as f:
        f.write(f"{room}|{message}|0\n")

    return redirect("/")


# 📺 Admin page
@app.route("/admin_food")
def admin_food():
    data = []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        lines = []

    for i, line in enumerate(lines):
        if "|" in line:
            parts = line.strip().split("|")
            if len(parts) == 3:
                room, message, status = parts
            elif len(parts) == 2:
                room, message = parts
                status = "0"  # default for old entries
            else:
                continue
            data.append((i, room, message, status))

    return render_template("admin_food.html", data=data)


@app.route("/complete_order/<int:order_id>", methods=["POST"])
def complete_order(order_id):
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if order_id < len(lines):
            parts = lines[order_id].strip().split("|")
            if len(parts) >= 2:
                room = parts[0]
                message = parts[1]
                lines[order_id] = f"{room}|{message}|1\n"
                
                with open(FILE_PATH, "w", encoding="utf-8") as f:
                    f.writelines(lines)
    except:
        pass

    return redirect("/admin_food")

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/admin")
def admin():
    return render_template("admin.html")
@app.route("/buy")
def buy():
    return render_template("buy.html")


@app.route("/room")
def room():
   return render_template("room.html")

@app.route("/FoiThong")
def FoiThong():
   return render_template("FoiThong.html")

# ▶️ Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)