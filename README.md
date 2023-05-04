<h1 align="center">🐝 JobHive</h1>

<p>JobHive is an agent-actor system for job search assistance. The system includes several child agents and a parent agent. The child agents are specialized in different areas, such as job search strategy, career coaching, resume writing, interview coaching, and networking. The parent agent acts as a project manager and coordinates the child agents to assist the user in their job search.
</p>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [How Do I Use It?](#how-do-i-use-it)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [🔧 Install](#-install)
  - [🏃🏽‍♂️ Run JobHive](#️-run-jobhive)
- [🌟 Contribute to JobHive 🌟](#-contribute-to-jobhive-)
  - [Server-Side](#server-side)
  - [Client-Side](#client-side)
  - [🔥 Issues 🔥](#-issues-)
  - [🛠 Pull Requests  🛠](#-pull-requests--)
  - [💬 Discussions 💬](#-discussions-)
- [Code of Conduct](#code-of-conduct)
- [Acknowledgments](#acknowledgments)

## How Do I Use It?
<h4>1️⃣ Upload your resume</p></h4> 

![Alt Text](_upload.gif)
<h4>2️⃣ Activate agent-actors</h4>

![Alt Text](_activate.gif)

<h4>3️⃣ View results</h4>

![Alt Text](_results.gif)

I am currently building out the client-side interface that renders the results in a more user-friendly way. An example of rendered output can be viewed [here](rendered_output.pdf). For now, you can view the results in the terminal and in the `agent_interactions` folder.

## Getting Started
### Prerequisites

[Poetry](https://python-poetry.org/docs/), a Python dependency management and packaging tool.

Secret API keys for [OPENAI](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key), [Serper](https://serper.dev/), and [Wolfram Alpha](https://products.wolframalpha.com/simple-api/documentation).

### 🔧 Install
```bash
poetry install --with dev --with typing
```

### 🏃🏽‍♂️ Run JobHive
```bash
poetry run python jobhive.py
```

## 🌟 Contribute to JobHive 🌟

Thank you for considering contributing to JobHive! Below are some immediate needs that I have identified, but I welcome any contributions that you think could help optimize the project.

### Server-Side
- **API Integration with Socket-IO:** We are looking to implement real-time communication of agent-actor results to the client-side using Socket-IO. If you have experience with Socket-IO or real-time communication, we would love to hear your thoughts!
- **New LangChain tool integrations:** We are always looking to enhance our agent-actor capabilities by integrating new LangChain tools. If you have experience with natural language processing or machine learning and have ideas for new integrations, we would love to hear from you!

### Client-Side
- **Agent-Actor Profile Customization:** We are looking to add more customization options for agent-actor profiles to better match users' needs. If you have experience with front-end development and are interested in helping us improve our customization options, we would love to hear from you!
- **Prompt tweaks and customization:** We are always looking for ways to improve the output of our agent-actors, and this often involves tweaking and customizing the prompts that they use. If you have experience with natural language generation would like to help us improve our prompts, we would love to hear your suggestions!

Thank you again for your interest in contributing to JobHive! If you have any questions or ideas for contributions beyond those listed above, please don't hesitate to reach out in our Discord channel.

### 🔥 Issues 🔥

1. **Boldly Raise Your Voice:** Create an issue for any bug or improvement.
2. **Be Specific, Be Fearless:** Provide precise information for the issue.

### 🛠 Pull Requests  🛠

1. **The March of the Brave:** Create a branch from the master, giving it a meaningful name.
2. **Commit with Passion, Push with Purpose:** Keep commits concise and meaningful.

### 💬 Discussions 💬

1. **The Forum of the Fearless:** Engage in discussions, propose ideas, features, or improvements.
2. **Respect, Honor, and Civility:** Treat all participants with the utmost respect.

As we embark on this journey, let us charge forth, united in purpose and fueled by the spirit of collaboration! Together, we shall overcome all adversities and build an awesome agent-actor system for job search assistance! 🚀


## Code of Conduct
We are building a tool to help people find jobs. As such, it's important people from all walks of life feel welcomed to contribute their time and talents to this project. We expect all contributors to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it. Please follow it. Please help us keep this project a safe and welcoming space for everyone.

## Acknowledgments

We would like to express our gratitude to the following projects and their contributors for their inspiration and valuable resources:

- [**LangChain**](https://github.com/hwchase17/langchain): LangChain is an AI-driven natural language to programming language translation platform. It significantly contributed to the development of this project by providing essential tools and resources. We highly appreciate their work and encourage you to check out their project.

- [**Agent-Actors**](https://github.com/shaman-ai/agent-actors): Agent-Actors is a proof-of-concept project inspired by BabyAGI, the Plan-Do-Check-Adjust (PDCA) cycle, and the actor model of concurrency. This project was a stepping stone in the development of our current repository, and we want to acknowledge the ideas and implementation details that have helped shape our work.

Thank you for your contributions and for helping to make this project a reality.


but with some exploration you'll find the agents to be highly customizable. For example, you can change the agent's name, the agent's description the agent's skills, and the agent's personality. You can also add new agents to the system.