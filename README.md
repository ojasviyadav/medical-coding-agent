# **Medical Coding Agent Readme**

**Overview**

**Project Description:**✨\
This project was undertaken as a weekend exploration to evaluate how agentic retrieval might be applied to a hierarchical record system, such as the ICD-10 coding schema. ICD-10 coding schem The approach differs from traditional AI-based methods that often operate as "black-box" classifiers. Instead, this system attempts to mimic a human coder’s process: it systematically navigates through the directory structure of ICD-10 codes, employing a graph-based, breadth-first search (BFS) strategy to locate the most precise and applicable codes. ✨

Recent advancements in artificial intelligence have significantly enhanced the automation of ICD-10 coding from clinical narratives. Notably: ✨

- **MedCodER**, a generative AI framework, achieved a micro-F1 score of **0.60** in ICD code prediction, outperforming state-of-the-art methods.

- A study evaluating OpenAI's GPT-3.5 Turbo for ICD code assignment reported an accuracy improvement from **29.7% to 62.6%** after fine-tuning with clinical notes.

- A multimodal machine learning model integrating various data types achieved a micro-F1 score of **0.7633** in predicting ICD-10 codes, surpassing traditional models.

These developments underscore AI's potential to streamline the ICD-10 coding process, reducing manual effort and improving accuracy. ✨

**Key Characteristics:**

1. **Agentic Retrieval:**

   - The system uses autonomous “agents” that step through the ICD-10 schema like a human would, examining nodes in a hierarchical directory.
   - Instead of a direct classification model, these agents traverse the coding structure, refining the search at each step.
   - By breaking this as a graph-traversal problem, we can CoT the human logic at each step of the code identification process and improve the results over time with a strong evals dataset. ✨

2. **Breadth-First Search (BFS) Approach:**

   - Employing BFS ensures a structured, level-by-level exploration of the coding schema.
   - Humans often engage in a similar pattern of searching—starting broad, then narrowing down to more specific categories.
   - This method allows for a human-in-the-loop scenario where the human can intervene at any point in the hierarchical search to guide the final selection. ✨

3. **Precision & Depth:**

   - The agent continues to delve deeper until it reaches the most accurate level of specificity that matches the clinical scenario.
   - As it goes deeper, it may propose primary, secondary, or even tertiary codes.
   - External causes and medication-related codes, which reside in their own sections, are also explored systematically. ✨

4. **Human-Centric Design:**

   - The methodology is designed for situations where a human coder supervises the AI assistant.
   - By observing the step-by-step BFS traversal, a human can review pattern matches and correct or confirm the results. ✨

**Future Work:**✨\
The current findings are preliminary and exploratory. I plan to revisit and refine this approach once I have the availability to do so. Future work may include:

1. This project will be a massive success with an evaluation dataset if the community contributes to an opensource dataset. ✨

2. **Improved Heuristics for Navigating the ICD-10 Graph:**

   - Developing more robust strategies for node prioritization during the BFS traversal.
   - Incorporating contextual clinical data to dynamically adjust traversal paths, potentially improving both accuracy and efficiency. ✨

3. **Integration with Advanced NLP Models:**

   - Utilizing advanced NLP techniques to better parse and interpret unstructured clinical text, enabling more accurate initial code suggestions.
   - The current parsing strategies are probably not comprehensive enough but can be improved through the creation of an evaluation set. I welcome opportunities to collaborate on creating such evaluations, which will massively enhance the agent's performance. ✨

4. **User Interface Enhancements:**

   - Designing interactive visualizations of the hierarchical traversal process to better support human oversight and decision-making. ✨

5. **Open Source LLM Integration:**

   - As [ pointed out](<insert LinkedIn URL>), open source medical coding agents should also utilize open source LLMs.
   - Experimenting with Llama 3.3 70B as a base model for improving search and contextual understanding within the ICD-10 schema. Perhaps a LiteLLM integration? The main blocker may be how this code is calling the claude agents by passing a list of tools. If someone is able to write a compatible litellm version and use that to route the requests to a an open source model provider. That would unlock steady progress in that domain and let healthcare facilities explore these applications in a truly secure and privacy compliant manner on their premises. ✨

6. **Medical Coding Schemas Beyond ICD-10:** ✨

   Medical coding involves various schemas beyond ICD-10, such as CPT (Current Procedural Terminology), HCPCS (Healthcare Common Procedure Coding System), SNOMED CT, LOINC (Logical Observation Identifiers Names and Codes), and RxNorm. These systems are supported by organizations like the AMA, CMS, SNOMED International, Regenstrief Institute, and NLM, which provide resources for proper usage. It is possible to develop parsing strategies for each schema to create hierarchical, agent-driven code suggestions. ✨

---

*I’ll return to this project later to improve and expand upon these concepts.* ✨

