# Contributing to Awesome Public APIs

Thank you for your interest in contributing to the Awesome Public APIs repository! This document provides guidelines and instructions for contributing to this project.

## How to Contribute

There are several ways you can contribute to this repository:

### 1. Adding a New API

To add a new API to the collection:

1. Fork the repository
2. Add the API information to the appropriate category in `data/apis.json`
3. Submit a pull request with your changes

When adding a new API, please include the following information:

```json
{
  "name": "API Name",
  "description": "Brief description of what the API does",
  "url": "https://link-to-api-documentation.com",
  "auth": "apiKey/OAuth/None",
  "https": true,
  "cors": "yes/no/unknown",
  "popularity": 75,
  "status": "active"
}
```

### 2. Updating Existing API Information

If you notice that information about an existing API is outdated or incorrect:

1. Fork the repository
2. Update the API information in `data/apis.json`
3. Submit a pull request with your changes

### 3. Reporting Non-Working APIs

If you discover an API that is no longer functional:

1. Open an issue with the title "Non-working API: [API Name]"
2. Include details about the API and why you believe it's no longer working
3. If possible, provide any error messages or responses you received

### 4. Suggesting New Categories

If you believe a new category should be added:

1. Open an issue with the title "New Category Suggestion: [Category Name]"
2. Explain why this category would be valuable
3. List a few example APIs that would fit in this category

### 5. Improving Documentation

Help us improve our documentation by:

1. Fixing typos or grammatical errors
2. Clarifying confusing sections
3. Adding examples or use cases

## Pull Request Process

1. Ensure your code follows the existing style and structure
2. Update the README.md if necessary with details of changes
3. The pull request will be reviewed by maintainers
4. Once approved, your changes will be merged

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior include:

* The use of sexualized language or imagery and unwelcome sexual attention or advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a professional setting

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances.

## Questions?

If you have any questions about contributing, please open an issue with your question or contact the repository maintainer.

Thank you for helping make this project better!
