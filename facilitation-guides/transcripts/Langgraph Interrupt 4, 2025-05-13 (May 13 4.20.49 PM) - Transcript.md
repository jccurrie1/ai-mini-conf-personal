Alright. Thanks a lot. Can everyone in the back hear me okay? Walk. Okay. So if that's working on great, I think And now we're gonna implement the final piece of the puzzle, which is memory.

And the reason memory is so crucial and helpful for an agent like the one we're building today is it enables our email system to become self improving.

And so the context of our email agents, right, what long term memory memory will offer is the ability to take in human feedback, save it down, and use it to both personalize end user response from the teacher and help our agent avoid making redundant mistakes.

And so that begs two questions. The first is, is, what is memory and land graph and how do we work with it as a developer? The second, how do I apply long term memory and land graph to my email system and make itself proven?

Well, let's actually just jump into the first question. So what is memory in line graph? Well, in line graph, there's two types of memories. The first is what we call thread scope or short term memory.

And this memory is only persistent within the boundaries of a single conversation thread. Short term memory is what enables your agent to retain context on the conversation history over the course of a given interaction with a user.

So in the hulu portion of the workshop, we just covered, Nick set up a check pointer. This check pointer enabled us to pause the execution of our graph at certain points and wait for human feedback. That functionality was all powerful for our network.

But what if you wanna retain context, save down information about the user across threads or across sections? Well, that's where long term memory comes into play. You can think of long term memory as a persistent knowledge base that spans multiple threads or sessions.

And in this notebook, we'll be working with long term memory. LightGraph makes it really easy to work with long term memory by providing a built in store. You can think of the store as a flexible database where your memories can be organized, retrieved, and updated over time.

And there's three types of implementations for the Landgraf and Memorystore. The first is at the first is in memory. So if you run the Landgraf store in memory, it's purely a Python dictionary and there is no persistence.

So if your process terminates, for example, your notebook starts, all the data is wiped. This is a great option for quick prototyping, but it quickly breaks down as you can expect for use cases beyond that.

The second implementation is using the local development server that's provided when you run LightGraph for dev. And this is very similar to the in boundary implementation, but it has a bit more persistence because it'll actually pickle the data to your local file system in between restarts.

Still designed for development, And just to show everyone how easy it is to both add and retrieve memories from the store, let's spin up a really quick code example. Because we're just gonna note that we'll do the in memory implementation.

The first step we're gonna take is we're gonna actually import the git memory store and initialize it. And because the memories in my store are namespaced by a tuple, I need to create a namespace for my numbers.

This namespace is just gonna have my user ID, which is dummy string one and the string memory. Now, LightGraph also makes it really easy for me to put away memories inside my namespace. To do that, LightGraph provides a dot put method.

So all I have to do is define the memory I wanna save down and its ID. In this case, I'm trying to save down the food preference. I like pizza. Once I've defined the memory, a simple in memory stored output is all I need.

Now let's say we wanna retrieve that memory down the line. Well, Landgraf has a dot search method as well. I'll run that dot search method over my namespace, and we'll get to print it out. It's my memory that I like pizza.

In addition to this, Landgraf makes it really easy for you to give your graph access to the memory store. So if you wanna give every node in your agent access to the store, all you have to do is compile your graph in the memory store.

So now everyone has a high level understanding how to work with memory in LangRap. Let's actually apply it to our assistant and make some improvement.

Well, the big change we're gonna make here is we're gonna start saving down human feedback that's provided over the course of the interaction with the user.

And we're also gonna retrieve and inject this piece of it into our agent's prompts, so as context user preferences for case is an action. This is different from our old agent. Right?

So during the human loop portion of the notebook, our agent would collect user feedback at certain points in this execution, but it would never save it down, they never retain it. So that's a big change we're make here.

Now one thing that's not gonna change in our code is the tools that we give our agent access to.

We're still gonna give our agent access to w tools so it can write emails on our behalf, schedule meetings on our calendar, check our calendar for availability, ask us ask us a question, etcetera, etcetera. So all the bots are gonna stay the same.

The critical part, the big piece that is gonna change is we'll start capturing user feedback into our long term memory score. And before we implement that in code, we have to ask ourselves two questions. The first, how should our agents long term memory be structured?

