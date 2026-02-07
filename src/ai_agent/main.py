"""CLI entrypoint for the AI agent."""

from ai_agent.agent import Agent
from ai_agent.tools import Calculator, CurrentTime, ToolRegistry


def main():
    """Run the agent in an interactive loop."""
    registry = ToolRegistry()
    registry.register(Calculator())
    registry.register(CurrentTime())

    agent = Agent(tool_registry=registry)
    print("AI Agent ready. Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        response = agent.chat(user_input)

        for call in agent.last_tool_calls:
            print(f"  [tool] {call['tool']}({call['input']}) -> {call['result']}")

        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
