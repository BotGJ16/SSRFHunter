# SSRFHunter Elite v3.0 - 2025 SSRF Arsenal

**The Ultimate Server-Side Request Forgery Framework for Red Teams & Bug Bounty Hunters**

## 🎯 Overview

SSRFHunter Elite v3.0 is a comprehensive, AI-enhanced SSRF (Server-Side Request Forgery) exploitation framework that automates the entire SSRF attack lifecycle from reconnaissance to critical impact demonstration. Built for elite red teams and bug bounty hunters, it integrates 2025's most advanced SSRF techniques, including GraphQL/WebSocket exploitation, serverless RCE chains, container escape vectors, and cloud metadata abuse.

***

## ✨ Key Features

### 🔥 **2025 Threat Intelligence**
- **452% surge detection patterns** from 2025 threat landscape
- **CVE-2025 specific exploits**: Oracle EBS (CVE-2025-61882), Azure OpenAI (CVE-2025-53767)
- **AI-generated payloads** with context-aware obfuscation
- **Serverless targeting**: Lambda, GCP Functions, Azure Functions exploitation
- **Kubernetes/container escape** via CVE-2025-31133

### 🌐 **Multi-Source Reconnaissance**
- **URL Discovery**: Integrates `gau`, `katana`, `waybackurls`, `urlfinder`
- **GraphQL Endpoint Detection**: Auto-discovers `/graphql`, `/gql`, `/query` endpoints
- **WebSocket Detection**: Identifies `ws://`, `wss://` upgrade vectors
- **AI Platform Detection**: Targets OpenAI, Azure AI, GCP AI endpoints
- **Wildcard Domain Support**: Scans `*.target.com` automatically

### 🎭 **Advanced Payload Generation (200+ Variants)**
- **Standard Payloads**: 50+ classic SSRF indicators
- **Cloud Metadata**: AWS IMDSv2, GCP, Azure, Oracle Cloud (100+ paths)
- **Container/K8s**: Kubernetes API, Docker socket, etcd, kubelet
- **WAF Bypass**: Unicode normalization, encoding, protocol smuggling, multipart confusion
- **OOB/Blind SSRF**: Integrated interactsh/Burp Collaborator callbacks
- **AI-Generated**: Context-aware bypass techniques
- **HTTP Redirect Loops**: Novel 2025 validation bypass

### 🛡️ **Stealth & OPSEC**
- **Randomized Delays**: 1-5 second jitter between requests
- **User-Agent Rotation**: 20+ realistic agents (browsers + AI clients)
- **Proxy Support**: HTTP/SOCKS5 rotation
- **WAF Fingerprinting**: Auto-detects Cloudflare, AWS WAF, Akamai, Imperva
- **Request Jitter**: Avoids detection patterns

### 🤖 **AI-Powered Analysis**
- **Confidence Scoring**: Auto-calculates CVSS (1.0-10.0)
- **Credential Extraction**: Regex patterns for AWS, GCP, Azure, K8s tokens
- **Response Diffing**: Time-based, size-based, header-based detection
- **Intelligent Correlation**: Links OOB callbacks to source IPs
- **Behavioral Analysis**: Detects internal vs external service responses

### 📊 **Specialized Detection Engines**
- **GraphQLSSRFDetector**: Field resolver injection, introspection abuse
- **WebSocketSSRFDetector**: Handshake hijacking, real-time testing
- **ServerlessExploitationEngine**: Metadata + runtime API chaining
- **ContainerEscapeEngine**: Docker socket, K8s API abuse
- **RedirectLoopSSRFEngine**: Novel HTTP redirect bypass

### 📁 **Comprehensive Reporting**
- **Markdown Report**: Professional executive summary
- **JSON Results**: Machine-readable for CI/CD integration
- **Specialized Outputs**:
  - `graphql_ssrf.json`
  - `websocket_ssrf.json`
  - `serverless_exploitation.json`
  - `container_escape.json`
  - `cloud_metadata.json`
- **Evidence Packaging**: Screenshots, curl commands, HTTP traces

***

## 📦 Installation

### Prerequisites
```bash
# Install Go tools (required for URL discovery)
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/projectdiscovery/urlfinder/cmd/urlfinder@latest

# Verify installation
which gau katana waybackurls urlfinder
```

