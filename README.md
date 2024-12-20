
# Medical Coding Agent

## Example:
input:
![WhatsApp Image 2024-12-20 at 17 18 16_7e0f40a2](https://github.com/user-attachments/assets/2ccba079-d819-42f7-8fb2-c58fa88fdab1)

output codes and analysis:
![WhatsApp Image 2024-12-20 at 17 18 15_39069d85](https://github.com/user-attachments/assets/352b3cbd-c009-49c1-87c7-20ab5b83f285)

---
## Canvas / Overview

### Project Description ✨
This project was undertaken as a weekend exploration to evaluate how agentic retrieval might be applied to a hierarchical record system, such as the ICD-10 coding schema. The approach differs from traditional AI-based methods that often operate as "black-box" classifiers. Instead, this system attempts to mimic a human coder’s process: it systematically navigates through the directory structure of ICD-10 codes, employing a graph-based, breadth-first search (BFS) strategy to locate the most precise and applicable codes.

### Recent Advancements ✨
Recent advancements in artificial intelligence have significantly enhanced the automation of ICD-10 coding from clinical narratives. Notably:

- A generative AI framework achieved a micro-F1 score of **0.60** in ICD code prediction, outperforming state-of-the-art methods.
- OpenAI's GPT-3.5 Turbo for ICD code assignment showed an accuracy improvement from **29.7% to 62.6%** after fine-tuning with clinical notes.
- A multimodal machine learning model integrating various data types reached a micro-F1 score of **0.7633**, surpassing traditional models.

These developments underscore AI's potential to streamline the ICD-10 coding process, reducing manual effort and improving accuracy.

## Key Characteristics

### 1. Agentic Retrieval
- The system uses autonomous “agents” that step through the ICD-10 schema like a human would, examining nodes in a hierarchical directory.
- Instead of a direct classification model, these agents traverse the coding structure, refining the search at each step.
- By framing this as a graph traversal problem, human logic can be encoded step-by-step to improve results over time with a strong evaluation dataset.

### 2. Breadth-First Search (BFS) Approach
- Employing BFS ensures a structured, level-by-level exploration of the coding schema.
- Humans often engage in a similar pattern of searching—starting broad, then narrowing down to more specific categories.
- This method allows for a human-in-the-loop scenario where a human can intervene at any point to guide the final selection.

### 3. Precision & Depth
- The agent delves deeper until it reaches the most accurate level of specificity matching the clinical scenario.
- As it goes deeper, it may propose primary, secondary, or even tertiary codes.
- External causes and medication-related codes, which reside in their own sections, are explored systematically.

### 4. Human-Centric Design
- Designed for situations where a human coder supervises the AI assistant.
- By observing the step-by-step BFS traversal, a human can review pattern matches and correct or confirm the results.

## Future Work ✨
The current findings are preliminary and exploratory. Future work may include:

### 1. Improved Heuristics for Navigating the ICD-10 Graph
- Developing more robust strategies for node prioritization during BFS traversal.
- Incorporating contextual clinical data to dynamically adjust traversal paths, improving accuracy and efficiency.

### 2. Integration with Advanced NLP Models
- Utilizing advanced NLP techniques to better parse and interpret unstructured clinical text, enabling more accurate initial code suggestions.
- The current parsing strategies can be expanded with evaluation datasets to enhance performance.

### 3. User Interface Enhancements
- Designing interactive visualizations of the hierarchical traversal process to better support human oversight and decision-making.

### 4. Open Source LLM Integration
- Experimenting with Llama 3.3 70B as a base model for improving search and contextual understanding within the ICD-10 schema.
- Developing a compatible open-source framework to integrate large language models (LLMs) securely and efficiently in healthcare environments.

### 5. Medical Coding Schemas Beyond ICD-10
- Expanding parsing strategies to other schemas like CPT, HCPCS, SNOMED CT, LOINC, and RxNorm, which are widely supported by organizations such as AMA, CMS, and NLM.

---

*I’ll return to this project later to improve and expand upon these concepts.*

