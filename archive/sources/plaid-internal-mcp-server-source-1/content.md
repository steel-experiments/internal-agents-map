> Archived source snapshot  
> Source ID: `plaid-internal-mcp-server-source-1`  
> Original URL: <https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb>  
> Final URL: <https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb>  
> Title: The Plaid internal MCP server. Maximizing the leverage of internal AI… | by Plaid Eng | Plaid Engineering  
> Captured at: `2026-08-31T17:45:43Z`

---

## Maximizing the leverage of internal AI applications

*The Internal MCP server and this blog post were created thanks to the hard work of many individuals at Plaid including: Jainil Ajmera, Allen Chen, Peter David, Evan Fuller, Zach Keller, Seyoung Kim, Charles Shinaver, Nathan Tindall, Roy Xu and many others.*

At Plaid, we have supercharged our AI efforts by building a foundational system to give AI applications the best possible context. Built on top of the [Model Context Protocol (MCP)](http://modelcontextprotocol.io/), developed by Anthropic, this system allows a variety of AI clients to access the data they need from our systems, and provides a consolidated, secure platform for working with AI at Plaid.

Now engineers are building agentic workflows that seamlessly integrate data used by employees in their day-to-day workflows like JIRA, application logs, and internal debugging interfaces. The platform has enabled us to build agents to triage bugs to improve support ticket resolution, look up data schemas to help data scientists write queries faster, and more! Let us show you how we did it.

### AI context problems

It’s no secret that the better context you give to AI systems, the better they will perform. If you are trying to debug issues with a production system, out-of-the-box LLMs can only take you so far — they need the specific information from and about *your* system, like your Prometheus metrics or recent server logs.

Retrieval Augmented Generation (RAG) systems were one of the early attempts to solve this problem, and they are certainly useful. However, mental models of context as document-only, or even document-first, have not been able to keep pace with the problem solving capabilities of the latest LLMs.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*9KkMbCkDPkKflsTLLdrtgA.png)

A conceptual diagram of a simple RAG system

