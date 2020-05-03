import requests
from requests.adapters import HTTPAdapter
from sys import argv

class ProxyHttpsChecker:
    def __init__(self, proxy_file, output_file):
        # Open proxy file
        proxy_file = open(proxy_file, 'r')

        # Get proxy list from file
        self.proxies = proxy_file.readlines()

        # Open output file
        self.output = open(output_file, 'w+')

        # Init counter
        self.counter = 0

        # Init session
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=1))

    @property
    def get_api_url(self):
        """Getter to API URL"""
        return "https://icanhazip.com"

    @property
    def total(self):
        return len(self.proxies)

    @property
    def success(self):
        return self.counter

    def get_proxies(self):
        """
        Get proxy list

        :returns list: A proxy list
        """
        # Return proxies
        return self.proxies

    def test_proxy(self, proxy):
        # Prepare proxy
        proxy = proxy.replace("\n", "")

        # Create proxy configuration
        configuration = {
            "https": f"https://{proxy}",
        }

        # Run request
        try:
            # Get response
            self.session.get(self.get_api_url,
                             proxies=configuration, timeout=3)

            # Save proxy
            self.save_proxy(proxy)

            # Return Success
            return True
        except requests.exceptions.ProxyError:
            # Return proxy error
            return "proxy_error"
        except requests.exceptions.ConnectionError:
            # Return connection error
            return "connection_error"

    def save_proxy(self, proxy):
        """Method to add proxy in output file"""
        # Prepare line
        line = f"{proxy}\n"

        # Add in counter
        self.counter += 1

        # Write line
        self.output.write(line)

# Main process
if __name__ == "__main__":
    # Check arguments
    if len(argv) != 3:
        # Show message
        print("Only 3 arguments expected.")

        # Stop code
        exit()
    
    # Init class
    checker = ProxyHttpsChecker(argv[1], argv[2])

    # Iterate proxies
    for proxy in checker.get_proxies():
        # Execute proxy test
        status = checker.test_proxy(proxy)

        # Check returns
        if status == True:
            # Show message
            print(f"[OK] Proxy: {proxy}")
        elif type(status) == str and status == "proxy_error":
            # Show message
            print(f"[Proxy Error] Proxy: {proxy}")
        elif type(status) == str and status == "connection_error":
            # Show message
            print(f"[Connection Error] Proxy: {proxy}")
        else:
            # Show message
            print(f"[Unknown Error] Proxy: {proxy}")

    # Final message
    print(f"The {checker.success} of {checker.total}")