### Python Dependencies
```bash
# Install Python 3.8+
python3 --version

# Install required packages
pip install aiohttp aiofiles websocket-client

# Or install via requirements.txt
pip install -r requirements.txt
```

### Download SSRFHunter Elite
```bash
git clone https://github.com/BotGJ16/GF_Patterns/ssrfhunter-elite
cd ssrfhunter-elite
chmod +x ssrfhunter_elite_v3.py
```

***

## 🚀 Usage Examples

### Basic Scan
```bash
# Standard domain scan
python ssrfhunter_elite_v3.py -d target.com -o results/

# Wildcard domain scan
python ssrfhunter_elite_v3.py -d "*.target.com" -o results/ --concurrency 20
```

### Advanced Stealth Mode
```bash
# Slow, undetectable scan with proxy
python ssrfhunter_elite_v3.py -d target.com -o results/ \
  --stealth --proxy http://127.0.0.1:8080 --concurrency 3
```

### Authenticated Testing
```bash
# With cookies and JWT token
python ssrfhunter_elite_v3.py -d target.com -o results/ \
  --session admin \
  --cookie "session=abc123;token=xyz456" \
  --jwt "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  --header "X-API-Key:secret123"
```

### AI Platform Targeting (2025)
```bash
# Target Azure OpenAI, GCP AI, etc.
python ssrfhunter_elite_v3.py -d openai.azure.com -o results/ --ai-platform
```

### Kubernetes/Container Escape
```bash
# Internal K8s scan with escape attempts
python ssrfhunter_elite_v3.py -d k8s.internal -o results/ \
  --internal-scan --container-escape --full-arsenal
```

### Complete 2025 Arsenal
```bash
# Enable EVERYTHING (elite red team mode)
python ssrfhunter_elite_v3.py -d *.target.com -o results/ \
  --full-arsenal --concurrency 20 --stealth
```

***

## 📊 Output Structure

```
results/
├── all_urls_2025.txt              # All discovered URLs (including GraphQL/WS)
├── ssrf_urls_2025.txt             # URLs with SSRF parameters
├── ssrf_results_2025.json         # Complete test results
├── cloud_metadata.json            # Cloud credentials found
├── graphql_ssrf.json              # GraphQL-specific findings
├── websocket_ssrf.json            # WebSocket SSRF results
├── serverless_exploitation.json   # Serverless RCE chains
├── container_escape.json          # K8s/Docker escape vectors
└── ssrf_report_2025.md            # Professional markdown report
```

***

## 📖 Feature Deep Dive

### 1. **Multi-Vector URL Collection**
The tool doesn't just run `gau` and `katana` - it intelligently merges results and **auto-discovers 2025 endpoints**:
- GraphQL: `/graphql`, `/gql`, `/api/graphql`, `/v1/graphql`
- WebSocket: `ws://`, `wss://` upgrade endpoints
- AI Platforms: OpenAI, Azure AI, GCP AI endpoints
- Serverless: `.lambda-url`, `.cloudfunctions.net`, `.azurewebsites.net`

### 2. **2025 Payload Arsenal (200+ Variants)**
Every payload is **CVSS-scored** and categorized:
- **Standard**: Classic SSRF (score: 7.5)
- **Cloud Metadata**: AWS IMDSv2, GCP, Azure (score: 9.0)
- **Container/K8s**: Docker socket, K8s API (score: 10.0)
- **WAF Bypass**: Unicode, encoding, protocol smuggling (score: 8.5)
- **OOB/Blind**: interactsh integration (score: 6.5)
- **AI-Generated**: Context-aware (score: 8.0)
- **CVE-2025**: Oracle EBS, Azure OpenAI (score: 10.0)

### 3. **Smart Confidence Scoring**
The AI engine calculates confidence based on:
- **Status codes** (200/30x = +1)
- **Response time** (<0.1s or >15s = +2)
- **Content size** (<200B or >10KB = +1)
- **WAF bypass success** (+2)
- **Network errors** (+1)
- **Cloud metadata leaked** (+3)
- **K8s/API access** (+3)

