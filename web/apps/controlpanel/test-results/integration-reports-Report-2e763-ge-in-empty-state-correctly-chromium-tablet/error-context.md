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
  - heading "GPU Market Reports" [level=1]
  - button "Refresh Reports"
  - text: Filter by Model
  - textbox "Filter by Model"
  - text: Number of Reports
  - button "10":
    - text: "10"
    - img
  - status:
    - paragraph: No reports available
    - paragraph: There are currently no GPU market reports matching your criteria.
- alert
```