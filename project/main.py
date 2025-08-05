import json

from test_script_writer_agent import TestScriptWriterAgent
 
def main():

    json_path = "project/generated_test_cases.json"  # Path to your existing test case JSON
 
    # Load the JSON test cases from file

    with open(json_path, "r") as f:

        test_cases = json.load(f)
 
    # Initialize your script writer agent

    script_agent = TestScriptWriterAgent()
 
    # Generate C# test scripts and save them to files

    script_agent.run_and_save(test_cases)
 
if __name__ == "__main__":

    main()

 