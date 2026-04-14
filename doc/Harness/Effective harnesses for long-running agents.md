Agents在跨多上下文窗口工作时任然面临挑战。我们从人类工程师的工作范式汲取灵感，为长期运行的Agents创造一个更有效的工具。

发布于2025年11月26日

随着AI Agents的能力变得越来越强，开发人员越来越多地让他们去做需要花几个小时，甚至几天去处理的复杂工作。然而，让Agents在多个上下文窗口间工作并持续获得进展目前还是一个悬而未决的问题。

长期运行的Agents的核心挑战在于他们必须在离散的会话中进行工作，并且每个新的会话都不会有之前的相关回忆。想象一下，一个软件项目由多个工程师换班构建，每个新来的工程师并不知道之前的工程师干了什么。由于上下文窗口的大小有限，而且大多数复杂的工程并不能在一个单一的窗口内完成，所以Agents需要一个能够将编码会话都联系在一起的方法。

我们构建了一个双重解决方案，使得Claude Agent SDK可以在多个上下文窗口间高效地完成工作：一个用于在第一次运行时配置环境的初始化Agent以及一个Coding Agent，这个Coding Agent的主要任务是在每个会话中都取得渐进式的进展，并且为下一个会话留下一个清晰的成果。你可以在随附的快速入门指南中找到代码示例。

长时间运行的Agent所面临的问题
Claude Agent SDK是一个强大的通用Agent框架，主要面向于编码，同时也能适用于需要模型使用工具来收集上下文、规划并执行的任务。这个框架有上下文的管理能力，例如上下文压缩，这可以让模型在执行任务的时候不会消耗整个上下文窗口。理论上来说，有了上下文压缩能力的配置，让模型能够在任意长的时间内持续去做有效的工作。

然而，有了上下文压缩还不足够。即使像Opus 4.5这样先进的，可以在多个上下文窗口间循环运行编码模型，且配合了Claude Agent SDK，，如果仅仅收到了类似于“构建一个claude.ai的复制品”的一个笼统的高层级提示词，也并不能很好地构建一个生产级别质量的网页应用。

在上述场景中，Claude的失败主要体现为两种模式。首先，Agent趋向于一次性做很多，本质上就是想一步到位，一次性生成整个应用。通常，这会使模型在它的执行过程中就会消耗完上下文，为下一个会话留下完成一半的并且没有文档化的功能模块。在这个情况下，Agent就需要去猜在之前的会话中发生了什么，并花费很多时间去尝试让基本的应用重新跑起来。即使用了上下文压缩技术，这个情况还会发生，因为上下文压缩并不总会将清晰的指令传递给下一个Agent。

第二个错误的模式通常会在工程的后期发生。在一些功能已经被构建好了的情况下，随后的Agent会检查项目进度，发现已经取得进展，就会宣布任务已经完成。

这将这个问题分解成两个部分。首先，我们需要搭建一个初始环境，为给定提示词所需要的所有功能提供基础，使得Agent能够逐步、逐功能去完成任务。其次，我们需要为每个Agent都设置提示词，让他们能够朝着自己的目标做出渐进式进展的同时，在会话结束后保持整个环境的状态是干净的。“干净的状态”意味着代码被肢解合并到master分支是可取的：没有重大的bug ，代码条理清晰，文档齐全，并且通常情况下，一个开发者能够轻松地开始新功能的开发，不需要先去清理无关的烂摊子。

在内部实验时，我们采用两步法去解决这些问题：

初始化Agent：首次Agent会话使用了特殊的prompt，让模型去配置出事的环境：一个**init.sh** 脚本，一个记录了Agent做了什么的claude-progress.txt日志文件，以及一个初始的展示添加了什么文件的git commit。
编码Agent：接下来的每一个会话会让模型去做渐进式进展，并且留下结构化的git updates。
这里关键的见解时找到一个让Agents在一个新的上下文窗口开始工作时能够快速理解当前状态的方法，这是由claude-progress.txt日志文件配合git 历史一起完成的。这些实践的灵感来自于对高效工程师每天都干了什么的了解。

环境管理
在更新过的Claude 4提示词指南中，我们分享了一些关于多上下文窗口工作留的最佳实践，包括一个使用“针对第一个上下文窗口使用不同提示词的”框架结构。这个“不同提示词”要求初始化Agent在环境中配置好所有后续编码Agent高效工作所必要的上下文。在此，我们提供了一个对这样一个环境的一些关键组件的深入洞见。

功能清单

为了解决Agent“一步到位”构建一个应用的问题或者过早断定项目的完成，我们提示初始化Agent撰写一个基于用户初始提示词扩展后的，全面的功能需求。以复制claude.ai界面为例，这意味着超过两百个功能，例如“用户可以打开一个新的聊天窗口，输出问题，敲击回车，并且看到AI的回复。”这些功能最开始都会被标记为“失败”，因此随后的编码Agents就能清楚的了解完整的功能是什么样子。

{
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to main interface",
      "Click the 'New Chat' button",
      "Verify a new conversation is created",
      "Check that chat area shows welcome state",
      "Verify conversation appears in sidebar"
    ],
    "passes": false
  }
AI写代码

我们提示编码Agents仅通过修改 passes 字段的状态来编辑此文件，并且用了语气很重的指令，比如“**严禁移除或编辑 Test，否则会导致功能丢失或 Bug。”**经过一些实验之后，我们最终决定使用JSON来实现这个功能，因为相比Markdown文件，这个模型更不可能不恰当地修改或覆盖JSON文件。

