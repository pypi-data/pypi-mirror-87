@echo off
clear
ECHO.
ECHO **************************************
ECHO Welcome to Scanner config
ECHO **************************************
echo.
echo.
echo -n "Enter your Amp user: "
read SCANNER_AMPUSER
echo -n "Enter your Amp pass: "
read SCANNER_AMPPASS
echo -n "Enter your QV username: "
read SCANNER_QVUSER
echo -n "Enter your QV pass: "
read SCANNER_QVPASS
echo -n "Enter your mqtt host: "
read SCANNER_IP
echo -n "Enter your mqtt port: "
read SCANNER_PORT

echo "export SCANNER_AMPUSER='$SCANNER_AMPUSER'" >> ~/.profile
echo $SCANNER_AMPUSER appended to ~/.profile
echo "export SCANNER_AMPPASS='$SCANNER_AMPPASS'" >> ~/.profile
echo $SCANNER_AMPPASS appended to ~/.profile
echo "export SCANNER_QVUSER='$SCANNER_QVUSER'" >> ~/.profile
echo $SCANNER_QVUSER appended to ~/.profile
echo "export SCANNER_QVPASS='$SCANNER_QVPASS'" >> ~/.profile
echo $SCANNER_QVPASS appended to ~/.profile
echo "export SCANNER_IP='$SCANNER_IP'" >> ~/.profile
echo $SCANNER_IP appended to ~/.profile
echo "export SCANNER_PORT='$SCANNER_PORT'" >> ~/.profile
echo $SCANNER_PORT appended to ~/.profile

source ~/.profile
