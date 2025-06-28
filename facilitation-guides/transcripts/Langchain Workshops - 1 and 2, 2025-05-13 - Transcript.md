We're gonna be talking about today. We're gonna build an email assistant that's a great example of an ambient name. Now here's a road map of where we're going and what we're gonna do. So first, we're gonna build the agent itself. That's blue.

We're gonna use Landgraf to do that. So you're gonna learn all about Landgraf. Then we're gonna test it. That's what you Let's say we have an email API. Say it's Gmail.

You can actually take that API and turn it into a tool, and you can bind that tool to a model. Okay? When you do that, as you see in step two, the model has awareness that this tool exists, and it can do what we call tool calling.

This is a central principle underpinning agents, and the idea is very simple. LLMs are present in that tool column. Okay? Those arguments be passed to the tool, and the tool will be executed. Two for kind of sending email. So two key ideas here.

One is the fact that LLMs can perform tool column. So I wanted to really make sure that's very crisp because that's the key idea that underpins agents. Now what is the simplest possible email system we could fill? It would be like this. We have an LLM.

It has one tool. It has an email tool. It runs that tool. It produces a tool call like we talked about. Just structure it out. We run the full send an email. So email in, email sent out. Think about it in terms of agency versus email.

Agency is the number of different decisions this thing can make. Predictability is the predictability of decisions that makes. Now let's bump this up a little bit in complexity. Let's add one other LM step before to just make a decision. Do we wanna send an email or ignore it?

Or just notify the user but not send it? This is what we call a workflow. It's a very useful pattern to basically call LLMs in predefined code paths. It gives the system a little bit more agency. It can make one decision, respond or not.

If we decide to respond, we send the emails. Okay? Now agents, you hear a lot about. What is an agent? An agent is very simple. Imagine we took that initial system. It had one tool. We give it a collection of tools. Give it three tools.

Previously, it called the tool and we finished it. Now we call the tool. We send that tool call back to the LLM. That's an agent. It's very simple. You keep calling tools in the loop until it gets some termination condition. We'll talk about that later.

This has more agents than the other two for this reason. The first system, always call an email tool. Now you can call any sequence of tools this? If you can easily draw ahead of time the control flow that you want, workflow's fine. You don't need an agent.

And people often don't need agents because it's interesting and it's a buzzword. Do you really need an agent? Oftentimes, if you can enumerate your steps in advance, the workflow is perfectly appropriate. Now agents are good if you actually need more flexible decision making at run time.

You can't predict what actually you need in terms of tool calls. They don't respond to an email. Every email's a little bit different. Sometimes you might need to just write a response, sometimes to schedule a meeting. That's why agents would be more appropriate for that particular task. Okay.

Now how does Landgraf come in? So here's the bridge. Landgraf lets you flexibly combine workflows and agents together. It's a set of low level components in an orchestration framework composed of nodes and edges. Nodes are units of work. Python functions are TypeScript code. You have direct control over.

There's no abstraction. Node is a simple function. Edges are transitions between nodes, which you can define. Now here's the key point. Landgraf lets you sit where you wanna live on this curve. So it lets you very easily build any of these different architectures because it's multiple components.

Many times agent libraries just have, like, front library for agent. It's an agent abstraction. It doesn't let you flexibly build many Now Landgraft also has a persistence layer that allows some important things we're gonna be using over the course of this workshop. It allows human loops.

You can pause the agent to collect feedback before making a sensitive tool called sending out an email. Which we'll be talking all about. And it has an easy on ramp deployment with Landgraft platform. It's gonna support many different things, streaming, long running background tasks, those memory can loop.

We'll show all this later. So one thing that comes up a lot that I wanna really make sure is clear, how does LangChain, LangArt, and LangSimit all connect? Okay?

LangChain, can think of as a set of standard interfaces for common components like chat models that allows you to connect to many different wires. Lang graph is orchestration as you're gonna see quite a bit here, but you can use language and abstractions within Lang graph.

That's the key point. Within these nodes, you can very easily have, for example, a Lang chain chat model. Now Langsmith allows for observability and testing of any workflow the foundation for building workflows pages.

And if you have the repo set up, make sure you cloned it, set it in the file, or just have an OBI key set in your records. And then you can initialize, in Oh, yeah? You wanna use my key? It did.

We can see we've built an LLM, and we get an AI message. Okay? So you wrote a model. You get an AI message. That AI message has content and some metadata, and you can easily extract this content out of here. So now let's talk about tools.

We introduced tools previously. Here is a simple way of creating tools from scratch. Here's a function called write email with a few different arguments to subject content and simple doctrine.

All you can do is take this decorator tool, add it, and now you can see the type of this function is structure tool. The arcs and the description of the tool are inferred from that function definition.

This is how we create a tool very easily from any Python function as an example. I also provide a link to the ability to easily create tools from MCP servers if you're interested in that. But the point is tool definition in LightningShade is quite easy.

Now tool column, we talked about that previously. The init chat model interface that we use has a very convenient method called time tools where I can pass in a list of tools, in this case, a single tool.

And there's a few parameters here I wanna introduce because they're useful. We'll use them later. Now all we need to do is just invoke our model tools just like before, and I'll show you something interesting, assuming this works. I will show you the type. It's still the messenger.

