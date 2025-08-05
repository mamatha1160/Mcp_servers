# test_script_writer_agent.py
 
import os

import json

from langchain.agents import Tool, initialize_agent

from langchain.agents.agent_types import AgentType

from langchain_groq import ChatGroq

from dotenv import load_dotenv
 
load_dotenv()
 
OUTPUT_DIR = "generated_scripts"  # Directory to store generated C# files
 
class TestScriptWriterAgent:

    def __init__(self):

        self.llm = ChatGroq(

            temperature=0.2,

            model_name="gemma2-9b-it"

        )
 
        self.tools = [

            Tool(

                name="generate_csharp_script",

                func=self._generate_csharp_script,

                description=(

                    "Generate a complete C# NUnit or MSTest test method from a single test case dictionary. "

                    "Return the full C# class or method only."

                ),

                return_direct=True

            )

        ]
 
        self.executor = initialize_agent(

            llm=self.llm,

            tools=self.tools,

            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,

            verbose=False

        )
 
    def _generate_csharp_script(self, test_case):

        if isinstance(test_case, str):

            test_case = json.loads(test_case)
 
        prompt = f"""

Generate a C# NUnit test method for the following test case.
 
Test Case ID: {test_case.get("test_case_id")}

Description: {test_case.get("description")}

Test Steps:

{json.dumps(test_case.get("test_steps", []), indent=2)}

Expected Result: {test_case.get("expected_result")}

Priority: {test_case.get("priority")}
 
Important:

- Return ONLY the C# method code.

- Do NOT include any comments, explanations, or extra text.

- Do NOT include namespace, class, or using directives.

- The method should be public, named with the test case ID.

- Use NUnit assertions like Assert.IsTrue, Assert.AreEqual, etc.

"""

        response = self.llm.invoke(prompt)

        return response.content.strip()
 
    def run_and_save(self, test_cases):

        os.makedirs(OUTPUT_DIR, exist_ok=True)
 
        for test_case in test_cases:

            script = self._generate_csharp_script(test_case)
 
            # Remove markdown code fences if present

            if script.startswith("```") and script.endswith("```"):

                script = "\n".join(script.split("\n")[1:-1])
 
            # Save each script to a file

            test_id = test_case["test_case_id"].replace(" ", "_")

            file_path = os.path.join(OUTPUT_DIR, f"{test_id}.cs")
 
            with open(file_path, "w") as f:

                f.write(f"// Auto-generated test case: {test_id}\n")

                f.write("using NUnit.Framework;\n\n")

                f.write("namespace NdcTests\n{\n")

                f.write("    [TestFixture]\n")

                f.write("    public class NdcTestCases\n    {\n")

                f.write("        " + script.replace("\n", "\n        ") + "\n")

                f.write("    }\n")

                f.write("}\n")
 
            print(f"✅ Saved: {file_path}")

 