And the second, how do we want to update our agent's long term memory over time? Well, for question one, we're gonna store our agent's long term memory as a string for simplicity. And for question two, we're gonna update it over time using an LLM.

What this LLM will do is it'll take in the existing memory profile. It's been tasked with updating the most recent piece of feedback that was given to you by the user and some custom instructions. It'll actually update the memory score using those instructions.

So now we've clarified those two pieces. Let's actually go about implementing our agent's long term memory solution. The first thing we're gonna do is we're actually gonna define some default memories for our agent. And we specifically want our agent to save down memories related to three topics.

The first topic is how we'd like to triage emails on our behalf. So which emails should we responded to? Which emails should be ignored? And which emails should we service to us, the human, as a notification?

The second topic we'd like our agent to save down memories about is how we like our meeting schedule. As you can see here, the default preferences I'm giving my agent in his memory store is we prefer thirty minute meetings, but we're also okay with fifty minute meetings.

The final and third topic we'd like our agents to say down memories about is how we like our email for you. So you can see from the default preferences here, we prefer professional and concise language.

If the email mentions the deadline, we'd like to explicitly acknowledge in reference deadline in the email copy, and a few other small things we just like the agent to keep in mind when it's writing email drafts on our behalf.

And so now that we've given our agent some default memories, let's define two helper functions that we were used throughout this logic. The first helper function will actually get or retrieve memories from the store. The get memory helper will take in three arguments.

The first input is the memory store we're working with. The second input is the namespace we'd like to get or treat memories from. And the third input is some default content. Right?

And so what's gonna take place inside get memory is we're gonna search the existing namespace for memories. If no memories are found, we'll add some default content to the namespace and return that.

But if existing memories are found, we'll just pull it and return that to the user as well. In the second helper function we're gonna implement, we'll actually update our agent's long term memory over time. And as stated earlier, we're gonna be giving an LLM this task.

And this LLM will take in some custom instructions to inform it on how it should update the memory profile. Right?

And the custom instructions are found here, and they were actually informed by g the g 4.1 property guy, which had a few really nice tricks that Lance looks at it about.

So you can see inside the instructions, we're basically telling our LLM to act as a memory profile manager or email to an agent that selectively updates user preferences based on feedback messages. We give it some really detailed instructions. For example, never overwrite the entire memory profile.

Only make targeted additions of new information, etcetera, etcetera. We give it some steps it should adhere to when it's reasoning about which memory should be added to the store.

And what's really, really helpful is we actually give it context on the existing memory profile that's been tasked with updating. Right? So those are our instructions. Now let's take a look at what the helper function actually does. Alright.

So the helper function called update memory takes in three arguments as well. First argument is also the memory store that we're working with. The second input is the namespace we'd like to update memories from.

And the third argument is the list of messages that have been exchanged between the user and the agent up at the up until this point in the execution program. And so what we're gonna do is we're gonna pull down NALA, in this case, q p 4.1.

We're gonna give it these very custom instructions, which also provide a context on the existing memory profile it's supposed to update. And we're gonna say, hey, you know, think carefully and update this existing memory profile based upon these user messages.

And then we're gonna inject the messages that we received as input. And in these messages, the agent will be able to see the most recent piece of feedback that was provided to it by the user. User. We'll call the LL with all this context.

The LL will return something, and we'll store an updated memory inside our memory storage. So now that we've implemented these helper functions, we need to make one small change to our triage router function.

If you remember from earlier in the workshop, the triage router is where the user actually gets their emails classified as respond, notify, or ignore. And before we gave our agents some parcoded preferences and how we liked our emails triaged.

But now we're gonna make these instructions and preferences dynamic. Right?

So before we ask our LLM to classify the incoming email as respond, ignore, or notify, we're gonna first pull down the triage instructions we gave it from its long term memory using the get memory helper we just defined. And then we're gonna inject these instructions inside the problem.

Awesome. And we also need to make a small change to our triage interrupt handler. And so it's inside the triage interrupt handler where the agent notifies us about certain emails.

And when the user provides feedback on these emails, we now want to save that feedback down inside our memory store so it can be used for personalized decisions in the future. K?

