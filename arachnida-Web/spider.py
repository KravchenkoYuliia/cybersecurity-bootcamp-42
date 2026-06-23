import sys
import requests

def main():
    args = sys.argv[1:]
    if ( len(args) < 1 ):
        print(f"Error: give an URL")
        return 1

    try:
        response = requests.get(args[0])
        if ( response.status_code != 200 ):
            print(f"Error {response.status_code}")
            return 1
        print(f"Code: {response.status_code}\nContent: {response.content}")
    
    except requests.exceptions.RequestException:
        print(f"Error: invalid URL or inaccesible site")

if __name__=="__main__":
    main()