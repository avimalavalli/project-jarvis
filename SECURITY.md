# Security Policy

Project JARVIS is private and pre-release. Do not place credentials, tokens,
personal memory, biometric data, camera data, production logs, or database
exports in this repository.

## Mandatory boundaries

- Models and retrieved content are untrusted inputs.
- Only the JARVIS policy gateway may authorise side effects.
- Tools are denied unless a narrow, time-bounded capability is granted.
- Consequential actions require the configured confirmation or step-up check.
- Services bind to loopback during local development.
- External telemetry is disabled in the private baseline.
- Secret values come from an OS-backed vault through a broker interface.
- Every action attempt produces a redacted durable audit event.

Security reports should be disclosed privately to the repository owner. Do not
open a public issue containing exploit details, credentials, or personal data.

