from spintop import Spintop

if __name__ == '__main__':
    client = Spintop(api_url='http://localhost:5000')
    client.login()