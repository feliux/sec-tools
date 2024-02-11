"""
This code creates a threat model using PyTM and represents the "Insecure Authentication
Protocols” threat scenario. It includes actors such as "Attacker” and "User,” a server representing
the application server, and a datastore representing the userʼs data.
The threat model defines the "Insecure Authentication Protocols” threat and includes attack paths
such as "Eavesdropping” and "Man-in-the-Middle Attack.” It also defines the impact of these
threats, such as unauthorized access to user data and data breaches.
"""

from pytm import TM, Server, Datastore, Actor, Dataflow

IMAGE_OUTPUT = "images/weakOrStolenCredentilas.png"

# Create a new threat model
tm = TM(
    name="Weak or Stolen Credentials", 
    description="Weak or Stolen Credentials Threat Model"
)

# Create actors
attacker = Actor("Attacker")
insider = Actor("Insider")

# Create server and datastore
server = Server("Application Server")
datastore = Datastore("Datastore")

# Define attack paths
Dataflow(attacker, server, "Password Guessing/Brute Force Attack")
Dataflow(attacker, server, "Credential Theft")
Dataflow(insider, server, "Insider Threat")

# Define impact
Dataflow(server, datastore, "Unauthorized Access to User Data")
Dataflow(server, datastore, "Data Breach and Exposure of Sensitive Information")

# Generate the threat model diagram
tm.process()
