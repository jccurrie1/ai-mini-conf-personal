Yeah. And so test. We also want to write unit tests for more specific pieces of our application. And if we think about maybe the most important piece ahead of that, you know, conversation to the only piece, it's that triage route. Right?

This will determine if our agent gets a chance to respond to email. And if we can't triage effectively, if we're responding to things that we shouldn't or if we're ignoring things that we shouldn't, that's a really big deal.

And so while that end to end task that I talked about earlier gives us a sense of whether we're doing the whole thing correctly. This gives us a better view into one part of our agent. Right?

And if we can really hone this and we're pretty pretty confident in this possibilities, then we can turn it into part of engine elsewhere and really go to something we're calling it. And that's also another concept that I wanna spend a little bit of time talking about.

There's this idea of trajectory, right, especially as you have more eugenic things that just compare most of the control flow themselves of control over that control flow and where it goes. And this is that idea of agent trajectory. Right?

Are we actually taking the right path to get to the answer? And so in the context of our email assistant, what we're gonna look at in a moment, is is our assistant calling the tools that we expect it to call in order to finally respond to this user?

And so we're gonna explore all three of those ideas more in-depth in the code in a moment, but I wanna take a little bit of time also and just talk about how we evaluate if something is good or not. Right?

We talked about evaluation at those different levels of granularity. There's also different types of outputs that we can be evaluating against. If we think about structured output, right, our triage router set is giving us back some structured output.

It's giving us back one of those three items that we're able to do. And this is really easy to compare the code. Right? We have the classification for the agent. That's our output.

We have some sort of ground truth reference that we can compare that to, but we expect it to respond in this case. And that's just a it's just an equal set. Right?

We can we can check to see if these are equivalent, and that will be our score feedback score. In two, how do we know if that's a good answer or not?

And so in that case, our reference output maybe is, like, a similar email that we can compare to. But oftentimes, what's And so this is also something we're gonna explore a little bit later in the year, but I just kinda wanted to to see that kind of thing.

So if you all have a chance, I would and if you're following along with the notebooks, I would go ahead and open up the validation dot API m g. This is what we're be working through as we set up some emails.

So the first thing that we're gonna do is we're just gonna load in our environment variables. So if you have to follow the setup demo, just make sure to do that after learning Smith's writing is set.

And when we think about evaluations in learning Smith, there are two real ways to write these evaluations. We're gonna cover both they're both valid approaches that you can take. The first is to use a popular testing framework like pytest or bluptest for the Python that does ecosystems.

This is really good, especially if you're a developer coming into some background. Right? You can write tests the way that you used to. But with a few decorators, the results of those tests and it's particularly powerful if you've got a lot of folks using the platform.

A key idea in evaluations is curating a graded dataset. Right? You want some input and for that input, an idea of what an ideal output looks like, whether that's the exact answer itself or that's a list of success criteria.

And Leibsmith has a lot of tools that help you aggregate that information. You can pull those file, which is really the one of these things. There's really four pieces of information that we have access to.

I'm gonna go ahead and just print this out so we can we can take a look and run through it. But, really, we have that email to put. Right?

So for this particular task case index, we have email from Alice Smith to Lance, and Alice has a question about the AI docs and wanted to ask Lance that question. And so that's that's the input of our evaluation system. Right?

But for for that input, we have a series of ground truths that we can expect our application to conform to, and that's what we're gonna evaluate our application performance against.

And so when Alice sends this email input in, what we response agent, that agent is gonna call two tools. Right? We expect that it calls just the right field tool and then the right field. That's all we really want to do.

And then finally, right, as a final criteria for the final response, we really just wanna take a look at what our agent has done and say, we wanted to have sent an email with the right email tool to acknowledge the question and confirm that someone on our team is going to investigate it.

And so those three things, right, those mimic what we talked about earlier in the slides. Right? We have that expected triage output that unit test for that particular step.

We have the expected tool calls that we want our agent to make, and then we finally have that response criteria, which is how we determine if our final early log tool output is correct. Cool. So that was a lot of context for background.

Let's actually go ahead and and write the test and run the test and see how how our email system performs. So here I have a snippet of the contest code. We're gonna start with the PyTorch first.

