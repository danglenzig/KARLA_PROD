# src/utilities/custom_hooks.py

from agents import (
    Agent,
    AgentHooks,
    AgentHookContext,
    RunHooks,
    RunContextWrapper,
    TResponseInputItem,
    ModelResponse,
    Tool,
    Usage
)
from typing import Any

class UsageHooks(AgentHooks):

    def __init__(self, display_name: str):
            self.event_counter = 0
            self.display_name = display_name

    async def on_end(
            self,
            context: RunContextWrapper[Any],
            agent: Agent[Any],
            output: Any
    ):
        u: Usage = context.usage
        requests: int      = u.requests
        input_tokens: int  = u.input_tokens
        output_tokens: int = u.output_tokens
        total_tokens: int  = u.total_tokens

        cached_input_tokens = u.input_tokens_details.cached_tokens
        reasoning_tokens = u.output_tokens_details.reasoning_tokens
        request_usage_entries = u.request_usage_entries

        info: str = f"""
{self.display_name}, on_end -- usage:
LLM requests:  {requests}

Input tokens:  {input_tokens}
    Cached input tokens: {cached_input_tokens}

Output tokens: {output_tokens}
       Reasoning tokens: {reasoning_tokens}

Total tokens:  {total_tokens}

===========================================

"""
        print(info)

class PrintToTerminalAgentHooks(AgentHooks):

    def __init__(self, display_name: str):
        self.event_counter = 0
        self.display_name = display_name

    async def on_start(
            self,
            context: AgentHookContext[Any],
            agent: Agent[Any]
    ) -> None:
        # return await super().on_start(context, agent) # default function content

        self.event_counter += 1
        # Access the turn_input from the context to see what input the agent received
        print(
            f"### AGENT_HOOKS ({self.display_name}) {self.event_counter}: Agent {agent.name} started with turn_input: {context.turn_input}"
        )
    
    async def on_end(
            self,
            context: RunContextWrapper[Any],
            agent: Agent[Any],
            output: Any
    ) -> None:
        #return await super().on_end(context, agent, output)
        self.event_counter += 1
        print(
            f"### AGENT_HOOKS ({self.display_name}) {self.event_counter}: Agent {agent.name} ended, and produced output of type: {type(output).__name__}"
        )

        u = context.usage
    
    async def on_handoff(
            self,
            context: RunContextWrapper[Any],
            agent: Agent[Any],
            source: Agent[Any]
    ) -> None:
        #return await super().on_handoff(context, agent, source)
        self.event_counter += 1
        print(
            f"### AGENT_HOOKS ({self.display_name}) {self.event_counter}: Agent {agent.name} recieved a handoff from agent {source.name}"
        )
    
    async def on_llm_start(
            self,
            context: RunContextWrapper[Any],
            agent: Agent[Any],
            system_prompt: str,
            input_items: list[TResponseInputItem]
    ) -> None:
        #return await super().on_llm_start(context, agent, system_prompt, input_items)
        self.event_counter += 1
        print(
            f"### AGENT_HOOKS ({self.display_name}) {self.event_counter}: Agent {agent.name} LLM start."
        )
    
    async def on_llm_end(
            self,
            context: RunContextWrapper[Any],
            agent: Agent[Any],
            response: ModelResponse
    ) -> None:
        #return await super().on_llm_end(context, agent, response)
        self.event_counter += 1
        print(
            f"### AGENT_HOOKS ({self.display_name}) {self.event_counter}: Agent {agent.name} LLM end."
        )
    
    async def on_tool_start(
            self,
            context: RunContextWrapper[Any],
            agent: Agent[Any],
            tool: Tool
    ) -> None:
        #return await super().on_tool_start(context, agent, tool)
        self.event_counter += 1
        print(
            f"### AGENT_HOOKS ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}"
        )

    async def on_tool_end(
            self,
            context: RunContextWrapper[Any],
            agent: Agent[Any],
            tool: Tool,
            result: str
    ):
        #return await super().on_tool_end(context, agent, tool, result)
        self.event_counter += 1
        print(
            f"### AGENT_HOOKS ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with and returned output: {result}"
        )

class PrintToTerminalRunHooks(RunHooks):
    def __init__(self):
        super().__init__()

    # ...