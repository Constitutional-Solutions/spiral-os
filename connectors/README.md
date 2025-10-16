# Connectors - External API Integration

This directory contains connectors for integrating Spiral OS with external systems, APIs, and services.

## Overview

Connectors bridge Spiral OS's choice-based architecture with the external world. They translate between choice primitives and various external protocols, APIs, and data formats.

## Design Philosophy

Connectors follow these principles:

1. **Choice-Native**: All external interactions exposed as choice primitives
2. **Declarative**: Configuration over code where possible
3. **Resilient**: Graceful handling of network failures and API changes
4. **Observable**: Full visibility into external interactions
5. **Secure**: Credential management and permission enforcement

## Architecture

```
connectors/
├── filesystem/      # Local and network file systems
├── network/         # HTTP, WebSocket, gRPC protocols
├── database/        # SQL, NoSQL database connectors
├── cloud/           # AWS, Azure, GCP integrations
├── messaging/       # Email, Slack, Discord, etc.
├── ai/              # LLM and AI service connectors
├── iot/             # IoT device integrations
├── framework/       # Common connector utilities
└── registry/        # Connector discovery and management
```

## Connector Types

### 1. Protocol Connectors
Low-level protocol implementations:
- HTTP/HTTPS client and server
- WebSocket for real-time communication
- gRPC for high-performance RPC
- MQTT for IoT messaging
- SSH/SFTP for secure remote access

### 2. Service Connectors
Integrations with specific services:
- **Cloud Providers**: AWS, Azure, GCP, DigitalOcean
- **Messaging**: Slack, Discord, Telegram, Email
- **Storage**: S3, Google Drive, Dropbox, OneDrive
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis
- **AI Services**: OpenAI, Anthropic, Google AI, local models

### 3. Device Connectors
Hardware and peripheral integrations:
- Display and graphics adapters
- Input devices (keyboard, mouse, touchscreen)
- Storage devices (USB, external drives)
- Sensors and IoT devices
- Audio/video capture and playback

### 4. Application Connectors
Integrations with other software:
- Docker and container orchestration
- Development tools (Git, CI/CD)
- Productivity suites
- Custom application APIs

## Connector Interface

All connectors implement a standard interface:

```python
class Connector:
    """Base connector interface."""
    
    def __init__(self, config: ConnectorConfig):
        self.config = config
        self.state = ConnectorState.DISCONNECTED
        
    async def connect(self) -> ChoicePrimitive:
        """Establish connection as a choice."""
        raise NotImplementedError
        
    async def disconnect(self) -> None:
        """Clean up connection."""
        raise NotImplementedError
        
    async def execute(self, choice: ChoicePrimitive) -> Result:
        """Execute a choice through this connector."""
        raise NotImplementedError
        
    def get_capabilities(self) -> List[Capability]:
        """Return supported operations."""
        raise NotImplementedError
        
    def get_status(self) -> ConnectorStatus:
        """Return current connector status."""
        return ConnectorStatus(
            state=self.state,
            last_activity=self.last_activity,
            error=self.last_error
        )
```

## Example: HTTP Connector

```python
class HTTPConnector(Connector):
    """HTTP/HTTPS connector for web APIs."""
    
    async def connect(self) -> ChoicePrimitive:
        """Initialize HTTP client."""
        return ChoicePrimitive(
            context="http_client",
            options=[
                "configure_timeout",
                "set_headers",
                "enable_redirects",
                "start"
            ]
        )
        
    async def execute(self, choice: ChoicePrimitive) -> Result:
        """Execute HTTP request as choice."""
        if choice.operation == "GET":
            return await self._handle_get(choice)
        elif choice.operation == "POST":
            return await self._handle_post(choice)
        # ... other methods
        
    async def _handle_get(self, choice: ChoicePrimitive) -> Result:
        """Handle GET request."""
        url = choice.params["url"]
        headers = choice.params.get("headers", {})
        
        try:
            response = await self.session.get(url, headers=headers)
            
            # Return as choice primitive
            return Result(
                success=True,
                data={
                    "status": response.status,
                    "headers": dict(response.headers),
                    "body": await response.text()
                },
                next_choices=self._generate_next_choices(response)
            )
        except Exception as e:
            return Result(
                success=False,
                error=str(e),
                recovery_choices=self._generate_recovery_choices(e)
            )
            
    def _generate_next_choices(self, response) -> List[ChoicePrimitive]:
        """Generate follow-up choices based on response."""
        choices = []
        
        # Parse links from response
        if "Link" in response.headers:
            for link in parse_links(response.headers["Link"]):
                choices.append(ChoicePrimitive(
                    context="follow_link",
                    options=[link.url],
                    metadata={"rel": link.rel}
                ))
                
        return choices
```

