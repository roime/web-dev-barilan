Creating the environment:
1. Download python 2.7 interpeter
2. Add to PATH in environment variable the path for the folder: Python27 and the path for the subfolder: Python27\Scripts
3. Run from command line the command: "pip install flask" (This will install the dependency for the web server)

Run the programs:
# To run the unit test, run from the project's directory the command: "python unit_test.py"
# To run the web server, run from the project's directory the command: "python web_server.py"
# To run the integration test, first run the web server as described above, then run from the project's directory the command: "python integration_test.py"

Building and running docker:
# Clone this repository
# Start from the parent folder of the repository and run 
'''
sudo docker build [repository name]
'''
# Than cd into the folder and run
'''
sudo docker-compose build calculator
'''
# Than to start the server and the service run
'''
sudo docker-compose up
'''
# Than you can access the service by opening the browser and going to 127.0.0.1:8080/login
