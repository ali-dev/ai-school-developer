# Tool Modifications
I updated the code generator agent to be specifialized in building data analysis Jupyter notebooks. 
I added a couple of tools that ingest SQL files that descipbe the database schema in order to make the Agent generate more accurate reports that actually takes how data is stored into account. I also updated the system prompt to be more specific to this usecase. it seems to work!!
I intend to add some fine-tuning docs with example questions and Query responses in order to train the model on even more specific use cases. 

### Notes:
- you can see a couple of the generated reports in the Reports directory
- I did not include the schema files for security reasons. In order to run the agent, you would need to create a `fulfillment.sql` and `subscription.sql` files in the root directory.

### Prompts:
Here are some prompts that I used:
- Generate a Jupiter report that summarizes meal_packaging statuses across all markets. If there is virtual environment set up in Reports directory, please create one, and add the necessary packages to do this type of data analysis
- Generate a report that displays number of new User subscriptions across different markets in the last 1 week
-  can you please generate a readme file in Reports. the file should include instructions on how to set up and run the virtual environment, how to run jupyter notebooks, and a Reports section that describes the reports that were generated with links to the code  


# AI For Developer Productivity: Coder Agent

## Overview
In this project, we developed a Coder Agent to enhance developer productivity. The core functionality of our agent is to write code and execute terminal commands on your behalf, streamlining your workflow and allowing you to focus on higher-level tasks. This innovative approach not only speeds up the development process but also ensures accuracy and efficiency.

## Now It's Your Turn!
Embrace your creativity and personalize this project to craft a solution that uniquely addresses the challenges and inefficiencies you face in your own coding workflow. After seeing what our Coder Agent can do, it’s time for you to take the reins. Use the foundation we’ve built and apply it to a challenge you face in your own professional or personal environment. Here’s how you can get started:

## Minimum Requirements
- **Custom Tool Creation:** Develop new custom tools for your Coder Agent to match your specific coding workflow needs. This could include automating repetitive tasks, integrating with specific APIs, or creating specialized commands that you frequently use.

## Stretch Goals
- **Advanced Code Analysis:** Enhance the agent to provide deeper code analysis, such as identifying potential bugs, suggesting performance improvements, and offering refactoring recommendations.
- **Context-Aware Assistance:** Develop features that enable the agent to understand the context of your code better, offering more accurate suggestions and command executions based on the current project structure and coding standards.
- **Collaboration Features:** Implement tools that facilitate better collaboration among team members, such as code review automation, integration with version control systems, and real-time coding suggestions in collaborative coding environments.
- **Continuous Integration/Continuous Deployment (CI/CD) Integration:** Integrate the agent with CI/CD pipelines to automate code testing, deployment processes, and monitoring, ensuring smoother and more reliable releases.
- **AI-Driven Learning:** Incorporate machine learning models that allow the agent to learn from your coding patterns over time, providing more personalized and relevant assistance as you continue to use it.

## Privacy and Submission Guidelines
- **Submission Requirements:** Please submit a link to your public repo with your implementation or a loom video showcasing your work on the BloomTech AI Platform.
- **Sensitive Information:** If your implementation involves sensitive information, you are not required to submit a public repository. Instead, a detailed review of your project through a Loom video is acceptable, where you can demonstrate the functionality and discuss the technologies used without exposing confidential data.
