# Airport Explorer app - Test Plan

## 1. Test Plan Overview

### Objective
The objective of this test plan is to verify the functionality
and integration of the Airport Explorer application. Testing covers the
application UI, internal APIs, database interactions, external API
integrations, and end-to-end user workflows.

### Application Under Test
Airport Explorer is a Flask web application that allows users to:
* Listed are only the tested functionality. App includes additional functionality.
- View airport information
- View domestic and international routes
- View airlines and destinations
- Generate AI airport summaries
- View airport locations on a map
- Access external information through Google and Wikipedia


## 2. Scope

### In Scope

- Airport/country selection
- Airport information display
- Airport database queries
- /api/airports internal API
- Wikipedia API 
- Aviation Weather API 
- OpenAI API airport summary 
- Domestic and international route information
- Airlines and destinations
- UI navigation
- State transitions
- Error and negative scenarios
- End-to-end Airport Info workflow

### Out of Scope

- Performance/load testing
- Security/penetration testing
- Cross-browser testing 


## 3. Test Approach

### API Testing
- Flask internal API endpoints
- Wikipedia API integration
- OpenAI API integration
- Positive and negative scenarios
- Malformed responses
- Empty responses

### Database Testing
- Airport records
- Required airport fields
- Database queries
- Database-to-UI data consistency

### Integration Testing
- Application/database integration
- Application/external API integration
- AI summary/database integration
- UI/database data consistency

### UI Testing
- Form controls
- Airport selection
- Airport information display
- Route information
- Links and navigation
- State transitions

### End-to-End Testing
- Complete Airport Info user workflow from airport selection through
  displayed airport information and related data.

### Exploratory Testing
Manual exploratory testing is used for scenarios that are better evaluated through direct user interaction.


## 4. Repository Locations

- Test Plan: docs/test-plan.md
- Test Cases: docs/test-scenarios.xlsx
- API Tests: tests/api/
- Database Tests: tests/database/
- E2E Tests: tests/e2e/
- Integration Tests: tests/integration/
- UI Tests: tests/ui/