Let's look at it, though. In this case, there's no content, and we have this tool call. Now let's look at that. We can extract the r's easily. It's just a dictionary. This is exactly what talked about before. Tool calling is nothing more than structured outputs.

That's the way it's doing. Can pass those args to the tool we defined. Now remember, this write email is a tool we defined using that tool decorator. We invoke it with the arguments from the tool call. We get a result, which will say email is sent.

This is a very subtle but important concept. LLMs can call tools, produce tool calls. That tool call is a structured output. We can pass that tool call to the tool itself to run the tool.

This write email tool in the real world or replication could be like the Gmail API. So it's actually doing some real thing in the world. It's just a test. But the point is models produce tool calls. Tools are executed using new arguments from the tool call.

That's the key point. Now we just did a model that's kind of like what we talked about previously. We did provide an external prompt, but the flow is very similar. In LLM, we bound a single tool. We force model the call in. It produces a structured output.

We have an email sent. Nice and simple. Now we talked about a simple flow like that. It's not what we actually want. We wanna build a we wanna build things like agents. We wanna build applications that can reason.

We've talked about workflows as one example, and we talked about agents as well. We talked about the differences. I just wanna reinforce them here in the notebook, but we kind of covered this already. Now the bridge here is how we can use line graph.

So Minecraft allows us to very simply set up so Minecraft gives us three fundamental benefits. Control, make it easy to find and combine agents and workflows. Persistence, provide a way to persist the state of the graph, and testing, debugging, and deployment.

I wanna talk about control first, and I'll introduce persistence and then deployment. So with control, there's three things to think about when you're setting up a graph line graph. One is the state. What information we need to track over the course of the application? The second is nodes.

How do we wanna modify that state over the course of the application? And the third is edges. How do we connect those nodes together? Okay? So we can use the state graph class in LandGraph to initialize a graph with a state object.

Now this state object is nothing more than typically a dictionary. Could be a data class, could be a pedantic object, but it's just a placeholder for the information you want your application to track over time. In this case, let's do something really simple.

We're gonna find what we call state schema here. It's a typefix with requests and email. We initialize the statecraft as a workflow. Here we go. Now remember, nodes, units of work, which could be functions. Edges connect nodes. Here is an example node. This is exactly we did above.

Call our model tools, get the arguments, execute our tool call. We see something interesting here. What's the input? What's the output? The only thing that's different about when you're setting up when you're setting up a node is in Minecraft. The input is our state. State is a dictionary.

From the state, we can get requests very easily. Just a dictionary. Now we write email out as a dictionary state. This is what we call state update.

So what happens is nodes typically do work on the state, and they can update the state with what you returned from them. In this case, we just overwrite the value of the enough, which was done before, with the enough we produce. We're done.

All we need to do is add our node to our graph. So at an edge, we start to our node from our node to end. Compile it. Run it. Run it with an initial value of our state. In this case, our initial state is just request. Boss.

That's what we saw before. And the state is now populated with email. This is like the simplest possible graph you can build, but it's just the concept of you're defining a state. That state is being passed between nodes. Nodes do some work on the state.

In this case, you just create the email, wrote it to state Okay. And just connect nodes together. That's it. Now in applications that we're gonna build, we want the ability to conditionally go to different nodes. We don't always wanna go from node a to node b.

We want the ability to route. That's what this notion of a conditional edge what this notion of a conditional edge is. I wanna take what we did before and split it into two different nodes now. Call it on to call our model. Run tool to run our tool.

K? I'm also gonna change this around a little bit. I'm now gonna use messages stage or state op. This is a little bit different. This is a prebuilt state op we have in Minecraft with a single key messages. Remember that Chef halts return messages.

This key will just accumulate a list of messages while this graph is running. Let me show you what I mean. In this call LLM node, we'll call our model. Remember before, this model produces an add message.

We're going to, you see, return that message as a list to the messages key. That's gonna append the message of the output of the model to our state. So it won't overwrite. It'll just append.

When we run the tool, we can just look at message, which is a list, get the the most recent one, which will be our call from the l one, run the tool path, generate a tool message, add that to our state. Very simple.

So our state, you can see, it's gonna be a list of messages. Our l l m call will make l m calls, add that AI message to our list. Our run tool node will call the tool, add a tool message to our list.

This is another important concept to understand. With messages, there's multiple types typically. User or human messages, that's me talking to the model. Shack or AI messages, the model responding. Tool messages, tools producing an output.

Many chahmals designed to use the three message types, and we use them right here. All you need to do is specify role, in this case, to den to delineate that that is a dual message.

Now should continue is a conditional edge that will very simply look at the last message, check if it has a tool called. If so, we run the tool. If not, we end. Very simple. Add our nodes. Add our conditional edge. The function here is our conditional edge.

It goes from call l m to either run tool or n. That's it. In node, we do state updates. As you see, we return here updates to our state. In edges, the conditional edge, return the name of the next node. Let's go ahead and compile that.

See our graph. Very nice. We're gonna be diagonal graph. We call our model. Conditionally, we run our tool, and then we end. Let's run that. There we go. There's a list of messages. Draft response to my boss. The tool call is made in that alone call node.

