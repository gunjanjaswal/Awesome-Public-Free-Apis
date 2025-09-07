<div align="center">

# 🌐 Awesome Public APIs | Free REST APIs Collection

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/gunjanjaswal/awesome-public-free-apis?style=social)](https://github.com/gunjanjaswal/awesome-public-free-apis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/gunjanjaswal/awesome-public-free-apis?style=social)](https://github.com/gunjanjaswal/awesome-public-free-apis/network/members)
[![GitHub issues](https://img.shields.io/github/issues/gunjanjaswal/awesome-public-free-apis)](https://github.com/gunjanjaswal/awesome-public-free-apis/issues)
[![GitHub license](https://img.shields.io/github/license/gunjanjaswal/awesome-public-free-apis)](https://github.com/gunjanjaswal/awesome-public-free-apis/blob/main/LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/gunjanjaswal/awesome-public-free-apis/graphs/commit-activity)


The ultimate, self-updating collection of **free public REST APIs** for developers to integrate into web applications, mobile apps, and software projects. Automatically discovers and tracks the most popular and reliable free APIs across 40+ categories.

[Browse APIs by Category](#-api-categories---find-the-perfect-api-for-your-project) • [Trending GitHub Repositories](#-trending-github-repositories) • [Trending GitHub API Repositories](#-trending-github-api-repositories) • [How to Contribute](#-how-to-contribute-to-this-api-collection) • [Automation Details](#-how-our-automated-api-tracking-works) • [License](#-license)

</div>

## 🌟 About This Free API Collection

This repository aims to be the most comprehensive and up-to-date collection of free public APIs for developers. Finding quality APIs can be challenging and time-consuming - this curated list solves that problem by automatically discovering, testing, and organizing the best free APIs available.

Key Features:
- 🔄 Self-updating API directory: Automatically checks API status weekly and discovers trending APIs monthly
- ✅ Verified working endpoints: All APIs are regularly tested to ensure they're functional
- 🏷️ Comprehensive categorization: 40+ categories covering everything from weather data to machine learning
- 🔒 Authentication details: Clear information about API keys, OAuth requirements, and more
- 📊 Popularity metrics: See which APIs are most widely used by the developer community
- 👥 Community-maintained: Contributions from developers worldwide keep this resource current
- 🔍 Detailed API information: HTTPS support, CORS compatibility, and status tracking

## 📃 API Categories - Find the Perfect API for Your Project

- [Authentication](#authentication) - APIs related to authentication, authorization, and identity management
- [Weather](#weather) - APIs for weather data and forecasts

### Authentication
APIs related to authentication, authorization, and identity management

| API | Description | Auth | HTTPS | CORS |
| --- | --- | --- | --- | --- |
| [Auth0](https://auth0.com/docs/api/authentication) | Authentication platform | OAuth | Yes | yes |
| [Okta](https://developer.okta.com/docs/reference/) | Identity management API | OAuth | Yes | yes |
| [Firebase Auth](https://firebase.google.com/docs/auth) | Authentication service by Google Firebase | apiKey | Yes | yes |

### Weather
APIs for weather data and forecasts

| API | Description | Auth | HTTPS | CORS |
| --- | --- | --- | --- | --- |
| [OpenWeatherMap](https://openweathermap.org/api) | Weather forecasts and data | apiKey | Yes | yes |
| [WeatherAPI](https://www.weatherapi.com/) | Weather API with forecasts | apiKey | Yes | yes |
| [Tomorrow.io](https://www.tomorrow.io/weather-api/) | Weather API powered by proprietary technology | apiKey | Yes | yes |


## 🔥 Trending GitHub Repositories

These are the most popular repositories on GitHub right now:

| Repository | Description | Stars | Language |
| --- | --- | --- | --- |
| [microsoft/vscode](https://github.com/microsoft/vscode) | Visual Studio Code | 150k+ | TypeScript |
| [facebook/react](https://github.com/facebook/react) | A declarative, efficient, and flexible JavaScript library for building user interfaces | 200k+ | JavaScript |
| [tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) | An open source machine learning framework | 175k+ | C++ |
| [flutter/flutter](https://github.com/flutter/flutter) | Google's UI toolkit for building natively compiled applications | 150k+ | Dart |
| [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) | Production-Grade Container Orchestration | 100k+ | Go |

## 📈 Trending GitHub API Repositories

These are the most popular API repositories on GitHub right now:

| Repository | Description | Stars | Language |
| --- | --- | --- | --- |
| [public-apis/public-apis](https://github.com/public-apis/public-apis) | A collective list of free APIs | 250k+ | Python |
| [microsoft/api-guidelines](https://github.com/microsoft/api-guidelines) | Microsoft REST API Guidelines | 20k+ | Markdown |
| [n0shake/Public-APIs](https://github.com/n0shake/Public-APIs) | A public list of APIs from round the web | 13k+ | Markdown |
| [APIs-guru/openapi-directory](https://github.com/APIs-guru/openapi-directory) | OpenAPI 3.0 directory | 4k+ | JavaScript |
| [postmanlabs/postman-docs](https://github.com/postmanlabs/postman-docs) | Documentation for Postman | 2k+ | JavaScript |

## 🤝 How to Contribute to This API Collection

We welcome contributions from the community! If you know of a high-quality API that should be included in this collection, please follow these steps:

1. Fork this repository
2. Add your API to the appropriate category in the README.md file
3. Submit a pull request with a brief description of the API and why it should be included

Please ensure that any API you submit meets the following criteria:
- Free to use (may require registration)
- Has proper documentation
- Is actively maintained
- Provides direct access to the API (not through a third-party service)

## 🔄 How Our Automated API Tracking Works

This repository leverages GitHub Actions to create a self-maintaining API directory that stays current without manual intervention:

Automated Processes:
- **Weekly API Status Checks**: Every Sunday at 00:00 UTC, our automation verifies all APIs are operational and updates their status
- **Monthly API Discovery**: On the 1st of each month at 00:30 UTC, our system scans sources like RapidAPI, GitHub trending repositories, and ProgrammableWeb to find new popular APIs
- **Daily Trending Repositories**: Every day at 01:00 UTC, we update the trending GitHub repositories section
- **Data Enrichment**: For each API, we automatically collect and verify information about authentication methods, HTTPS support, and CORS compatibility
- **Trend Analysis**: APIs are ranked by popularity based on usage metrics and community adoption

This automation ensures you always have access to the most current and reliable free API information for your development projects. Each category includes only high-quality, verified APIs without any artificial limits on the number of APIs per category.

## 📜 License

[MIT](LICENSE)
