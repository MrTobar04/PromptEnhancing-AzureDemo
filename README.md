# ✨ Prompt Enhancer — Gradio Application

A multi-agent prompt optimization tool powered by Azure OpenAI

---

## 📌 **1. Introduction**

Prompt Enhancer is an interactive **Gradio-based web application** designed to help users transform raw, unclear, or unstructured prompts into clean, precise, and high-quality instructions for AI systems.

The application uses a **three-agent pipeline**—Intent Clarifier, Prompt Enhancer, and Final Polisher—to refine user input and generate a structured, optimized prompt tailored to a specific use case (e.g., ChatGPT, GitHub Copilot, Stable Diffusion, data analysis, code generation).

### **Key Features**

* 🧠 **Three-Agent Architecture** for high-accuracy prompt refinement
* 🎨 **Clean Gradio UI** with inline editing and one-click enhancement
* 🔁 **“Back” feature** to restore the original input
* ⚙️ **Supports multiple use cases** like coding, chat, analysis, or image generation
* ☁️ **Powered by Azure OpenAI** for enterprise-grade performance
* 🧩 **Modular codebase** (agents, services, UI separated for maintainability)

---

## 🚀 **2. Setup and Installation**

Follow these steps to set up and run the Prompt Enhancer application locally.

---

### **2.1 Requirements**

Make sure your system includes:

* **Python 3.9 – 3.12**
* An **Azure OpenAI resource**
* A deployed model such as **gpt-4o**, **gpt-4o-mini**, or similar
* The following Python packages (installed later):

```
gradio
python-dotenv
azure-ai-inference
azure-core
```

---

### **2.2 Clone the Repository**

```bash
git clone https://github.com/your-username/prompt-enhancer.git
cd prompt-enhancer
```

---

### **2.3 Environment Variables**

Create a `.env` file in the project root:

```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
```

Make sure:

* The **endpoint** ends with `.azure.com/`
* The deployment corresponds to an existing **model deployment** in Azure OpenAI Studio

---

### **2.4 Install Dependencies**

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install gradio python-dotenv azure-ai-inference azure-core
```

---

### **2.5 Project Structure**

```
project/
│
├── app.py
├── .env
├── requirements.txt
│
├── agents/
│   ├── intent_agent.py
│   ├── enhancer_agent.py
│   └── polisher_agent.py
│
├── services/
│   ├── aoai_client.py
│   └── enhancer_pipeline.py
│
├── ui/
│   └── components.py
│
└── assets/
    └── styles.css
```

---

## 🖥️ **3. Usage Instructions**

### **3.1 Launching the App**

Run the main Python module:

```bash
python app.py
```

Gradio will start a local server and display a URL such as:

```
Running on http://127.0.0.1:7860
```

Open it in your browser.

---

### **3.2 How to Use**

1. **Choose a Use Case**
   Select a target system (ChatGPT, Copilot, Image Generation, etc.).

2. **Enter Your Prompt**
   Type or paste the text you want to improve.

3. **Click “Enhance”**
   The multi-agent pipeline:

   * Clarifies your intent
   * Enhances structure and instructions
   * Polishes the final prompt

4. **Review Output**
   The enhanced version replaces the original in the textbox.

5. **Click “Back”** to restore the original prompt at any time.

---

### **3.3 Example Use Case**

**Input:**

```
Write me a python scraper but I only want the basic version.
```

**Output (enhanced prompt):**

```
Create a clear and minimal Python web scraper with only the essential functionality using the specified tools or libraries. Provide structured, well-commented code while avoiding unnecessary features or advanced optimizations.
```

---

## 📚 **4. Additional Information**

### **Troubleshooting**

**Issue:**
`azure.core.exceptions.HttpResponseError: 401 Unauthorized`

**Fix:**

* Check your API key
* Validate the model deployment name
* Ensure `AZURE_OPENAI_ENDPOINT` ends with `/`

---

**Issue:** Gradio interface won't load

* Check that no firewall blocks port **7860**
* Ensure Python version ≥ 3.9
* Confirm dependencies installed properly

---

### **Contributing**

Contributions are welcome!
Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear explanation

---

### **Useful Links**

* 🌐 **Gradio documentation:** [https://www.gradio.app/docs](https://www.gradio.app/docs)
* 📘 **Azure OpenAI documentation:** [https://learn.microsoft.com/azure/ai-services/openai/](https://learn.microsoft.com/azure/ai-services/openai/)
* 🤖 **Prompt engineering guide:** [https://learn.microsoft.com/azure/ai-services/openai/concepts/prompt-engineering](https://learn.microsoft.com/azure/ai-services/openai/concepts/prompt-engineering)
* 💬 **Support / Discussions:** GitHub Discussions or Azure AI forum

---

### 📄 License

MIT License

Copyright (c) 2025 Gabriel Tobar TA220649

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---
