# ComfyUI API

A simple API server which communicates with the ComfyUI API. Which enables you to prompt it from pre-defined workflows.

## Project Structure

Following Clean Architecture we can represent the layers by following folders:

- Domain: ```models```, ```interfaces```
- Application: ```services```
- Infrastructure: ```repositories```, ```clients```
- Presentation: ```routers```