So for example, if the email talked to this email if the agent talked that this email should be classified as notified, but we came back and said, hey, know, we actually should have just responded to this email.

We'll save down inside our memory as, you know, the user wanted to reply to this email. So please update your triage preference accordingly. Similarly, if the agent surfaced that email has a notification, we came in and said, you know, you actually should have ignored this email altogether.

We're gonna save some content down inside the long term memory that says, the user decided to ignore this email even though it's classified as notified. So please update the true out preferences with this new information. Simple enough. Right? Great.

Now we're not just gonna want to give our agent context on our true out preferences. Right? We also want our agent to know how we like our emails written, how we like our meeting schedule.

So we're also going to inject memory inside its prompt when it's about to work with any of those tools. So this LLM call node should look familiar.

And inside the LLM call node, what we're gonna do now is we're gonna fetch our calendar preferences and our response preferences from the memory store, and we're gonna inject it inside the LLM prompt.

So now when this LM goes about calling tools to check our availability, scheduling meeting on our calendar, or writing email drafts on our behalf, we'll have our preferences in mind. Great.

So the last place where we're gonna integrate long term memory into our agent is inside the interrupt handler. In the interrupt handler, the agent is able to surface certain tool calls to the human for feedback. Right? And in the past, we never retain that feedback down anywhere.

But now we're gonna start saving that down inside the numbers store. So as an example, let's say the user actually edited a tool called the agent wanted to make. Right here.

Well, if the initial tool called the agent wanted to make was writing an email draft on our behalf, what we'll wanna do is we'll wanna look at the edit of user made and save that down inside our memory as some new properties. Right?

So we'll update our memory to a content that says, hey, the user edited your email response. Here's the initial email that was generated by the assistant. Here's the edited email. Now please update your memory board. And this isn't just gonna be for the right email tool call. Right?

So, for example, if the initial tool called agent wanna enable is scheduling a meeting, we're gonna save some similar content now. The user added your account invitation. Here's the initial invitation you generated. Here's a new one.

Implied preferences from the chain and save them now inside your local account. Right? Pretty simple. Save them down inside of one Right? Pretty simple. And we're not just gonna save down feedback from the user at a call.

So if the user decides to ignore a tool call, we're also gonna take that signal and save it down inside of one their memory.

So if the user ignores the tool call and the initial tool call was writing an email on our behalf, well, we'll tell the agent if the user ignored your email drafts, that means they did not want to respond to the email at all.

So you just update your preference accordingly. We can speed run the rest of these cases. Right? So the agent wanted to schedule a meeting. We didn't. Take that into account in your memory, etcetera, etcetera.

And the last case I wanna point out is when the user provides free form feedback to the tool call. Right? So the user responds and the initial tool call the agent wanna make was writing an email, we'll also see some context down there.

User gave feedback on the email that you wanted to write and send to the expert. Team. Please update your response preference. Similarly, if the user provides free form feedback on the scheduled meeting pool call, please update your challenge preference. Simple enough. And that's it. Right?

Those are all the code changes we need to make to get it from our agent long term and the ability to be self improvement. The rest of the graph is the rest of the graph is exactly the same.

LLM call node is the same, often does small logic changes. Intro is relatively the same as well. And we compile a visualizer graph, you'll see the underlying architecture is also being the same. So we have a triage gutter.

We have a triage in front camera, and we have a response unit. Architecture's the same, but now the assistant is self improving. Alright. So now we've built a version of our email assistant that is self improving. You can learn from our preferences over time.

Now let's talk to test it out with mutation. And see how it learns from your feedback and maps over time. What was a few key questions that we're gonna try and answer through these tests? The first, how does our system actually capture and store user preferences?

The second, how do these store preferences affect future decisions? And the third, patterns of interaction actually lead to which type of of memory updates? Right? So these are all questions we'll be answering when we run these test cases.

Before we run these test cases though, we're gonna implement another helper function. What this helper function will do is display the agent's memory content at a certain point in the graph's execution.

This helper function will help us visualize the differences in memory when we, let's say, edit a tool called as proposed by the agent. Right? So we'll build up this self function called display memory content. And now let's move into our first test case.

So this first test case will examine what happens when a user accepts the agent's actions without any modification whatsoever. This baseline case model is to understand what the system will do when there's no human feedback.