It's added to the state. Remember, we're just looking at the final value of our state here. That's a list of messages. The nodes added to that list incrementally as it ran. Human message goes in. AI message is appended when LM node runs with the tool call.

The tool can run, and we end. That's it. Very simple. Now with these local components, you can build a lot of things, and we'll show that shortly. But because agents are so popular, I do wanna call out we have

an abstraction for agents called pretty react agent right here. You pass in the model, you pass in the list of tools, and you pass in a system prompt. There's some instructions. This is an example shown we did previously, but as an agent. I'll show you the only difference.

It's very minor. And, again, we'll look at the list of messages. There we go. Same input. Same tool call. Same tool message. Previously, we sent this. Now the tool message is sent back to the LM.

The LM looks and says tool call is made and responds with a message. The way agents are often set up is that they continue calling tools until no tool is called, and they end. That's exactly what happens here. We call a tool.

The tool must have sent back to the model. The model looks and says, okay. The tool call's made. No more tool calls are needed, and it just responds to the message. Our agent then knows to exit the loop, and we're finished. That is been the way this works.

So now you've seen the ability to build agents very simply using the prebuilt interaction in Minecraft. Now I wanna talk about persistence briefly because we're gonna need that later.

Oftentimes, when building agents with sensitive tool calls like this, we need the ability to actually pause and approve certain tool calls like So persistence allows us to do that. First, the persistence layer in LightGraph will save the state of the graph after every step.

We can very simply create a React agent with this in memory saver checkpoint. This is going to allow us to basically save the state of our graph at every step to this thread. We pass in a thread ID. We can run that.

So what's gonna happen is our agent now runs. Every step, the state at that point is saved down, and we can go ahead and look at the current state of the agent. It's run. We can see. Okay. Human message went in.

AI message is you know, gives us some tips writing emails. We can continue that conversation by passing in the config, which has the thread ID. Cool. When we continue the conversation, the prior state is persisted by a checkpoint. You can see here it's our input.

Here is that initial AI message, and there is a follow-up. Cool. Very nice. We can continue to follow-up on this and say, I like it. Go ahead and send the email. Cool.

And now we can see the whole history is persisted by our checkpoint and available at every subsequent invocation of our agent. That's the key idea behind using persistence, which we're gonna see a lot more later.

Now I do wanna call out that another thing persistence lets us do is specifically interrupt the graph at targeted points. Here's an example of building a graph with human feedback node with an interrupt. This interrupt object is very powerful.

We can very simply stop the graph and collect feedback from a user. Let's go ahead and run that to see. I build a graph. Show it. I became feedback known now with an interrupt. I can run my graph until I hit that interrupt right here.

The interrupt value can see is please provide feedback. To resume from interrupt, I can just pass the resume value to this command object in my graph. K? So this allows me, once the graph is paused, to send information to the graph that it can use.

So I'll send in this feedback. Cool. My user input is to to step three again. So this interrupt resume mechanism, we're gonna see much later with you in the loop.

But it's a very simple, powerful way to stop our graph as an example after specific tool calls and say, hey. Give me feedback on this tool call. Edit it. Approve it or whatnot. So this is very foundational to how we're gonna build our email system.

Now I do wanna call out briefly that because our Langsmith API key was set here, everything we just did was traced. I open up Langston, we can look at the trace. And this is the trace for the agent we just looked at.

We can see here is our agent. Call model node. We can look within each node and actually inspect the specific unlimbed calls. And I like this model. I use this all the time.

You can see the tools down to the model, The fact that we call the right email tool, this shows you the full set of messages that went into the model. And this is the resulting tool call.

This is just the tool being run, and this is the final output of arrangement. The final thing I wanna highlight is the fact that we can do multiple points in Landgraf platform.

We built all this code in the notebook, but we can very easily go from notebook to a deployment. If you look in the repo, you'll see this line graph one zero one script.

If you run line graph dev, that creates a local deployment of the code in this repo.

And all we needed to do that is very simply have a langrof JSON file, which is configuration specifies the graphs that we want to include in our local deployment, PyTorch TOML, which still has the dependencies, and the layer from JSON just points to the the graphs in our repo.

With just this, you can run Lightroom dot dev, and it will spin up Studio. So it should be just running. See, that's an Internet issue. So there we go. Cool. And I can just go ahead and grab the input that we played with previously.

I had this in there before, but there we go. Let's grab this one just to show you. And I like using Studio a lot because you can see right here. Just go to Landgraf one zero one.

This is just one of the very simple graphs we built in the notebook. Open up this inputs, pass in a message, submit, and we can see each node line. On the right here, you see the state that we're at each step.

I use this all the time for debugging and for inspecting my graphs. You can see very nicely in Studio. You get a good visualization of what happened. We're using this a lot more later, but this just sets all the foundations.

So after Landgraft one zero one, sorry for the Internet issues, but hopefully now, you have a foundation. You understand what workflows are. You understand what agents are. You understand what chat models. You understand tool calling, you understand the basics of Landgraft, nodes and edges.

