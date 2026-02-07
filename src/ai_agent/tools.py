"""Tool definitions and registry for the AI agent."""

import ast
import operator
from abc import ABC, abstractmethod
from datetime import UTC, datetime


class Tool(ABC):
    """Base class for all agent tools."""

    name: str
    description: str

    @abstractmethod
    def get_input_schema(self) -> dict:
        """Return JSON Schema for the tool's parameters."""

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Run the tool and return a string result."""

    def to_api_format(self) -> dict:
        """Convert to the Anthropic API tool format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.get_input_schema(),
        }


class ToolRegistry:
    """Holds registered tools and converts them to the Anthropic API format."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool by its name."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        """Look up a tool by name."""
        return self._tools.get(name)

    def to_api_format(self) -> list[dict]:
        """Return all tools in the format expected by the Anthropic API."""
        return [tool.to_api_format() for tool in self._tools.values()]

    def __len__(self) -> int:
        return len(self._tools)


# Safe operators for the calculator
_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.AST) -> float:
    """Recursively evaluate an AST node using only safe arithmetic operations."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPS:
        return _SAFE_OPS[type(node.op)](_safe_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPS:
        return _SAFE_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


class Calculator(Tool):
    """Evaluates basic math expressions safely."""

    name = "calculator"
    description = "Evaluate a mathematical expression. Supports +, -, *, /, **, %, //."

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate, e.g. '2 + 3 * 4'",
                },
            },
            "required": ["expression"],
        }

    def execute(self, **kwargs) -> str:
        expression = kwargs["expression"]
        try:
            tree = ast.parse(expression, mode="eval")
            result = _safe_eval(tree)
            # Display as int when the result is a whole number
            if isinstance(result, float) and result == int(result):
                return str(int(result))
            return str(result)
        except Exception as exc:
            return f"Error: {exc}"


class CurrentTime(Tool):
    """Returns the current date and time."""

    name = "current_time"
    description = "Get the current date and time in UTC."

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {},
        }

    def execute(self, **kwargs) -> str:
        return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
