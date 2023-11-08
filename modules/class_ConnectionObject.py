class ConnectionObject:
    """ Connection object for storing connection information and credentials
    """
    def __init__(self, address:str, userName:str, password:str, identifier:str='', port:int=0) -> None:
        """ Constructor for class ConnectionObject

        Args:
            address (str): IP-Address of target object
            userName (str): userName
            password (str): userPassword
            identifier (str, optional): Additional info (e.g. databasename or FritzBox Identifier). Defaults to ''.
            port (int, optional): port. Defaults to 0.
        """
        self.address = address
        self.port = port
        self.userName= userName
        self.password = password
        self.identifier = identifier