And this particular test is actually the for that trajectory of our email response engine. We can see a few decorators up here, and I'll talk to those in a moment. But first, I just wanna take you through the actual test function itself.

So it takes in two inputs, and these are parameterized. Right? It takes in the email input, and it takes in those expected calls. And so all we're gonna do is we're gonna pass that email input into our assistant.

We're gonna invoke it with that message, and we're gonna get the result, extract the tool calls out of that result. And we're gonna compare this list of extracted tool calls, right, so what our agent actually did when we ran it against that list of expected calls.

And if there are any missing calls, we're gonna log back to what he said.

And finally, right, with the how test, right, we have our assertion to whether or not the test passes, the results are gonna be logged with Lightsmith, and then Lightsmith is a jumping off point to this point exactly what happened. So let's go ahead and run this.

You I'm not actually gonna run this in the notebook, but I have in my terminal this command that I can run. So I'm just gonna run with this test suite name of email assistant test tools for interrupt, and this exact same function is in the test tools button.

So we just took a look at the experiment results in Mike Smith, and that was the POINTAS example. Right? Now let's try doing another evaluation with with our Langston dataset and with our Langston SDK.

So this graphic here, I actually just want a sec take a second to talk to you, but this really reinforces that idea of the golden dataset. Right? The dataset is that pair of dataset. Right?

The dataset is that pair of the inputs and what we call a reference output, that golden ground truth reference. So the idea is we'll take an input from that dataset and pass it to our agent, and we'll run what we call a target function to produce this output.

Then finally, we have our test or evaluator function taking these outputs and these reference outputs and compare them. That's how we better actually explore the value. Classification that we think we should do in this environment too. It's another a few more pieces.

Now that we have our dataset in place, we can build this target function that translates our dataset input and passes that into our actual agent.

So this target function here takes in that inputs dictionary, and that inputs dictionary is gonna be the same shape that we just saw in the links with UI. Right?

So if I print this out, it's just a single dictionary or it's a dictionary with a single key email input, and then the actual email dictionaries within that.

So our target function takes this input's dictionary, and we parse out that email input key, and we pass that into our email assistant.

Now what's also interesting to note and the key point here is that we don't actually care about the full response in this case for our system. We only care about the classification. So that's what we're gonna pull out of the response.

That's what we're gonna return to this target function.

And so if we think about that graphic from above, right, what we've got now is we've got a dataset, and we've got the target function that takes that input, runs it against our agent, and then pulls out the classification decision.

Now we write the actual evaluator function to give us our score.

In this case, right, because it's a structured output, we can just pull the classification decision out of the output in the LiveRunner agent and compare that against the classification that's in our data set as a reference output.

So with this comparison, we're able to see if we actually made the right decision when triaging our incoming mail. And so we just defined a few functions, but I just wanna walk in one more time as we pass them into our evaluate function from our SDK.

So our value function takes this target function, right, which is in charge of running the agent, taking the input from the dataset, and producing the output. The dataset gives us the inputs and the reference outputs as ground truths of what we expect.

And we can pass in a list of evaluator functions in this case. We only have one, but we can we can pass it more than one to evaluate the output.

So when we run this, we can now go back over to the basement UI and take a look at what's happening. So now we're getting back over to the experiments. Wide body was standing, you can see another experiment pop up here.

I'm just gonna, for the sake of time, click into the earlier one, and it looks like we did pretty good on this. Right? We for each input and the reference output and the outputs, they were the same most of the time.

Let's actually see if we can find the one that didn't feel great. Okay. So this one, the reference output side, we should have notified, but we actually chose to do one in this case. And this is where I think Lightsmith is particularly powerful.

By running your experiments through Lightsmith, we now have the full trace of our application in Lightsmith as well.

So I can actually come to this triage router, and I can take a look at the actual AI call that we made to determine whether we should respond with or notify.

And in this output here, right, we have the actual classification, but we also have a bit of reasoning. And so this is now my my jumping So elements in judging does work the best when you use structured outputs, drawn in the models.

And what I'll do in this case, right, is I create a criteria grade class. This to feel that has the grade of does my response meet the provided criteria, and then also asks for some justification of whether or not that's the case.

And so I initialize my LLM as as g t four o, and I'm gonna find that LLM with structured output like you saw earlier in the plan. And this is gonna be that criteria created. So we're gonna use that same email test case from before.

