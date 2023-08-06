import requests

from AuthGG import error_handler

class AdminClient:
    def __init__(self, auth_key: str):
        """ 
        Requires a authorization key which can be found in the application settings
        """

        self.authorization = auth_key

    # def generateLicense(self, days: int, amount: int, level: int):
    #     """ 
    #     Generates a license.

    #     E.g.
    #     ```
    #     from AuthGG.admin import AdminClient
    #     client = AdminClient("auth")
    #     codes =  client.generateLicense(days=1, amount=50, level=0)
    #     ```

    #     """

    #     headers = {
    #         "Content-Type": "application/x-www-form-urlencoded"
    #     }        

    #     link = f"https://developers.auth.gg/LICENSES/?type=generate&days={str(days)}&amount={str(amount)}&level={str(level)}&authorization={self.authorization}"

    #     print(link)

    #     r = requests.get(link, headers=headers)

    #     response = r.json()

    #     print(response)

    def deleteUser(self, username: str):
        """
        Deletes a user from your Auth.GG application
        """

        r = requests.get(f"https://developers.auth.gg/USERS/?type=delete&authorization={self.authorization}&user={username}")             
        if r.json()['status'] == "success":
            return True
        else:
            raise error_handler.FailedTask(message="Failed Deleting User!")

    def getUserCount(self):
        """
    
        """
        r = requests.get(f"https://developers.auth.gg/USERS/?type=count&authorization={self.authorization}")
        if r.json()['status'] == "success":
            jsonResponse = r.json()["value"]
            return True and jsonResponse
        else:
            raise error_handler.ErrorConnecting()

