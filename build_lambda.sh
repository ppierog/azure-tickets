currDir=$(pwd)
rm -Rf aws_lambda.zip
cd .venv/lib/python3.10/site-packages
#$SHELL
zip -r ../../../../aws_lambda.zip .
cd $currDir
zip aws_lambda.zip lambda_function.py
zip aws_lambda.zip azure_tickets.py
zip aws_lambda.zip teams_notifier.py

echo $currDir