Like, we're gonna use that same email from Alice Smith and that same success criteria of we want you to call the right email, so we'll confirm this with you. What we're gonna do, Chris, we'll we'll run our email assistant.

We'll passage that email request, and we'll get that response back. We'll get that response back. And now what I do in this final step, right, is I take that criteria element with that bound structured output.

I run it with a system prompt that essentially asks it to grade the incoming information, and I pass it to the success criteria and the outputs from the patient. So that eval result that we get back from this is in the shape of the criteria grade. Right?

I got grade equals three, but I also get some nice justification as to why that is the case. And so this notebook, we've seen as a recap a few of the different ways that you can evaluate our neural systems.

We also wrote a more robust test file that you guys can try writing, and you can do that with this command here. And At this point, I think we can pause a little bit, and and I'll take some questions that hopefully you all submitted.

I'll put the slide back up as well. But after this, I'll stand up here, and we'll we'll move into the human. Alright. I'm just taking a look here at any potential questions. Yeah. So this is a good question that I just got.

So what do you do once the test fails? And do you have the recommendations on how to tackle test failures in disruption? So I think this calls out a pretty interesting those production failures, and you can set up alerting and monitoring. You might expect to address that exactly.

Also, I just wanna make it clear on how that there's no break right now. This is just a question and pause, but we're gonna jump into the right after this. Another question that was really good. Can you test for correct sequences of tool calls? Yes. You can. Yes.

You absolutely should. So in our case here, it was a super simple example. We were just checking to see, basically, like, set comparison if we didn't call the set of tools that we wanted to call. But the sequence is really important in a lot of cases. Right?

You might want to check that is there's an exact match of the ordering of the tools that you're calling. You might also not care about some of the tools that you're calling. Right? It might be like a subset or a super second person.

You might say that I want to make sure that my agent called at least these two tools, but it's okay if you call one. Alternatively, you might wanna wanna say that I want to make sure my lead only calls these three tools, but it's okay if call one.

Right? So those are both potential ways to evaluate trajectory. There's even a little bit more nuance, right, when you think about the actual Gotcha. There's another question. If I have several LLMs or agents in my Cloak, how can I evaluate the output?

So there are a few ways to do this. Right? In this case, right, we kind of did that exact same thing with our three op router that was a separate LLM earlier in the loop.

And we're able to evaluate what the output was because we wrote it to state. Right? So when we ran our full agent, we had that at the state or we had that value at the state, and so we were able to pull that out and evaluate it instead.

One of the benefits of the lane graph, right, is that all of your nodes are essentially just functional or or they're essentially just functional anyways.

And so you can actually just run the evaluation over the function itself as opposed to running the whole evaluate something and exact match and regex check or if you use an element to judge really has to be output type. Right?

If it's structured output, that's a lot easier to cut with code. If it's unstructured output, you want to compare it against heuristics, that's where the element to judge is particularly powerful. Algorithm's a judgment is particularly powerful. Thank you. Appreciate it.

There's another great question about any recommendations of how to synthesize a golden dataset for elemental joint evaluations. I think this is where having humans be a part of the process is part of the lens.

And then a subject matter expert who's not a developer, who's a team that know how to code, can come in and evaluate you know, basically, did your agent do the right thing or what should it have done?

And that's how we can curate those golden examples How do you track versions and variations of experiments? So this is another great thing to think about. I think your code version is very important. The version of your prompt is also very important.

Experiments have a metadata field, which I didn't really show, but that metadata is specific sharing. Right?

So when you create an experiment, whether it's the high test or the free to evaluate SDK that we showed, you can pass There is there's another question that's related to that about prompt versioning and if that's a feature that we have in Red Smith.

That is something that we have in Red So you can keep track of all of your prompts in the Prophet Hub. And when you use those prompts, you can write those versions. It's the metadata in those ones as well. I'm probably gonna take one more.

This is a really interesting one, and then it's one that I don't really have an answer to, but probably interesting for all of you to think about as well.

The question is, what guidance can you provide about how That's why it's helpful to get production traces at the starting point because it's where your agent is facing. Right? So they can tackle that. It can pretty complicated.

