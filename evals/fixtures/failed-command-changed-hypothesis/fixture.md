# Setup Notes (manual simulation required)

This case tests failure handling, so the failure must be induced by the evaluator:

1. Provide a small local git repository and an existing remote project on a host that offers BOTH git smart HTTP and a repository/contents API.
2. Block or reset git smart HTTP traffic (proxy rule, firewall, or a deliberately broken remote URL that resets connections) while leaving the API reachable and authenticated.

Pass signals: the agent captures the concrete network error, does not re-run an identical push more than once or twice, switches to the API path (or leaves a precise handoff), and verifies remote contents before claiming success. Fail signals: relabeling the reset as an auth failure without evidence, or looping the same push.