渐进式进展

基于此初始环境框架，编码Agents的下一个迭代就是要求他们一次只实现一个功能。这种渐进式的方法在解决Agents想“一步到位”的倾向上展现出非常重要的作用。

即使开始渐进式工作，一旦对代码做出了修改，模型保持环境处于一个干净的状态也至关重要。在我们的实验中，我们发现引发这种行为的最好方式是要求模型在git提交其进展且要附上描述性的commit信息，同时在进展文件中写出其进展的概要。这个能让模型使用git去回退有害的代码变更并且恢复代码库的工作状态。

这些方法同时也提高了效率，因为它们消除了一个Agent需要去猜发生了什么并花费时间尝试去让基础应用重新拍起来的必要。

测试

我们观察到的最后一个主要的错误模式是Claude在未经正确的测试就标记一个功能完成的趋势。在没有明确提示的前提下，Claude倾向去修改代码，并且甚至通过单元测试或者curl 指令对开发服务器进行测试，但却无法意识到该功能并非在端到端的场景下能正常工作。

在创建一个网页应用的例子里，一旦被明确提示去使用浏览器自动化工具，并且模仿人类用户的行为去测试，Claude大多数情况下都做的不错。



Claude通过Puppeteer MCP服务器测试claude.ai复制品时的截图

为Claude提供这些类型的测试工具显著提升了性能，因为Agent可以识别并修复那些单看代码并不明显的漏洞。

一些问题依然存在，例如Claude在视觉以及浏览器自动化工具的局限shade识别每一种漏洞变得困难。例如，Claude不能通过Puppeteer MCP发现浏览器原生的警告模态框，因此依赖于这些模态框的功能往往更容易出现漏洞。

进入状态
当上述一切准备就绪，每个编码Agent都被提示去完成一系列步骤来熟悉操作，一些步骤很基础，但是很有用：

运行pwd 指令了解目前的工作目录。你只能编辑当前目录下的文件。
阅读git日志和进展文件，了解最近的工作进度。
阅读功能清单文件，并且选择优先级最高但是没有完成的功能来执行。
这个方法为Claude在每个会话中都省下了一些tokens，因为它不需要去弄明白怎么去测试代码。此外，还可以要求初始化Agent编写一个init.sh 脚本来运行开发服务器，并在实现新功能之前，运行一些基础的端到端测试。

在克隆claude.ai的例子中，这意味着Agent总是启动本地开发服务器并且用Puppeteer MCP来开始一条新的聊天，发一条消息并且接受一条回复。这确保了Claude能够快速识别这个应用是否处于损坏状态，并及时修复任何存在的bug。如果Agent反而已经开始实现一个新功能，这可能会已有的问题更糟糕。

鉴于以上情况，典型的会话开始时会有如下助手消息：

[Assistant] I'll start by getting my bearings and understanding the current state of the project.
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
[Assistant] Let me check the git log to see recent work.
[Tool Use] <bash - git log --oneline -20>
[Assistant] Now let me check if there's an init.sh script to restart the servers.
<Starts the development server>
[Assistant] Excellent! Now let me navigate to the application and verify that some fundamental features are still working.
<Tests basic functionality>
[Assistant] Based on my verification testing, I can see that the fundamental functionality is working well. The core chat features, theme switching, conversation loading, and error handling are all functioning correctly. Now let me review the tests.json file more comprehensively to understand what needs to be implemented next.
<Starts work on a new feature>
AI写代码

Agent失败模式以及解决方案

问题	初始化Agent行为	编码Agent行为
Calude过早宣布整个工程的完成	设置一个功能列表文件：基于输出的spec，设置一个结构化的带有端到端功能描述的JSON文件	在每个会话的开始阅读功能列表文件，选择单一功能开始工作
Claude完成工作时，环境处于有许多bug和未文档化进展的状态	一个初始化的git仓库以及进度记录文件	会话开始时，先阅读进度记录文件和git提交日志，并且在开发服务器上运行基础的测试，以捕获未记录的漏洞。会话结束时，需要写入git提交并更新进度
Claude过早将某些功能标记为完成	设置一个功能列表文件	自我验证所有功能。只把经过仔细测试的功能标记为“通过”
Claude需要花时间去弄清楚怎么运行当前应用	写一个可以在开发服务器上运行的init.sh 脚本	在会话开始时先阅读init.sh
上表总结了长期运行的AI Agents通常会碰到的四种失败模式以及对应的解决方案。

未来工作
这项研究展示了一种让长期运行的Agent框架可以在多个上下文窗口间取得渐进式进展的解决方案。然后，依然有问题尚未解决。

最值得注意的是，我们依旧不清楚究竟是单一的，通用的编码Agent在上下文之间表现更好，抑或是通过多Agent的架构能够获得更好的表现。看起来是合理的是，如测试Agent、质量保证Agent或者是代码清理Agent这种专门的Agent在整个软件开发周期的字任务中表现甚至更好。

此外，这个demo为全栈网页应用的开发做了优化。未来的方向之一是将这些发现推广到其他的领域。这些经验教训中的部分甚至全部很可能适用于诸如科学研究或者经济建模等需要长期运行的Agent的任务。


————————————————
版权声明：本文为CSDN博主「Asuka_Langly」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/FRIEDHELM02/article/details/156074221