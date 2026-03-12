# Python Zero to One

> **From absolute beginner to building modern, efficient Python applications—amplified by AI.**

Welcome to **Python Zero to One**.

This course is designed to take you from knowing nothing about code (Zero) to building your first Python application (One).  
(The name is inspired by the phrase "Zero to Hero.")  
We'll learn how to use AI to generate rapid prototypes, then refine those outputs into more concise and reliable code by learning basic syntax and concepts.  
The total estimated time required to complete this course is approximately 30 hours.

## Getting Started

Before you begin this course, please set up the following environment.  
> The following tools are not mandatory; you can use any alternative.

* Step 1: Prepare at least one AI Assistant

  AI assistants can generate examples, explain unfamiliar syntax, and help you debug errors while learning.  
  Gemini was launched by Google and is offered free of charge.  
  We will use Gemini as our AI assistant throughout the course.  
  Open [Gemini](https://gemini.google.com/) in your browser.  
  If you encounter any problems, you can first ask Gemini to help you confirm what went wrong and how to fix it.

* Step 2: Install Python

  Python is the core programming language used throughout this course.  
  It is the environment that runs your scripts and allows you to build applications.  
  Download and install [Python](https://www.python.org/downloads/).

  During installation, make sure Python is added to your system PATH if the installer provides that option.  
  After installation, open your terminal and run the following command to confirm it works:

  ```bash
  python --version
  ```

* Step 3: Install a code editor / IDE

  Code editors and IDEs make it easier to write, run, and debug Python code.  
  Even if you can use a plain text editor, a dedicated development tool will significantly improve your learning efficiency.  
  JetBrains is a leading provider of IDEs and tools.  
  Download and install [JetBrains PyCharm](https://www.jetbrains.com/pycharm/).

* Step 4: Clone this repository

  Git is a version control system that allows you to easily update the course materials.  
  Download and install [Git](https://git-scm.com/).  
  Open your PyCharm and click the `Clone Repository` button.  
  Copy the URL of this repository: `https://github.com/kevinju0827/Python-Zero-to-One.git` and paste the URL into the field.  
  Click the `Clone` button to download the repository to your local machine.  
  Next time you want to update the course materials, you can simply click the `Update Project` button to pull the latest changes.

  > **MacOS Users**  
  > On macOS, we recommend installing [Homebrew](https://brew.sh/) first, then using it to install Git.  
  > Homebrew is a package manager for macOS that makes it much easier to install and manage developer tools.  
  > Open the `Terminal` app and run the following commands:
  > ```bash
  > /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  > ```
  > Then, run the following command to install Git:
  > ```bash
  > brew install git
  > ```

* Step 5: Open the `README.md` file

  `README.md` is the first file you should see when you open the repository.  
  Open the `Python-Zero-to-One` repository in your PyCharm and click the `README.md` file to open it.  
  Switch to the `Preview` tab at the top right to view the content.

  > `.md` stands for Markdown, which is a lightweight markup language that allows you to write formatted text using a simple syntax.  
  > It is not necessary to understand Markdown to follow along with this course.  
  > You can refer to the [Markdown Guide](https://www.markdownguide.org/basic-syntax/) for a quick introduction.

  In every module, we will also provide a `README.md` file as a learning guide.

## Philosophy

**AI is best suited for handling common requirements, boilerplate code, or building rapid prototypes.**

In the age of AI, coding has changed. You don't need to hand-code every single line anymore.
However, because AI works with limited context, it can struggle to account for the full details of large-scale projects or handle highly specific, complex business logic.

**To use AI effectively, you cannot rely on it blindly.**

The core focus of this course is to equip you with the understanding of programming concepts, control flow, and basic syntax.  
This fundamental knowledge is the minimum requirement for you to review, modify, and fix the AI-generated content when it occasionally hallucinates or makes logical errors.

## Curriculum Structure

The repository is organized into modules. Each module in this course is designed as a self-contained learning journey, moving from conceptual understanding to practical mastery.  
To ensure a consistent and effective learning experience, Each module contains the following:

1. **The "Why?"**  
   Before diving into the code, we answer the most important question: Why are we learning this?  
   You will explore how these specific concepts are applied in the real-world context.
2. **Goals**  
   The Goals serve as your objectives for learning this module.   
   Written in plain, accessible language, these goals define what you should understand and be able to articulate by the end of the module.
3. **Core Concepts**  
   This is the heart of the module. Core Concepts provide a deep-dive explanation of programming syntax and technical concepts.  
   It includes detailed explanations and code demonstrations for each topic.
4. **Guided Practice**  
   To make each module easier to follow, we also provide a step-by-step walkthrough.  
   This section is designed to guide you through a small but complete practice sequence, allowing you to apply what you just learned in a concrete way.  
   By following the execution flow, you will:
   - know exactly where to start
   - produce a small example that demonstrates the core concepts of the module
5. **Checkpoints**  
   Checkpoints are designed to verify your learning through practical scripting.  
   Successfully completing these checkpoints serves as proof of your technical competency and readiness for the next module.  
   > **There is no single "correct" answer for the checkpoints.**  
   > Programming is about problem-solving. Since we embrace AI tools for code generation, success is defined by your ability to **explain** your logic, handle errors, and **modify** your code confidently.  
   > Please do not consider a checkpoint "done" just because AI produced an output.

## Tech Stack

### Languages

- **[Python](https://www.python.org/)**  
  The core environment required to run your scripts. We focus on modern Python 3.x features.

### Tools

#### Integrated Development Environment (IDE)

- **[Visual Studio Code](https://code.visualstudio.com/)**  
  The industry-standard, lightweight code editor. It supports a massive ecosystem of extensions, making it perfect for Python.
  - **[GitHub Copilot Chat](https://github.com/microsoft/vscode-copilot-chat)**  
    The AI pair programmer for VS Code. You can chat with it to generate algorithms, explain complex logic, or debug errors directly in your editor.
- **[JetBrains PyCharm](https://www.jetbrains.com/pycharm/)**  
  A powerful IDE designed specifically for professional Python development. It provides deep code analysis and intelligent refactoring right out of the box.
  - **[JetBrains AI](https://www.jetbrains.com/ai-ides/)**  
    Integrated AI assistant that provides code generation, explanation, and unit test writing seamlessly within PyCharm.
  - **[Junie](https://www.jetbrains.com/junie/)**  
    The next-generation AI agent for JetBrains, focusing on advanced predictive coding assistance.

#### AI

- **[Gemini](https://gemini.google.com/)**  
    Google’s AI assistant for brainstorming, explaining concepts, and generating code or content from prompts.

#### External Data

- **[JSONPlaceholder](https://jsonplaceholder.typicode.com/)**  
  A free, fake REST API. Perfect for practicing how to fetch and process data using Python without dealing with complex authentication.
- **[Kaggle Datasets](https://www.kaggle.com/datasets)**  
  A huge repository of community-published datasets. Great for finding real-world CSV or JSON data to manipulate and analyze with your scripts.
- **[Taiwan Government Open Data](https://data.gov.tw/)**  
  A massive collection of real-world datasets provided by the Taiwanese government. An excellent resource for practicing how to fetch, parse, and analyze localized CSV or JSON data (such as real-time weather forecasts, public transit status, or economic indicators) using Python's requests and JSON modules.

## Recommended Resources

(Optional) In addition to the resources provided within this repository, we highly recommend learning from and utilizing the following:

- **[Official Python Documentation](https://docs.python.org/3/)**  
  The gold standard documentation. While it can be dense, it is the ultimate source of truth for how Python works under the hood.
- **[roadmap.sh Python Developer](https://roadmap.sh/python)**  
  A visual guide to the Python landscape. Use this to track your progress and understand what concepts to learn next.
- **[Real Python](https://realpython.com/)**  
  One of the highest-quality sources for Python tutorials. It provides in-depth, practical examples covering everything from basic syntax to advanced concepts.
- **[Atguigu Python](https://youtu.be/n97hSmVyjsg?list=PLmOn9nNkQxJFWhyrhPNkpI3lMuKxBTxBe)**  
  Comprehensive and free video tutorials in Chinese. An excellent choice if you prefer learning complex concepts through video content in Mandarin.
- **[LeetCode](https://leetcode.com/)**  
  Gamified platforms for practicing coding challenges. Essential for sharpening your algorithmic thinking and preparing for technical interviews.

## License

Distributed under the MIT License. See `LICENSE` for more information.