You see how to build agents in Landgraft using our prebuilt abstraction. You understand persistence, base level. You see interrupts, and you see creating a local deployment and visualizing it with Liner Studio.

So this sets up everything we need, and I have eight seconds left, to build everything else we're gonna build in this workshop. So, unfortunately, we don't have time for questions, but I'll have a lot of time in the next session for questions because that'll be shorter.

And, again, sorry for the Internet issues. But that's all we have for now. And and now we're gonna introduce line graph.

We want to introduce an example of line graph in Carlos and his team will be demoing how they're using Minecraft at Cisco with their customer experience AI assistant. Please welcome them right now. That was not us.

And I've been asked to tell you that they're working on it and they're also working on the air conditioning situation. It's kinda toasty in here, but it's gonna get better very Alright. Lance is a tough act to follow, of course. He's a he's a celebrity.

But we'll do our best here to over the next twenty minutes to keep you entertained. So good afternoon. My name is Thomas Murdana. I'm a senior product architect on the Cisco customer experience AI engineering team. With me today is Prince Mato, principal at media.

And we also have Carlos Pereira in the in the crowd. Not enough space for the three of us to be here, obviously, but he's gonna be talking tomorrow.

So over the next twenty minutes or so, we're gonna walk you through one of several ways in which we use Landgra within Cisco's fifteen billion dollar customer experience organization.

This is the part of Cisco that looks after our customers, makes sure Oh, I was waiting to ask somebody about value from their investments in better, to make them more productive, and to help them have more informed conversations with customers. We're gonna go over our use case.

We're gonna talk about what business problems and technology problems are gonna solve. Today throughout the workshops today. This this session is really just meant to be a fly by overview of how some of those concepts can be applied in the production setup to deliver powerful outcomes. Alright.

So let's start with the use case and then look at the business lens first and then get technical. So customer experience at Cisco follows the LARE methodology, l a e r. That stands for land, adopt, expand, and review. This is an industry standard. Right?

We didn't invent this, so some of you may already be familiar with this. But what this actually means is customers choose Cisco, they purchase Cisco products and services to solve a business problem that they have. Right?

Our teams engage with them to make sure that the products and services that they purchase are fit for purpose. They're genuinely solving the problems that customers want to solve, and that customers are adopting our products. They're using our products to realize some of that value.

Obviously, customer needs evolve over time, so there's potentially an opportunity to expand our strategic relationship with customers. Right? So you can position more products, position more services over time. And you do all of that with the hope that over time, they will renew their subscriptions with us.

They will, you know, continue to maintain that relationship with Cisco. So that process, of course, is supported by people and functions internally within Cisco. Right?

So you've got a customer success organization that primarily looks after the land and adopt stages of this life cycle, and then you've also got a renewals organization that looks after the organization that looks after the expanded renew stages of this life cycle.

But, of course, both of those work together pretty closely. As you can imagine, adoption and renewals have a pretty strong correlation. If a customer doesn't use our product, they don't see value in it, they're very less likely to renew at the end of their subscription. Right?

And then you've got horizontal with technical support, service delivery, and advisories throughout the life cycle. This is really just Cisco experts who are doing the work you know, helping customers with their deliverables. But today, we're gonna focus on these two boxes. Right? Customer success and renewals.

These are people who are who are bogged down with information overload. Right? They are they are looking at tons and tons of dashboards and portals and consoles, just major enterprise tools for deep. Right?

In some cases, they're hopping between 10 to 20 different consoles on any given day and time just to get to the information that they need. So the question that we ask ourselves is, can we use AI here to to to make this better for them?

Can we use AI to make data and information more consumable and accessible to these people? Can we help them get more done? Right?

Because they've got a lot to do and not nearly enough time, which I'm sure is a lead time that many of you guys share within your organizations. So let's talk about what problems we're trying to solve.

And on the left chair, I've got business problems to solve and how they're translating to technical problems to solve. So problem number one. Right?

We wanna we wanna bring all of this data together, you know, from all of these different consoles and and portals that exist within Cisco to enable our internal setters to have a meaningful conversation with customers. That's a great example. Right?

But there's a pretty important and critical accuracy target here. Right? These are people who are going out in front of customers. There's financials involved here. So we put ourselves up for a target of 95% accuracy. Are ordered and weak, honestly. Right? They're archaic. They don't have APIs.

There's no consistency. And so how what what we did was we intercept the problem at the data. Right? So all of this data now is is dispersed across Snowflake databases. Right? So it's pretty structured in the bit of SQL. Right?

And so the problem now becomes the technical problem now becomes a text to SQL problem. You've got all these business users who are gonna ask natural language queries. Data databases across Snowflake. Right?

And so you want AI, you want ML to navigate all these complex databases and provide a response back to the user in in natural language. Right? Sounds good, except that 95% accuracy for text to SQL is a three to all order. Right?

You won't find too many people in the industry who can claim that they've done that at this scale, especially when some of our tables have 700 dot columns. Right? People are trying to get an LLM to navigate all of that. Problem number two. Right?

We're not just talking one dashboard. We're not just talking one database. We're talking hundreds. Right? All of those boxes on the previous slide, everybody has their favorite tool and tools and, like, tens and hundreds of tools potentially at scale.

