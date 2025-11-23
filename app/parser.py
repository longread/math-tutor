import xml.etree.ElementTree as ET
import re

class LLMResponseParser:
    def parse(self, raw_xml_string: str) -> dict:
        steps = []
        final_answer = None

        # Wrap the raw string in a root tag if it's not already a single root to make it valid XML
        # This handles cases where the LLM might return multiple top-level <step> tags without a parent.
        # However, the prompt specifically asks for no markdown blocks, so it should be clean XML already.
        # We'll use a regex to extract content to be more robust against minor LLM formatting deviations.
        
        step_matches = re.findall(r'<step>(.*?)</step>', raw_xml_string, re.DOTALL)
        for step_content in step_matches:
            steps.append(step_content.strip())

        answer_match = re.search(r'<answer>(.*?)</answer>', raw_xml_string, re.DOTALL)
        if answer_match:
            final_answer = answer_match.group(1).strip()

        if not steps and not final_answer:
            # If no structured content found, assume the entire response is a single step (e.g., for non-math inputs)
            # Or, if the LLM politiely declined as per the prompt.
            # We'll check for the "politely decline" case more specifically.
            if "politely decline" in raw_xml_string.lower() or "not a math problem" in raw_xml_string.lower():
                steps.append(raw_xml_string.strip())
            else:
                raise ValueError("Could not parse AI response: No steps or answer found.")
        
        if not final_answer and steps: # If steps found but no final answer, consider the last step as potential answer
             # This is a heuristic and might need refinement based on actual LLM behavior.
             # For now, if there's no explicit <answer> tag, the parser will return None for final_answer.
             # The PRD expects an <answer> tag, so we'll enforce that.
             pass


        return {
            "steps": steps,
            "final_answer": final_answer
        }