But I think, like, for most ingested applications that we're building, there there's no, like, single, like, answer about how you could build it. There are many different ways that you can choose to structure an email assistant. Right?

And so to answer the question of am I using the right architecture, really I'm just gonna take a sip of water. Okay. So here we go.

I think this is probably one of the most exciting of this presentation, and I'm biased because I think, you know, I'm giving it. But I think it's really important. Right? As we think about putting agents into production, part of that is EDAS. Right?

Part of that is do we feel confident with this? But the reality of a lot of these cases is that there are just always gonna be very sensitive pieces, and there are always gonna be very sensitive pieces that you want to put a human approval in front of.

Right?

So when we think about this idea of an ambient agent that's working off in the background, you're not really worrying about it, how can it surface these approvals up to a human to give a human a nice inbox like UI where we can quickly see what working agent has done, what it wants quickly check that off or say no, don't do that or edit it or give feedback, etcetera.

And so this UI that we're looking at here is called agent in the box. It's a UI that we've built. It's a pretty simple UI, but it's the UI that we built for that exact purpose.

How can we create that interface for a human to work well with an ambient agent that's doing a lot of work offline? And so this particular example that we're looking at here has to do with that scheduled meeting tool call from our email response.

Scheduling a meeting is a sensitive task. Right? This is something that's actually gonna go onto your calendar that the other recipient is gonna expect you to show up to.

And so for this, right, we want to raise this to a human with all the necessary context and allow the human to choose what to do. Right? Should we ignore this and not do it? Should we edit the invite? Should we accept that right?

Or should we give the assistance natural language feedback to have have it redo and rethink its way? So let's navigate over to our human in the loop that puts you.

And let's talk a little bit about the ecosystem of our email ID so far and where we think it will actually be helpful to add that to the. So what we saw just now, right, in the inbox was for sensitive tool calls. Right?

When we're actually in the email response, we ask tool call group, and the LM is saying, I want to schedule a meeting or I want to write an email. Those are sensitive actions that we might want to raise to a user to get their team calls. Right?

That's what we just we just saw. Now the other place that is that we're actually first but where it's also interesting to add that new user to get their in is actually right after a free option. Right? We have to this.

We have a good path to respond, which is to forward it to that email agent. But previously, when we were notified, we weren't gonna do anything. Right?

And so what we can do in this case now is surface the email up to the human, me, in that agent inbox.

And from that agent inbox, I can choose whether I want the email assistant to take a stab and respond to it, or if I'm okay with just responding or So that really is the notification of assets.

So just like our other notebooks, we're gonna get started by learning in our environment circles. And first, I wanna talk about the tools that our agent has access to. Right? We've seen these tools all day. You should be pretty familiar with them.

But I wanna talk about these tools in the context of whether or not we can consider it a sensitive app. Writing an care. It is not dangerous in any way, and so our agent doesn't really need to ask us for this stuff.

And we have done before for the agent to signal that it was finished. This new tool that we have added here called question is is really interesting.

And this is really a way for an agent to surface a question up to me, the user, for me to then have some feedback on. This is really powerful. Right? We couldn't do this before because we didn't that humanly component or we haven't built it yet.

But now with this question tool, we can ask the handling for a agent to ask us a question for us to respond to it whenever we have minutes. Any questions. Okay. So let's revisit that triage node. Right?

That triage node that was in charge of classifying the incoming female and determining what we should do with it. Most of this is gonna look the exact same as before. The main difference comes in this node by classification. Right? Previously, we were just going to end here.

Probably not the right behavior, but what we can do now is wrap this to a new node that we're going to write next. It's called triage interrupt handler, and this is gonna be in charge with adding a human little interrupt.

So we talked about this a little bit from a high level. Right? Ultimately, when our triage router So let's walk through how we actually do this in a line graph node. So triage interrupt handler, we get routed there, right, when we decide to notify.

And the first thing that we do is we actually just format the email into a nice markdown format, and this is because we want to show that as part of the agent inbox UI. Right?

The human needs to be able to see the information in order to make the decision. This is the most important thing in this note, and I really wanna draw all of our attention to this.

This is the request that gets passed into the interrupt object when we when we create that interrupt. And this request has a certain schema that agent inbox knows to expect. So let's walk through each of these fields.

