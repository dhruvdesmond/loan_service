# Loan Service

## Features implemented

1. Ability to create account with two user roles (admin, customer) and log in
2. User can add loans and decide the amount, tenure and loan start date.
3. Admin will need to approve loan using the loan UUID to make it work.
4. Customer can request for his loans and corresponding repayments.
5. Customer can now add repayments if his loan is approved.





## Running the application

Complete application is dockerized and docker-compose can be used to run the application.
Environment variables can be configured in config/.env file. config/env.sample provided for reference.
TO simply run the application with default config, you can run the following command.
Application would be available at [http://localhost:9999](http://localhost:9999)

```bash
cd docker && docker compose up
```

## Running the tests

unit tests are also dockerized and can be run using the following command

```bash
cd docker_test && docker compose up
```

## API Documentation

1. swagger documentation is available at [swagger docs](http://localhost:9999/docs) when you run the application.
2. postman documentation with example requests(success, failure , validation , etc) is also provided
   at [postman docs](https://api.postman.com/collections/8409262-fdea59ae-38a4-4ee8-b2e0-c2c88db9f4f5?access_key=PMAT-01GZ97NKWANAHXVAYF034MAJVC)