So while it is very aspirational to to bring everything together, to bring all of this data together and just feed it to another level to you know, chat with your data, you're running into teams like, you know, problems with access controls.

All of these datasets, all of these tools have their own design factors, their own access controls. Right?

So when you when you treat the problem with the data there, you bring all of that data together, how do you ensure you're not leaking sensitive privileged customer information to a user who's not authorized to access it?

Problem number three, we want sellers to be able to have access to this information holistically. Right? Very often, people are very siloed to their function and what they have visibility into. Right? A customer may be loving our products of of the product. Right?

And maybe their sentiment is low. Maybe there's competitors in the account. So you gotta give these sellers a holistic view, right, of what the customer is doing across all of these touch points in the life cycle. Right? Except that how do you get AI?

How do you get LLMs to understand what good or bad looks like for a business? Right? You want them to be able to reason across these complex schemas that exist within Snowflake. Right?

And and then be able to provide an interpretation that lines up with a good or bad definition for the business. Problem number four, we want insights that are repeatable, explainable, and standardized. All of the things that LLMs are not great at. Right? They are probabilistic machines.

They don't create deterministic outwards. You don't go to chat GPD and get the same answer twice if you ask a subjective question. Right? So how do you produce deterministic explainable output? And finally, problem number five, how do you know it's working? Right?

And so this is where the calls come in. Nikki's gonna talk to you about this later today. But curating an evaluation set is super, super difficult for something like this. And so here's what we built. Right?

We call this a Cisco AI assistant for customer experience, and this is a very high level architecture. It's a it's a simplified view even though it's a crowded slide. And I wanna draw your attention to a few different things on here.

First of all, you'll notice there's multiple agents. Right? So it's a multi agent design pattern. They've got a supervisor agent a specialist in in news data. We've got an agent for adoption. We've specialists in in adoption data. We've got a sentiment analysis agent.

And then we've a discovery agent that works in tandem with the supervisor agent to sort of demystify a weak question that comes in from a user in natural language and translate that into something that we can answer based on semantic understanding of our of our data within Snowflake.

Each of these agents has tools. They they have tools. They have examples to start to work with. And then you'll also notice we've got multiple elements that we work with. Right? So we've got cloud and OpenAI that are in the cloud.

We've also got Mistral and GoHear that are deployed on premises within Cisco data center.

Landing abstractions make it super easy for us to switch between them and also delineate each of these task agents, right, based on the need, based on cost requirements, based on latency requirements, based on data sensitivity requirements. We can switch back and forth very, very easily. Right?

Based on the task at hand. You'll also notice we've got a predictive ML pipeline. Right? Machine learning is just as important here as generative AI, right, the new kid on the block.

But all of those determinism require deterministic requirements, you know, explainable AI, all of that comes from machine learning workflows.

And all of those outputs from machine learning are persisted back into Snowflake for the LLM and for the AI agents to to summarize in their responses back to the user. Got also got a couple more components for persistence and and and and vector DB. We use VBA.

We use MongoDB. And of course, Landscape, we use that in a big way for evaluations as well as just observability. Alright. What does that do for the business? Right?

In the couple of months that this has been in production, we've already given 20% time back to the business to focus on spending more time with customers and less time chasing data. Right? That's a pretty big win.

And this is obviously the numbers continue to go up every single day. We brought together data from over 50 signals. Right? A lot of this would have taken hours for humans to do manually, for humans to curate manually across all these different tools that exist within Cisco.

And if at all possible, right, many of this many of these tools, like, they're siloed behind organization boundaries and you wouldn't So first thing we're gonna see here my recorded demo. Start. Still having technical difficulties.

So the first thing we're gonna show here is just we can have different subs since each of the agents that Manu was showing you, we can give them not only different tasks but also different LMs.

So the one that we're gonna be showing here is using clock sign at three seven as the supervisor, and the agents below that are all gonna be using b p four, but we can switch to using, like, a Mistral local with the ProHair.

For this demonstration, you're you're looking at SONET 37 and OpenAI's LN. So this would be a typical question that renewals manager might ask, showing the top five deals aggregated by ATR. Also, I wanna point out that ATR may not be understood by the LLM.

We'll show you later on how it understands what ATR is within the context of this question. For all the customers along with their renewals, risks of every level, sentiment classification, and adoption score in the top of the format.

So this question is a good one because it will utilize all of the agents that we were just showing. And so we're gonna hit send on that.

And so while that's the agents are working on answering that question, we're just gonna switch over again to the the infrastructure that we have here.

And if we look at what we have as far as the agents and then look at the the studio version of that, we can see that the supervisor is gonna create an action plan.

Once it's created the action plan, it's then gonna call one or several of these agents. And then once the agents are complete, it'll go back to the supervisor and we'll synthesize the results of the license for the user.

And so if we look at each one of the agents individually, you can see that they're all set up similar where they're gonna handle the input. So it's gonna format the input properly. And then we have a React style for each one of these.

And so they're all pretty much set up the same except they have access to different tables. Their prompts are different, so they're being set up to specialize in the task that they're meant to do.

