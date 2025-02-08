import requests
with open('GEMINI.txt','r',encoding='utf-8') as f:
    a = f.readlines()
GEMINI_API_KEY = ''.join(a).replace('\n','')
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def generate_mcq(section, head="Summarize the following section. "):
    payload = {
        "contents": [{"parts": [{"text": head + section}]}]
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        response_json = response.json()
        return response_json['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return ""

if __name__ == "__main__":
    sample_text = '''[00:00:00] Professor: Alright, class, today we're going to dive into the concept of photosynthesis. Can someone tell me what the basic process of photosynthesis is?
[00:00:15] Student A: Photosynthesis is when plants use sunlight, water, and carbon dioxide to create oxygen and glucose.
[00:00:25] Professor: Excellent! Now, let's break down the stages involved. First, we have the light-dependent reactions which occur in the thylakoids of the chloroplast.
[00:00:40] Student B: Can you explain what a thylakoid is again?
[00:00:45] Professor: Sure, a thylakoid is a flattened sac-like structure within the chloroplast where chlorophyll molecules are embedded, which are crucial for capturing light energy.
[00:01:00] Professor: During the light-dependent reactions, water molecules are split, releasing electrons, protons, and oxygen gas.
[00:01:15] Student C: So, the oxygen we breathe comes from the process of photosynthesis?
[00:01:20] Professor: Exactly! This is why plants are so important for our survival.
[00:01:25] [Professor continues explaining the Calvin Cycle, discussing the role of carbon fixation, and answering further student questions, with timestamps throughout the recording].'''
    head = '''
**Instructions:**

Transcribe *only* the instructor's lecture content below from the attached audio recording of a class.  The transcription should be:
* **Concise & Non-Verbose:** Avoid unnecessary filler words (e.g., "um," "uh," "like," repeated words) and overly long sentences where possible. Paraphrase slightly if it improves clarity and conciseness while preserving the original meaning. The goal is to produce a clean, readable transcript suitable for self-study notes. Do *not* summarize the content; simply transcribe it accurately and concisely.
* **Formatted for Readability:** Use paragraphs to separate different topics or sections of the lecture. Use bullet points or numbered lists where appropriate to enhance readability (e.g., when the instructor lists key concepts).
OUTPUT the material in MD format. WITH CLEAR BULLET POINTS. 
**Example of Desired Output:**

```
Alkanes are saturated hydrocarbons, meaning they contain only carbon and hydrogen atoms, and all carbon-carbon bonds are single bonds.
Key characteristics of alkanes include:
*   Relatively unreactive
*   Nonpolar Below begin the prompt```
    '''
    print(generate_mcq(sample_text,head))