And we'll be using this this famous tax planning email that was surfaced in the QA and q and a last time. This tax planner is emailing Lance and saying, hey, can we if you hop on a call and strategize about your taxes. Right?

Well, the agent actually thinks this this email is pretty compelling. So let's let's schedule a meeting with Lambda. We're just gonna accept the scheduled meeting tool call. Great. Meeting was scheduled. And now, Giju wants to write an email as well. Okay? So we have a meeting.

Now we wanna send an email back. Let's just accept that. Write an email and we'll call as well. And what you'll see is that after you accept those both these tool calls, there's actually no change made to our long term memory. Right?

Our calendar preferences and our response preferences and our drive preferences have stayed exactly the same because there was zero feedback provided. Right? Now let's talk into a case where the user does provide feedback and we actually do see changes to our members.

So in this case, what we're actually gonna do is edit tool calls that the agent wants to execute. So the first tool call that we're gonna wanna make is schedule a meeting. Right? Because we're going to be sending this, again, very famous taxi bell plans.

We'll send the taxi bell plans. The agent will decide who wants to schedule a meeting on our calendar. And we'll edit the scheduled meeting tool called now. So we're not actually gonna accept it as is.

And the big change we're gonna make here is we're going to change the length of the meeting from forty five minutes to thirty minutes. We're also gonna simplify the subject line. Right? So the agent wanted to name the subject tax planning strategies discussion.

We're just gonna make tax planning discussion. What you'll be able to see is our agent will be able to capture that nuance and update our long term memory accordingly. Right. So this code will simulate us editing the scheduled meeting tool call with those changes.

And for visibility, I've got the two before and after of our agent's long term memory. After we had a tool call and before it had tool call. Right? So before, it knew we'd like thirty minute meetings, but we're also fine with fifteen.

But now it knows it should definitely default to thirty minutes unless otherwise specified, and subject line should be a bit more concise. Right? So it's able to save that feedback down inside the memory store.

And, you in the future, I should I should take that into account when I schedule meetings with with Lance. This is really impressive because it doesn't just record your specific edit. It actually generalizes a broader preference pattern and saves that down.

And one thing Lance will also talk about after as well is actually getting the prompting right for this specific part of the the agent was very difficult. The agent had a tendency to overwrite the memory profile completely sometimes saving up incorrect memory.

So getting the prompting right was actually fairly difficult. Right? It was way too robust. Mhmm. There's also way too professional, so we're gonna make it a bit more casual.

And at the very end, something we like to do with these light, we're actually gonna ask the recipient of the email if the proposed time works for them instead of just assuming that they're good and and they'll solve the VA. And when

we do this, you'll actually see all that nuance again get saved out of tag agents long term memories. And that's all done automatically under the hood by the two helper functions we defined earlier in the code.

So the last test case the last test case we're gonna go through here is what happens when we actually respond to a proposed tool call with free form feedback. So these will involve the same two tool calls you've been seeing, write emails, schedule meetings.

This time, instead of editing full calls directly, for example, for the scheduled meeting full call, we're just gonna get free form text in response. Right? So say hold, tap it's task it's tax season again, Lance. Let's schedule a call. Our agent wants to schedule a call.

And let's just provide some free form of text feedback. Let's say, you know, I'd love to talk, but instead of meeting for forty five minutes, could we please meet for thirty minutes? Right?

And we're also gonna express a preference that going forward, we'd like our meetings to be after 2PM. Right? Not a big not a big board meeting person. And after we provide this feedback to the agent, same deal.

You'll see some information saved up inside the long term memory score will be injected inside these prompts when it takes this action to get captured. Same deal now. The agent wants to write an email. Instead of editing this email draft directly, we'll provide some preform text feedback.

What we're gonna request is a shorter, less formal email. And we're also gonna want to express that we look forward to the meeting. Right? So we're gonna ask you to include that in the closing closing line of the email.

So the agent will take that free form feedback in, rewrite the email drafts, and save down our preferences save down our preferences inside the storage. And so if you were to take a look at your memory score before and after, you'll see content like this was saved up.

So the agent knows now we favor shorter and less formal language than possible unless the context requires formality. And we prefer to include a statement expressing that we look forward to the meeting or conversation when we're confirming.