And then Amal also discover mentioned the discovery agent, which I'm not sure we're gonna have time in the presentation to go over, but the discovery agent is there for those questions that come in that are very vague and we don't quite LM doesn't quite understand what the user wants, but it's given access to a semantic model which essentially is all the metadata for the the database behind it that it can hold the conversation and extract the news of what they're actually looking for.

And we know we can answer that question because the conversation is based on the metadata for the tables behind the answer for that. And so we're back now to that question that I asked and we get a nice rich output for that.

And so a renewals manager could use this to start looking for things that they should work on. But before we get back into the business use case, we're gonna take a little behind the scenes look. And so a lot of this you saw from Lance show earlier.

And so we're gonna just look at the traces for what was going on. So here we can see the AI assistant, which essentially is the supervisor, is is involved and then hands out the tasks to the renewal, the center, and the adoption agent.

And so if we look again at what's going on at the supervisor level, first thing that's gonna happen first, we can see that within Langsmith, we can see all of the different nodes that we're executing within the graph here.

And as we dive in deeper, the first thing it's gonna do is categorize the question. Does this question need an agent? Is it something that's unrelated, or does it need discovery because it's an evade question? So in this case, it identified that agents are required.

It gives the reason for that. The first thing we do is each agent has also access to a vector source. The first thing we're gonna see is do we have any examples of the question that are being asked? And if we do, we're gonna use those examples.

In this case, there was no examples, so the LLN is gonna try to dissect that question and decide which agents are needed.

And so in this case, it decided that the question requires both the renewals, the sentiment, and the adoption agent and breaks up the question into individual tasks that those agents have to perform.

And so if we now go in and we look at what the renewals agent does, again, we can see that the nodes within the graph are well represented within Langsmith. And so now we're gonna go down to the end here.

I'm gonna start walking through what the renewals agent is. So the first thing we see are the tools that renewals agent has access to. So it has access to the four SQL tools where it can list the tables. It can create a query.

It can get the scheme on the table, and there's a query checker.

We also have search examples because for the renewals agent, it needs to do some research on the Internet for some of the questions that they may ask as well as well, actually, examples from the vector store and the web searches for anything that needs to go out to the top floor.

Then we see the system prompt. Oh my gosh. Sorry. A lot of technical kids. Then we see the task that was assigned by the supervisor. We then see that it's gonna search for examples. In this case, it does find an example.

As part of that example, it we give it steps that it can do. In this case, this is a very simple example. We just literally give it English steps that it can follow as well as an table that it has access to.

It then goes and gets the schema of those tables. Now as part of the schema, we also have been leveraging Snowflake has something that is a cortex semantic model.

So we're not using their LLMs, but we are leveraging their data model for doing semantic modeling, which essentially is, you know, metadata for the tables.

And so here we can see we have the column names, but we also have sample values that are in that column, synonyms that a user may say, you know, client ID which we can then map back to the column name of the cat view view ID.

There's other information here such as for this total customers is I mean this one is a simple one, it's just account. But in some cases things like filters or calculations are in here.

Here's one for instance where high risk deal count, it probably wouldn't know that offhand how to do that, but here we're telling it how to calculate that. And so this metadata helps a lot to get the accuracy of the LLM up as as people are asking questions.

And I'm gonna go through this a little bit quicker since I'm running out of time, but essentially, we'll we'll create a query based on that, get an answer, and and then synthesize the result.

Here, notice that this output matches the example output that we were showing up up further. So that's part of that example. And each one of these agents is then gonna do that same procedure, so I'm just gonna go through this quick.

And then once all three of those agents have done their job, it goes back to the supervisor who's gonna take that output and synthesize a final answer, which is then displayed back to the user. And I'll just quickly go through this.

So the user can then use this information. So here, he's looking for high risk opportunities. It's also highlighted as key insights as well as Alright. Thank you, guys. Well, thank you to our presenting sponsor, Cisco customer experience, for making Interrupt clinical advice possible.

We're taking a short break now before our next workshop session. It's a perfect opportunity to refresh, network with fellow attendees. For our engineers, do a demo of the demo of ours.

I know we're working hard to get the Internet fixed or at least improved, which we marked here by the yellow star. Our next session on

Reasonable tools that one on one with an email system. Now these are just mock tools. Okay? I'm not actually naming the API, although the repo does have support for connecting to Gmail. But for now, I'm just gonna use these mock tools as a demo.

And I'm gonna add another tool called done, which will signal that our agent is finished with the work. So those are our tools.

And I'm gonna go ahead and try to use Wi Fi here, but if it doesn't work, I'm gonna fall back because I reran every cell in the notebook, but it won't be as fun.

So I'm gonna try to make this more fun by actually running in and live on the edge a little bit. We're gonna build our system, and it's gonna be be structured like this. We're gonna have a routing step up front to receive emails.

It will route them notify the user or just respond. K. If we respond, we'll then go to agent that handles the email response. So now remember, why do we set up like this? Okay?

So the reason why, I'm gonna build it this way, is that think about that notion of workflow with And here, I'm just importing our repo a few different prompts Okay. That I'm gonna use in this triage process. So what's Your role is to triage coming emails.

I'm gonna input some background information about the user, which you see right here. And I'm gonna tell it the three suspicious emails, and so forth. So you're just laying out here the rules for this. Okay. This is the problem. Very simple. And, again, that's imported up here.

