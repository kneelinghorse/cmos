# AI Agent Configuration

## Project Overview
**Project Name**: [Project Name]
**Project Type**: [Type: Web Application, CLI Tool, Library, etc.]
**Primary Language**: [JavaScript, Python, TypeScript, etc.]
**Framework**: [React, Next.js, FastAPI, etc.]

## Build & Development Commands

### Installation & Setup
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

### Testing Commands
```bash
# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration

# Run E2E tests
npm run test:e2e

# Generate coverage report
npm run test:coverage
```

## Project Structure & Navigation

### Directory Layout
```
project-root/
├── src/                    # Source code
├── tests/                   # Test files
├── docs/                    # Documentation
├── config/                   # Configuration files
├── scripts/                   # Build and utility scripts
├── public/                   # Static assets
└── dist/                     # Build output
```

### Monorepo Navigation (if applicable)
```bash
# Navigate to specific package
cd packages/[package-name]

# Run commands for specific package
npm run [package-name]:dev

# Build specific package
npm run build:[package-name]
```

## Coding Standards & Style

### Language-Specific Guidelines

#### JavaScript/TypeScript
- Use TypeScript for type safety
- Prefer ES6+ features and modern syntax
- Use meaningful variable and function names
- Add JSDoc comments for public APIs
- Prefer `const` and `let` over `var`
- Use arrow functions for callbacks
- Handle async/await properly

#### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Prefer list comprehensions and generator expressions
- Use `pathlib` for file path operations
- Follow docstring conventions (Google style)
- Use f-strings for string formatting

### Testing Preferences
- **Framework**: Use pytest (not unittest classes)
- **Style**: Prefer fixtures over setup/teardown methods
- **Coverage**: Maintain >80% test coverage
- **Structure**: Group tests by feature/module
- **Naming**: Use descriptive test names that explain what is being tested

### Code Quality & Linting
- **JavaScript**: ESLint with Airbnb config
- **Python**: flake8 with strict configuration
- **TypeScript**: Strict TypeScript compiler options
- **Formatting**: Prettier for consistent code style

## Security & Quality Guardrails

### OWASP Top 10 Implementation

#### A01: Broken Access Control
**Security Rules:**
- Implement proper authentication and authorization checks
- Validate user permissions on all protected resources
- Use principle of least privilege
- Implement rate limiting for API endpoints
- Log all access attempts and failures

**Forbidden Patterns:**
- Never use hardcoded credentials or API keys
- Avoid direct database queries with user input
- Never expose sensitive information in error messages

**Validation Requirements:**
- All authentication must be validated before resource access
- Authorization checks must be performed for every protected endpoint
- Session management must be secure against hijacking

#### A02: Cryptographic Failures
**Security Rules:**
- Use strong encryption algorithms (AES-256, RSA-2048)
- Never store passwords in plaintext
- Use TLS 1.3+ for all communications
- Implement proper key management and rotation
- Use cryptographically secure random number generators

**Secure Patterns:**
- Always use established crypto libraries instead of custom implementations
- Implement proper key derivation functions (PBKDF2)
- Use authenticated encryption for data at rest
- Validate certificate chains and implement certificate pinning

**Validation Requirements:**
- All sensitive data must be encrypted at rest
- All communications must use TLS 1.3+
- Key rotation must be implemented and automated

#### A03: Injection
**Security Rules:**
- Use parameterized queries for all database operations
- Implement input validation and sanitization
- Use ORM with built-in injection protection
- Escape user-provided content in all outputs
- Use whitelist approach for allowed inputs

**Safe Patterns:**
- Always use prepared statements with parameter binding
- Implement input validation schemas
- Use ORM methods that automatically escape inputs
- Never concatenate user input into queries

**Validation Requirements:**
- All user inputs must be validated against schema
- SQL queries must use parameter binding
- All user-provided content must be escaped in outputs

#### A04: Insecure Design
**Security Rules:**
- Implement secure by design principles
- Use threat modeling for all features
- Implement defense in depth
- Use secure defaults and fail-safe options
- Document security requirements for all features

**Design Patterns:**
- Implement principle of least privilege in system design
- Use secure communication protocols by default
- Implement proper error handling without information leakage
- Use secure session management patterns

