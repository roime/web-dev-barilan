Creating the environment:
1. Download python 2.7 interpeter
2. Add to PATH in environment variable the path for the folder: Python27 and the path for the subfolder: Python27\Scripts
3. Run from command line the command: "pip install flask" (This will install the dependency for the web server)

Run the programs:
# To run the unit test, run from the project's directory the command: "python unit_test.py"
# To run the web server, run from the project's directory the command: "python web_server.py"
# To run the integration test, first run the web server as described above, then run from the project's directory the command: "python integration_test.py"