So again, what all these test cases really show is that our system's able to organize our learning preferences into these different categories, save them down to the store, it's able to extract the correct insights from human feedback and use that in the future to learn about our preferences.

And what's really, really cool about this, right, once we finish the testing, is we can take a look at memory and run it locally with Landgraft Studio and Agentbox. And so I already have a little local development server running locally in my terminal.

What I'm gonna go ahead and do is hop over to browser where I have Landgraf Studio pulled up. And inside Landgraf Studio, I have an example email I'm gonna send to my agent that now has long term memory. Okay. This email is from someone named Alice.

They've already flashed this up earlier in the workshop so I won't go into too deep detail. But Alice is asking, John, if we intentionally emitted certain endpoints from the API documentation. Well, Alice will send that email to our assistant. Our assistant will don't interrupt. Great.

Our assistant wants to ask us for clarification on whether we intentionally admitted endpoints or not. Well, to process this, I can really easily just go over to agent inbox. Click in. Let's zoom in a bit for the people in back. Next week. No worries. Looks good to me.

Except so the email we sent over to Alice, if we hop back over to Legrand Studio, you'll see now it's all done. We'd like to deploy this agent to production and hook it up to our real Gmail.

Well, Lendrar platform, which is our solution for deploying ejected applications production, is perfect for this. With Lendrar platform, you can deploy a locally running agent to a production ready API in just one clip. And the API that Lendrar platform deploys your graph to is feature rich.

So it's a bunch of native APIs that make it easy for you to get your agent in short and long term memory, the ability to run on a special basis across, and a whole bunch of other functionalities. We're actually making Liner platform generally available tomorrow.

Liner platform is also purpose built to scale. Every deployment Liner platform has built in task queue. This task queue enables you to scale horizontally and gracefully handle bursting cross loads or splicing traffic. So let's actually deploy our agent production with Lagrack platform.

So we'll go back over to our browser. I'll hop into Lagrack platform. And to give everyone a sense of how easy it is to deploy your agent with Landgraft platform, let's actually just go through it live. So I'll click new deployment in the top right corner.

Once I do that, all I got to do is specify the GitHub repository that the agent lives in from the drop down, add any fire repair names, and it clicks in there. And because of the WiFi issues, I actually already deployed the first plane.

So We have documentation, like, inside the briefing. But again, we're making it generally available for us. What's really great as well is once we have this agent deployed in production, we can actually hook it up to a real inbox. For example, a real email. Right?

So here I have inbox. You can see that I actually already sent an email to myself asking how's the workshop going? Do people have any questions at all? What I was able to do is actually write a quick little script.

And inside this quick little script, I'm able to hit my production deployment and have the assistant go about triaging and handling the message. Right? So it went over this memory workshop email. I can hop over to agent inbox. I can see, okay.

Dave's asking how the workshop's going so far. Okay. Well, workshop's going pretty well, and maybe I wanna make this bit more concise. That's great. I'll send this for you for text as feedback. Right?

The agent will make the response much more concise in return, and I can just accept it. Okay. Great. Workout's going well. Main question so far about use case integration. So I can delete that. We have q and a coming up shortly on all the I'll hit some edge.

So what we're gonna do now is hop back over to my my Gmail, right, the Gmail that I'm actually sent by inbox. You'll see that it'll actually have registered inside my inbox. Okay? So workshop is good. It's going well.

So now you can actually run this on a scheduled basis as a prod job. Lance actually has hooked up to his real work email. Harrison's had this email. He's been running on his email for many months now.

And now he's running on schedule if you're on a basis and I can have a triage manager and box for you. You know, with that being said, we're gonna turn it over to you all.

We have some time set up so you can ask questions about not just long term memory, also building the initial architecture, playing around, and all that good stuff. So thanks. This is a this is a good one. This is a good one.

What is the best way to define the scope Yeah. So actually, the the way when when we're gonna say this stuff, think about it is, work backwards where you wanna use memory. Like, what LLM calls specifically need context for memory.

And that kind of flows pretty naturally because then you're like, okay. Well, the router needs memory. So say that as part of the namespace. It's like triage references goes to the router.

And then the LM needs memory for a couple of different things, calendar preference or small preference are obvious. So those go into the LM column in the agent loop. So that kinda makes sense. And also think about the memory updating itself.