#### A05: Security Misconfiguration
**Security Rules:**
- Implement secure default configurations
- Regularly audit and update configurations
- Disable unnecessary features and services
- Use minimal attack surface principles
- Implement configuration validation

**Configuration Requirements:**
- All default configurations must be secure
- Configuration files must be validated on startup
- Sensitive configuration must be encrypted
- Configuration changes must be logged and audited

#### A06: Vulnerable and Outdated Components
**Security Rules:**
- Regularly update all dependencies and components
- Implement automated vulnerability scanning
- Use software composition analysis (SCA) tools
- Maintain component inventory and patch management
- Implement component isolation and sandboxing

**Dependency Management:**
- Use automated dependency update tools
- Implement dependency vulnerability scanning in CI/CD
- Maintain minimal dependency footprint
- Use trusted package repositories only

#### A07: Identification and Authentication Failures
**Security Rules:**
- Implement multi-factor authentication (MFA)
- Use secure password policies and storage
- Implement proper session management
- Use secure authentication protocols (OAuth 2.0, OpenID Connect)
- Implement account lockout and brute force protection

**Authentication Patterns:**
- Use established authentication libraries
- Implement secure password reset flows
- Use short-lived tokens and refresh mechanisms
- Implement proper logout and session invalidation

#### A08: Software and Data Integrity Failures
**Security Rules:**
- Implement integrity checks for all data and software
- Use digital signatures for code and data validation
- Implement secure update mechanisms
- Use checksums and hash verification
- Implement secure deserialization practices

**Integrity Controls:**
- Verify integrity of all downloaded components
- Implement code signing for all releases
- Use secure CI/CD pipelines with integrity checks
- Implement data integrity validation in APIs

#### A09: Security Logging and Monitoring Failures
**Security Rules:**
- Implement comprehensive security logging
- Log all security-relevant events
- Implement real-time monitoring and alerting
- Use secure logging practices (no sensitive data)
- Implement log integrity and tamper detection

**Logging Requirements:**
- Log all authentication and authorization events
- Log all input validation failures
- Log all security configuration changes
- Implement centralized logging with integrity

#### A10: Server-Side Request Forgery (SSRF)
**Security Rules:**
- Implement SSRF protection mechanisms
- Validate and sanitize all URLs and endpoints
- Use allowlists for permitted destinations
- Implement network segmentation and isolation
- Use secure HTTP clients with SSRF protection

**Protection Patterns:**
- Validate URL schemes and hostnames
- Implement request rate limiting per destination
- Use network-level controls for egress traffic
- Implement response validation and filtering

### Input Validation Requirements
- Validate all user inputs against schema
- Sanitize data before processing
- Implement length limits and format validation
- Use whitelist approach for allowed inputs
- Log all validation failures for monitoring

### Error Handling Patterns
- Implement comprehensive error handling
- Use structured error responses
- Log errors with appropriate context
- Implement graceful degradation for non-critical failures
- Never expose internal stack traces to users

## Architecture Patterns

### Preferred Design Patterns
- **Repository Pattern**: Use repository pattern for data access
- **Service Layer**: Implement business logic in service layer
- **Controller Pattern**: Use controllers for API endpoints
- **Factory Pattern**: Use factories for object creation
- **Observer Pattern**: Use observers for event handling

### Integration Approaches
- **API Integration**: Use RESTful APIs with proper versioning
- **Database Integration**: Use connection pooling and transactions
- **Message Queue**: Use message queues for async processing
- **Caching**: Implement appropriate caching strategies

### Performance Considerations
- Implement lazy loading where appropriate
- Use database indexes for query optimization
- Implement pagination for large datasets
- Use CDN for static assets
- Monitor and optimize database queries

## Development Workflow

### Branching Strategy
- **Main Branch**: `main` (production-ready code)
- **Development Branch**: `develop` (integration branch)
- **Feature Branches**: `feature/[feature-name]`
- **Hotfix Branches**: `hotfix/[issue-number]`

### Commit Message Format
```
[type](scope): description

Examples:
feat(auth): add OAuth2 authentication support
fix(api): resolve user profile data corruption
docs(readme): update installation instructions
test(auth): add integration tests for OAuth flow
```

### Code Review Process
- All changes must be reviewed via pull request
- Minimum of one reviewer approval required
- Automated tests must pass before merge
- Code coverage must not decrease
- Documentation must be updated for API changes

