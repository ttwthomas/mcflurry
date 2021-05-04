# Création et déploiement de la fonction Lambda
## Instalation des modules python
```
pip3 install -r requirements.txt --system --target ./packages
```

##  Création du package zip
```
cd packages
zip -r ../my-deployment-package.zip .
zip -g mcflurry.zip  *.py
```

## Création du role IAM d'execution
```
aws iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/CloudFrontFullAccess
```

## Création de la lambda
```
aws lambda create-function --function-name update-mcflurry --zip-file fileb://mcflurry.zip --handler ma_lambda.lambda_handler --runtime python3.8 --role arn:aws:iam::1232456789:role/lambda-ex --timeout 600
```

## Invocation de la Lambda
```
aws lambda invoke --function-name update-mcflurry --payload '{"event": "abc123"}'
```

## Mise a jour du code de la lambda (sans mise a jour des dépendences)
```
zip -g mcflurry.zip *.py
aws lambda update-function-code --function-name update-mcflurry --zip-file fileb://mcflurry.zip
```