So if the calendar tool call is edited, you wanna edit a particular namespace of memory like calendar preferences. So actually, it's kinda nice to break it up into, like, where in what memory edits need to be made.

Like, you wanna be able to edit edit your calendar preferences and your response preference independently. So that's why it makes sense to namespace them separately. Like, if the calendar tool call is edited, you only wanna hit the calendar preferences.

That's kinda how I split it up, you know, based on the tool calls being made and then based on where memory is gonna be used. I will note, you should check out Langmem. So Will from our team built a very, very nice kind of memory library called Langmem.

And I mentioned the repo. A future extension is to incorporate Langmem in particular.

Background preferences are a thing that I actually wanna add to my own system that uses repo to just learn general facts about the user, and you can actually just fetch them using, like, symmetric lookup from the store, and that's also where very nice is find them.

Very nice kind of interface over memory to memory management. So I look at that as well. I think it's another interesting memory type that can be added and incorporated into your LLM call. In fact, it has default background.

We can incorporate that as a memory type that you add to your store. Yeah. Yeah. Great. That's great. Questions come in. So I'll answer the most recent one of how you can update and maintain memory from different users. It's a relationship here, ones I've seen.

So from the from the notebook, we have different namespaces that are related to different user IDs. And so that's how you do it. So maybe that user authenticated when they first started drafting the creation.

And you take that user ID and every time you go to update its memory score, you just fetch the namespace as soon as you get that user ID. And another question I was talking about is, can we pool memories together? You definitely can.

You'd likely wanna be very careful about privacy and data security in that case because then when you're retrieving memory from a pooled data source, you'd have DII from a whole bunch a whole bunch of different users you're after if you end up with. So yeah.

Configure memory memory updating. That's why we use the LLM call with the custom prompt to do all that. So you can really kind of customize how you do memory update. In our case, it's with a single LLM call. That's gonna be plus one.

And a related point is how do you ensure memory is scalable since we have limited context? So this brings up some interesting points. Right now, we're doing the simplest possible thing with memory. We have a single profile, you do much more than this.

In particular, if you look at langmem, you can save collections of memory. So that's like it can be a list of different memories that are stored over time. And how do you treat them?

You can use things like semantic search to actually look up based upon semantic similarity to, like, the email in question or other heuristics, like, look at the sender of the email and fetch all memories from that sender, like, relate to that sender and use that as context to answer the question.

So you can be very flexible when I set up the retrieval mechanism for memory. What we do here is the simplest possible approach, which is basically editing and updating a single string simple string and pass it to the L. Yep.

And the one question I'll take here is why not use the VectorDB for long term memory? Right? So actually the production implementation of Lendout memory store is PostgreSQL with DG bathroom, which enables you to smash the search across the document. Yeah. It's easy to configure that. Yeah.

And and I'll I'll ask, like, in the in the report in the future that shows how to do that. But it's very easy to configure that using the store. Yep. Yep. Yep. Yeah.

And one other question I'll I'll take here one other question I'll take here is how do you manage long Does Langman use some LaPrompts? Fine. Will. He will know. So the reason why I didn't use Langman here, although I initially did, is because

I wanted to show the simple, like, principles, like, very the very simplest implementation so you understand this idea of using an LM to update a memory profile sitting in the screen. That's really the starting point.

You get much more sense here with how you manage memory in different schemas, with collections, with different search mechanisms. So it's really like very much the one on one, which is good for this particular repo, but that is it's a very, very big topic.

I would definitely find Will for language and good questions. Yeah. And one really good question I'm seeing in CCOT is how do two agents share memory? I can take that. But so so my favorite way for agents to share memories using the remote graph interface.

So if you have to deploy two agents to production using, like, our platform, they'll to both have the same APIs back. They'll hop over to that point side by flashing on the screen further. So you'll able to communicate, share state, and work together in a really nice way.

So and so, you know, in layman's sort of remote graph interface basically lets you call out to a separately deployed agent as if it's I'm actually so so Harrison really turned me on to this because he was using it in his email system.

And I think it's a little bit of a underappreciated concept. Human loop is very obvious. Memory Memory in isolation is very obvious, but the way the two play together is like was a little bit less obvious, but it makes a ton of sense.