### Testing Protocols
- Write tests before writing code (TDD approach)
- Run full test suite before committing
- Integration tests must cover critical user flows
- Performance tests for API endpoints
- Security tests for authentication and authorization

## AI Agent Specific Instructions

### Context Loading Priority
1. Read agents.md file first for project-specific guidance
2. Load PROJECT_CONTEXT.json for current session state
3. Load MASTER_CONTEXT.json for project history and decisions
4. Reference SESSIONS.jsonl for recent mission history

### Output Formatting Preferences
- Use Markdown for documentation and reports
- Use JSON for structured data and configuration
- Use YAML for mission definitions and templates
- Prefer tables over long paragraphs for data presentation
- Include code examples with syntax highlighting

### Tool Usage Guidelines
- Prefer built-in tools over external dependencies when possible
- Use version-specific tool configurations
- Document tool versions and compatibility requirements
- Implement tool validation and error handling

### Communication Style
- Be concise and direct in responses
- Use structured formats (lists, tables, code blocks)
- Ask clarifying questions when requirements are ambiguous
- Provide confidence levels for uncertain information

## Project-Specific Configuration

### Advanced Orchestration Patterns
- Select a single orchestration pattern per mission via `domainFields.orchestrationPatterns.selectedPattern` in Build.Implementation templates (`none|rsip|delegation|boomerang` only).
- Patterns are mutually exclusive for Sprint 08. Enabling multiple patterns is invalid; only the configuration block that matches `selectedPattern` may set `enabled: true`.
- Delegation pulls worker definitions from `workers/manifest.yaml`. Ensure every referenced worker template exists under `workers/`.
- Boomerang checkpoints and state must be written to `runtime/boomerang/`; telemetry events stream to `telemetry/events/<mission-id>.jsonl`.
- RSIP refinement loops must declare convergence criteria and stop after the configured `maxIterations` or escalate per failure policy.

### Failure Escalation (All Patterns)
- Tier 1: Automatic retry on `worker_timeout`, `evaluation_call_failure`, or `network_errors` (one retry per worker/iteration).
- Tier 2: Pattern-specific thresholds (RSIP max iterations, Delegation two failed workers, Boomerang two failed step attempts or checkpoint write failure).
- Tier 3: Fallback gracefully to linear execution and emit `status=fallback`, `fallbackTriggered=true` in telemetry.
- Tier 4: Require human review before closing missions that triggered fallback; document remediation steps in mission notes.

### Runtime Directories
- `runtime/boomerang/` — checkpoint storage and resumable state bundles.
- `telemetry/events/` — append-only JSONL streams keyed by mission id.
- `workers/` — worker manifest plus individual worker templates used by delegation scenarios.

### Environment Variables
```bash
# Development
NODE_ENV=development
DEBUG=true

# Production
NODE_ENV=production
DEBUG=false
API_KEY=[your-api-key]
```

### Database Configuration
```yaml
development:
  host: localhost
  port: 5432
  database: project_dev

production:
  host: ${DB_HOST}
  port: 5432
  database: project_prod
  ssl: true
```

### External Service Configuration
```yaml
# API Keys (store in environment, not code)
api_service:
  endpoint: https://api.example.com
  version: v2
  timeout: 30000

# Storage Configuration
storage:
  type: s3
  bucket: project-files
  region: us-west-2
```

---

## Notes for AI Agents

### Critical Context Files
- **agents.md**: This file - primary source of project-specific guidance
- **PROJECT_CONTEXT.json**: Current session state and working memory
- **MASTER_CONTEXT.json**: Project history and architectural decisions
- **SESSIONS.jsonl**: Chronological log of all agent actions

### Mission Execution Guidelines
- Always read agents.md before starting any mission
- Update PROJECT_CONTEXT.json after each mission completion
- Log all significant decisions to MASTER_CONTEXT.json
- Append session events to SESSIONS.jsonl

### Quality Assurance
- Follow all coding standards defined in agents.md
- Implement all security guardrails specified
- Use specified testing frameworks and approaches
- Maintain code coverage thresholds defined in project

---

**Last Updated**: [Date]
**Version**: 1.0.0
**Maintained by**: [Team/Person]