**Confidence Levels**:
- `critical` (score ≥3): Immediate action required
- `high` (score 2): Likely exploitable
- `medium` (score 1): Possible SSRF
- `low` (score 0): Unlikely

### 4. **Real-Time Monitoring Dashboard**
Live stats during scan:
```
============================================================
 SSRFHUNTER ELITE - REALTIME DASHBOARD (2025)
============================================================
 URLs Collected      : 15,432
 SSRF-Susceptible    : 1,247
 Test Cases          : 24,680
 Potential Findings  : 892
 High Confidence     : 156
 Cloud Metadata      : 23
 Internal Services   : 67
 Blind SSRF          : 45
 GraphQL SSRF        : 12
 WebSocket SSRF      : 8
 Serverless RCE      : 34
 Container Escape    : 19
 CVE-2025 Exploits   : 5
============================================================
```

### 5. **Specialized Detection Engines**
Each engine handles a specific 2025 attack vector:

- **GraphQLSSRFDetector**: Tests field resolvers, mutations, nested queries
- **WebSocketSSRFDetector**: Performs handshake tests, message injection
- **ServerlessExploitationEngine**: Chains metadata access to runtime API abuse
- **ContainerEscapeEngine**: Tests Docker socket, K8s exec, etcd access
- **RedirectLoopSSRFEngine**: Uses HTTP redirect chains to bypass validation

### 6. **Comprehensive Reporting**
The markdown report includes:
- **Executive Summary**: CVSS scores, impact assessment
- **Cloud Metadata Section**: Stolen credentials, platform-specific guidance
- **Container Escape Section**: K8s API access, escape paths
- **GraphQL/WebSocket Sections**: Specialized findings
- **CVE-2025 Section**: Specific exploit confirmations
- **2025 Recommendations**: Immediate, short-term, long-term actions

***

## 🎯 Real-World Use Cases

### Bug Bounty Hunting
```bash
# Find P1 SSRF in minutes
python ssrfhunter_elite_v3.py -d api.target.com -o bounty_results/

# Check for blind SSRF with OOB
# Submit high-confidence findings to HackerOne/Bugcrowd
```

### Red Team Assessments
```bash
# Internal network recon via SSRF
python ssrfhunter_elite_v3.py -d internal.app -o redteam/ --internal-scan

# Cloud credential exfiltration
# Use stolen keys for lateral movement
```

### Cloud Security Auditing
```bash
# Audit cloud metadata protection
python ssrfhunter_elite_v3.py -d ec2-instance.com -o cloud_audit/

# Verify IMDSv2 implementation
# Check for serverless metadata leaks
```

### CI/CD Security Integration
```bash
# Automated scanning in pipeline
python ssrfhunter_elite_v3.py -d staging.app -o ci_cd/ --json-output

# Parse results.json for critical findings
# Fail pipeline on CVSS ≥9.0
```

***

## 🔧 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    SSRFHunter Elite v3.0                     │
│                    2025 SSRF Arsenal                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    RECONNAISSANCE PHASE                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐  ┌──────────┐  │
│  │  GAU    │  │ Katana  │  │ WaybackURLs │  │ URLFinder│  │
│  └────┬────┘  └────┬────┘  └──────┬──────┘  └─────┬────┘  │
│       │            │               │               │        │
│       └────────────┴───────────────┴───────────────┘        │
│                              │                               │
│       ┌──────────────────────┴──────────────────────┐        │
│       │  GraphQL Endpoint Detection                 │        │
│       │  WebSocket Upgrade Detection                │        │
│       └──────────────────────┬──────────────────────┘        │
└──────────────────────────────┼───────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              PAYLOAD GENERATION PHASE (200+ variants)        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Standard   │  │   Cloud     │  │  WAF Bypass │         │
│  │  Metadata   │  │  Container  │  │   AI-Gen    │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                 │                 │                │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐         │
│  │  Redirect   │  │  GraphQL    │  │ WebSocket   │         │
│  │    Loop     │  │   SSRF      │  │    SSRF     │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         └────────────────┴────────────────┘                │
│                              │                               │
└──────────────────────────────┼───────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              TESTING & ANALYSIS PHASE (Async)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Stealth    │  │  WAF Evade  │  │  OOB Detect │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                 │                 │                │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐         │
│  │  CVSS       │  │  Cloud      │  │ Container   │         │
│  │  Scoring    │  │  Metadata   │  │   Escape    │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         └────────────────┴────────────────┘                │
│                              │                               │
└──────────────────────────────┼───────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              REPORTING PHASE (Professional)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Markdown   │  │   JSON      │  │  Evidence   │         │
│  │   Report    │  │  Results    │  │  Package    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

