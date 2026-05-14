from app.dashboard import app

if __name__ == "__main__":
    print("\n🚀 Dashboard running at: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000, host="127.0.0.1")