It is true. Can go and modify that repo any way you want. Okay? Now I wanna show you a very nice trick for doing things like rally. With many different steps, they produce an output in that that adheres to that schema. So here's a simple case.

I can create a pedantic model, and it just has two fields. We need a decision. And here's the reasoning for it. Decision is one of these three categories, and the decision is just some free form reasoning the model can provide about why I made this decision. K?

I can bind the schema to the model using the structured out with with structured out method that is provided by the in it chat model interface. So what happens is the model looks at the schema, LLMs is very, useful when you're building a workflow.

So what we're gonna do is set a single function here, which your router takes in our state just just like before. And from our state, we're gonna get a new what is doing some of this is control of our email.

This part of this is the author to subject horizon. We format the triage prompt with those components from the email. We then just invoke our router with a list of messages. You can see that right here.

Instructions, and then the model will see, and your email is the new output in it. It's gonna be a structured object, and you're gonna see it has this classification field in the dynamic model.

So I can just run her call, result classification and check the various it's notified, for now, I go to end. Now I also update the state of the graph. In this case, I update the state with the null itself, and this is a message key in our state.

This is a subtle point I wanna make sure is very clear. If this is just a response, our routers run and decide, let's respond. We then write to our state the email, in particular with the state key messages. Now why do I do that?

We do that because I want that input to be received by my agent. The agent is using the messages key. So this is how in Minecraft, you can connect different components together using the state object. The router can write the state and say, okay.

If this is respond to the state key messages, append. This is a message that you can email. The agent then receives that message, and then receives.

So you can connect different components together in Landgraft using the state updates in our nodes by returning it in, and we're using conditional edges to do routing. And then build both, which is another option to build geo print graph.

In this case, I like it because it's bit of a nice shortcut. In this case, I wanna both the state and dictate where I go. Command is very nice with each of that. Okay? So there we go. We've now defined our route. Now to our agent.

Now remember, before, we use the prebuilt, I wanna build agent from scratch because I wanna show you what happens under the hood with our prebuilt. So if you think about the agent, there's just a few things you need.

You need a system prompt to tell the agent what to do. Okay? System prompt, you can see, just has some instructions here. Your executive assistant who cares about helping your executive you can make this anything you want. It's just a prompt. Basically say, here's the tools you have.

This is our tools list. Write email, schedule meeting, check calendar, done. Those are tools we defined above. We just indicate to the model that here's your tools in the prompt. Okay? We just say, look. What you should how should you handle emails?

We just give all these instructions here in the system and we give it its tools. You can read through this. You can modify anything want, but that's what's happening here in the system prompt. We collect our tools in the list. We initialize our chat model.

We bind the tools just like before. Past tool push required. Why? I want my agent to always call a tool. So that's kind of interesting. Why do I want that? Okay? If you think about this system, this is gonna be deployed as an email system.

It's only gonna act with me as a user through human move. I'm not actually gonna be looking at chat messages and produces.

It's a subtle point we'll talk about a lot more later, but the point is what I'm gonna do in this case is I'm gonna have the agent always call a tool, and if it's done, it's called a done tool, and that exits the glove.

It's a little bit different. Remember before, you call tools until no tool is called, and then the LLM just says, okay. I'm done. Thank you. But that final okay.

I'm done thing I don't need here because no one is actually looking at that final message from the agent in this deployed email application. Subtle point, we'll understand it more later because we're actually using the looping record of these agents, not the messages themselves.

And so the point is there's different ways you can instrument agents and, in particular, instrument determination conditions. Sometimes you can have it just run until no true call is made. It returns a message telling the user, hey. I'm done. That makes a lot of sense for chat agents.

For an agent like this that's ambient, it doesn't really make sense. So it just makes a tool call to say done and the process happens. So that's that. So that's the LLM call. Now what's gonna happen here? I'm just gonna call my LLM.

I format the prompt, and the output of the LM is just a chat message. It's gonna be appended to messages, same as before. Nice and simple. Now I need to call the tool. I set up a node called tool handler.

It just looks at the tool calls, grabs the tool, calls it, appends a tool message to messages, and I'm done. Message and data. That's the tool handler. Just like we saw before. There's one node that will call the model, one node that calls the corresponding tool. Conditional router.

That's all we need. So we basically continue calling tools until some termination condition. In this case, termination can't change just the done tool. Because if you call the done tool, you exit the loop. That's it. That's all I need to build an agent.

It's an element with a prompt and some tools. It's a node that calls the tools, some term some termination condition. It's pretty simple. And just build a graph like this. This is what's happening under the hood with that create react agent abstraction.

Define the graph, pass in the state, add her nodes, add the edges. And let's see if this works out. Internet's kinda working. Good. Hopefully, three guys too, but maybe we still got it. Okay. There's our graph. LM calls done. Calls tool.

If the tool is not the done tool, goes to tool handler. Tools invoked. Back to L1. Call another tool. Tool handler. Back to L1. Loop that until it's a known tool. That's all making this. Now we need to connect our router with this agent.

