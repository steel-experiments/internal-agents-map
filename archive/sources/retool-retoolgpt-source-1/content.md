> Archived source snapshot  
> Source ID: `retool-retoolgpt-source-1`  
> Original URL: <https://retool.com/blog/how-we-built-retoolgpt>  
> Final URL: <https://retool.com/blog/how-we-built-retoolgpt>  
> Title: What is RetoolGPT? How we built an internal AI assistant | Retool Blog  
> Captured at: `2026-08-31T17:47:13Z`

---

When deciding how to adopt AI inside an organization, the most common first use case is to reach for one of the public chatbots—the ChatGPTs and Claudes of the world. While these chatbots each have their own privacy and data-sharing policies, they often lack the ability to seamlessly incorporate data from your business efficiently or at scale.

We faced this challenge at Retool, too. Some team members preferred ChatGPT, others wanted to use Claude, and a few were exploring Gemini, but none of these AI tools could provide accurate, up-to-date information about Retool beyond what was available in their public training data. At the same time, there was all sorts of information buried in Confluence docs that weren’t effectively searchable. By exposing this data to LLMs, we hoped to more easily surface the Retool-specific information members of our team were looking for.

**In this post you'll learn:**

- What RetoolGPT is, and why we built it
- How we integrated with internal knowledge sources
- How the frontend, backend, and model selection all come together
- Why this app set the stage for building [AI agents](https://retool.com/resources/what-are-ai-agents) in Retool

RetoolGPT is an internal version of ChatGPT that has access to our Confluence documents, Retool documentation, and Linear tickets as data sources. This means we can easily switch between chat models if one isn’t working as expected, and RetoolGPT can use internal company data to provide better, more specific answers to users’ questions.

![Blog post image](https://retool.com/vc-ap-126ac9/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fbclf52sw%2Fproduction%2F76a59ad0818e4d3ac605788e4b2e3cf6652482b7-1999x1142.png%3Fw%3D1920%26q%3D80%26fit%3Dmax%26auto%3Dformat&w=3840&q=75)

Blog post image

We considered several off-the-shelf SaaS options for this functionality but chose to build it internally instead. This decision allowed us to not only test [Retool’s AI features](https://retool.com/ai) ourselves, but also gave us the flexibility to customize the interface, select the most relevant integrations, and quickly iterate based on user feedback.

Let’s examine how the different components work together and what to consider when building a similar tool for your organization. On the frontend of the application, several key factors contribute to creating an excellent chat experience.

When designing the interface, we aimed to align closely with ChatGPT’s interface since our users would likely already be familiar with it. The first important decision to make was deciding on a user interface. Retool provides a [pre-configured Chat component](https://docs.retool.com/apps/reference/components/chat), which is the fastest way to build a RAG chat app with a few clicks. But we wanted more customization. Luckily, with Retool, you can choose: use an out-of-the-box component, compose something with [Retool components](https://docs.retool.com/apps/concepts/components/), or build a fully custom React component. We opted for the middleground and assembled our chat out of various Retool components—which gave us a ton of customization options without having to write any UI components:

- **Core chat components**: All the expected elements—like the main message box, send button, and message history display—take up the main portion of the interface.
- **Collapsible sidebar**: We built a feature that lets you hide and show previous chats, which is particularly helpful during screen sharing when you want to keep your chat history private. Each chat thread in the sidebar displays a clear title that summarizes the conversation’s content.
- **File upload**: Just like ChatGPT, we wanted to let users upload files and include their contents in the context for their selected language model.

However, we also made some key upgrades that allowed RetoolGPT to be even more powerful than ChatGPT for our specific use case.

RetoolGPT’s model selector gives you more flexibility than ChatGPT by letting you choose between OpenAI, Anthropic, and DeepSeek modelsThis approach allows you to try multiple models and even switch between them mid-conversation—going beyond ChatGPT’s OpenAI-only options. We also recently launched the ability to [dynamically select a model](https://docs.retool.com/changelog/retool-ai-dynamic-model-selection) in an AI query, making this much easier to handle on the backend.

Just above the chat input, you’ll find a set of toggles that let you select which data sources to include in the LLM’s context when generating an answer. These data sources are already ingested into Retool’s built-in vector database (more on that later). Turning these toggles on or off controls how much vector data is included in each prompt sent to an LLM. For example, if you’re chatting about a specific engineering issue or seeking context about a reported bug, you might enable the Linear and Docs toggles while leaving the Docs toggle, while leaving the Confluence toggle disabled.

In the upper-right corner, we have a feedback button/interface that lets users share their thoughts and report issues. This is important because RetoolGPT is under active development, and it’s vital that users can report bugs and give more context to the issues they’re encountering.

Overall, we maintained key similarities to ChatGPT’s core interface while adding thoughtful customizations to address our specific internal use cases.

When building a chat interface in Retool, you’ll run into an interesting decision point around state management. Retool’s template syntax—those double curly braces you see everywhere—is incredibly powerful for quick development. You don't have to think about dependencies because Retool automatically figures out which components need to update when. This is a helpful feature that makes building simple apps lightning fast.

However, when building RetoolGPT, we needed to modify that approach slightly because of the app’s complexity and our specific requirements.

In addition, instead of using Retool’s default event handlers, which respond to events at the component level and allow components to trigger queries and other functionality in the app, we opted to standardize all of our logic in a single JavaScript file, much like developers would be familiar with in a traditional codebase. Especially when an app has lots of event handlers, it can be much easier to manage complexity in a single JavaScript file than trying to piece together logic across 15 different query handlers.

This became particularly important for features like message handling, where we needed to update the UI immediately while waiting for server responses. If we had built this using Retool's template approach, we would have needed to coordinate multiple event handlers—one for showing the message, another for saving it, another for getting the AI response, and yet another for updating the UI when the response came back. By centralizing all of this in JavaScript, we could orchestrate this complex dance of updates in a much more straightforward way, making our code easier to understand and maintain.

![A completely-custom Javascript query that manages the state of our app.](https://retool.com/vc-ap-126ac9/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fbclf52sw%2Fproduction%2Fe855482ec180fd62cd26950f8c7024f5444a51e9-1999x1409.jpg%3Fw%3D1920%26q%3D80%26fit%3Dmax%26auto%3Dformat&w=3840&q=75)

A completely-custom Javascript query that manages the state of our app.

Outside the UI of the app, multiple [backend workflows](https://retool.com/workflows) make the app run smoothly. Let’s explore how these come together to power RetoolGPT.

![Blog post image](https://retool.com/vc-ap-126ac9/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fbclf52sw%2Fproduction%2Fd89ad689249f5bfa98bb7feb45d39fded9891366-1971x1000.png%3Fw%3D1920%26q%3D80%26fit%3Dmax%26auto%3Dformat&w=3840&q=75)

Blog post image

This workflow powers the core chat functionality of our app. When a user clicks “Send” in the UI, this workflow initiates its run.

- **Get the context**: At the beginning of the workflow, we query [Retool Database](https://retool.com/database) for all previous messages from this thread. We combine these messages with relevant context about the user and map the data into XML to make it [more digestible for large language models](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags).
- **Save the message**: This step saves the user’s latest message to Retool Database, ensuring the message history stays consistent and up-to-date.
- **Handle special cases**: If there is a file attached to the message, it is uploaded to Retool storage, transformed into text, and included with the user’s message. The same process applies when a data source is selected. Based on the enabled toggles, the workflow performs a semantic search through Linear, Confluence, and/or our documentation and includes relevant results as context for the eventual LLM call.
- **Generate a response**: This is where we gather all the context added to the user’s message and send it to their specified LLM. Once the model generates a response, we save it to Retool Database to maintain an accurate message history. The response is then passed back to the UI for display to the user.

To keep our data sources in Retool’s vector database current and synchronized, we use a set of workflows that leverages the relevant API. These workflows first determine what content needs ingestion, then download the data and process it through an embedding model before storing it in the vector database. These workflows run periodically to make sure that our vector database is always up-to-date.

To ingest our Confluence documents, for example, we first query the Confluence API to get a list of all Spaces containing our documents. Then we call a separate sub-workflow to retrieve all documents within each Space.

![Blog post image](https://retool.com/vc-ap-126ac9/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fbclf52sw%2Fproduction%2F02235cd9226b58bfbee9bb8cbfda0015d76b4f18-1971x1150.png%3Fw%3D1920%26q%3D80%26fit%3Dmax%26auto%3Dformat&w=3840&q=75)

Blog post image

For each document, we run another workflow that processes the content and “upserts” it into the vector database, making it accessible to future RetoolGPT users.

![Blog post image](https://retool.com/vc-ap-126ac9/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fbclf52sw%2Fproduction%2Fd37cf190604a33a986aa858c9e6b0c3069e78c3d-1971x1150.png%3Fw%3D1920%26q%3D80%26fit%3Dmax%26auto%3Dformat&w=3840&q=75)

Blog post image

These workflows are flexible enough to be cloned and repurposed for ingesting data from almost any source using one of Retool’s [native integrations](https://retool.com/integrations) or any REST API. And because all document ingestion and storage happens in Retool’s [built-in vector database](https://docs.retool.com/data-sources/tutorials/retool-vectors), this system can handle data from any source while still producing reliable output that helps a large language model provide relevant, correct responses to users.

RetoolGPT automatically generates titles for chat threads using its thread titling workflow, which activates when the first message in a thread is sent. Instead of requiring manual thread naming, the system sends the initial message to a language model to generate a quick summary of the thread’s topic. This summary is saved to the database and displayed in the left sidebar, making it easy for users to identify and navigate between conversations. The entire process runs in the background without user intervention — users simply start a conversation, and RetoolGPT handles the thread organization automatically.

Once we had the first version up and running, we needed to figure out how to deploy it across our entire organization. Because of the complexity of this particular app, we wanted to make sure it was relatively locked down and not editable by just anyone in our organization. This is where Retool’s permissions capabilities come in handy. We deployed it into an environment where user permissioning was already largely read-only, meaning that everyone on our team could benefit from RetoolGPT without worrying about accidentally misconfiguring the app.

For sensitive applications, setting up granular user permissions at the app level ensures that your data stays secure and your apps remain reliable.

Building RetoolGPT taught us several valuable lessons about developing AI applications in Retool. While Retool provides powerful out-of-the-box components like the chat component and handles the complex concept of state management automatically, sometimes you need to go beyond these defaults. For example, rather than using the built-in chat component, we built our interface from individual Retool components. Similarly, instead of relying on Retool's automatic state management, we took control of our state manually through JavaScript. These decisions required more upfront work but gave us the flexibility to create exactly the experience we wanted.

Unlike ChatGPT, which is tied to OpenAI's models, RetoolGPT can work with any language model available in Retool. This means you can easily switch between different providers, compare their performance, and adapt as new models become available. Whether it's OpenAI, Anthropic, or a [custom LLM provider](https://docs.retool.com/data-sources/guides/connect/custom-ai-provider) like DeepSeek, you're not locked into any single solution.

The foundation of RetoolGPT rests on three core Retool building blocks: Retool Database for storing conversation history, Retool Vectors for managing our knowledge base, and Retool Storage for handling file uploads. This infrastructure ensures that all our data—whether it's chat threads, vectorized documents, or uploaded PDFs—is always available and in the right format. By leveraging these built-in tools, we were able to focus on building features rather than managing infrastructure, while maintaining complete control over our data and user experience.

As we continue to add [AI agent capabilities](https://retool.com/ai) to the Retool platform, RetoolGPT will continue to get even better. Whereas today you need to specify whether you want to pull data from Confluence or other sources, in the future, RetoolGPT will be able to decide which tools to call in order to solve user questions and dive deeper into different levels of detail depending on the question asked.

These are the sorts of problems that we’re helping users solve with [Retool Agents](https://retool.com/agents). Building RetoolGPT as an agent means all the workflow complexity and need for explicit tool calling has gone away. By configuring your agent with access to a large language model and a base set of instructions, as well as a set of tools (things like Confluence, Google Docs and Linear access), your agent will be able to respond to user queries by deciding what tools to call at run time to get users access to the best, most up-to-date information.

RetoolGPT was a big inspiration for the kinds of features we added to our new Agents features and now makes it even easier to build these kinds of tools inside your own business.

RetoolGPT started as an internal solution to a common problem—how to make company knowledge more accessible through AI while maintaining control over data and user experience. By building it ourselves using Retool, we not only solved our immediate needs but also created a blueprint for how other organizations can approach similar challenges. The project demonstrates that you don't need to choose between off-the-shelf solutions and building from scratch—with Retool, you can take a path that gives you the best of both worlds.

For us, RetoolGPT has become more than just a chat interface—it’s a testament to how internal tools can be both powerful and polished when built with the right platform. We hope sharing our experience helps other teams see what's possible and inspires them to build their own solutions that fit their unique needs.

Want more? [Check out our AI Build Week session on RetoolGPT.](https://retool.com/resources/videos/ai-build-week-day-3-how-we-made-retool-gpt)

![](https://www.youtube.com/watch?v=8VTdYUBAZsY)