## Configuration

Connectors are configured through declarative YAML or JSON:

```yaml
connectors:
  - name: github_api
    type: http
    config:
      base_url: https://api.github.com
      authentication:
        type: token
        token_env: GITHUB_TOKEN
      timeout: 30
      retry:
        max_attempts: 3
        backoff: exponential
        
  - name: local_postgres
    type: database.postgresql
    config:
      host: localhost
      port: 5432
      database: spiral_os
      credentials:
        username_env: DB_USER
        password_env: DB_PASS
      pool_size: 10
      
  - name: openai_api
    type: ai.openai
    config:
      api_key_env: OPENAI_API_KEY
      model: gpt-4
      max_tokens: 2000
      temperature: 0.7
```

## Connector Registry

The connector registry manages installed connectors:

```python
class ConnectorRegistry:
    """Central registry for all connectors."""
    
    def register(self, connector: Connector) -> None:
        """Register a new connector."""
        
    def get(self, name: str) -> Optional[Connector]:
        """Get connector by name."""
        
    def list_by_capability(self, capability: Capability) -> List[Connector]:
        """Find connectors with specific capability."""
        
    def discover(self) -> List[ConnectorInfo]:
        """Discover available connectors."""
```

## Security Considerations

### Credential Management
- Never store credentials in code
- Use environment variables or secure vaults
- Support credential rotation
- Encrypt credentials at rest

### Permission Model
- Connectors declare required permissions
- Users approve connector access
- Fine-grained permission scopes
- Revocable access tokens

### Network Security
- TLS/SSL for all network communication
- Certificate validation
- Network isolation options
- Traffic monitoring and filtering

## Development Status

🚧 **Planning Phase**

Priorities:
- [ ] Define connector interface standard
- [ ] Implement filesystem connector
- [ ] Build HTTP connector
- [ ] Create connector registry
- [ ] Design configuration system
- [ ] Add credential management
- [ ] Build testing framework

## Open Design Questions

### 1. Connector Lifecycle
**Question**: How should connectors be managed?
- **Static**: All connectors loaded at startup
- **Dynamic**: Load connectors on-demand
- **Hybrid**: Core connectors static, optional ones dynamic

**Trade-offs**: Startup time vs. resource usage vs. flexibility

### 2. Error Handling Strategy
**Question**: How should connector failures be handled?
- **Fail-Fast**: Propagate errors immediately
- **Retry Logic**: Automatic retry with backoff
- **Circuit Breaker**: Temporarily disable failing connectors
- **Graceful Degradation**: Continue with reduced functionality

**Trade-offs**: Reliability vs. responsiveness vs. complexity

### 3. Caching Strategy
**Question**: Should connectors cache responses?
- **No Caching**: Always fetch fresh data
- **Time-Based**: Cache with TTL
- **Event-Based**: Invalidate on updates
- **Configurable**: Let users choose per-connector

**Trade-offs**: Performance vs. freshness vs. consistency

### 4. Rate Limiting
**Question**: How should rate limiting be handled?
- **Per-Connector**: Each connector manages its own limits
- **Global**: System-wide rate limiting
- **User-Based**: Limits per user/application
- **Adaptive**: Learn and adjust based on API responses

**Trade-offs**: Simplicity vs. flexibility vs. API compliance

### 5. Monitoring and Observability
**Question**: What telemetry should connectors provide?
- **Basic**: Success/failure counts
- **Detailed**: Request/response logging
- **Full**: Distributed tracing
- **Custom**: User-defined metrics

**Trade-offs**: Visibility vs. performance vs. privacy

## Example Connectors

### Filesystem Connector
Provides choice-based file operations:
- Browse directories as choice trees
- Read/write files
- Watch for changes
- Search and filter

### Git Connector
Integrates with version control:
- Clone repositories
- Commit changes
- Branch and merge
- Pull requests

### OpenAI Connector
LLM integration:
- Chat completions
- Embeddings
- Fine-tuning
- Function calling

## Contributing

Connector development is essential for Spiral OS adoption. Contributions needed:

- **Core Connectors**: Fundamental system integrations
- **Service Connectors**: Popular API integrations
- **Protocol Support**: New protocol implementations
- **Testing**: Connector test suites
- **Documentation**: Usage guides and examples

## References

- [Connector Interface Specification](../docs/connector-interface.md)
- [Security Guidelines](../docs/connector-security.md)
- [Configuration Format](../docs/connector-config.md)
- [Testing Framework](../docs/connector-testing.md)

---

**Note**: Connectors are the bridge between Spiral OS's choice-based philosophy and the practical reality of external systems.
