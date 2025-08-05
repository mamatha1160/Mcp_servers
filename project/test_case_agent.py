import os
import json
import re
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
 
load_dotenv()
 
NDC_PAX_SCHEMA = """<PaxList xmlns="http://www.iata.org/IATA/2015/EASD/00/IATA_OffersAndOrdersCommonTypes">
    <Pax>
        <PaxID>ADULT_1</PaxID>
        <PTC>ADT</PTC>
    </Pax>
    <Pax>
        <PaxID>ADULT_2</PaxID>
        <PTC>ADT</PTC>
    </Pax>
    <Pax>
        <PaxID>CHILD_1</PaxID>
        <PTC>CHD</PTC>
    </Pax>
    <Pax>
        <PaxID>YOUTH_1</PaxID>
        <PTC>GBE</PTC>
    </Pax>
    <Pax>
        <PaxID>INFANT_1</PaxID>
        <PTC>INF</PTC>
    </Pax>
    <Pax>
        <PaxID>INFANT_2</PaxID>
        <PTC>INF</PTC>
    </Pax>
</PaxList>"""
 
class TestCaseAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.2,
            model_name="gemma2-9b-it"
        )
 
        self.tools = [
            Tool(
                name="generate_test_cases",
                func=self._generate_test_cases,
                description=(
                    "Generate test cases from user story, acceptance criteria, and NDC schema snippet. "
                    "Output must be a JSON array with test_case_id, description, test_steps, expected_result, priority."
                ),
                return_direct=True
            )
        ]
 
        self.executor = initialize_agent(
            llm=self.llm,
            tools=self.tools,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
 
    def _generate_test_cases(self, input_data):
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
 
        user_story = input_data.get("user_story", "")
        acceptance_criteria = input_data.get("acceptance_criteria", "")
        ndc_schema = input_data.get("ndc_schema", NDC_PAX_SCHEMA)
 
        prompt = f"""
You are an expert test case writer for IATA NDC XML APIs.
 
Generate detailed test cases in JSON format ONLY.
Each test case object MUST contain these fields:
  - test_case_id (string)
  - description (string)
  - test_steps (array of strings)
  - expected_result (string)
  - priority (High/Medium/Low)
 
Input:
User Story:
{user_story}
 
Acceptance Criteria:
{acceptance_criteria}
 
NDC Schema:
{ndc_schema}
 
Output ONLY a JSON array of test case objects. No explanations or extra text.
"""
        response = self.llm.invoke(prompt)
        return response.content
 
    def run(self, user_story: str, acceptance_criteria: str, ndc_schema: str = None):
        if ndc_schema is None:
            ndc_schema = NDC_PAX_SCHEMA
 
        input_json = json.dumps({
            "user_story": user_story,
            "acceptance_criteria": acceptance_criteria,
            "ndc_schema": ndc_schema
        })
 
        raw_output = self.executor.invoke({"input": input_json})["output"]
 
        try:
            match = re.search(r"(\[.*\])", raw_output, re.DOTALL)
            if match:
                json_str = match.group(1)
                return json.loads(json_str)
            else:
                return {
                    "error": "No JSON array found in LLM output.",
                    "raw_output": raw_output
                }
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse LLM output as JSON.",
                "raw_output": raw_output
            }
 
def main():
    agent = TestCaseAgent()
 
    user_story = (
        "As a travel agent, I want to create a passenger list containing different types of passengers "
        "such as adults, children, youth, and infants, so that bookings can be accurately priced and "
        "validated based on passenger types."
    )
 
    acceptance_criteria = """
- The passenger list must support multiple passenger types: ADT (Adult), CHD (Child), INF (Infant), and GBE (Youth).
- Each <Pax> must contain a unique <PaxID> and a valid <PTC> value.
- The system must allow multiple infants to be associated with adults (INF <-> ADT relationships).
- Maximum of one infant (INF) per adult (ADT) must be validated.
- The system must reject unknown or invalid <PTC> codes.
- Each passenger's PTC must follow IATA standard codes.
- The schema must support at least one adult (ADT); a booking cannot contain only minors or infants.
"""
 
    # print("Generating NDC test cases in JSON format...\n")
    # result = agent.run(user_story, acceptance_criteria)
 
    # if isinstance(result, dict) and "error" in result:
    #     print("Error parsing output as JSON:")
    #     print(result["raw_output"])
    # else:
    #     print("=== Generated Test Cases JSON ===")
    #     print(json.dumps(result, indent=2))
 
 
 
 
    print("Generating NDC test cases in JSON format...\n")
    result = agent.run(user_story, acceptance_criteria)
 
    if isinstance(result, dict) and "error" in result:
        print("Error parsing output as JSON:")
        print(result["raw_output"])
    else:
        print("=== Generated Test Cases JSON ===")
        print(json.dumps(result, indent=2))
 
        # ✅ Save to file
        output_file = "generated_test_cases.json"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f"\n✅ Test cases saved to '{output_file}'")
        except Exception as e:
            print(f"\n❌ Failed to save test cases: {e}")
 
 
if __name__ == "__main__":
    main()
 