Human loop without memory is kind of like so much people have mentioned this. I don't wanna keep telling this is the same thing over time, so it makes sense to save your feedback in memory. Very natural.

Harrison's already doing it, but I don't know if we have other repos that showcase it, but it's a very generally useful concept. It probably applies anywhere we're using human blue. Well, update sorry. Not anywhere. It's really where, like, you want it's person you want personalization.

Like, I used human loop in a separate repo that's an open deep researcher, but there, it's like, who cares about memory? I used human loop there to, like, clarify questions to do research. Research. So it's kind of more persistence where you want personalization.

I don't know if we have other examples. I don't if you guys know. Maybe not for the kind of human loop plus memory. Think this is really this and Harrison's email system, which was the basis for this Yep. Were really the classic examples.

But it's the principle is very, very useful when you want personalization. Will might know too. Will can just yell out if he knows how to repo that he does. Check out Langmem for sure. But I I don't know if he's got the show.

I don't know that it's an end to end, like, human loop plus memory example. Good question. Yeah. I I can take one. I also see someone putting ignore all previous instructions. No. I'm looking at it. It's it's just it's just

one thing that we keep track of with online emails is we ask LLNs to categorize basically what people are asking to this endpoint, and we keep track of that as monitoring trucks.

So we see how many questions are people asking about lane chain or lane graph or Python or JavaScript, etcetera. JavaScript, etcetera. And it's just a good way to use LLMs as part of the feedback pipeline of what people would actually do with the application. Yeah.

I I think a helpful way to think about that as well is, you know, any evaluation that you wanna run where you don't need some reference output at runtime, online emails are great for that because then you can run some custom code, you can run it out and judge over it, but there cannot be a reference because we don't know exactly what content comes through our value.

So here's a good question. What is the process for iterating on the prompt in order to store memories effectively? I'll tell you my process, but we do have a lot of prompt engineering tools.

But I built a simple eval for basic updating schema, and I it's a very good way to inform the engineers that really works well. And you'll do that. And it it can reflect on what Okay. Yeah. The MCP thing's interesting.

So my my kinda take there is actually, like, when you're building so when you're building an agent like we and a bunch of the last question too. When you're building an agent like we did here, why would you need MCP tools versus the tools we're talking about?

So Gmail is an API. Right? I just redefine a bunch of custom functions that hit Gmail's API. I don't necessarily get MCP for that. Right? There's an API that can divide function. I can use tool decorator. I'm done.

Because LMS have this bind tools method where can take a tool, bind with a list, and I'm done. MCP is like buying tools for different clients, like, quad code, like, cursor. That's where MCP shines. It's buying tools for, like, apps.

But if I'm using SDK, why do I need it? I think my thinking is I would need it only if there's a tool that I don't wanna write myself.

That, like, someone can build a server for that's, like, very well developed and, like, would be hard to write, that might just wanna use out of box. Or another I was talking to Will about this recently.

Or it could be tools are written in, like, TypeScript and I wanna use Python. So you want, like, a protocol to connect the tools across languages. But, like, here's a good example. I noticed Taply released a Taply is a search tool. They released an NTP server.

Would I ever use that with agent? No way because there's a really good Taply API. Can just hit. Hit Taply as a function with my query and my act tool and I'm done. We've never pre built for that. So I've

never used MCP for that because it's very easy to find a tool just in native Python as a function, decorate it, and you're done. So it's kinda like this brushed MCP. It's like you have to think about what why you're actually using MCP if you're building an agent.

It really be for if the tools are, like, maybe a different language or they're very advanced, like a very advanced MCP server, you don't just write you can't just write yourself, then I would consider it. Yeah. And this is a good question.

So this is a nice tip I like to share with lots of customers I I work with that are on self hosted Lightsmith. So is if you run the local Lightning Graph server and use Wild Lightning Graph Studio, is anything stored on our servers? Right?

So a lot of self hosted customers version in Studio. If you just use Cloud Lightsmith or Lightgraph Studio, we won't sort things on our servers, but you can specify if you wanna trace to your self hosted. Right? So yeah. Hope that answers the question.