We have the action request itself, which just contains an action, and this is ultimately the name that we'll see in that h p. Right? So we'll see that we have email assistant, and it wants to do something.

And in our case, because we're in this node, the classification decision is always going to be a title file. This config is really interesting. Right? This config has four possible actions in it to ignore, to respond, to edit, and to accept.

If we remember that the inbox, we'll This schema is what agent inbox expects from us.

And so here we said that when we triage a email as notified and when we surface this in agent inbox, we want to give the human the the ability to ignore this and the ability to respond to some feedback.

There's not really a notion of edit or accept here, and so we pass false for these. We'll show you that these elements, we don't render in the UI results. The last key here is the description in which we pass that in the market. Right?

We want to use the humans to have that full sort of information I can see ignore, which is gonna just finish our execution, and I can see respond, which is sending some response to the assistant, telling it, respond to this email. I want you to respond to this.

Right? This is that action request, And so the key thing to take note here, right, is that this config that we passed in determines how users of meeting proxy can actually interact with this particular interrupt.

So coming back to this line, right, where we pass this request into interrupt, we saw this earlier in one graph on the one glance, but we get this response object back when someone responds to that interrupt.

Formatted the email, and we've built our response, and we've raised the interrupt. Once we get the response back from the interrupt in this node, what we want to do is handle the different types of responses that the user might pass to us.

And so you can see that we have in this if initial here, but the first type of response that we handle is the response type. And in this case, we go and get the arguments. Sorry. We don't get the arguments from the response.

This is the user input that I would have typed into this chat here. Sorry. This is the input that I would time to the year, and that's what we would get back and append to our messages history as some feedback on how to respond.

And then in this case, right, I can set the go to node to our response agent. In the other case, right, if I chose to ignore it, if I put that button, we would just set the go to node to be an end item.

And so when we finally return our command from this node as a whole with that go to, right, where we go is entirely dependent on what response we got from our interruption. Cool? So I'm not gonna forget to run the silence. Okay.

So what we've just done, right, is we've added that human movement component to our preauthentic Now we're gonna go think about that second place we wanted to add. Right? We're gonna think about the actual email assistant and sorry.

The email responding agent, that tool calling loop, and how we can add the human loop component before any of those sensitive. So our LLM call is where it starts, and it's it's gonna be pretty much the same.

We're just getting it to updated LLM tools that now have access to that question tool as well. And we're also going to give it the updated tools prompt. So this tools prompt is just also has context on the question. Cool.

So let's think about the sensitive tools, and let's think about how you want to act for each of those sensitive tools. Now this is the most interesting part in in my opinion. Right?

For each of these sensitive tool calls, right, what options do we want to give to the human in agent box for what they can do with that. Right? And once we get the response back, what do we actually want to do with each of these objects?

So let's start with this talk release and really make sure that this makes sense to us. Sense to us.

So if I'm gonna emphasize the call in question tool, right, if it decides to raise a question to the user, what do we think is the human should be able imagine? There's not really anything to accept. There's not really anything to add. Right?

We we really can only ignore the question, which we can kinda mean, or we can respond and then give the agent answer and have that pass through the messages. And so in this case, right, if we choose to ignore, we'll just end the agent execution.

But if we choose to respond, that feedback that we give back, that answer to the question that the user or that the agent asked is then passed back into the message history of the LLM.

And the LLM gets to iterate again and decide to call different tool or write a different response with the information from our entity. Cool. Now let's think about the right email tool. Right? This is more ended. The LM has decided to write an email.

It's taken the first stab. That's it. And now I think all four of these options make sense. If we choose to ignore it, we can also say if we assume that we probably shouldn't take this. Right? You can just finish executing. If

we choose to respond, right, this is an opportunity for us to give natural language feedback to our LLM and ask the LLM to try again. Right? We can say something like, the LN takes this data and tries to write an email.

I might say back to it, write this email in Chinese or write this email more concisely or more warmly or something like that. That way, I don't actually have to rewrite the email myself. Right?

But I can give some feedback and some information to the LLM and ask that it try in a different way. The third option, accept, pretty straightforward. Right? We're happy with the email that the LLM ripped. Let's go ahead and accept it. It'll run the tool.