Define some of our workflow. Add the router and the node. We defined that previously. Now this is the key trick. Add a node. I'm gonna call response agent, and I pass in this compiled graph. So it's like, wait. Why can you do that? How does that work?

With langraphing, you can compose graphs. This is now a subgraph in this overall workflow. I can compile this. I can look at it. Pretty cool. So this yellow thing is our agent. It's a subgraph now part of this overall system. Triage happens first. Emails triage to respond.

Personality agent takes it, does its work. We end. Or if the decision is not to respond, we end anyway. That's it. Nice and simple. Let's test this. Here's an email from sysadmin, scheduled maintenance. Let's just run this.

Call our workflow and vote with email input, get a response, look at the messages. Run that. And classification classification decision is notified. It doesn't go to the caging. Just happens. K? Now why did notify?

It's because in my triage rules, I had something about emails from sysadmin notified people don't respond. That's the only reason why that router made the decision to notify. Alternatively, pass an email, quick question about API docs. It seems important. Let's run that and see what happens.

Decisions are gone. Okay? We then now this is important. The router added the email to messages. Remember that? So this is the first message respond to this email. Where did that happen? We can go back and look at the router group.

You guys wanna make sure this is clear. Go to the router. Right here, respond to this email. When the decisions respond, we update the state of the graph with the email in the messages piece. Our agent if you look at our agent right here, grabs messages.

That's how these two things communicate. That shows you the power using Minecraft because this state object is passed between your nodes. You can write that state object in each node and subsequent nodes can then read from it and do stuff. That's kind of a big idea.

It's a very nice way to communicate from different subsystems. In this case, could be on a router and a response agent. So here's your email. Our agent makes a tool call. Great. It makes a tool call. As you can see, the right email, it writes email.

Then it goes to that tool handler node, tool run, and then it calls the dumb tool, and then we exit. So perfect. All working as we expect. Some nice little tests. Now let me show you this with studio. So I'm already running my studio. Studio is running here.

Now we're gonna end a little bit early so there's gonna be time for q and a. So I wanna make sure that you really understand what's happening here.

But basically, there's a local deployment running on that machine where all the graphs in this repo are exposed and accessible for me to run. We're gonna use this a lot more later.

But what's really cool is I can go ahead and take an email just like we did in the notebook and then run it in a graph. And I can see there's a response agent getting hit. Boom. So it runs pretty quickly. Wi Fi's little better maybe.

And we can see everything that happened. Scroll through. Here's your input. Hit the triage router. You can see the state update made by the triage router. Hits the response agent. You see what happens inside the response agent. You can even open it up here in Studio. Pretty cool.

You can kinda play around, move these things. You saw some nice image in Studio. It's very convenient. That's used all the time. You can see the tool calls, and you can see here is that done tool call, and we exit. Now I'll show you one other cool thing.

From here, click on this thing open on LangGraph and Langsmith. Open the Langsmith. Here's our run. You dig into each LM call and see the latency, see the messages, the tool calls, and so forth. So this provides the foundations for our email system.

We built I'll show you kind of the schematic here. We have built an email system that can perform triage of incoming emails right here. Right now, if notification is done, nothing happens, we're gonna fix that later with We go to respond. Our response agent calls some tools.

Response email done. Now would you actually turn this on? Probably not. That's why we're gonna introduce both evaluations and human loop to probably make this link even actually deploy. But this sets up the guts of the agent, and you can see with places, it's really simple.

It's just a router and a very simple pool calling agent, but with this, you can do it not. I have this running right now, and runs works really well. So I'm gonna go Yeah. So Wi Fi is bad. Good question. A good statement. You are not wrong.

So okay. Let me start from the back. So, yeah, go get the done tool, nothing happens. So, basically, if I go here, let's look at our tools. Right? So in this particular case, done has no return. You call a tool, and it actually does nothing.

The point is, though here's the interesting point. When the model calls this tool, it's a signal to the system, and we can use that signal to determine the control problem. And let me explain what I mean by that. If you go down to our should continue. Okay?

We look for that done tool to know when to finish. So the model calls this done tool. It does nothing, but it indicates to the system that the process is finished.

So you can use tool calls kind of as signals in a flow to indicate something that then you can cache in your router to determine a next step. In this case, we call the dump tool, and we determine it.

So that's how tool calling is a really useful trick, not only for actually calling external tools, but also for direct control flow and creation. Cool. When should one oh, nice. When should one put a their prompt in a system message versus an AI message?

This is a good question, and I've seen a lot of kind of I've seen a lot of kind of conflicting takes on this. I would honestly look at the model provider you're using for the best practice.

Typically, like in this case, I like to put the instructions that are invariant for any given email in the system prompt. And then in my user prompt, you see that right here. But let's look at the triage router, an even better example.

So what's happening is my system prompt has all the general instructions about how to respond emails. The user prompt just has email itself. So I like to delineate typically a system prompt having the general instructions.

User prompt having whatever is variant like the user input that I wanna process. It does depend on provider though, and I've seen a lot of conflicting takes based upon who the provider actually is. But that's just one generalization I tend to use. Okay.

I think we are now out of time. So that concludes our session on building our email engines. Let's take a fifteen minute break. We'll have some snacks in the back room and clickers usually not work, but it's okay.