Not intuitive at first, but hopefully it's helpful. You'd expect it to be. And I think this is a really interesting question when you think about l one misjudging particular because then the l one gradient is kind of like an application in a sense. Right?

It's a little bit meta, but that gradient itself is something that you can then evaluate against the set criteria on how you would expect it to grade certain scores, and then you can iterate with the prompting the grader to try to align that to give the right scores.

So, Yeah. A question for you guys. A lot of people I mean, I've seen a lot of interest just from the general open source community, but any plans to do more versions of OpenDeepResearcher? Yeah. Like that? Yeah. That's actually a funny one.

So while I was doing this on the side, I did open deep research as a multi agent thing, but I never talked about it. It's like it's just in the repo You can give give context on open deep research. Yeah.

So like deep research is is obviously a great agent use case. Basically, having to learn iteratively do research against, for example, the web, but I I have a PR on to generalize if any is concerned with Wells.

I can get Postgres or anything you want or look at files. So I actually have it, but but I haven't done I haven't, like, published I haven't talked about it on YouTube or anything, but it exists. It's in the repo.

Look up multi agent dot py and open the research. And David actually has been working on a little bit. We've been talking on the side about moving it to some new stuff that's coming out soon. It's pretty cool.

It's a much similar implementation of the only research thing as a supervisor, kind of a multi agent setup where you have a supervisor that fans out to a bunch of researchers and they send back the supervisors. It's pretty cool. I haven't tested it that much.

I was so busy on this, but it it does it does work. David's hacked on it as well. It needs a little bit of tuning, but it is there. So yeah. If anyone has ideas, you can put up the r's in repo.

Look up multiagent.i and open these research. It's there. But so we're on the middle left, but then it's a good one to to end on. Someone asked, would love to hear more about thoughts on agent design and generally any mental models we follow when building AI agents.

I think we talked about this earlier with workflows procedures. Yeah. You guys go through it. My my general take here is I think you should try to get away with something as simple as possible for as long as you can.

And so whether that's just a single React agent that specific step where you actually meet the agent. That's really difficult. You're maybe not too sure when you're out of eating if the agent can handle it today.

So the email preferences example or the email specific example we showed up today or step that's difficult isn't necessarily triaging, but it's stringing you out We'll call it the right way to fit the meeting and put together a high quality hardwrap.

So I'd isolate that one part of your agent's architecture that is difficult and you don't know the full work. And like Nick said, trying to build the simplest version that we did it, running it off, and then play our complexity as as needed. Yeah. No.

I think those are that's a very great point. It's like, do you actually need an agent or not? It's like the first question if you do need an agent.

I actually from doing this and from doing some deep research stuff, I might put out a little blog post on, like, a bunch of hard things.

Like, I have a bunch of these little things I hit while doing this and opening deep research and some other stuff, like, I do have tons of traces in a Notion doc of like, oh, context management with cost with I was talking about David about this.

Context heavy tool calls are hard. Like, imagine you're hitting you're doing retrieval tool call and then you have this tool message in your history that has a bunch of context and you keep making tool calls, your context blows up. So you have to deal with, like, message management.

So there's all these little tricks to building agents even though the architecture is simple to call in a loop. There's all these little gotchas. I might just write it up as, like, a bunch of little nasty things I found, like, hard things off of building agents.

It's just, like, literally a bunch of, like, specific examples and Lang Smith trace and, like, here's what I did. And I still don't have a great solution for some of them, but so I think the do you need an agent at all is question one.

Ideally, frankly, a lot of times you don't, that'd be great. It's simpler. If you do, then, like yeah. I'll I'll try to put out, like, a blog or something. It's just like, here's a bunch of little lessons learned and things that are hard.

But obviously, it's like I think the biggest lesson actually is sending a good email first.

Set a really nice simple, crisp, little email, and and and nice frankly, if you need to do prompt engineering, just have one that's good and just, like, iterate your prompt for you against an eval, and maybe even set up a simple eval for whom calling and just, like, run that in the loop with your agent, update the prompts, update.

Frankly, the thing about an agent, it's just like it's the tool definitions and the prompt, really. So it's just modifying those things against assembly all set is is pretty effective. And then there's a bunch of other little tricks up that that I'll write right up. That's yeah.

That's probably about it, though. Awesome.