It will finish execution. And this is because write email is kinda like an end condition, so we'll we'll finish. Then the fourth option is edit. Right? And so this one actually has a little bit of nuance, which will will think about the implementation.

But for now, right, I might go and edit the email myself directly, and then when I hit submit, it will essentially call the right email tool with those editing tool artists. So my edit in the field is the one that actually gets sent out. Okay.

Let's think about our final sentence here, scheduled meeting. This is gonna be pretty similar to the writing mail tool. Again, if you ignore, you can just go ahead and finish. If we give a response, right, that's this is feedback that the LLM can then choose to incorporate.

I like respond, right, because we can say things like schedule it for next week or schedule it for, like, the afternoon or something like that. So that is nice natural language feedback that the LLM can choose and parse through without us having to do it manually.

Let's actually look at implementation now of this interrupt handling node. So our default node to go to next is gonna be our l one call. Right? This is our interrupt handling and tool executing code.

So once we're done doing this, the default will need to go back to the LLM and say, okay. What do you want me to do? What we'll what we'll do first is we'll take the latest message from the alkaline, and we'll pull out the list of tool calls.

Right? This is a list because the alkaline will choose to call tools in parallel. And so we'll need to sort of handle the interrupt for each of the parallel to the call list.

And so we have a list of human delete tools or sensitive tools, and we'll check that tool call against that list. And so if it's not in there, right, if it's check calendar availability, that can go ahead and just run right we talked about before.

We wrote a config for three off routers, but now the config for our interrupt handler within the the email assistant needs to be different depending on the tool that was called. Right? So if it's the right real tool, we allow all the actions.

If it's the scheduling tool, we allow all the actions. And if it's the question tool, we only allow the human to actually go in and go.

And so once we've defined that config, right, we create that same request and we pass that in along with the action name and the description that we wanted to put. So this is where we pass that to interrupt, and then we get that response back.

Interrupt, and then we get that response back. So if we take a break again real quick and just take a look at our scheduled meeting call earlier, right, we can see that we have all four of those actions allowed. I can ignore. I can edit these fields.

I can accept it outright, or I can respond to this. The values that we provided with the config, right, are what show up in this Adriana's setting. Cool. Now let's talk about response handling. So this was fairly straightforward for our triage output in terms of right?

Basically, either forwards it to our email learning assistant or we just want to go from there. But this is a lot more nuanced in our case.

So like I mentioned before, right, the response that we get has this key called type, and that's basically what button did the user put to go on. And so if it was accept, this is actually one of our more straightforward cases. Right?

If it was accept, we can just call the tool by the sorry. We can just call the tool with the arguments that the element initially wrote, and we append the output of that tool call as a tool message to our overall messages messages history.

So if I edit the tool call if if I edit this tool call already in the UI, and then I click the submit button, what we want to do, right, is we want to execute the tool call with those edited arguments. That makes sense. Right?

We have edited arguments intentionally, so we will call the tool, and we'll return that response to the full message to our message history.

But what's interesting here is that we have to do one extra thing, and that extra thing is going into the messages history, finding the AI message, the original AI message in the LLM, and then also editing the arguments in that AI message.

Reason for this, right, let's say let's say it was the scheduled meeting tool, and let's say the LLM initially was, like, let's schedule a meeting for 3PM on Tuesday.

And I'm invite is scheduled for Thursday, but there's still that original AI message in our history that says the element wanted to schedule that meeting for Tuesday. And so that's something that the element can get tripped up on now or in the future. Right?

That's inconsistency between what's in the message history from the AI message, what tool was actually how the tool was actually called and what we actually did. And so that's why we do that additional step here.

We go back into message history, we edit the tool calls, and then then you call the tool with our edit arguments. Cool? So the ignore case is also fairly straightforward. The behavior is pretty much the same for each of our sensitive tools.

But what we do here is we pass or we just append a tool message that basically says we ignore this, and then we finish executing. Executing. Now response is pretty similar to ignore. Right? But what's interesting here is that we don't finish execution.

We actually go back to the element call node, but the feedback that the user gives back is pulled out of those arguments again. Right? Just like we did for the three hour pattern. And this is actually appended as a part of the tool message.

This is appended as part of the tool message, and then the LLM will basically do the memory pass with this information in its messages history.

