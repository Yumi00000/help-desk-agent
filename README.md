# help-desk-agent

## Code structure

```
.
├── main.py                        # Entry point
├── .env.exempel                   # Example environment variables (copy to .env)
└── src/
    ├── core/
    │   └── settings.py            # App settings (Claude, Qdrant)
    ├── database/                  # Database / vector store access
    ├── llm/                       # LLM (Claude) client and prompts
    ├── tools/                     # Tools the agent can call
    └── assignments-docs/          # Source data for the agent
        ├── bookings.json          # Sample bike rental bookings
        └── policies/
            ├── cancellations.md   # Cancellation and refund rules
            ├── faq.md             # Frequently asked questions
            └── prices.md          # Rental prices and fees
```
