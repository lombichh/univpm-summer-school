# UNIVPM summer school
This is an Amazon Alexa skill that aids agriculture managers by offering them precise daily water recommendations based on real-time weather insights, sun angle, and crop-specific data.

## How to use
1. Insert the file 'lambda_function.py' into Amazon AWS as a new Lambda function (replace {API key} with your OpenWeatherMap API key).
2. Create, using Amazon AWS, a new API Gateway. Within it, create a new resource with a POST method to connect to the Lambda function created earlier, and create a new deployment stage for the API.
3. Go to [developer.amazon.com](https://developer.amazon.com/) and create a new Alexa skill.
    1. Modify the Invocation Name.
    2. Create a new Intent and insert the phrases to execute the skill
        ```sh
            - Evapotranspiration in field {field_num} {keyword}
            - Evapotranspiration {keyword} in field {field_num}
            - Evapotranspiration in field {field_num} in {days} day
            - Evapotranspiration in field {field_num} in {days} days
            - Evapotranspiration in field {field_num} in {days} day
            - Evapotranspiration in field {field_num} in {days} days
            - Calculate evapotranspiration in field {field_num} in {days} day
            - Calculate evapotranspiration in field {field_num} in {days} days
            - Calculate evapotranspiration in field {field_num} in {days} day
            - Calculate evapotranspiration in field {field_num} in {days} days
            ```
    3. Modify the skill code by inserting the content of the file 'request_handler.py' as a new class.
5. Perform the deployment of the code, build, and test of the skill.