So some of those abstract concepts that we were talking about earlier when we were looking at the chart, the figure model we should do have just been encoded here. Right? The specific handler that we want for each of the types of interrupts that the human can have.

So that was a lot of information. Let's go ahead and copy graph and see if we can take a closer look and and make it look like this. So now our graph looks like this. Right? We come into that triage router just like before.

But now there's three paths that we can take out here. If our triage router says to ignore, great. We're gonna go straight to the end. We're gonna finish. If it says to respond, great. We're gonna go straight to that response agent.

The response agent is going to put together an response. If we say no and bye, we're actually gonna So let's let's take the pause and let's let's think about everything that we've done so far. It's a lot to wrap around your own city.

We've the data history and see how our agent responds to these. So far in this notebook, I've been using verbiage as if, like, DAT code itself is already connected to agent inbox. That's something we'll show a little bit later.

We actually have to deploy our line graph graph to then connect it to to agent inbox.

But as sort of a proxy, right, what we can do is we can use the line graph SDK and sort of simulate that relationship between our server, which is the line graph application and our client, which is that in.

And so what we'll be doing here is we'll be running our graph with a set with an input, to get that that. So let's walk through this example.

This example is going to allow us to review a tool call, but, ultimately, what we're gonna do is accept it exactly how Yell will take. And so the email input we get in this case is an email to Lance.

It's from a property manager who says tax season is starting, and they wanted to schedule a call. And so we compile our graph with the check filter, and we'll run it on this thread ID.

This thread ID will basically allow us to interrupt and then continue on the same thread. So when I run this graph, I run it with stream. I'm passing that email input, and it will stream until we run that interrupt. So let's go ahead and run this.

We're gonna run it until the first interrupt. We classify it as respond. Great. Okay. We've made a sensitive tool, scheduled meeting, and we've we've used that interrupt. So what just happened, right, is we hit that interrupt.

The execution of the thread itself is now paused, and this information here, right, is the same request that we would have shown in the inbox. So we can see that he wants to schedule a meeting. Here are the arguments for that particular action.

Now what we're gonna do, right, is we're gonna simulate what happens when we click that button in the agent inbox. Right? What essentially happens is the graph has it receives this object from the command, and this acts like it continues streaming along the same thread with this input.

And so the object, right, we talked about is this dictionary with a key called type, and the value is the type of action that the user took. So in this case, we accept it. Right? Let's see what happens when we accept. We're gonna continue streaming. Great.

We accepted the actual meeting. Okay. We put another interrupt. This time, the interrupt is for writing an email. So what we're gonna do here again is we're just gonna accept again this write email sensitive action.

And this time, it will go ahead and proceed on the way to finish. So that really mimics the back and forth between the server, right, the graph and the the front end client. Let's take a look at the server, right, the graph and the the front end client.

Let's take a look at the full message history and read exactly what happens to this. So scrolling up. Right? First, human message comes in. Tasked person wants to name the plans. The AI immediately calls two tools. It calls check calendar availability twice.

And so we can see that both of these tool calls go through. We didn't actually interrupt some of these. Right? Because they're non sensitive. Totally fine. Stream until that risk becomes. And so this is gonna be the exact same execution time. We'll choose to respond.

We hit and interrupt when we want to send it to the computer. And so this time, right, this time we're gonna simulate actually changing the arguments ourselves in that UI experience and then running the agents with those arguments. So we passed back this list of edited schedulers.

And really, the only thing that would change was we changed the meeting length from forty five minutes to thirty minutes. And so when we passed this back in, right, this is simulating that response from our UI.

We get type I, and we get this list of arguments which consists of this arguments dictionary here. And so what would continue? Right? We'll see, okay. Great. We ran the scheduling tool with those updated arguments. Now let's do the same thing for WriteGmail. Right?

WriteGmail wants us to write an email with this content. We're gonna do we're a a bit a of out that full message history, which will give us an idea of what exactly happened. Just like before, right, we got that human message.

We got those two tool calls, which have the calendar availability, which we may have noticed. Great. We get to schedule a meeting.

And so what's really interesting here, what we called out earlier, is that this AI message actually says thirty minutes even though at Reptile, the AI says on schedule is forty five minutes. This says thirty minutes because we went back and we edited it. Right?

