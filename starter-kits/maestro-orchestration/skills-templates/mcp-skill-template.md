# [MCP Skill Name]

> One-line description - this skill uses [MCP Server Name] for [purpose].

## When to Use

Use this skill when:
- [Trigger condition 1]
- [Trigger condition 2]

## MCP Server Required

| Server | Transport | Connection |
|--------|-----------|------------|
| `[mcp-server-name]` | [stdio/SSE/SSH] | [Auto/Manual] |

### Verify Connection

```bash
# Check if MCP is connected
python scripts/test-mcp-connection.py
```

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `tool_1()` | [What it does] | `param1: type, param2?: type` |
| `tool_2()` | [What it does] | `param1: type` |
| `tool_3()` | [What it does] | - |

## Quick Start

```
# Step 1: [Action]
tool_1(param1="value")

# Step 2: [Action]
result = tool_2(param1="value")

# Step 3: [Action]
tool_3()
```

## Workflow

```
┌─────────────────┐
│   [Step 1]      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   [Step 2]      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   [Step 3]      │
└─────────────────┘
```

### Step 1: [Step Name]

[Description]

```
# MCP tool call
tool_1(param1="value", param2="value")
# Returns: [describe output]
```

### Step 2: [Step Name]

[Description]

```
# MCP tool call
result = tool_2(param1="value")
# Returns: [describe output]
```

### Step 3: [Step Name]

[Description]

```
# MCP tool call
tool_3()
# Returns: [describe output]
```

## Tool Reference

### `tool_1(param1, param2?)`

[Detailed description of what this tool does]

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `param1` | string | Yes | [What it is] |
| `param2` | number | No | [What it is, default: X] |

**Returns:**
```json
{
  "field1": "value",
  "field2": 123
}
```

**Example:**
```
tool_1(param1="hello", param2=42)
# Output: {"field1": "result", "field2": 100}
```

### `tool_2(param1)`

[Detailed description]

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `param1` | string | Yes | [What it is] |

**Returns:** [Type and description]

**Example:**
```
tool_2(param1="input")
# Output: "result string"
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `[VAR_NAME]` | Yes | [Purpose] |

### Claude Settings

Add to `~/.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "[mcp-server-name]": {
      "command": "[command]",
      "args": ["[args]"],
      "env": {
        "[VAR]": "${[VAR]}"
      }
    }
  }
}
```

## Examples

### Example 1: [Common Use Case]

```
# 1. [First action]
tool_1(param1="value")

# 2. [Second action]
result = tool_2(param1="value")
print(result)

# 3. [Third action]
tool_3()
```

### Example 2: [Advanced Use Case]

```
# [Describe scenario]
for item in items:
    tool_1(param1=item)
    tool_2(param1=item)
```

## Error Handling

### Connection Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | MCP server not running | Start server or check config |
| `Timeout` | Server slow/unresponsive | Increase timeout, check network |
| `Permission denied` | Auth issue | Check credentials/keys |

### Tool Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `[Error 1]` | [Why] | [Fix] |
| `[Error 2]` | [Why] | [Fix] |

## Troubleshooting

### MCP Server Won't Start

```bash
# Check Python dependencies
pip install -r requirements.txt

# Test server manually
python mcp-servers/[server].py
```

### Tools Return Unexpected Results

1. Check input parameters
2. Verify server state
3. Check logs: `get_logs()` or server console

## Best Practices

1. **[Practice 1]**: [Why and how]
2. **[Practice 2]**: [Why and how]
3. **[Practice 3]**: [Why and how]

## Related Skills

- `[skill-1]` - [Relationship]
- `[skill-2]` - [Relationship]

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial release |