***

## 📚 Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-d, --domain` | Target domain (required) | `-d target.com` |
| `-o, --output` | Output directory (required) | `-o results/` |
| `-c, --concurrency` | Parallel requests (default: 10) | `-c 20` |
| `--stealth` | Enable stealth mode | `--stealth` |
| `--proxy` | Proxy URL (http/socks5) | `--proxy http://127.0.0.1:8080` |
| `--internal-scan` | Scan internal networks | `--internal-scan` |
| `--container-escape` | Test container escape | `--container-escape` |
| `--ai-platform` | Target AI platforms | `--ai-platform` |
| `--full-arsenal` | Enable ALL 2025 features | `--full-arsenal` |
| `--session` | Session name for auth | `--session admin` |
| `--cookie` | Cookies (name=value;...) | `--cookie "sess=abc;token=xyz"` |
| `--header` | Custom headers (Header:Value,...) | `--header "X-API:secret"` |
| `--jwt` | JWT token for authentication | `--jwt "eyJhbGc..."` |

***

## 🎓 Best Practices

### 1. **Start Stealthy**
```bash
# Always start with low concurrency
python ssrfhunter_elite_v3.py -d target.com -o results/ --concurrency 5 --stealth
```

### 2. **Authenticate When Possible**
```bash
# Auth bypasses often lead to higher impact SSRF
python ssrfhunter_elite_v3.py -d target.com -o results/ --session user --jwt "$JWT"
```

### 3. **Focus on High-Confidence**
```bash
# After scan, prioritize critical/high findings
grep -B5 -A5 "confidence.*critical" results/ssrf_results_2025.json
```

### 4. **Chain Exploits**
```bash
# Use cloud metadata to access internal services
# Use SSRF to steal K8s tokens → access K8s API → escape containers
```

### 5. **Document Everything**
```bash
# The markdown report is your proof-of-concept
cat results/ssrf_report_2025.md
```

***

## ⚠️ Legal Disclaimer

**SSRFHunter Elite v3.0 is for authorized security testing only.**  
You must have explicit permission to scan any target. Unauthorized scanning is illegal. The authors are not responsible for misuse.

***

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/2025-payload`)
3. Commit changes (`git commit -am 'Add CVE-2025-61882 exploit'`)
4. Push to branch (`git push origin feature/2025-payload`)
5. Open a Pull Request

***

## 📄 License

**MIT License** - Free for educational and authorized security testing purposes.

***

## 🏆 Elite Features Checklist

- [x] 100+ SSRF parameter patterns (2025)
- [x] 200+ payload variants with CVSS scoring
- [x] GraphQL SSRF detection & exploitation
- [x] WebSocket SSRF testing
- [x] Serverless RCE chains (Lambda, GCP, Azure)
- [x] Container/K8s escape vectors
- [x] HTTP redirect loop bypass
- [x] AI-generated WAF bypass payloads
- [x] Cloud metadata exploitation (AWS IMDSv2, GCP, Azure, Oracle)
- [x] Blind SSRF OOB detection (interactsh)
- [x] Real-time monitoring dashboard
- [x] Comprehensive markdown reporting
- [x] Stealth mode with OPSEC features
- [x] JWT/session management
- [x] Proxy support (HTTP/SOCKS5)
- [x] Auto CVSS calculation
- [x] Credential extraction (AWS, GCP, Azure, K8s)
- [x] Internal network reconnaissance
- [x] CVE-2025 specific exploits
- [x] Time-based enumeration
- [x] WAF fingerprinting & bypass

**Total: 25 elite features integrated** 🎉

***

## 📞 Support

For issues, feature requests, or 2025 payload contributions, visit:
**https://github.com/BotGJ16**

***

**Happy Hunting!** May you find critical SSRF in every target. 🎯🔥