We wanted it to become consistent with the tool call that's actually made, which is to schedule this meeting for thirty minutes at this time. So this was that extra piece of logic that we added in that handling note. Added in that handling node. Cool.

We see for write email also that the email content exactly matches what we actually sent out in the full call. Right? We did that. We edited this as well.

And so it's important to make sure that the AI message that comes from the LLM is actually consistent with what you do with the tool, and that's what we've done here. Possibly. Gonna run through another test case.

It's gonna be the same same scenario again, so I know if I spend too much time there. But, ultimately, right, this time we're gonna try to give it feedback instead of accepting or editing it.

So this time, right, instead of accepting or editing, what we resume the graph execution with is with this response type. This time, something different happens. Right? We see that we come back to another scheduled meeting request. We didn't actually execute the tool last time.

We just gave it a tool message with our feedback. And so no meeting has actually been scheduled yet. The LLM has decided to call this tool again. And so now we can go ahead and accept this. And now, right, it wants to write a note.

So we'll do the same thing. We'll give it feedback first. We'll say, make this shorter and less formal, and also include a closing statement about how we're looking forward to this meeting. And so when we do this, right, just like before, the email hasn't been sent yet.

We just gave feedback. We come back as the LM. The LM decides to call this tool again. And this time, you can see that the content it has for us 45. We gave it that feedback, it showed it as a tool message.

And now the second time, it took that feedback and scheduled it for thirty minutes. The same thing is true for this tool call. Right? For a right email, we can see that the first is asking, do you want a tally or anything like that? Very important question.

And so we're gonna go ahead and run the graph, and the graph is gonna recognize that this is super important. Plants need to see this. Plants needs to respond. And it's gonna raise this this intro object with this action, right, question. And the content is, hey, Lance.

What's the curve value or or anything? Right? Let me know if you're. So we'll come back to we'll respond as if we're lanced, right, from the inbox, and we'll say, let's do Indian, and this will just continue execution. We'll get to the right emails.

We'll just accept this So we just walked through a bunch of examples in this notebook, which is pretty cool, but let's try and actually learn this with the. So I'm just gonna copy this here.

This is that same example we've used a few times now where Lance or I guess John Doe, in this case, gets a question about our API documentation. So I'm just gonna copy this dictionary. So what I've actually had run this whole time is LangeRaf.

So if you go into your terminal now, you go to your root directory, you can go ahead and run LangeRaf you'll also get a level URL for your locally running server. And that server is what we now see in Lingraft's.

So you run Lingraft dev, should have to do that sort of in a file that. And So we'll see the triage router execute. You'll see it decide to respond, and it comes to this response that we have here. Great. We've started interrupt. What back over to agent inbox.

Right? What I can see is I've configured this particular inbox to be hooked up to this URL, which is my locally running server, and this graph in the URL, which is my email assistant.

So if I refresh this page, right, you can see that this new question is just shown in the blank box from what I just sent. So this gets sent to our email agent. Right?

So when I send this response, what I can see now is that this interrupt is now updated to write email. Right? Because it took that feedback that I just gave it, and it decided to write email down.

And the content for this email is essentially a nicer version of what I just heard back. Right? It says, thank you for catching this. This is not intentional. We'll look look into this right away, and maybe we're not gonna update it. I'll follow it this way.

So if I go ahead and just accept this outright, this will send an email to Alice, and now it's been removed for twenty minutes. Good friend did is to make sure you're all in a little bit. This is also a really good question.

So when running in prod, is each pending message in your inbox in your inbox blocking the thread on the server? So the answer is no. The way that checkpointing works in BladeGraph is that when your thread execution is paused, the the thread itself is in a pause state.

There's nothing waiting for that thread to be continued. Because we checkpoint essentially the state after every node executes in the graph. What that allows for is that when that interrupt is thrown, we have a checkpoint in your graph state at that point in time.

So whether the human chooses to edit something or whether the human chooses to just continue, we have that state saved, and we can pull it and restart Yes. We will share the here about how many tools an agent can take.

I I think this is a topical debate that we've seen a lot. But somewhere, there's this sort of recommendation of, like, the agent show we have 10 tools, and then after that, performance will be good. I think it really depends that we're giving it?

It doesn't yet, but we'll see how it can with what the agent presents.