As the models advanced, and as our understanding of them grew, practitioners have gravitated towards more agentic systems that rely on tool use and other meta-primitives like Prompts and Queries. All of these concepts are represented in the [MCP specification](https://modelcontextprotocol.io/specification).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*jifY2siSwoEJc-5n7Caazg.png)

A conceptual example of MCP integration in a typical MCP client system

Still, all of these ideas — from MCP servers generally to MCP primitives to ordinary RAG systems — are still fundamentally targeting the same underlying idea: delivering the right context to the underlying LLM at the right time. Most of the focus on context availability has been externally oriented; helping users access data that exists in managed services or services outside of the user’s owned systems, such as data from Github, Glean, or JIRA.

### What’s missing

We felt this picture was still incomplete. Claude Code and Cursor, AI tools used by over 80% of Plaid engineers, have robust interfaces for connecting MCP servers already, but a few key problems limited their full efficacy in terms of **velocity** and **security**:

- **Managing one-to-many arrangements of MCP servers**: There is a lot of variation in stability and quality when every engineer is managing their own arrangement of MCP servers in their local development setup. This introduces additional overhead and setup time, and ultimately limited how many people we saw experimenting with MCP.
- **Availability of MCP servers with service providers**: Any integration with a third-party tool requires a new MCP server to be set up in order to be made accessible to the dev. So, for any individual tool we’d need to hope our vendor offers an MCP server, test it out, provide feedback to the vendor, and then harden the integration. This didn’t allow us to move fast enough — and it wouldn’t enable internal data use cases anyway.
- **MCP authentication and authorization**: Authentication and Authorization with MCP servers is still fairly immature; not all of them support OAuth, and even if they did, our SSO integration or our enterprise self-hosted integration might not be directly supported.
- **Enabling access to internal data remains a challenge**: Third party MCP servers don’t help us access data from our own internal systems.

Of these, the fragmented local setups and internal data access were the most acute blockers. Engineers were spending more time wrestling with server configs than with code. The other issues compounded that drag, creating manual workarounds and interdependencies that further eroded our speed. Altogether, these frictions forced engineers to divert development time into chores, or to abandon AI tools entirely, directly undermining our mandate to accelerate development.

### Problem space

When thinking about how to solve this problem, we started by outlining the resources that we had, and the things that constrained us.

We realized Plaid already had existing security infrastructure to scalably manage user-based access to specific production resources and internal tools. For example, our internal permissioning system controls which gRPC methods a given user is allowed to call within our global gRPC debugging UX. Similarly, a constellation of existing services already managed the authorization token generation and verification portion of enabling that access at the user level.

## Get Plaid Eng’s stories in your inbox

Join Medium for free to get updates from this writer.

Internally, Plaid runs an identity aware proxy that protects internal tools. A centralized authorization server for employees checks the access that an individual has to production resources. Since Plaid primarily runs gRPC services, we allow service owners to selectively enable employee debugging access by gRPC method. Our identity aware proxy validates that the employee is running a Plaid managed device and has authenticated through our identity provider before allowing the employee through to the gRPC service.

A signed identity token is then validated and parsed to get the employee’s identity. Finally, our centralized authorization server validates whether the employee has access to the gRPC method. We support CLI based authentication with [Device Authorization Grant flow](https://oauth.net/2/grant-types/device-code/) with [DPoP](https://oauth.net/2/dpop/) and short lived bearer tokens. Bearer tokens are signed with a private key pair initially generated and validated during the device flow. The CLI based auth is used in the Internal MCP server to provide auth through a locally running proxy.

On the constraint side, Plaid has a robust LLM data access policy that dictates what sorts of data can go to which kinds of LLM and when. Respecting this data access policy is a core constraint of any LLM system at Plaid, and we needed to ensure granular control over data access.

So, to enable us to move quickly and securely, we needed an approach that let us directly control all of the third party integrations ***and*** document context ***and*** data from production services. But we don’t want engineers to have to manage all of these connections themselves.

### What we did

Given our needs for velocity and security, we implemented one central *internal* MCP server: a server that would connect engineers and their AI tools to the data they needed.

Our philosophy was to leverage the existing components, along with our LLM data access policy, to safely and securely abstract away all of the overhead that comes with adding context to user-driven internal LLM applications, and to do this in a way that minimizes dev-local tool management.

The diagram below illustrates an example of how the internal MCP server can be implemented for a typical use case.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*3N2LgVFhT5spzLBT0dq8zg.png)

Internal MCP diagram

**This design has a few interesting points:**

- The internal MCP server is separated from the existing LLM gateway, which can be a separate component that lets internal users create specialized AI agents, but have them share the same tool library. This approach feels somewhat unnatural at first; the internal LLM gateway could alternatively connect to the internal MCP server as an MCP client. However, this approach has some advantages:
- The tools that should be allowed for the internal MCP server and for the LLM gateway form an intersecting set, but not a subset in either direction. That is, there are tools that should be available in the internal MCP but not to agents, and vice versa. Enforcing this restriction at the service level would involve difficult to parse logic that is likely to become a footgun.
- By pushing the tool definitions out to a library, data usage restrictions can be implemented at the tool level that address the root of where the allowed tool differences stem from.
- The existence and importance of an LLM data usage policy — common at many firms — imposes certain constraints that make a centralized system of access control and verification, caller identity inspection, and audit logging more attractive than decentralized alternatives.
- This system is built on top of the existing security framework for user-level permissions. While not universal, our view is that this sort of access control framework likely does exist at many companies today, and can be naturally replicated.

At a high level, this consolidated, one to one to many approach maximizes future extensibility. Accessing context sources directly, rather than waiting for plugins to become available, allows fine grained control not only over how those integrations work, but also provides discretion in using availability constraints, for example, with respect to which tools publish plugins.

Another supporting consideration is the LLM data usage policy. This design enables enforcement of controls on these restrictions at the tool level at call-time, ensuring policy compliance. By connecting directly to data sources directly via API and feeding that data straight into our internal LLM interface, we can move at full speed with zero external barriers.

All told, we have integrated more than 20 tools, a half-dozen internal services, our documentation, and more into the internal MCP server. Plaids have made thousands of tool calls and created dozens of agents across the engineering, product, and support spectrum that rely on the internal MCP server.

### What’s next

You might have noticed some comments about an internal LLM gateway. The next step for our internal MCP server is to continue to build agent-building components on top of it that allow Plaids to create their own agents right out of the box, using the same tools that are in the internal MCP.

We’ve already built a UX service for creating and interacting with these agents, and expect to continue adding capabilities for agent creation, interaction, and integration into live services — all powered by the data access of the internal MCP server.

As with everything AI, the future is not assured. It is difficult to see how these quickly-evolving systems will develop. However, the need for immediate, task-specific, high quality context seems likely to remain important well into the future. And for that, there’s the internal MCP.
