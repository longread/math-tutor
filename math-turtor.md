# Product Requirement Document: MathTutor AI

## 1. Executive Summary
**Purpose:** To build an interactive, AI-powered tutoring assistant that helps students understand the *methodology* of solving math problems. The system will break down complex problems into logical, pedagogical steps using a strict XML-based format, ensuring students learn the "how" and "why" rather than just the final answer.

## 2. User Personas
*   **The Student:** Needs help with homework or test prep. Often struggles to type complex math symbols. Wants to learn the step-by-step logic.
*   **The Parent/Educator:** Wants to ensure the tool is educational and safe, not just a shortcut/cheating tool.

## 3. Functional Requirements

### 3.1. Input Methods (The "Post" Phase)
1.  **Text Input:** Standard text box for word problems or simple equations.
2.  **LaTeX Support:** Support for raw math notation (e.g., `\frac{1}{2}`) with a live preview.
3.  **Image Upload (Critical):** 
    *   User can upload/paste an image of a math problem.
    *   System must perform OCR (Optical Character Recognition) via a vision-capable model (e.g., GPT-4o, Claude 3.5 Sonnet) to convert the image to text before processing.

### 3.2. AI Processing (The "LLM" Phase)
1.  **System Prompting:** The backend must wrap the user's question with a strict system prompt to enforce the XML output format.
2.  **Pedagogical Logic:** The model must be instructed to "think step-by-step" to minimize calculation errors and maximize educational value.
3.  **Format Validation:** The system must parse the response to ensure valid `<step>` and `<answer>` tags exist. If validation fails, the system should auto-retry.

### 3.3. Solution Presentation (The "Solution" Phase)
1.  **Step-by-Step Reveal:** 
    *   The UI shall not display the full solution immediately.
    *   Steps should be displayed as "Cards" or distinct blocks.
    *   **Interaction:** A "Show Next Step" button allows the student to progress at their own pace.
2.  **Math Rendering:** 
    *   All LaTeX math content (inside `$..$` or `$$..$$`) must be rendered using **MathJax** or **KaTeX**.
3.  **Final Answer:** The content inside `<answer>` tags remains hidden until the user reaches the end of the steps.

## 4. Technical Specifications

### 4.1. The System Prompt
The following prompt must be sent to the LLM as the `system` message to ensure reliability:

```text
You are an expert Math Tutoring AI designed to help students learn problem-solving logic. Your goal is to provide clear, step-by-step solutions that explain the "why" and "how," not just the result.

### OUTPUT FORMAT RULES
You must strictly follow this XML-style format for your response. Do not include markdown code blocks (like ```xml) around the output.

<step>
[Explain the first logical step here. Define variables or state the formula being used.]
</step>
<step>
[Perform the next calculation or logical deduction. Show intermediate work.]
</step>
... (add as many steps as necessary) ...
<answer>
[The final result]
</answer>

### CONTENT GUIDELINES
1. **Math Formatting:** Use LaTeX formatting for all mathematical expressions. Enclose inline math in single dollar signs (e.g., $x^2$) and block math in double dollar signs (e.g., $$ \frac{a}{b} $$).
2. **Pedagogy:** Do not skip logical jumps. Write as if you are teaching a student who needs to see the intermediate work.
3. **Tone:** Be encouraging, professional, and concise.
4. **Non-Math Inputs:** If the user sends text that is not a math problem, politely decline inside a single <step> tag.

### EXAMPLE INPUT
"Solve for x: 2x + 5 = 15"

### EXAMPLE OUTPUT
<step>
First, we want to isolate the variable $x$. We can start by subtracting 5 from both sides of the equation:
$$ 2x + 5 - 5 = 15 - 5 $$
</step>
<step>
Simplify the equation:
$$ 2x = 10 $$
</step>
<step>
Now, divide both sides by 2 to solve for $x$:
$$ \frac{2x}{2} = \frac{10}{2} $$
</step>
<answer>
x = 5
</answer>
```

### 4.2. Data Structure (Parsing Logic)
The backend (Python/Node) must parse the raw string into a structured object for the frontend.

**Raw Output:**
```xml
<step>Step 1 content...</step>
<step>Step 2 content...</step>
<answer>Final Answer</answer>
```

**Parsed JSON:**
```json
{
  "steps": [
    "Step 1 content...",
    "Step 2 content..."
  ],
  "final_answer": "Final Answer"
}
```

## 5. UI/UX Wireframe Concepts
1.  **Home:** Clean search bar + Camera Icon.
2.  **Loading:** "Tutor is thinking..." (avoid generic spinners; use math-related loading text).
3.  **Result View:**
    *   **Top:** Original Question.
    *   **Center:** Scrollable list of steps.
    *   **Bottom:** Floating "Show Next Step" button.
4.  **Error Handling:** If the AI fails to solve it (or format is broken), show: "I'm having trouble reading that. Could you try typing it?"

## 6. Future Roadmap (v2)
*   **Follow-up Chat:** Allow users to highlight a specific step and ask "Why?"
*   **Practice Mode:** Generate a similar problem with different numbers for the student to try immediately after reading the explanation.
*   **Python Integration:** Use a code interpreter tool for heavy arithmetic to prevent AI hallucination on large numbers.
