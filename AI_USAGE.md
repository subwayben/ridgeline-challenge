# AI Usage

## AI Tool Used

* ChatGPT (OpenAI)

## How AI Was Used

I used ChatGPT as a learning and development assistant while completing this project because I was new to Django.

Specifically, I used AI to:

* Learn the Django project structure and understand how projects, apps, views, URLs, and templates work together.
* Receive explanations of Django concepts and Python code while building the application.
* Troubleshoot development issues, including debugging routing errors, file path problems, Pandas data loading, and ZIP file handling.
* Discuss approaches for organizing the project and separating responsibilities between different modules.
* Receive guidance on using Git throughout the development process, including meaningful commit practices.
* Review documentation such as the README and this AI usage summary.

## Development Process

All project code was developed, tested, and integrated by me. AI assistance was used to explain concepts, provide implementation guidance, and help diagnose issues encountered during development. I reviewed the suggested solutions, adapted them to the project where necessary, and verified that the application behaved correctly after each change.

## Example of Incorrect AI Output

One AI suggestion assumed that the EPA dataset used the CBSA name **"San Diego-Chula Vista-Carlsbad, CA"**, which matched the wording in the assignment. However, when I tested the application, the San Diego page displayed no data.

To investigate, I loaded the EPA dataset in the Django shell and queried the unique values in the `CBSA Name` column. I found that the 2024 EPA dataset actually used the name **"San Diego-Carlsbad, CA"**.

After updating my application's mapping to use the value that existed in the dataset, the San Diego chart and monthly averages loaded correctly.

This reinforced the importance of validating AI-generated suggestions against the actual data rather than assuming they are always correct.

## Verification

I manually tested the completed application to verify that:

* The interactive Leaflet map displays the required cities.
* Selecting each city loads the appropriate EPA PM2.5 data.
* The daily PM2.5 time-series chart displays correctly.
* The monthly average table correctly summarizes March, April, and May values for each available year.
* The application runs successfully using Django's development server.
