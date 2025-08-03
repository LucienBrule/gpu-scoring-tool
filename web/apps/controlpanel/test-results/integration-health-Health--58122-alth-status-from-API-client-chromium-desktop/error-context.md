# Page snapshot

```yaml
- navigation:
  - text: GPU Scoring Tool
  - link "Home":
    - /url: /
  - link "Listings":
    - /url: /listings
  - link "Models":
    - /url: /models
  - link "Reports":
    - /url: /reports
  - link "Forecast":
    - /url: /forecast
  - link "ML Playground":
    - /url: /ml-playground
  - link "Import":
    - /url: /import
  - link "About":
    - /url: /about
  - link "Dev Harness":
    - /url: /dev-harness
- main:
  - heading "API Integration Test" [level=1]
  - heading "Health Check" [level=2]
  - button "Refresh Status"
  - status:
    - paragraph: Status
    - paragraph: ok
  - paragraph: This page demonstrates integration with the backend API using the OpenAPI-generated client.
  - paragraph: The health check endpoint is called when the page loads, and the result is displayed above.
- alert
```