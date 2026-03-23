Registry Additional Info

This file is an extensible JSON object for runtime hints and other derived data
that should not be mixed directly into the canonical registry entry schema.

Current shape:

```json
{
  "generated_at": "2026-03-23T12:34:56+00:00",
  "useful_md_probe_base_urls": [
    "https://ai-sdk.dev",
    "https://docs.civic.com"
  ]
}
```

### Current Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `generated_at` | string | yes | UTC timestamp for when the artifact was generated. |
| `useful_md_probe_base_urls` | list[string] | yes | Flat list of primary base URLs where cached forced `.md` probing was shown to return Markdown successfully. |

## Why The Additional Info File Exists

`useful_md_probe_base_urls` is derived operational data, not core library
identity metadata. Keeping it in a separate file keeps the registry contract
clean while still making the runtime hint available to the MCP server.

This file is meant to grow over time if other stable derived hints become worth
publishing.

