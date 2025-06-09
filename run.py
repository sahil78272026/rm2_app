from app import app


app.route('ping/')
def ping():
    return 'pong'

if __name__=='__main__':
    app.run()