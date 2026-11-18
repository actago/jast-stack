# Safety and publication policy

## Exclude from user and admin copy

- Credentials, tokens, keys, secret locations, internal URLs, IP addresses, hostnames, and account identifiers.
- Customer names, tenant content, personal data, support-case details, and raw usage data.
- Exploit instructions, unpatched vulnerability details, detection gaps, and sensitive architecture information.
- Internal disagreements, reviewer comments, staff identities, and confidential roadmap information.

## Security changes

Describe a security change publicly only when the source explicitly authorizes disclosure or the vulnerability is already safely disclosed. Otherwise use a neutral statement such as “Sicherheits- und Stabilitätsverbesserungen” and place details in restricted internal notes. Never infer a CVE or severity.

## Approval boundary

All output remains `draft`. Generating content does not authorize:

- creating or editing GitHub releases;
- pushing commits or tags;
- changing UI content or a database;
- sending messages to users or administrators;
- publishing through Cliq or any other channel.

Require an explicit, scoped approval for each external write or publication step and verify the resulting state afterward.
